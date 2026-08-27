"""Pydantic models for claims and related entities."""

from typing import Optional, List
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class FlagReason(str, Enum):
    """Enumeration of claim flag reasons."""
    NEEDS_REVIEW = 'Needs Review'
    HIGH_PRIORITY = 'High Priority'
    REJECTION_MISSING_AUTH = 'Potential Rejection: missing auth'
    REJECTION_MODIFIER_ERROR = 'Potential Rejection: modifier error'
    REJECTION_ICD_MISMATCH = 'Potential Rejection: ICD mismatch'
    DENTAL_EXT_REQUIRED = 'Dental EXT required'
    OTHER = 'Other'


class Claim(BaseModel):
    """Claim entity."""
    claim_no: str = Field(..., description='Unique claim number')
    provider: str = Field(..., description='Provider name')
    service: str = Field(..., description='Service description')
    icd10: str = Field(..., description='ICD-10 code')
    description: str = Field(..., description='Clinical description')
    discipline: str = Field(..., description='Discipline code')
    amount: float = Field(..., gt=0, description='Claim amount in N$')
    submission_date: Optional[datetime] = None
    patient_age: Optional[int] = None
    authorisation_code: Optional[str] = None


class ClaimFlag(BaseModel):
    """Flag attached to a claim."""
    claim_no: str = Field(..., description='Claim number')
    reason: FlagReason = Field(..., description='Reason for flag')
    note: str = Field(..., description='Additional context')
    assessor: str = Field(..., description='Assessor name')
    timestamp: datetime = Field(default_factory=datetime.now)
    resolved: bool = False
    resolution_note: Optional[str] = None


class TimeLog(BaseModel):
    """Time log entry for productivity tracking."""
    claim_no: str
    minutes: float = Field(..., gt=0)
    delegated: int = 0
    timestamp: datetime = Field(default_factory=datetime.now)


class SessionSummary(BaseModel):
    """Summary of a claims processing session."""
    assessor: str
    committed_count: int
    flag_count: int
    average_minutes: float
    baseline_minutes: Optional[float]
    total_minutes: float
    exported_at: datetime = Field(default_factory=datetime.now)
    flags: List[ClaimFlag] = []
    time_logs: List[TimeLog] = []
