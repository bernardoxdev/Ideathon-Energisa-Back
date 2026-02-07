from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.security import (
    require_role,
    get_current_user
)
from backend.core.uploads import salvar_imagem

from backend.models.fotos import Fotos
from backend.models.solicitacoes import Solicitacoes
from backend.models.chamados import Chamados
from backend.models.user import User

router = APIRouter(prefix="/solicitacoes", tags=["Solicitações"])

@router.post(
    "/", status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("usuarios"))]
)
def criar_solicitacao(
    descricao: str = Form(...),
    tipo_id: int = Form(...),
    endereco_id: int = Form(...),
    imagem: UploadFile = File(None),
    usuario: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    solicitacao = Solicitacoes(
        descricao=descricao,
        client_id=usuario.id,
        endereco_id=endereco_id,
        tipo_id=tipo_id
    )

    db.add(solicitacao)
    db.commit()
    db.refresh(solicitacao)

    if imagem:
        caminho = salvar_imagem(imagem, "solicitacoes")
        foto = Fotos(
            caminho=caminho,
            origem="SOLICITACAO",
            solicitacao_id=solicitacao.id
        )
        db.add(foto)
        db.commit()

    return solicitacao

@router.get(
    "/", status_code=status.HTTP_200_OK,
    summary="",
    description="",
    dependencies=[Depends(require_role("funcionarios", "admin", "owner"))]
)
def listar_solicitacoes(
    db: Session = Depends(get_db),
    usuario: User = Depends(get_current_user)
):
    query = db.query(Solicitacoes)

    if usuario.role == "usuarios":
        query = query.filter(Solicitacoes.client_id == usuario.id)

    return query.order_by(Solicitacoes.criado_em.desc()).all()

@router.post(
    "/{solicitacao_id}/aprovar", status_code=status.HTTP_200_OK,
    summary="",
    description="",
    dependencies=[Depends(require_role("funcionarios", "admin", "owner"))]
)
def aprovar_solicitacao(
    solicitacao_id: int,
    db: Session = Depends(get_db),
    usuario: User = Depends(...)
):
    if usuario.role not in ["funcionarios", "admin"]:
        raise HTTPException(403, "Permissão negada")

    solicitacao = db.query(Solicitacoes).get(solicitacao_id)
    if not solicitacao:
        raise HTTPException(404, "Solicitação não encontrada")

    if solicitacao.status != "PENDENTE":
        raise HTTPException(400, "Solicitação já processada")

    chamado = Chamados(
        protocolo=f"CH-{solicitacao.id}",
        descricao=solicitacao.descricao,
        status="ABERTO",
        client_id=solicitacao.client_id,
        endereco_id=solicitacao.endereco_id,
        tipo_id=solicitacao.tipo_id
    )

    solicitacao.status = "APROVADA"

    db.add(chamado)
    db.commit()

    return {"msg": "Solicitação aprovada e chamado criado"}

@router.post(
    "/{solicitacao_id}/rejeitar", status_code=status.HTTP_200_OK,
    summary="",
    description="",
    dependencies=[Depends(require_role("funcionarios", "admin", "owner"))]
)
def rejeitar_solicitacao(
    solicitacao_id: int,
    motivo: str,
    db: Session = Depends(get_db),
    usuario: User = Depends(get_current_user)
):
    if usuario.role not in ["funcionarios", "admin"]:
        raise HTTPException(403, "Permissão negada")

    solicitacao = db.query(Solicitacoes).get(solicitacao_id)
    if not solicitacao:
        raise HTTPException(404, "Solicitação não encontrada")

    solicitacao.status = f"REJEITADA: {motivo}"
    db.commit()

    return {"msg": "Solicitação rejeitada"}

if __name__ == '__main__':
    pass