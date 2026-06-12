from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(
    title="API - Predição de Saúde Mental (Adolescentes)",
    description="API que verifica o nível de ansiedade e suas correlações na saúde mental de adolescentes.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TeenHealthData(BaseModel):
    idade: int
    genero: str
    horas_diarias_redes_sociais: float
    uso_plataforma: str
    horas_sono: float
    tempo_tela_antes_dormir: float
    desempenho_academico: float
    atividade_fisica: float
    nivel_interacao_social: str
    nivel_estresse: int
    nivel_vicio: int

try:
    modelo = joblib.load("models/melhor_modelo.pkl")
    print("Modelo carregado com sucesso!")
except FileNotFoundError:
    modelo = None
    print("Aviso: Modelo não encontrado. Verifique o diretório 'models/'.")

@app.get("/")
def home():
    return {"mensagem": "API de Predição online! Acesse /docs para ver a documentação."}

@app.post("/predict")
def fazer_predicao(dados: TeenHealthData):
    dados_dict = dados.model_dump()
    df_entrada = pd.DataFrame([dados_dict])
        
    try:
        resultado = modelo.predict(df_entrada)
        
        return {
            "status": "sucesso",
            "predicao_ansiedade_alta": int(resultado[0]),
            "dados_recebidos": dados_dict
        }
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}