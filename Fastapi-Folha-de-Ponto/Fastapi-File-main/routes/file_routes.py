from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

# Simular um banco de dados em memória
registros_ponto = []

@router.post("/registrar_ponto/")
def registrar_ponto(usuario: str):
    horario_atual = datetime.now()
    registros_ponto.append({"usuario": usuario, "horario": horario_atual})
    return {"message": f"Ponto registrado para {usuario} às {horario_atual}"}

@router.get("/consultar_pontos/")
def consultar_pontos():
    return {"registros": registros_ponto}
