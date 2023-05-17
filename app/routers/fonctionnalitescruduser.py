import sqlite3
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel

class User(BaseModel):
    id: int
    nom: str
    prenom: str
    email: str
    mot_de_passe: str
    entreprise_id: int
    rang: str

class CreateUserRequest(BaseModel):
    nom: str
    prenom: str
    email: str
    mot_de_passe: str
    entreprise_id: int
    rang: str

class UpdateUserRequest(BaseModel):
    nom: str
    prenom: str
    mot_de_passe: str
    rang: str

def get_db_conn():
    conn = sqlite3.connect('bdd.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_current_user(db: sqlite3.Connection = Depends(get_db_conn)):
    user_data = {
        "id": 1,
        "nom": "John",
        "prenom": "Doe",
        "email": "john.doe@example.com",
        "mot_de_passe": "password",
        "entreprise_id": 1,
        "rang": "admin"
    }
    return User(**user_data)

router = APIRouter()

@router.post("/users", status_code=201)
def create_user(user: CreateUserRequest, db: sqlite3.Connection = Depends(get_db_conn)):
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO utilisateur (nom, prenom, email, mot_de_passe, entreprise_id, rang) VALUES (?, ?, ?, ?, ?, ?)",
        (user.nom, user.prenom, user.email, user.mot_de_passe, user.entreprise_id, user.rang)
    )
    db.commit()

    return {"message": "Utilisateur créé avec succès."}

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, current_user: User = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db_conn)):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM utilisateur WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    
    user = User(**row)

    if current_user.entreprise_id != user.entreprise_id:
        raise HTTPException(status_code=403, detail="Accès interdit.")
    return user

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_data: UpdateUserRequest, current_user: User = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db_conn)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM utilisateur WHERE id = ?", (user_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    user = User(**row)

    if current_user.entreprise_id != user.entreprise_id:
        raise HTTPException(status_code=403, detail="Accès interdit.")

    cursor.execute(
        "UPDATE utilisateur SET nom = ?, prenom = ?, mot_de_passe = ?, rang = ? WHERE id = ?",
        (user_data.nom, user_data.prenom, user_data.mot_de_passe, user_data.rang, user_id)
    )
    db.commit()

    return user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, current_user: User = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db_conn)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM utilisateur WHERE id = ?", (user_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    user = User(**row)

    if current_user.entreprise_id != user.entreprise_id:
        raise HTTPException(status_code=403, detail="Accès interdit.")

    cursor.execute("DELETE FROM utilisateur WHERE id = ?", (user_id,))
    db.commit()

    return {"message": "Utilisateur supprimé avec succès."}

app = FastAPI()

app.include_router(router, prefix="/api/users", tags=["users"])