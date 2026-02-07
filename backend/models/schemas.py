from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    dadoLogin: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    
class RegisterAdminRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str

class ChangePasswordRequest(BaseModel):
    new_password: str

class ListaUsuariosRequest(BaseModel):
    role: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None