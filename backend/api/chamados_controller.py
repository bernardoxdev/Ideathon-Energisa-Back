from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

from backend.core.database import get_db
from backend.core.security import (
    require_role,
    get_current_user
)
from backend.core.uploads import salvar_imagem

from backend.models.fotos import Fotos
from backend.models.chamados import Chamados
from backend.models.enderecos import Enderecos
from backend.models.tipo_chamado import TiposChamados
from backend.models.user import User

router = APIRouter(prefix="/chamados", tags=["Chamados"])

@router.post(
    "/", status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("parceiros", "funcionarios", "admin", "owner"))]
)
def criar_chamado(
    descricao: str = Form(...),
    tipo_id: int = Form(...),
    endereco_id: int = Form(...),
    imagem: UploadFile = File(None),
    usuario: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chamado = Chamados(
        protocolo=f"CH-{usuario.id}-{tipo_id}",
        descricao=descricao,
        status="ABERTO",
        client_id=usuario.id,
        endereco_id=endereco_id,
        tipo_id=tipo_id
    )

    db.add(chamado)
    db.commit()
    db.refresh(chamado)

    if imagem:
        caminho = salvar_imagem(imagem, "chamados")
        foto = Fotos(
            caminho=caminho,
            origem="CHAMADO",
            chamado_id=chamado.id
        )
        db.add(foto)
        db.commit()

    return chamado

@router.get(
    "/", status_code=status.HTTP_200_OK,
    summary="",
    description="",
    dependencies=[Depends(require_role("parceiros", "funcionarios", "admin", "owner"))]
)
def listar_chamados(
    status_chamado: Optional[str] = Query(None),
    tipo_id: Optional[int] = Query(None),
    client_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    usuario: User = Depends(get_current_user)
):
    query = db.query(Chamados)

    # Regras por role
    if usuario.role == "parceiros":
        query = query.filter(Chamados.status == "ABERTO")
    elif usuario.role == "funcionarios":
        pass
    elif usuario.role == "admin":
        pass
    else:
        query = query.filter(Chamados.client_id == usuario.id)

    if status_chamado:
        query = query.filter(Chamados.status == status_chamado)
    if tipo_id:
        query = query.filter(Chamados.tipo_id == tipo_id)
    if client_id:
        query = query.filter(Chamados.client_id == client_id)

    return query.order_by(Chamados.criado_em.desc()).all()

@router.get(
    "/{chamado_id}", status_code=status.HTTP_200_OK,
    summary="",
    description="",
    dependencies=[Depends(require_role("parceiros", "funcionarios", "admin", "owner"))]
)
def obter_chamado(
    chamado_id: int,
    db: Session = Depends(get_db),
    usuario: User = Depends(get_current_user)
):
    chamado = db.query(Chamados).get(chamado_id)
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")

    if usuario.role not in ["admin", "funcionarios"] and chamado.client_id != usuario.id:
        raise HTTPException(403, "Acesso negado")

    return chamado

@router.patch(
    "/{chamado_id}", status_code=status.HTTP_200_OK,
    summary="",
    description="",
    dependencies=[Depends(require_role("parceiros", "funcionarios", "admin", "owner"))]
)
def atualizar_chamado(
    chamado_id: int,
    descricao: Optional[str] = None,
    status_chamado: Optional[str] = None,
    tipo_id: Optional[int] = None,
    db: Session = Depends(get_db),
    usuario: User = Depends(get_current_user)
):
    chamado = db.query(Chamados).get(chamado_id)
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")

    if usuario.role not in ["admin", "funcionarios"]:
        raise HTTPException(403, "Permissão negada")

    if descricao:
        chamado.descricao = descricao
    if status_chamado:
        chamado.status = status_chamado
    if tipo_id:
        chamado.tipo_id = tipo_id

    db.commit()
    db.refresh(chamado)
    return chamado

if __name__ == '__main__':
    pass