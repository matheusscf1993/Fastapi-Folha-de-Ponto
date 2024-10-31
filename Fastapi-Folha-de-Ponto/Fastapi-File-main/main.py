import uvicorn
from fastapi import FastAPI
from routes import file_routes

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Sistema de Folha de Ponto - Bem-vindo"}

# Incluir as rotas de controle de ponto
app.include_router(file_routes.router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)