from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
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

historico_predicoes = []

def converter_categoricas(dados_dict):
    genero_map = {'M': 1, 'F': 2}
    plataforma_map = {'Instagram': 1, 'TikTok': 2, 'ambos': 3}
    interacao_map = {'baixo': 0, 'medio': 1, 'alto': 2}

    dados_dict['genero'] = genero_map.get(dados_dict['genero'], -1)
    dados_dict['uso_plataforma'] = plataforma_map.get(dados_dict['uso_plataforma'], -1)
    dados_dict['nivel_interacao_social'] = interacao_map.get(dados_dict['nivel_interacao_social'], -1)

    return dados_dict

@app.get("/")
def home():
    return {"mensagem": "API de Predição online! Acesse /docs para ver a documentação."}

@app.post("/prever")
def fazer_predicao(dados: TeenHealthData):
    dados_dict = dados.model_dump()
    dados_dict = converter_categoricas(dados_dict)
    df_entrada = pd.DataFrame([dados_dict])
        
    try:
        resultado = modelo.predict(df_entrada)
        predicao = int(resultado[0])

        historico_predicoes.append({
            "id": len(historico_predicoes) + 1,
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dados_entrada": dados_dict,
            "predicao_ansiedade_alta": predicao
        })
        
        return {
            "status": "sucesso",
            "predicao_ansiedade_alta": predicao,
            "dados_recebidos": dados_dict
        }
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}
    
@app.get("/predicoes")
def consultar_predicoes():
    return {
        "total": len(historico_predicoes),
        "predicoes": historico_predicoes
    }