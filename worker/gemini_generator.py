import asyncio
import os
import time
from typing import Optional

import google.generativeai as genai


class GeminiGenerator:
    def __init__(self, api_key: str) -> None:
        model_name = os.getenv('GEMINI_MODEL', 'gemini-pro')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

        self.requests_per_minute = int(os.getenv('GEMINI_RPM', '2'))
        self.requests_per_day = int(os.getenv('GEMINI_RPD', '50'))
        self._request_times: list[float] = []
        self._daily_count = 0
        self._last_reset = time.time()

    async def generate(self, prompt: str, *, retry: int = 3) -> str:
        attempt = 0
        last_error: Optional[Exception] = None

        while attempt < retry:
            try:
                await self._enforce_rate_limits()
                response = await asyncio.to_thread(self.model.generate_content, prompt)
                text = (response.text or '').strip()
                if not text:
                    raise RuntimeError('Gemini returned an empty response')
                self._request_times.append(time.time())
                self._daily_count += 1
                return text
            except Exception as exc:  # pylint: disable=broad-except
                last_error = exc
                attempt += 1
                await asyncio.sleep(attempt * 2)

        raise RuntimeError(f'Gemini generation failed after {retry} attempts') from last_error

    async def _enforce_rate_limits(self) -> None:
        now = time.time()

        if now - self._last_reset >= 86400:
            self._daily_count = 0
            self._last_reset = now

        if self._daily_count >= self.requests_per_day:
            hours = (86400 - (now - self._last_reset)) / 3600
            raise RuntimeError(f'Daily Gemini quota reached. Resets in {hours:.1f}h')

        self._request_times = [t for t in self._request_times if now - t < 60]
        if len(self._request_times) >= self.requests_per_minute:
            wait_seconds = 60 - (now - self._request_times[0]) + 0.5
            await asyncio.sleep(wait_seconds)
