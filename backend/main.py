from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_database
import models
import routes

# Inicializar o banco de dados (executa SQL setup se necessário)
init_database()

app = FastAPI(title="Expense Tracker API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "Expense Tracker API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
