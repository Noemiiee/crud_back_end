import sqlite3
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel

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

# Fonctions d'accès aux données
def get_db_conn():
    conn = sqlite3.connect('bdd.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_current_user(db: sqlite3.Connection = Depends(get_db_conn)):
    # Ici, vous pouvez implémenter la logique d'authentification pour récupérer l'utilisateur actuel en fonction des informations d'authentification.
    # Dans cet exemple, nous supposons que l'utilisateur est authentifié et nous renvoyons un utilisateur fictif pour les besoins de démonstration.
    # Vous pouvez personnaliser cette fonction pour récupérer les informations de l'utilisateur à partir du jeton d'authentification, de la session, etc.
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

@router.post("/plannings", status_code=201)
def create_planning(planning: CreatePlanningRequest, db: sqlite3.Connection = Depends(get_db_conn)):
    cursor = db.cursor()
    cursor.execute(
    "INSERT INTO planning (entreprise_id, activite, jour, heure_debut, heure_fin) VALUES (?, ?, ?, ?, ?)",
    (planning.entreprise_id, planning.activite, planning.jour, planning.heure_debut, planning.heure_fin)
    )
    db.commit()

    return {"message": "Planning créé avec succès."}

@router.get("/plannings/{planning_id}", response_model=Planning)
def get_planning(planning_id: int, db: sqlite3.Connection = Depends(get_db_conn)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM planning WHERE id = ?", (planning_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Planning non trouvé.")

    planning = Planning(**row)
    return planning

@router.put("/plannings/{planning_id}", response_model=Planning)
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

@router.delete("/plannings/{planning_id}")
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

app.include_router(router, prefix="/api/plannings", tags=["plannings"])