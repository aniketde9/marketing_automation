import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import asyncpg
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Database:
    def __init__(self) -> None:
        self.database_url = os.getenv("DATABASE_URL")
        self.encryption_key_hex = os.getenv("ENCRYPTION_KEY")
        self.pool: Optional[asyncpg.Pool] = None

        if not self.database_url:
            raise ValueError("DATABASE_URL is not configured")
        if not self.encryption_key_hex:
            raise ValueError("ENCRYPTION_KEY is not configured")
        if len(self.encryption_key_hex) != 64:
            raise ValueError("ENCRYPTION_KEY must be a 32-byte (64 hex chars) string")

        self.encryption_key = bytes.fromhex(self.encryption_key_hex)

    async def get_pool(self) -> asyncpg.Pool:
        if not self.pool:
            self.pool = await asyncpg.create_pool(self.database_url, min_size=1, max_size=10)
        return self.pool

    def decrypt_api_key(self, encrypted: str) -> str:
        try:
            iv_hex, cipher_hex = encrypted.split(":")
        except ValueError as exc:
            raise ValueError("Encrypted API key has invalid format") from exc

        iv = bytes.fromhex(iv_hex)
        cipher_bytes = bytes.fromhex(cipher_hex)

        cipher = Cipher(
            algorithms.AES(self.encryption_key),
            modes.CBC(iv),
            backend=default_backend(),
        )
        decryptor = cipher.decryptor()
        padded = decryptor.update(cipher_bytes) + decryptor.finalize()

        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        data = unpadder.update(padded) + unpadder.finalize()
        return data.decode("utf-8")

    async def get_pending_job(self) -> Optional[Dict[str, Any]]:
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow(
                    """
                    SELECT *
                    FROM jobs
                    WHERE status = 'pending'
                    ORDER BY created_at ASC
                    FOR UPDATE SKIP LOCKED
                    LIMIT 1
                    """
                )

                if not row:
                    return None

                await conn.execute(
                    """
                    UPDATE jobs
                    SET status = 'processing',
                        started_at = NOW(),
                        latest_message = 'Worker picked up job',
                        updated_at = NOW()
                    WHERE id = $1
                    """,
                    row["id"],
                )

                return dict(row)

    async def get_user_api_key(self, user_id: str) -> Optional[str]:
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT gemini_api_key_encrypted FROM users WHERE id = $1",
                user_id,
            )
            if not row or not row["gemini_api_key_encrypted"]:
                return None
            return self.decrypt_api_key(row["gemini_api_key_encrypted"])

    async def get_user_prompts(self, user_id: str) -> Optional[Dict[str, str]]:
        """Fetch user's custom prompts"""
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT templates FROM prompts WHERE user_id = $1",
                user_id,
            )
            
            if not row or not row["templates"]:
                return None
            
            templates = row["templates"]
            
            # Handle both string (JSON) and dict formats
            if isinstance(templates, str):
                try:
                    return json.loads(templates)
                except (json.JSONDecodeError, TypeError):
                    return None
            elif isinstance(templates, dict):
                return templates
            
            return None

    async def get_job_topics(self, job_id: str) -> List[Dict[str, Any]]:
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT row_number, topic, content_type
                FROM generated_content
                WHERE job_id = $1
                ORDER BY row_number ASC
                """,
                job_id,
            )
            return [dict(row) for row in rows]

    async def update_generated_content(self, job_id: str, row_number: int, generated_text: str) -> None:
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE generated_content
                SET generated_text = $1
                WHERE job_id = $2 AND row_number = $3
                """,
                generated_text,
                job_id,
                row_number,
            )

    async def update_job(self, job_id: str, **fields: Any) -> None:
        if not fields:
            return

        pool = await self.get_pool()
        assignments = []
        values: List[Any] = []

        for idx, (key, value) in enumerate(fields.items(), start=1):
            assignments.append(f"{key} = ${idx}")
            values.append(value)

        assignments.append("updated_at = NOW()")
        assignment_sql = ", ".join(assignments)

        values.append(job_id)

        async with pool.acquire() as conn:
            await conn.execute(
                f"UPDATE jobs SET {assignment_sql} WHERE id = ${len(values)}",
                *values,
            )

    async def update_generation_log(self, user_id: str, job_id: str, posts_count: int) -> None:
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE user_generation_log
                SET posts_generated = $1
                WHERE user_id = $2 AND job_id = $3
                """,
                posts_count,
                user_id,
                job_id,
            )

    async def record_file(self, job_id: str, user_id: str, file_name: str, data: bytes) -> None:
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO files (job_id, user_id, file_name, file_data, file_size)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (job_id) DO UPDATE
                SET file_data = EXCLUDED.file_data,
                    file_size = EXCLUDED.file_size
                """,
                job_id,
                user_id,
                file_name,
                data,
                len(data),
            )

