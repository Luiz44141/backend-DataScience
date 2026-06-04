from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="API - Predição de Saúde Mental (Adolescentes)",
    description="API para classificar o impacto das redes sociais na saúde mental.",
    version="1.0.0"
)

# Configuração de CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # PESSOAL DO FRONTEND, SUBSTITUAM O '*' PELO DOMÍNIO DO SEU FRONTEND (ex: 'http://localhost:3000')
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 1. DEFINIÇÃO DOS DADOS DE ENTRADA
# ==========================================
# Baseado nas colunas traduzidas no Google Colab
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
    nivel_ansiedade: int
    nivel_vicio: int

# ==========================================
# 2. CARREGAMENTO DO MODELO (MOCK TEMPORÁRIO)
# ==========================================
# TODO: Quando o modelo real estiver pronto, descomente o bloco abaixo e apague a classe Mock.

'''
try:
    with open("models/modelo_classificacao.pkl", "rb") as f:
        modelo = pickle.load(f)
except FileNotFoundError:
    modelo = None
    print("Aviso: Modelo não encontrado. Verifique o diretório 'models/'.")
'''

class MockModel:
    def predict(self, df):
        # Simula uma predição
        return [1] 

modelo = MockModel()

# ==========================================
# 3. ENDPOINTS DA API
# ==========================================

@app.get("/")
def home():
    return {"mensagem": "API de Predição online! Acesse /docs para ver a documentação."}

@app.post("/predict")
def fazer_predicao(dados: TeenHealthData):
    # 1. Transforma os dados recebidos do JSON em um Dicionário, e depois em um DataFrame do Pandas
    dados_dict = dados.model_dump()
    df_entrada = pd.DataFrame([dados_dict])
        
    # 2. Realiza a predição
    try:
        resultado = modelo.predict(df_entrada)
        
        # 3. Retorna o resultado para o frontend
        return {
            "status": "sucesso",
            "predicao_indicador_depressao": int(resultado[0]),
            "dados_recebidos": dados_dict
        }
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}