#System imports

#Libs imports
from fastapi import FastAPI, Response, status

#Local imports
from routers import fonctionnalitescruduser, fonctionnalitescrudplanning, fonctionnalitescrudentreprises
from internal import connexion, creationbdd

app = FastAPI()

app.include_router(connexion.router, tags=["Connexion"])
app.include_router(creationbdd.router, tags=["Création de la base de données"])
app.include_router(fonctionnalitescruduser.router, tags=["CRUD Utilisateurs"])
app.include_router(fonctionnalitescrudplanning.router, tags=["CRUD Planning"])
app.include_router(fonctionnalitescrudentreprises.router, tags=["CRUD Entreprises"])