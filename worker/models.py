from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Job(BaseModel):
    id: str
    user_id: str
    status: str
    progress: int
    total: int
    latest_message: Optional[str] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime


class JobTopic(BaseModel):
    job_id: str
    row_number: int
    topic: str
    content_type: str


class WorkerHealth(BaseModel):
    status: str
    processed_jobs: int
    last_job_id: Optional[str] = None

