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

class Entreprise(BaseModel):
    id: int
    nom: str
    adresse: str

class CreateEntrepriseRequest(BaseModel):
    nom: str
    adresse: str

class UpdateEntrepriseRequest(BaseModel):
    nom: str
    adresse: str

class Planning(BaseModel):
    id: int
    entreprise_id: int
    activite: str
    jour: str
    heure_debut: str
    heure_fin: str

class CreatePlanningRequest(BaseModel):
    entreprise_id: int
    activite: str
    jour: str
    heure_debut: str
    heure_fin: str

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

router_users = APIRouter()

@router_users.post("/users", status_code=201)
def create_user(user: CreateUserRequest, db: sqlite3.Connection = Depends(get_db_conn)):
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO utilisateur (nom, prenom, email, mot_de_passe, entreprise_id, rang) VALUES (?, ?, ?, ?, ?, ?)",
        (user.nom, user.prenom, user.email, user.mot_de_passe, user.entreprise_id, user.rang)
    )
    db.commit()

    return {"message": "Utilisateur créé avec succès."}

@router_users.get("/users/{user_id}", response_model=User)
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

@router_users.put("/users/{user_id}", response_model=User)
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

@router_users.delete("/users/{user_id}")
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
router_entreprises = APIRouter()

@router_entreprises.post("/entreprises", status_code=201)
def create_entreprise(entreprise: CreateEntrepriseRequest, db: sqlite3.Connection = Depends(get_db_conn)):
    cursor = db.cursor()
    cursor.execute(
    "INSERT INTO entreprise (nom, adresse) VALUES (?, ?)",
    (entreprise.nom, entreprise.adresse)
    )
    db.commit()

    return {"message": "Entreprise créée avec succès."}

@router_entreprises.get("/entreprises/{entreprise_id}", response_model=Entreprise)
def get_entreprise(entreprise_id: int, db: sqlite3.Connection = Depends(get_db_conn)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM entreprise WHERE id = ?", (entreprise_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Entreprise non trouvée.")

    entreprise = Entreprise(**row)
    return entreprise

@router_entreprises.put("/entreprises/{entreprise_id}", response_model=Entreprise)
def update_entreprise(entreprise_id: int, entreprise_data: UpdateEntrepriseRequest, db: sqlite3.Connection = Depends(get_db_conn)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM entreprise WHERE id = ?", (entreprise_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Entreprise non trouvée.")

    cursor.execute(
    "UPDATE entreprise SET nom = ?, adresse = ? WHERE id = ?",
    (entreprise_data.nom, entreprise_data.adresse, entreprise_id)
    )
    db.commit()
    entreprise = Entreprise(id=entreprise_id, nom=entreprise_data.nom, adresse=entreprise_data.adresse)
    return entreprise

@router_entreprises.delete("/entreprises/{entreprise_id}")
def delete_entreprise(entreprise_id: int, db: sqlite3.Connection = Depends(get_db_conn)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM entreprise WHERE id = ?", (entreprise_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Entreprise non trouvée.")

    cursor.execute("DELETE FROM entreprise WHERE id = ?", (entreprise_id,))
    db.commit()

    return {"message": "Entreprise supprimée avec succès."}

router_plannings = APIRouter()

@router_plannings.post("/plannings", status_code=201)
def create_planning(planning: CreatePlanningRequest, db: sqlite3.Connection = Depends(get_db_conn)):
    cursor = db.cursor()
    cursor.execute(
    "INSERT INTO planning (entreprise_id, activite, jour, heure_debut, heure_fin) VALUES (?, ?, ?, ?, ?)",
    (planning.entreprise_id, planning.activite, planning.jour, planning.heure_debut, planning.heure_fin)
    )
    db.commit()

    return {"message": "Planning créé avec succès."}

@router_plannings.get("/plannings/{planning_id}", response_model=Planning)
def get_planning(planning_id: int, db: sqlite3.Connection = Depends(get_db_conn)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM planning WHERE id = ?", (planning_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Planning non trouvé.")

    planning = Planning(**row)
    return planning

@router_plannings.put("/plannings/{planning_id}", response_model=Planning)
def update_planning(planning_id: int, planning_data: CreatePlanningRequest, db: sqlite3.Connection = Depends(get_db_conn)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM planning WHERE id = ?", (planning_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Planning non trouvé.")

    cursor.execute(
        "UPDATE planning SET entreprise_id = ?, activite = ?, jour = ?, heure_debut = ?, heure_fin = ? WHERE id = ?",
        (planning_data.entreprise_id, planning_data.activite, planning_data.jour, planning_data.heure_debut, planning_data.heure_fin, planning_id)
    )
    db.commit()

    planning = Planning(id=planning_id, **planning_data.dict())
    return planning

@router_plannings.delete("/plannings/{planning_id}")
def delete_planning(planning_id: int, db: sqlite3.Connection = Depends(get_db_conn)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM planning WHERE id = ?", (planning_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Planning non trouvé.")

    cursor.execute("DELETE FROM planning WHERE id = ?", (planning_id,))
    db.commit()

    return {"message": "Planning supprimé avec succès."}

app = FastAPI()

app.include_router(router_users, prefix="/api/users", tags=["users"])
app.include_router(router_entreprises, prefix="/api/entreprises", tags=["entreprises"])
app.include_router(router_plannings, prefix="/api/plannings", tags=["plannings"])