import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st

# Configuracao da pagina
st.set_page_config(
    page_title="CardioRisk AI | Triagem Cardiovascular",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilizacao CSS personalizada
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .risk-card-high {
        background-color: #fee2e2;
        border-left: 6px solid #ef4444;
        padding: 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .risk-card-low {
        background-color: #dcfce7;
        border-left: 6px solid #22c55e;
        padding: 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .risk-card-borderline {
        background-color: #fef3c7;
        border-left: 6px solid #f59e0b;
        padding: 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .stButton>button {
        background-color: #1e40af;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        width: 100%;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
</style>
""", unsafe_allow_html=True)

# Cache do modelo
@st.cache_resource
def carregar_modelo():
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, "models", "heart_disease_pipeline.joblib")
    if not os.path.exists(model_path):
        st.error(f"Arquivo do modelo nao encontrado em: {model_path}. Execute o treinamento primeiro!")
        return None
    return joblib.load(model_path)

pipeline = carregar_modelo()

# Barra lateral - Identificacao e Casos Pré-configurados
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/865/865969.png", width=80)
st.sidebar.title("CardioRisk AI")
st.sidebar.markdown("""
**Disciplina:** Tópicos Avançados em Inteligência Artificial  
**Docente:** Prof. Dr. Márcio Andrey Teixeira  
**Discente:** Pedro Henrique Oliveira Pereira  
**Instituição:** IFSP — Câmpus Catanduva
""")

st.sidebar.markdown("---")
st.sidebar.subheader("🧪 Casos de Teste Prontos")
st.sidebar.info("Selecione um caso para preencher o formulário automaticamente:")

caso_selecionado = st.sidebar.selectbox(
    "Carregar Caso de Teste:",
    [
        "Entrada Manual",
        "Caso 1 (Válido: Baixo Risco - Jovem)",
        "Caso 2 (Válido: Risco Moderado - Meia Idade)",
        "Caso 3 (Válido: Alto Risco - Idoso Sintomático)",
        "Caso 4 (Inválido: Valores Biológicos Inconsistentes)",
        "Caso 5 (Limítrofe / Borderline: Fronteira de Decisão)"
    ]
)

# Valores padrao conforme o caso selecionado
default_vals = {
    "age": 54, "sex": "Masculino", "cp": "Dor Não Anginosa", "trestbps": 130,
    "chol": 240, "fbs": "Não (<= 120 mg/dl)", "restecg": "Normal",
    "thalach": 150, "exang": "Não", "oldpeak": 0.8, "slope": "Plano",
    "ca": 0, "thal": "Normal"
}

if caso_selecionado == "Caso 1 (Válido: Baixo Risco - Jovem)":
    default_vals = {
        "age": 32, "sex": "Feminino", "cp": "Dor Não Anginosa", "trestbps": 115,
        "chol": 175, "fbs": "Não (<= 120 mg/dl)", "restecg": "Normal",
        "thalach": 178, "exang": "Não", "oldpeak": 0.0, "slope": "Ascendente",
        "ca": 0, "thal": "Normal"
    }
elif caso_selecionado == "Caso 2 (Válido: Risco Moderado - Meia Idade)":
    default_vals = {
        "age": 52, "sex": "Masculino", "cp": "Angina Atípica", "trestbps": 135,
        "chol": 225, "fbs": "Não (<= 120 mg/dl)", "restecg": "Normal",
        "thalach": 145, "exang": "Não", "oldpeak": 1.2, "slope": "Plano",
        "ca": 1, "thal": "Normal"
    }
elif caso_selecionado == "Caso 3 (Válido: Alto Risco - Idoso Sintomático)":
    default_vals = {
        "age": 68, "sex": "Masculino", "cp": "Assintomático (Típico Isquêmico)", "trestbps": 165,
        "chol": 295, "fbs": "Sim (> 120 mg/dl)", "restecg": "Alteração ST-T",
        "thalach": 118, "exang": "Sim", "oldpeak": 2.8, "slope": "Descendente",
        "ca": 2, "thal": "Defeito Reversível"
    }
elif caso_selecionado == "Caso 4 (Inválido: Valores Biológicos Inconsistentes)":
    default_vals = {
        "age": 145, "sex": "Masculino", "cp": "Assintomático (Típico Isquêmico)", "trestbps": 20,
        "chol": 30, "fbs": "Não (<= 120 mg/dl)", "restecg": "Normal",
        "thalach": 350, "exang": "Não", "oldpeak": -5.0, "slope": "Plano",
        "ca": 0, "thal": "Normal"
    }
elif caso_selecionado == "Caso 5 (Limítrofe / Borderline: Fronteira de Decisão)":
    default_vals = {
        "age": 57, "sex": "Masculino", "cp": "Dor Não Anginosa", "trestbps": 130,
        "chol": 236, "fbs": "Não (<= 120 mg/dl)", "restecg": "Normal",
        "thalach": 174, "exang": "Não", "oldpeak": 0.0, "slope": "Ascendente",
        "ca": 1, "thal": "Defeito Reversível"
    }

# Cabecalho Principal
st.markdown('<div class="main-header">🫀 CardioRisk AI — Sistema de Apoio à Triagem de Cardiopatias</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Aplicação de Aprendizado de Máquina para predição precoce de risco de doença arterial coronariana baseada em parâmetros clínicos e eletrocardiográficos (Dataset Cleveland / UCI Machine Learning).</div>', unsafe_allow_html=True)

# Layout em Tabs
tab_pred, tab_about, tab_metrics = st.tabs(["🩺 Formulário de Triagem", "ℹ️ Sobre o Problema e Atributos", "📊 Métricas dos Modelos"])

with tab_pred:
    st.subheader("Entrada de Dados Clínicos do Paciente")
    st.caption("Preencha todos os parâmetros clínicos para realizar a inferência em tempo real.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("##### 👤 Dados Demográficos")
        age = st.number_input(
            "Idade (anos):",
            min_value=1, max_value=150, value=default_vals["age"],
            help="Idade cronológica do paciente em anos completos."
        )
        sex_str = st.selectbox(
            "Sexo Biológico:",
            ["Masculino", "Feminino"],
            index=0 if default_vals["sex"] == "Masculino" else 1,
            help="Sexo biológico de nascimento (relevante para calibração de risco vascular)."
        )
        cp_str = st.selectbox(
            "Tipo de Dor no Peito:",
            [
                "Dor Não Anginosa",
                "Angina Típica",
                "Angina Atípica",
                "Assintomático (Típico Isquêmico)"
            ],
            index=[
                "Dor Não Anginosa", "Angina Típica", "Angina Atípica", "Assintomático (Típico Isquêmico)"
            ].index(default_vals["cp"]),
            help="Classificação semiológica da dor torácica reportada."
        )

    with col2:
        st.markdown("##### 🩸 Parâmetros Hemodinâmicos")
        trestbps = st.number_input(
            "Pressão Arterial em Repouso (mmHg):",
            min_value=10, max_value=350, value=default_vals["trestbps"],
            help="Pressão arterial sistólica aferida na admissão em repouso."
        )
        chol = st.number_input(
            "Colesterol Sérico (mg/dl):",
            min_value=10, max_value=800, value=default_vals["chol"],
            help="Nível de colesterol total no sangue em jejum."
        )
        fbs_str = st.selectbox(
            "Glicemia de Jejum > 120 mg/dl:",
            ["Não (<= 120 mg/dl)", "Sim (> 120 mg/dl)"],
            index=0 if "Não" in default_vals["fbs"] else 1,
            help="Indicador de hiperglicemia ou histórico de diabetes mellitus."
        )
        restecg_str = st.selectbox(
            "ECG em Repouso:",
            ["Normal", "Alteração ST-T", "Hipertrofia Ventricular Esquerda"],
            index=["Normal", "Alteração ST-T", "Hipertrofia Ventricular Esquerda"].index(default_vals["restecg"]),
            help="Achados do eletrocardiograma basal de repouso."
        )

    with col3:
        st.markdown("##### 🏃 Teste Ergométrico & Cintilografia")
        thalach = st.number_input(
            "Frequência Cardíaca Máxima (bpm):",
            min_value=20, max_value=350, value=default_vals["thalach"],
            help="Frequência máxima atingida durante teste de esforço ergométrico."
        )
        exang_str = st.selectbox(
            "Angina Induzida por Exercício:",
            ["Não", "Sim"],
            index=0 if default_vals["exang"] == "Não" else 1,
            help="Ocorrência de dor anginosa durante o esforço físico."
        )
        oldpeak = st.number_input(
            "Depressão de ST (oldpeak em mm):",
            min_value=-10.0, max_value=15.0, value=float(default_vals["oldpeak"]), step=0.1,
            help="Depressão do segmento ST induzida pelo exercício relativa ao repouso."
        )
        slope_str = st.selectbox(
            "Inclinação do Segmento ST (slope):",
            ["Ascendente", "Plano", "Descendente"],
            index=["Ascendente", "Plano", "Descendente"].index(default_vals["slope"]),
            help="Morfologia do segmento ST no pico do esforço físico."
        )
        ca = st.slider(
            "Vasos Principais com Fluoroscopia (0 a 3):",
            min_value=0, max_value=3, value=default_vals["ca"],
            help="Número de grandes vasos coronarianos coloridos por fluoroscopia."
        )
        thal_str = st.selectbox(
            "Cintilografia / Talassemia (thal):",
            ["Normal", "Defeito Fixo", "Defeito Reversível"],
            index=["Normal", "Defeito Fixo", "Defeito Reversível"].index(default_vals["thal"]),
            help="Avaliação de perfusão miocárdica."
        )

    st.markdown("---")
    
    # Validacao de Regras de Negocio e Biologia Clinica
    erros_validacao = []
    
    if age < 18 or age > 115:
        erros_validacao.append(f"⚠️ Idade informada ({age} anos) fora da faixa biológica humana recomendada (18 a 115 anos).")
    if trestbps < 60 or trestbps > 250:
        erros_validacao.append(f"⚠️ Pressão arterial sistólica ({trestbps} mmHg) incompatível com parâmetros vitais estáveis (60 a 250 mmHg).")
    if chol < 80 or chol > 600:
        erros_validacao.append(f"⚠️ Colesterol sérico ({chol} mg/dl) fora da amplitude clínica de análise (80 a 600 mg/dl).")
    if thalach < 50 or thalach > 230:
        erros_validacao.append(f"⚠️ Frequência cardíaca ({thalach} bpm) fora dos limites fisiológicos aceitáveis (50 a 230 bpm).")
    if oldpeak < 0.0 or oldpeak > 8.0:
        erros_validacao.append(f"⚠️ Depressão de ST ({oldpeak} mm) fora dos padrões clínicos eletrocardiográficos (0.0 a 8.0 mm).")

    # Botao de Submissao
    btn_predict = st.button("🔍 Executar Inferência do Modelo de IA")

    if btn_predict:
        if erros_validacao:
            st.error("### ❌ Erro de Validação de Dados de Entrada")
            st.write("A entrada fornecida contém inconsistências fisiológicas que invalidam a inferência médica confiável:")
            for err in erros_validacao:
                st.markdown(f"- {err}")
            st.info("💡 Por favor, corrija os valores antes de solicitar nova predição.")
        else:
            # Mapeamento para as categorias numericas do dataset Cleveland
            sex_val = 1.0 if sex_str == "Masculino" else 0.0
            
            cp_map = {
                "Angina Típica": 1.0,
                "Angina Atípica": 2.0,
                "Dor Não Anginosa": 3.0,
                "Assintomático (Típico Isquêmico)": 4.0
            }
            cp_val = cp_map[cp_str]
            
            fbs_val = 1.0 if "Sim" in fbs_str else 0.0
            
            restecg_map = {
                "Normal": 0.0,
                "Alteração ST-T": 1.0,
                "Hipertrofia Ventricular Esquerda": 2.0
            }
            restecg_val = restecg_map[restecg_str]
            
            exang_val = 1.0 if exang_str == "Sim" else 0.0
            
            slope_map = {
                "Ascendente": 1.0,
                "Plano": 2.0,
                "Descendente": 3.0
            }
            slope_val = slope_map[slope_str]
            
            thal_map = {
                "Normal": 3.0,
                "Defeito Fixo": 6.0,
                "Defeito Reversível": 7.0
            }
            thal_val = thal_map[thal_str]

            # Montagem do DataFrame compativel com o Pipeline
            dados_entrada = pd.DataFrame([{
                'age': float(age),
                'sex': float(sex_val),
                'cp': float(cp_val),
                'trestbps': float(trestbps),
                'chol': float(chol),
                'fbs': float(fbs_val),
                'restecg': float(restecg_val),
                'thalach': float(thalach),
                'exang': float(exang_val),
                'oldpeak': float(oldpeak),
                'slope': float(slope_val),
                'ca': float(ca),
                'thal': float(thal_val)
            }])

            # Execucao da Inferencia
            predicao = pipeline.predict(dados_entrada)[0]
            probabilidades = pipeline.predict_proba(dados_entrada)[0]
            prob_risco = probabilidades[1] * 100
            prob_saudavel = probabilidades[0] * 100

            st.markdown("### 📋 Resultado da Inferência Clínica")

            res_col1, res_col2 = st.columns([1.2, 1])

            with res_col1:
                if 45.0 <= prob_risco <= 55.0:
                    st.markdown(f"""
                    <div class="risk-card-borderline">
                        <h3 style="color: #b45309; margin-top:0;">⚠️ Caso Limítrofe / Fronteira de Decisão ({prob_risco:.1f}%)</h3>
                        <p>O modelo identificou um perfil de risco limítrofe (probabilidade de cardiopatia de <b>{prob_risco:.1f}%</b> vs <b>{prob_saudavel:.1f}%</b> de normalidade). Em contextos clínicos de alta incerteza, o limiar padrão de 50% exige exames complementares de imagem e avaliação presencial especializada.</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif predicao == 1:
                    st.markdown(f"""
                    <div class="risk-card-high">
                        <h3 style="color: #b91c1c; margin-top:0;">🚨 Alto Risco de Doença Cardiovascular ({prob_risco:.1f}%)</h3>
                        <p>O modelo supervisionado identificou evidências consistentes de estenose coronariana significativa (> 50% de estreitamento). <b>Probabilidade estimada: {prob_risco:.1f}%</b>.</p>
                        <p><b>Recomendação:</b> Encaminhamento imediato para avaliação cardiológica completa, realização de ecocardiograma e acompanhamento médico especializado.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="risk-card-low">
                        <h3 style="color: #15803d; margin-top:0;">✅ Baixo Risco Cardiovascular ({prob_risco:.1f}%)</h3>
                        <p>O perfil clínico inserido indica baixa probabilidade estatística de cardiopatia coronariana isquêmica. <b>Probabilidade estimada: {prob_risco:.1f}%</b> (ausência de doença: {prob_saudavel:.1f}%).</p>
                        <p><b>Recomendação:</b> Manutenção de estilo de vida saudável, controle regular de pressão arterial e exames de rotina preventivos.</p>
                    </div>
                    """, unsafe_allow_html=True)

            with res_col2:
                st.markdown("##### 📈 Distribuição de Probabilidade")
                st.progress(float(prob_risco) / 100.0)
                st.write(f"- **Probabilidade de Cardiopatia:** `{prob_risco:.2f}%`")
                st.write(f"- **Probabilidade de Ausência:** `{prob_saudavel:.2f}%`")
                st.write(f"- **Algoritmo em Execução:** `Regressão Logística Regularizada (L2)`")
                st.write(f"- **Tempo de Inferência:** `< 15ms`")

    # Secao de Limitacoes Obrigatoria
    st.markdown("---")
    st.markdown("""
    #### ⚠️ Limitações e Responsabilidade Ética da Aplicação
    1. **Finalidade Educacional e Triagem:** Esta aplicação foi desenvolvida no âmbito acadêmico da disciplina de *Tópicos Avançados em IA* (IFSP Catanduva) e destina-se exclusivamente a fins didáticos e triagem experimental.
    2. **Não Substituição do Diagnóstico Clínico:** Nenhuma saída gerada por este modelo substitui consulta médica, parecer de cardiologista, anamnese detalhada ou exames laboratoriais/imagem (como cineangiocoronariografia).
    3. **Origem dos Dados e Vieses:** O modelo foi treinado sobre o *Cleveland Heart Disease Dataset*, coletado em ambiente hospitalar especializado na década de 1980, podendo refletir distribuições demográficas e tecnológicas específicas da época.
    """)

with tab_about:
    st.subheader("Origem dos Dados e Significado das Variáveis")
    st.markdown("""
    O dataset utilizado é o **Heart Disease Dataset (Cleveland)** disponibilizado pelo repositório **UCI Machine Learning Repository**, consolidado pelo Dr. Robert Detrano (Cleveland Clinic Foundation).
    
    | Variável | Nome Clínico | Tipo | Unidade / Valores | Descrição |
    |---|---|---|---|---|
    | `age` | Idade | Contínua | Anos (29 a 77) | Idade cronológica do paciente |
    | `sex` | Sexo Biológico | Categórica | 1 = Masc; 0 = Fem | Fator epidemiológico associado ao perfil de risco |
    | `cp` | Tipo de Dor Torácica | Categórica | 1 a 4 | 1: Angina típica, 2: Angina atípica, 3: Dor não anginosa, 4: Assintomático |
    | `trestbps` | Pressão em Repouso | Contínua | mmHg (94 a 200) | Pressão arterial sistólica na admissão hospitalar |
    | `chol` | Colesterol Sérico | Contínua | mg/dl (126 a 564) | Colesterol total medido em jejum |
    | `fbs` | Glicemia de Jejum | Categórica | 1 = >120; 0 = <=120 | Indicador correlacionado a diabetes mellitus |
    | `restecg` | Eletrocardiograma Basal | Categórica | 0 a 2 | 0: Normal, 1: Alteração de onda ST-T, 2: Hipertrofia Ventricular Esquerda |
    | `thalach` | Frequência Cardíaca Máx | Contínua | bpm (71 a 202) | Pico de pulsação atingido durante esforço físico |
    | `exang` | Angina de Esforço | Categórica | 1 = Sim; 0 = Não | Dor no peito desencadeada pelo teste ergométrico |
    | `oldpeak` | Depressão de ST | Contínua | mm (0.0 a 6.2) | Depressão do segmento ST induzida pelo exercício |
    | `slope` | Inclinação de ST | Categórica | 1 a 3 | 1: Ascendente, 2: Plano, 3: Descendente |
    | `ca` | Fluoroscopia Coronária | Discreta | 0 a 3 | Número de vasos maiores corados por contraste radiológico |
    | `thal` | Cintilografia Miocárdica | Categórica | 3, 6, 7 | 3: Normal, 6: Defeito Fixo, 7: Defeito Reversível |
    | `target` | Diagnóstico Alvo | Binária | 0 = Ausente; 1 = Presente | Estenose coronariana > 50% em pelo menos um vaso |
    """)

with tab_metrics:
    st.subheader("Resultados Comparativos e Avaliação dos Modelos")
    st.markdown("""
    Foram treinados e comparados dois algoritmos supervisionados clássicos: **Regressão Logística** (modelo linear probabilístico) e **Random Forest** (ensemble de árvores de decisão), avaliados em validação cruzada estratificada (5-folds) e teste cego hold-out (20% das amostras).
    """)

    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.markdown("##### Regressão Logística (Modelo Escolhido para Deploy)")
        st.write("- **Acurácia (Teste):** `86.89%`")
        st.write("- **Sensibilidade (Recall):** `89.29%` *(apenas 3 falsos negativos)*")
        st.write("- **Precisão:** `83.33%`")
        st.write("- **F1-Score:** `86.21%`")
        st.write("- **Área sob a Curva ROC (AUC):** `0.9621`")
        st.write("- **Acurácia CV 5-Fold:** `84.29% (± 1.68%)`")
        st.write("- **F1-Score CV 5-Fold:** `82.14% (± 2.15%)`")

    with m_col2:
        st.markdown("##### Random Forest Classifier (Modelo Alternativo)")
        st.write("- **Acurácia (Teste):** `86.89%`")
        st.write("- **Sensibilidade (Recall):** `89.29%`")
        st.write("- **Precisão:** `83.33%`")
        st.write("- **F1-Score:** `86.21%`")
        st.write("- **Área sob a Curva ROC (AUC):** `0.9481`")
        st.write("- **Acurácia CV 5-Fold:** `77.67% (± 2.17%)`")
        st.write("- **F1-Score CV 5-Fold:** `74.46% (± 2.37%)`")

    st.markdown("---")
    st.markdown("##### 🖼️ Gráficos Gerados pelo Pipeline")
    
    g_col1, g_col2 = st.columns(2)
    fig_dir = os.path.join(os.path.dirname(__file__), "reports", "figures")
    
    cm_img = os.path.join(fig_dir, "matriz_confusao_comparativa.png")
    roc_img = os.path.join(fig_dir, "curvas_roc.png")
    rf_img = os.path.join(fig_dir, "importancia_atributos_rf.png")

    if os.path.exists(cm_img):
        g_col1.image(cm_img, caption="Matrizes de Confusão Comparativas (Teste N=61)", use_container_width=True)
    if os.path.exists(roc_img):
        g_col2.image(roc_img, caption="Curvas ROC e Valores de AUC Comparativos", use_container_width=True)
    if os.path.exists(rf_img):
        st.image(rf_img, caption="Importância dos Atributos Clínicos Calculada pelo Random Forest", use_container_width=True)
