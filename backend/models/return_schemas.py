from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time, datetime

class Status(BaseModel):
    status: str
    
class LoginAndRegister(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    
class Refresh(BaseModel):
    access_token: str
    token_type: str

class RiskResponse(BaseModel):
    risco: str
    confianca: float
    justificativa: str