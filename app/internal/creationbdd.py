import sqlite3
from fastapi import FastAPI, APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Bienvenue sur mon API FastAPI."}

@router.post("/createdb")
def create_database():
    try:
        with sqlite3.connect('bdd.db') as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS utilisateur (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    email TEXT NOT NULL,
                    mot_de_passe TEXT NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS entreprise (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    adresse TEXT NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS planning (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entreprise_id INTEGER,
                    activite TEXT NOT NULL,
                    jour DATE NOT NULL,
                    heure_debut TIME NOT NULL,
                    heure_fin TIME NOT NULL,
                    FOREIGN KEY (entreprise_id) REFERENCES entreprise(id)
                )
            ''')

        return {"message": "Base de données créée avec succès."}
    except Exception as e:
        return {"message": f"Erreur lors de la création de la base de données : {str(e)}"}

@router.get("/users")
def list_users():
    try:
        with sqlite3.connect('bdd.db') as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM utilisateur")
            rows = cursor.fetchall()

            users = []
            for row in rows:
                user = {
                    "id": row[0],
                    "nom": row[1],
                    "prenom": row[2],
                    "email": row[3],
                    "mot_de_passe": row[4]
                }
                users.append(user)

            return {"users": users}
    except Exception as e:
        return {"message": f"Erreur lors de la récupération des utilisateurs : {str(e)}"}

@router.get("/entreprises")
def list_entreprises():
    try:
        with sqlite3.connect('bdd.db') as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM entreprise")
            rows = cursor.fetchall()

            entreprises = []
            for row in rows:
                entreprise = {
                    "id": row[0],
                    "nom": row[1],
                    "adresse": row[2]
                }
                entreprises.append(entreprise)

            return {"entreprises": entreprises}
    except Exception as e:
        return {"message": f"Erreur lors de la récupération des entreprises : {str(e)}"}

@router.get("/plannings")
def list_plannings():
    try:
        with sqlite3.connect('bdd.db') as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM planning")
            rows = cursor.fetchall()

            plannings = []
            for row in rows:
                planning = {
                    "id": row[0],
                    "entreprise_id": row[1],
                    "activite": row[2],
                    "jour": row[3],
                    "heure_debut": row[4],
                    "heure_fin": row[5]
                }
                plannings.append(planning)

            return {"plannings": plannings}
    except Exception as e:
        return {"message": f"Erreur lors de la récupération des plannings : {str(e)}"}

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
   
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)