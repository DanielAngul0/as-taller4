from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from database_sql import get_db
from models import Usuario, UsuarioCreate, UsuarioRead, UsuarioBase, UsuarioLogin


# --- Configuración ---
SECRET_KEY = "supersecretkey"  # en producción, cargar desde variable de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["auth"])

# --- Helpers ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



# ===========================
# Endpoints
# ===========================

# --- Endpoints de gestión de usuarios ---

# Registrar usuario
@router.post("/register")
def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    
    hashed_password = get_password_hash(usuario.password)
    new_user = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password=hashed_password,
        role=usuario.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User created", "id": new_user.id, "role": new_user.role}

# Loguear usuario
@router.post("/login")
def login(credenciales: UsuarioLogin, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.email == credenciales.email).first()
    if not db_user or not verify_password(credenciales.password, db_user.password):
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    
    access_token = create_access_token(
        data={"sub": db_user.email, "role": db_user.role}
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Listar todos los usuarios
@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return [
        {
            "id": u.id,
            "nombre": u.nombre,
            "email": u.email,
            "role": u.role,
            "fecha_registro": u.fecha_registro
        }
        for u in usuarios
    ]

# Obtener usuario por ID
@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "role": usuario.role,
        "fecha_registro": usuario.fecha_registro
    }

# Eliminar usuario
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"msg": f"Usuario {usuario.email} eliminado correctamente"}

# Actualizar rol de usuario
@router.put("/users/{user_id}/role")
def update_user_role(user_id: int, role: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.role = role
    db.commit()
    db.refresh(usuario)
    return {"msg": "Rol actualizado", "id": usuario.id, "nuevo rol": usuario.role}
