import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from backend.core.limiter import limiter
from backend.core.database import init_db, create_tables
from backend.data.seed import criar_admin_se_nao_existir

from backend.ai.risk.train_runner import train_if_needed

from backend.api.auth import router as auth_router
from backend.api.auth_admin import router as auth_admin_router
from backend.api.risk import router as risk_router

try:
    load_dotenv()
except ImportError:
    pass

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    create_tables()
    criar_admin_se_nao_existir()
    auto_train = os.getenv("AUTO_TRAIN_RISK_MODEL", "true").lower() == "true"
    force_train = os.getenv("FORCE_TRAIN_RISK_MODEL", "false").lower() == "true"

    print(
        f"[RISK] auto_train={auto_train} | "
        f"force_train={force_train} | "
    )

    if auto_train:
        print("[RISK] Auto treino habilitado")
        train_if_needed(force=force_train)
    else:
        print("[RISK] Auto treino desabilitado")

    yield

app = FastAPI(
    title="API Aulas",
    summary="",
    description="""
    API responsável por fornecer dados acadêmicos como:
    - Sistema de Login e Autenticação
    - Cadastro de Alunos
    """,
    version="v0.1.0-BETA",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5000",
        "http://localhost:5000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )

app.include_router(auth_router)
app.include_router(auth_admin_router)
app.include_router(risk_router)

if __name__ == '__main__':
    pass