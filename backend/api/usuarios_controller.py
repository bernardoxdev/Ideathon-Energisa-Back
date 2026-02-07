from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import cast

from backend.core.database import get_db
from backend.core.security import require_role

from backend.models.user import User
from backend.models.parceiros import Parceiros
from backend.models.funcionarios import Funcionarios
from backend.models.admin import Admin
from backend.models.schemas import ListaUsuariosRequest
from backend.models.return_schemas import Status

router = APIRouter(
    prefix="/usuarios-controller",
    tags=["Usuarios Controller"]
)

@router.get(
    "/", status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="Pega a lista de todos os usuarios",
    dependencies=[Depends(require_role("admin", "owner"))]
)
def listar_usuarios(
    data: ListaUsuariosRequest,
    db: Session = Depends(get_db)
):
    query = db.query(User)

    if data.role:
        query = query.filter(User.role == data.role)
    if data.username:
        query = query.filter(User.username.ilike(f"%{data.username}%"))
    if data.email:
        query = query.filter(User.email.ilike(f"%{data.email}%"))

    return query.all()

@router.patch(
    "/{user_id}/role", status_code=status.HTTP_200_OK,
    response_model=Status,
    summary="Atualizar Role",
    description="Atualiza a role de um usuario e faz os metodos necessarios para a troca de role",
    dependencies=[Depends(require_role("admin", "owner"))]
)
def alterar_role(
    user_id: int,
    nova_role: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "Usuário não encontrado")

    if user.role == nova_role:
        return {"msg": "Usuário já possui essa role"}

    if user.role == "parceiros" and user.parceiros:
        db.delete(user.parceiros)
    elif user.role == "funcionarios" and user.funcionarios:
        db.delete(user.funcionarios)
    elif user.role == "admin" and user.admin:
        db.delete(user.admin)

    user_id = cast(int, cast(object, user.id))

    if nova_role == "parceiros":
        db.add(Parceiros(user_id=user_id))
    elif nova_role == "funcionarios":
        db.add(Funcionarios(user_id=user))
    elif nova_role == "admin":
        db.add(Admin(user_id=user_id))
    else:
        raise HTTPException(400, "Role inválida")

    user.role = nova_role
    db.commit()

    return Status(status="Role alterada com sucesso")

@router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT,
    summary="",
    description="",
    dependencies = [Depends(require_role("admin", "owner"))]
)
def deletar_usuario(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).get(user_id)

    if not user:
        raise HTTPException(404, "Usuário não encontrado")

    db.delete(user)
    db.commit()

if __name__ == '__main__':
    pass