import sqlite3
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel

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

@router.post("/entreprises", status_code=201)
def create_entreprise(entreprise: CreateEntrepriseRequest, db: sqlite3.Connection = Depends(get_db_conn)):
    cursor = db.cursor()
    cursor.execute(
    "INSERT INTO entreprise (nom, adresse) VALUES (?, ?)",
    (entreprise.nom, entreprise.adresse)
    )
    db.commit()

    return {"message": "Entreprise créée avec succès."}

@router.get("/entreprises/{entreprise_id}", response_model=Entreprise)
def get_entreprise(entreprise_id: int, db: sqlite3.Connection = Depends(get_db_conn)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM entreprise WHERE id = ?", (entreprise_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Entreprise non trouvée.")

    entreprise = Entreprise(**row)
    return entreprise

@router.put("/entreprises/{entreprise_id}", response_model=Entreprise)
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

@router.delete("/entreprises/{entreprise_id}")
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

app = FastAPI()

app.include_router(router, prefix="/api/entreprises", tags=["entreprises"])