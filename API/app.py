import os
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/familia")
def get_familia():
    rows = ["Amin", "Marce", "Miranda"]
    return rows

@app.get("/superheroesDC")
def get_superheroes():
    rows = ["Superman", "Batman", "Flash", "Linterna Verde", "Mujer maravilla", "Aquaman", "Shazam", "Cyborg"]
    return rows


@app.get("/superheroes")
def get_superheroes(
    universo: Optional[str] = Query(None, description="Filtrar por universo (DC, Marvel, Image)"),
    contiene: Optional[str] = Query(None, description="Filtrar por nombre que contenga este texto"),
    limite: int = Query(10, ge=1, le=50, description="Límite de resultados")
) -> List[str]:
    """
    Obtiene lista de superhéroes con filtros opcionales.
    Ejemplos:
    - /superheroes?universo=DC
    - /superheroes?contiene=man
    - /superheroes?universo=Marvel&limite=5
    """
    resultados = []
    
    # Filtrar por universo si se especifica
    if universo:
        resultados.extend(superheroes_db.get(universo.capitalize(), []))
    else:
        # Todos los superhéroes si no hay filtro
        for heroes in superheroes_db.values():
            resultados.extend(heroes)
    
    # Filtrar por texto en nombre
    if contiene:
        resultados = [hero for hero in resultados if contiene.lower() in hero.lower()]
    
    # Aplicar límite
    return resultados[:limite]

