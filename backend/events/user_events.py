from sqlalchemy.orm import Session

from backend.models.user import User
from backend.models.parceiros import Parceiros
from backend.models.funcionarios import Funcionarios
from backend.models.admin import Admin

def on_user_created(user: User, db: Session):
    role_map = {
        "parceiros": Parceiros,
        "funcionarios": Funcionarios,
        "admin": Admin
    }

    model = role_map.get(user.role)
    if not model:
        return

    existe = db.query(model).filter_by(user_id=user.id).first()
    if existe:
        return

    db.add(model(user_id=user.id))
    db.commit()
