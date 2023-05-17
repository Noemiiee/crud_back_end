import sqlite3
from fastapi import FastAPI, APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Bienvenue sur mon API FastAPI."}

@router.post("/createdb")
def create_database():
    try:
        conn = sqlite3.connect('bdd.db')
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

        conn.close()

        return {"message": "Base de données créée avec succès."}
    except Exception as e:
        return {"message": f"Erreur lors de la création de la base de données : {str(e)}"}

@router.get("/users")
def list_users():
    try:
        conn = sqlite3.connect('bdd.db')
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

        conn.close()

        return {"users": users}
    except Exception as e:
        return {"message": f"Erreur lors de la récupération des utilisateurs : {str(e)}"}

@router.post("/users/create")
def create_user(nom: str, prenom: str, email: str, mot_de_passe: str):
    try:
        with sqlite3.connect('bdd.db') as conn:
            cursor = conn.cursor()
        return {"message": "Utilisateur créé avec succès."}
    except Exception as e:
        return {"message": f"Erreur lors de la création de l'utilisateur : {str(e)}"}

@router.post("/users/login")
def login_user(email: str, mot_de_passe: str):
    try:
        conn = sqlite3.connect('bdd.db')
        cursor = conn.cursor()

        cursor.execute("SELECT mot_de_passe FROM utilisateur WHERE email = ?", (email,))
        row = cursor.fetchone()

        if row is not None:
            hashed_password_from_db = row[0]
            if mot_de_passe == hashed_password_from_db:
                return {"message": "Connexion réussie."}
            else:
                return {"message": "Mot de passe incorrect."}
        else:
            return {"message": "Utilisateur non trouvé."}

        conn.close()
    except Exception as e:
        return {"message": f"Erreur lors de la connexion de l'utilisateur : {str(e)}"}

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

