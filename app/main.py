
#Libs imports
from fastapi import FastAPI, Response, status

#Local imports
from internal import connexion, creationbdd

app = FastAPI()

app.include_router(connexion.router, tags=["Connexion"])
app.include_router(creationbdd.router, tags=["Création de la base de données"])