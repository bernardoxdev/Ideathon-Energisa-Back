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
from backend.events.register_events import register_events

from backend.ai.risk.train_runner import train_if_needed

from backend.api.auth import router as auth_router
from backend.api.auth_admin import router as auth_admin_router
from backend.api.risk import router as risk_router
from backend.api.chamados_controller import router as chamados_router
from backend.api.solicitacoes import router as solicitacoes_router
from backend.api.usuarios_controller import router as usuarios_router

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

    register_events()

    yield

app = FastAPI(
    title="Delta 360",
    summary="DELTA 360 — Portal Corporativo de Coordenação Multiconcessionária com ERP, API Integrada e Agentes de IA para Prevenção de Acidentes Elétricos",
    description="""
    O Delta 360 é um portal corporativo (ERP) desenvolvido para a Energisa com o objetivo de centralizar, coordenar e prevenir riscos associados a intervenções realizadas em proximidade com a rede elétrica. A solução integra, por meio de uma API aberta, concessionárias, prefeituras, empresas de telecomunicações, iluminação pública, saneamento, construção civil e operadores de veículos de grande porte, oferecendo à Energisa uma plataforma própria de gestão de chamados, conflitos operacionais e riscos. Agentes de inteligência artificial orquestrados analisam eventos de campo, identificam duplicidades, detectam conflitos, calculam riscos e recomendam ações preventivas, reduzindo acidentes, custos operacionais e passivos jurídicos.
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
app.include_router(chamados_router)
app.include_router(solicitacoes_router)
app.include_router(usuarios_router)

if __name__ == '__main__':
    pass