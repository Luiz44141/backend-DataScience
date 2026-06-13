# API - Predição de Saúde Mental (Adolescentes)

API desenvolvida com FastAPI para prever o nível de ansiedade de adolescentes com base em hábitos de uso de redes sociais.

## 📋 Pré-requisitos

- Python 3.10+
- pip

## 🚀 Como rodar

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd <nome-da-pasta>
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Coloque o modelo treinado em `models/melhor_modelo.pkl`

4. Inicie o servidor:
```bash
uvicorn main:app --reload
```

5. Acesse a documentação em `http://localhost:8000/docs`

## 📁 Estrutura do projeto

```
├── main.py
├── requirements.txt
├── .gitignore
└── models/
    └── melhor_modelo.pkl
```

## 🔌 Endpoints

### GET /
Verifica se a API está online.

### POST /prever
Recebe os dados de um adolescente e retorna a predição de ansiedade.

**Valores aceitos:**
| Campo | Valores aceitos |
|---|---|
| genero | `M`, `F` |
| uso_plataforma | `Instagram`, `TikTok`, `ambos` |
| nivel_interacao_social | `baixo`, `medio`, `alto` |

**Exemplo de resposta:**
```json
{
  "status": "sucesso",
  "predicao_ansiedade_alta": 1,
  "dados_recebidos": { ... }
}
```

> `predicao_ansiedade_alta`: **0** = ansiedade baixa, **1** = ansiedade alta

#### 🧪 Exemplos de requisição

**Perfil 1 — Adolescente com alto risco:**
```json
{
  "idade": 16,
  "genero": "M",
  "horas_diarias_redes_sociais": 7.5,
  "uso_plataforma": "TikTok",
  "horas_sono": 4.5,
  "tempo_tela_antes_dormir": 2.5,
  "desempenho_academico": 2.0,
  "atividade_fisica": 0.0,
  "nivel_interacao_social": "baixo",
  "nivel_estresse": 9,
  "nivel_vicio": 9
}
```

**Perfil 2 — Adolescente com baixo risco:**
```json
{
  "idade": 15,
  "genero": "F",
  "horas_diarias_redes_sociais": 1.5,
  "uso_plataforma": "Instagram",
  "horas_sono": 8.5,
  "tempo_tela_antes_dormir": 0.5,
  "desempenho_academico": 3.8,
  "atividade_fisica": 2.0,
  "nivel_interacao_social": "alto",
  "nivel_estresse": 2,
  "nivel_vicio": 1
}
```

**Perfil 3 — Adolescente intermediário:**
```json
{
  "idade": 17,
  "genero": "F",
  "horas_diarias_redes_sociais": 4.0,
  "uso_plataforma": "ambos",
  "horas_sono": 6.5,
  "tempo_tela_antes_dormir": 1.5,
  "desempenho_academico": 3.0,
  "atividade_fisica": 1.0,
  "nivel_interacao_social": "medio",
  "nivel_estresse": 5,
  "nivel_vicio": 5
}
```

### GET /predicoes
Retorna o histórico de todas as predições feitas desde que o servidor foi iniciado.

> ⚠️ O histórico é armazenado em memória. Ao reiniciar o servidor, o histórico é perdido.

**Exemplo de resposta:**
```json
{
  "total": 1,
  "predicoes": [
    {
      "id": 1,
      "data_hora": "2026-06-12 19:29:15",
      "dados_entrada": { ... },
      "predicao_ansiedade_alta": 1
    }
  ]
}
```

## 👥 Como contribuir com histórico persistente

O histórico atual é armazenado em memória e é perdido ao reiniciar o servidor. Caso queira persistir os dados, algumas opções são:

- **SQLite** — banco de dados local simples, sem necessidade de servidor
- **PostgreSQL** — banco de dados robusto para produção
- **MongoDB** — banco NoSQL, ideal para armazenar documentos JSON