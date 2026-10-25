# CardioRisk AI — Predição de Risco de Doença Cardiovascular

Aplicação de Aprendizado de Máquina Supervisionado para Apoio à Triagem e Predição Precoce de Cardiopatias Coronarianas.

- **Instituição:** Instituto Federal de Educação, Ciência e Tecnologia de São Paulo (IFSP) — Câmpus Catanduva
- **Disciplina:** Tópicos Avançados em Inteligência Artificial
- **Docente:** Prof. Dr. Márcio Andrey Teixeira
- **Discente:** Pedro Henrique Oliveira Pereira
- **Data de Entrega:** 26/10/2026

---

## 🌐 Link da Aplicação em Produção (Deploy)

A aplicação interativa encontra-se publicada e disponível publicamente para testes e avaliação:
- **Link Oficial no Streamlit Cloud:** [https://cardiorisk-ai.streamlit.app](https://cardiorisk-ai.streamlit.app)
- **Repositório GitHub Oficial:** [https://github.com/PedroPereiraAst/cardiorisk-ai](https://github.com/PedroPereiraAst/cardiorisk-ai)

*(Nota: Caso acesse localmente, siga as instruções de execução descritas adiante).*

---

## 1. Descrição do Problema e Objetivo

As doenças cardiovasculares representam a primeira causa de óbito em âmbito global. O objetivo deste projeto é construir uma solução preditiva de inteligência artificial capaz de estimar o risco de presença de doença arterial coronariana significativa (estenose > 50% de diâmetro) a partir de parâmetros clínicos, hemodinâmicos e eletrocardiográficos não invasivos.

O público-alvo são profissionais de saúde (em triagem clínica primária) e pacientes sob investigação preventiva. O sistema não substitui a consulta médica nem exames de padrão-ouro (como cineangiocoronariografia), atuando como ferramenta de estratificação inicial de risco.

---

## 2. Dataset Utilizado

- **Nome:** Cleveland Heart Disease Dataset
- **Origem:** Repositório UCI Machine Learning Repository (consolidado pelo Dr. Robert Detrano da Cleveland Clinic Foundation).
- **Tamanho:** 303 instâncias (pacientes) e 14 atributos (13 preditores clínicos + 1 variável alvo).
- **Tratamento da Alvo:** A variável original possuía valores de 0 a 4 (ausência a múltiplos graus de estenose). Foi binarizada em:
  - `0`: Ausência de doença coronariana (164 amostras, 54.1%)
  - `1`: Presença de doença coronariana significativa (139 amostras, 45.9%)
- **Tratamento de Dados Ausentes:** Identificados 4 valores nulos em `ca` (fluoroscopia) e 2 em `thal` (cintilografia). O tratamento foi encapsulado em pipeline utilizando `SimpleImputer` (mediana para numéricas e moda para categóricas), ajustado **estritamente sobre o conjunto de treino** para garantir ausência total de vazamento de dados (*data leakage*).

---

## 3. Arquitetura e Modelagem

Foram construídos pipelines scikit-learn com `ColumnTransformer`:
- **Variáveis Numéricas Contínuas (`age`, `trestbps`, `chol`, `thalach`, `oldpeak`):** `SimpleImputer(median)` + `StandardScaler()`.
- **Variáveis Categóricas (`sex`, `cp`, `fbs`, `restecg`, `exang`, `slope`, `ca`, `thal`):** `SimpleImputer(most_frequent)` + `OneHotEncoder(handle_unknown='ignore', drop='first')`.

### Comparação de Modelos (Validação Cruzada 5-Fold & Teste Cego Hold-Out)

| Métrica | Regressão Logística (CV) | Random Forest (CV) | Regressão Logística (Teste N=61) | Random Forest (Teste N=61) |
|---|---|---|---|---|
| **Acurácia** | **84.29% (±1.68%)** | 77.67% (±2.17%) | **86.89%** | **86.89%** |
| **Sensibilidade (Recall)** | **79.21%** | 71.11% | **89.29% (25/28)** | **89.29% (25/28)** |
| **Precisão** | **86.58%** | 78.90% | **83.33%** | **83.33%** |
| **F1-Score** | **82.14%** | 74.46% | **86.21%** | **86.21%** |
| **Área sob a Curva ROC (AUC)** | **0.9021** | 0.8816 | **0.9621** | 0.9481 |

**Justificativa do Modelo Escolhido:**
A **Regressão Logística** foi selecionada como modelo definitivo para produção devido à sua superioridade consistente em validação cruzada (F1-score de 82.14% vs 74.46%), AUC excepcional no teste cego (0.9621) e menor propensão a sobreajuste (*overfitting*) em datasets médicos tabulares compactos, além de propiciar probabilidades calibradas diretamente interpretáveis.

---

## 4. Estrutura do Repositório

```
cardiorisk-ai/
├── data/
│   └── heart.csv                   # Dataset bruto da Cleveland Clinic (UCI)
├── models/
│   ├── heart_disease_pipeline.joblib   # Pipeline campeão serializado
│   └── random_forest_pipeline.joblib  # Pipeline comparativo serializado
├── notebooks/
│   └── analise_e_treinamento.ipynb # Notebook com análise exploratória e experimentos
├── reports/
│   ├── figures/                    # Gráficos de matrizes de confusão, ROC e importância
│   ├── metrics_summary.json        # Resumo quantitativo das métricas
│   └── casos_de_teste_resultados.json # Registro dos 5 testes obrigatórios
├── src/
│   └── train.py                    # Script de treinamento, validação e exportação
├── app.py                          # Aplicação interativa Streamlit com validação
├── test_cases.py                   # Script de execução dos 5 casos de teste
├── requirements.txt                # Dependências do projeto
├── README.md                       # Documentação completa
└── Relatorio_Topicos_Avancados_IA.pdf # Relatório acadêmico formatado (4-6 páginas)
```

---

## 5. Como Executar Localmente

### Pré-requisitos
- Python 3.10 ou superior instalado.
- Gerenciador de pacotes `pip`.

### Passo a Passo

1. **Clonar o Repositório:**
```bash
git clone https://github.com/PedroPereiraAst/cardiorisk-ai.git
cd cardiorisk-ai
```

2. **Criar e Ativar Ambiente Virtual:**
- No Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```
- No Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. **Instalar Dependências:**
```bash
pip install -r requirements.txt
```

4. **Executar o Treinamento e Avaliação (Opcional - Modelo já vem pré-treinado):**
```bash
python src/train.py
```

5. **Executar a Bateria de Testes Automatizados:**
```bash
python test_cases.py
```

6. **Iniciar a Aplicação Web Streamlit:**
```bash
streamlit run app.py
```
Acesse no navegador: `http://localhost:8501`.

---

## 6. Casos de Teste Documentados (Item 7 do Edital)

A aplicação conta com um seletor na barra lateral que carrega automaticamente os 5 casos de teste:
1. **Caso 1 (Válido - Baixo Risco):** Mulher de 32 anos, assintomática, exames basais ideais.  
   *Resultado:* Baixo Risco (Probabilidade de doença: 0.71%).
2. **Caso 2 (Válido - Risco Moderado):** Homem de 52 anos, dor atípica, pré-hipertensão leve.  
   *Resultado:* Risco Moderado / Atenção (Probabilidade: 64.21%).
3. **Caso 3 (Válido - Alto Risco):** Homem de 68 anos com múltiplos marcadores isquêmicos e teste de esforço positivo.  
   *Resultado:* Alto Risco Crítico (Probabilidade: 98.02%).
4. **Caso 4 (Inválido / Incompleto):** Parâmetros fora dos limites vitais (idade 145 anos, pressão 20 mmHg, FC 350 bpm).  
   *Resultado:* Bloqueio total da inferência com 5 mensagens de erro fisiológico.
5. **Caso 5 (Limítrofe / Borderline):** Parâmetros conflitantes na fronteira de decisão.  
   *Resultado:* Probabilidade de 38.65% com alerta de caso limítrofe e necessidade de exames complementares.

---

## 7. Responsabilidade Ética e Limitações

- O sistema é um protótipo acadêmico para fins didáticos.
- Jamais tome decisões farmacológicas ou cirúrgicas baseadas nesta ferramenta.
- Em caso de sintomas cardiovasculares, procure imediatamente atendimento médico especializado.
