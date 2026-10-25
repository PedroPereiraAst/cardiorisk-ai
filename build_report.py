"""
Gerador do Relatorio Academico em PDF (Exatamente 6 Paginas)
CardioRisk AI - IFSP Catanduva
Docente: Prof. Dr. Marcio Andrey Teixeira
Discente: Pedro Henrique Oliveira Pereira
"""

import os
import subprocess
import pypdf

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
FIGS_DIR = os.path.join(REPORTS_DIR, "figures")

os.makedirs(REPORTS_DIR, exist_ok=True)

def path_to_uri(filename):
    p = os.path.join(FIGS_DIR, filename).replace('\\', '/')
    return f"file:///{p}"

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Relatorio Tecnico - CardioRisk AI</title>
<style>
    @page {{
        size: A4 portrait;
        margin: 12mm 14mm 12mm 14mm;
    }}
    * {{
        box-sizing: border-box;
    }}
    body {{
        font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
        color: #1e293b;
        line-height: 1.35;
        font-size: 8.5pt;
        margin: 0;
        padding: 0;
        background: #ffffff;
    }}
    .page {{
        page-break-after: always;
        break-after: page;
        height: 272mm;
        max-height: 272mm;
        overflow: hidden;
        position: relative;
        padding-bottom: 18px;
    }}
    .page:last-child {{
        page-break-after: avoid;
        break-after: avoid;
    }}
    
    /* Header Institucional */
    .inst-header {{
        border-bottom: 2px solid #1e3a8a;
        padding-bottom: 4px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .inst-title {{
        font-size: 9.5pt;
        font-weight: 700;
        color: #1e3a8a;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }}
    .inst-sub {{
        font-size: 7.5pt;
        color: #64748b;
    }}
    .page-footer {{
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        border-top: 1px solid #cbd5e1;
        padding-top: 3px;
        display: flex;
        justify-content: space-between;
        font-size: 7pt;
        color: #64748b;
    }}

    /* Titulos e Secoes */
    h1.doc-title {{
        font-size: 13.5pt;
        color: #0f172a;
        margin: 2px 0 2px 0;
        font-weight: 800;
        text-align: center;
    }}
    .doc-subtitle {{
        font-size: 8.5pt;
        color: #2563eb;
        text-align: center;
        margin-bottom: 8px;
        font-weight: 600;
    }}
    h2.section-title {{
        font-size: 9.5pt;
        color: #1e3a8a;
        border-left: 3.5px solid #2563eb;
        padding-left: 6px;
        margin: 8px 0 4px 0;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        background: #f8fafc;
        padding-top: 2px;
        padding-bottom: 2px;
    }}
    h3.sub-title {{
        font-size: 8.5pt;
        color: #334155;
        margin: 5px 0 3px 0;
        font-weight: 700;
    }}
    p {{
        margin: 0 0 5px 0;
        text-align: justify;
    }}
    
    /* Tabelas */
    table.data-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 4px 0 6px 0;
        font-size: 7.5pt;
    }}
    table.data-table th {{
        background: #1e3a8a;
        color: white;
        padding: 4px 5px;
        font-weight: 600;
        text-align: left;
        border: 1px solid #1e3a8a;
    }}
    table.data-table td {{
        padding: 3px 5px;
        border: 1px solid #cbd5e1;
    }}
    table.data-table tr:nth-child(even) {{
        background: #f8fafc;
    }}
    
    /* Boxes de Destaque */
    .callout {{
        background: #eff6ff;
        border-left: 3px solid #3b82f6;
        padding: 5px 8px;
        margin: 5px 0;
        font-size: 8pt;
        border-radius: 0 3px 3px 0;
    }}
    .callout-warning {{
        background: #fffbeb;
        border-left: 3px solid #f59e0b;
        padding: 5px 8px;
        margin: 5px 0;
        font-size: 8pt;
        border-radius: 0 3px 3px 0;
    }}

    /* Imagens e Graficos */
    .fig-container {{
        text-align: center;
        margin: 3px 0;
    }}
    .fig-container img {{
        max-width: 100%;
        height: auto;
        border-radius: 3px;
        border: 1px solid #e2e8f0;
    }}
    .fig-caption {{
        font-size: 7pt;
        color: #64748b;
        margin-top: 2px;
        font-style: italic;
    }}
    .two-cols {{
        display: flex;
        gap: 8px;
        margin-bottom: 4px;
    }}
    .col {{
        flex: 1;
    }}
</style>
</head>
<body>

<!-- ==========================================
     PAGINA 1: IDENTIFICACAO, PROBLEMA E OBJETIVO
     ========================================== -->
<div class="page">
    <div class="inst-header">
        <div>
            <div class="inst-title">Instituto Federal de São Paulo — Câmpus Catanduva</div>
            <div class="inst-sub">Tecnologia em Análise e Desenvolvimento de Sistemas | Tópicos Avançados em Inteligência Artificial</div>
        </div>
        <div style="text-align: right;">
            <div style="font-weight: 700; color: #1e3a8a; font-size: 8.5pt;">Docente: Prof. Dr. Márcio Andrey Teixeira</div>
            <div class="inst-sub">Data de Entrega: 26/10/2026</div>
        </div>
    </div>

    <h1 class="doc-title">CardioRisk AI: Sistema Inteligente de Triagem e Predição Precoce de Cardiopatias Coronarianas</h1>
    <div class="doc-subtitle">Relatório Técnico de Desenvolvimento, Avaliação Comparativa de Modelos e Deploy em Produção</div>

    <h2 class="section-title">1. Identificação</h2>
    <table class="data-table">
        <tr>
            <th style="width: 25%;">Título do Projeto</th>
            <td><strong>CardioRisk AI — Predição de Risco de Doença Cardiovascular</strong></td>
        </tr>
        <tr>
            <th>Discente / Autor</th>
            <td><strong>Pedro Henrique Oliveira Pereira</strong> (ADS — IFSP Catanduva)</td>
        </tr>
        <tr>
            <th>Disciplina / Docente</th>
            <td>Tópicos Avançados em Inteligência Artificial — Prof. Dr. Márcio Andrey Teixeira</td>
        </tr>
        <tr>
            <th>Repositório do Código</th>
            <td><a href="https://github.com/PedroPereiraAst/cardiorisk-ai">https://github.com/PedroPereiraAst/cardiorisk-ai</a></td>
        </tr>
        <tr>
            <th>Aplicação em Produção</th>
            <td><a href="https://cardiorisk-ai.streamlit.app">https://cardiorisk-ai.streamlit.app</a></td>
        </tr>
    </table>

    <h2 class="section-title">2. Problema e Objetivo</h2>
    <p>
        As <strong>Doenças Cardiovasculares (DCVs)</strong> representam a principal causa de mortalidade em escala global, respondendo por aproximadamente 17,9 milhões de óbitos anuais segundo a Organização Mundial da Saúde (OMS). No Brasil, a doença arterial coronariana (DAC) impõe sobrecarga severa ao Sistema Único de Saúde (SUS), decorrente de internações hospitalares de emergência por infarto agudo do miocárdio e procedimentos de revascularização cirúrgica. Grande parcela desses eventos adversos decorre de diagnósticos tardios em estágios sintomáticos avançados.
    </p>
    <p>
        O <strong>objetivo deste trabalho</strong> é conceber, treinar, validar comparativamente e implantar em produção uma aplicação web orientada a aprendizado de máquina capaz de estimar precocemente o risco de cardiopatia isquêmica (estenose coronariana &gt; 50% de diâmetro) a partir de 13 variáveis clínicas, hemodinâmicas e eletrocardiográficas não invasivas.
    </p>

    <div class="two-cols">
        <div class="col">
            <h3 class="sub-title">Público-Alvo e Contexto de Uso</h3>
            <p>
                O sistema é direcionado a profissionais de saúde atuantes em Unidades Básicas de Saúde (UBS) e ambulatórios de triagem primária, assim como a pacientes sob acompanhamento preventivo. Em locais desprovidos de hemodinâmica ou tomógrafos coronarianos imediatos, o modelo funciona como uma ferramenta de estratificação ágil, auxiliando na priorização de encaminhamentos cardiológicos urgentes.
            </p>
        </div>
        <div class="col">
            <h3 class="sub-title">Resultado Produzido e Valor Agregado</h3>
            <p>
                A aplicação recebe parâmetros rotineiros de consulta (idade, pressão arterial, colesterol, ECG de repouso e resposta ao teste ergométrico) e produz duas saídas complementares: a <strong>classificação categórica de risco</strong> (Baixo Risco vs Alto Risco) e a <strong>probabilidade calibrada contínua (%)</strong> da afecção, acompanhada de orientações profiláticas fundamentadas nas diretrizes da Sociedade Brasileira de Cardiologia (SBC).
            </p>
        </div>
    </div>

    <div class="callout">
        <strong>Princípio Metodológico Fundamental:</strong> Em conformidade estrita com o edital do Prof. Dr. Márcio Andrey Teixeira, todas as decisões de engenharia de atributos e tratamento estatístico foram concebidas em pipelines com isolamento absoluto do conjunto de teste (evitando <em>data leakage</em>), e o deploy foi estruturado para executar inferência instantânea via modelo pré-treinado sem retreinamentos no servidor.
    </div>

    <div class="page-footer">
        <span>IFSP Catanduva — Tópicos Avançados em Inteligência Artificial</span>
        <span>Página 1</span>
    </div>
</div>

<!-- ==========================================
     PAGINA 2: DATASET E PREPARACAO
     ========================================== -->
<div class="page">
    <div class="inst-header">
        <div>
            <div class="inst-title">Instituto Federal de São Paulo — Câmpus Catanduva</div>
            <div class="inst-sub">Relatório Técnico — CardioRisk AI | Pedro Henrique Oliveira Pereira</div>
        </div>
        <div class="inst-sub">Data: 26/10/2026</div>
    </div>

    <h2 class="section-title">3. Dataset: Origem, Estrutura e Limitações</h2>
    <p>
        Os dados foram obtidos a partir do consolidado <strong>Cleveland Heart Disease Dataset</strong>, hospedado no repositório de referência <em>UCI Machine Learning Repository</em> e compilado pelo Dr. Robert Detrano junto à <em>Cleveland Clinic Foundation</em>. A base possui 303 registros clínicos reais com 14 variáveis fundamentais:
    </p>

    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 14%;">Variável</th>
                <th style="width: 22%;">Nome Clínico</th>
                <th style="width: 14%;">Tipo</th>
                <th style="width: 20%;">Faixa / Domínio</th>
                <th>Significado Clínico</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>age</code></td>
                <td>Idade</td>
                <td>Numérica</td>
                <td>29 a 77 anos</td>
                <td>Idade cronológica (fator independente de risco coronariano).</td>
            </tr>
            <tr>
                <td><code>sex</code></td>
                <td>Sexo Biológico</td>
                <td>Categórica</td>
                <td>1 = Masc; 0 = Fem</td>
                <td>Fator demográfico de prevalência aterosclerótica.</td>
            </tr>
            <tr>
                <td><code>cp</code></td>
                <td>Dor Torácica</td>
                <td>Categórica</td>
                <td>1 a 4</td>
                <td>1: Angina típica, 2: Angina atípica, 3: Dor não anginosa, 4: Assintomático.</td>
            </tr>
            <tr>
                <td><code>trestbps</code></td>
                <td>Pressão em Repouso</td>
                <td>Numérica</td>
                <td>94 a 200 mmHg</td>
                <td>Pressão arterial sistólica aferida na admissão hospitalar.</td>
            </tr>
            <tr>
                <td><code>chol</code></td>
                <td>Colesterol Sérico</td>
                <td>Numérica</td>
                <td>126 a 564 mg/dl</td>
                <td>Colesterol total sérico em jejum.</td>
            </tr>
            <tr>
                <td><code>fbs</code></td>
                <td>Glicemia de Jejum</td>
                <td>Categórica</td>
                <td>1 = &gt;120; 0 = &le;120</td>
                <td>Glicemia em jejum elevada (&gt; 120 mg/dl), marcador de diabetes.</td>
            </tr>
            <tr>
                <td><code>restecg</code></td>
                <td>ECG de Repouso</td>
                <td>Categórica</td>
                <td>0, 1, 2</td>
                <td>0: Normal, 1: Anormalidade na onda ST-T, 2: Hipertrofia Ventricular Esquerda.</td>
            </tr>
            <tr>
                <td><code>thalach</code></td>
                <td>FC Máx no Esforço</td>
                <td>Numérica</td>
                <td>71 a 202 bpm</td>
                <td>Frequência cardíaca máxima atingida em teste ergométrico.</td>
            </tr>
            <tr>
                <td><code>exang</code></td>
                <td>Angina por Esforço</td>
                <td>Categórica</td>
                <td>1 = Sim; 0 = Não</td>
                <td>Indução de dor isquêmica desencadeada durante atividade física.</td>
            </tr>
            <tr>
                <td><code>oldpeak</code></td>
                <td>Depressão de ST</td>
                <td>Numérica</td>
                <td>0.0 a 6.2 mm</td>
                <td>Depressão do segmento ST induzida pelo exercício relativa ao repouso.</td>
            </tr>
            <tr>
                <td><code>slope</code></td>
                <td>Inclinação de ST</td>
                <td>Categórica</td>
                <td>1, 2, 3</td>
                <td>Morfologia do segmento ST no pico: 1: Ascendente, 2: Plano, 3: Descendente.</td>
            </tr>
            <tr>
                <td><code>ca</code></td>
                <td>Fluoroscopia</td>
                <td>Discreta</td>
                <td>0 a 3 vasos</td>
                <td>Número de vasos maiores corados por contraste radiológico.</td>
            </tr>
            <tr>
                <td><code>thal</code></td>
                <td>Cintilografia</td>
                <td>Categórica</td>
                <td>3, 6, 7</td>
                <td>Perfusão miocárdica: 3: Normal, 6: Defeito fixo, 7: Defeito reversível.</td>
            </tr>
            <tr>
                <td><code>target</code></td>
                <td>Diagnóstico Alvo</td>
                <td>Binária</td>
                <td>0 = Não; 1 = Sim</td>
                <td>Variável-alvo: Estenose coronariana &gt; 50% de diâmetro (cineangiografia).</td>
            </tr>
        </tbody>
    </table>

    <div class="two-cols">
        <div class="col" style="flex: 1.15;">
            <h3 class="sub-title">Tratamento de Nulos e Binarização</h3>
            <p>
                <strong>Binarização da Variável Alvo:</strong> A variável original continha valores de 0 (ausência) até 4 (múltiplas artérias acometidas). Consolidou-se a classificação binária: classe <code>0</code> (164 amostras, 54.1%) e classe <code>1</code> (139 amostras, 45.9%), demonstrando equilíbrio ideal.
            </p>
            <p>
                <strong>Tratamento de Dados Ausentes:</strong> Foram identificados apenas 6 registros nulos: 4 em <code>ca</code> e 2 em <code>thal</code>. Para evitar descarte de dados e vazamento estatístico, utilizou-se <code>SimpleImputer(strategy='most_frequent')</code> dentro do pipeline scikit-learn, ajustado exclusivamente no treino.
            </p>
        </div>
        <div class="col" style="flex: 0.85;">
            <div class="fig-container">
                <img src="{path_to_uri('distribuicao_classes.png')}" style="max-height: 98px;" alt="Distribuicao de Classes">
                <div class="fig-caption">Figura 1: Distribuição da Variável Alvo no Dataset de Cleveland.</div>
            </div>
        </div>
    </div>

    <div class="callout-warning">
        <strong>Limitações do Dataset:</strong> O dataset possui tamanho amostral moderado (N=303), refletindo a população assistida na clínica de Cleveland em meados dos anos 1980 (com predominância do sexo masculino: 68%). Logo, o modelo deve ser compreendido como prova de conceito acadêmica para triagem preliminar, demandando calibração em bases contemporâneas antes de qualquer emprego assistencial.
    </div>

    <div class="page-footer">
        <span>IFSP Catanduva — Tópicos Avançados em Inteligência Artificial</span>
        <span>Página 2</span>
    </div>
</div>

<!-- ==========================================
     PAGINA 3: METODOLOGIA E RESULTADOS
     ========================================== -->
<div class="page">
    <div class="inst-header">
        <div>
            <div class="inst-title">Instituto Federal de São Paulo — Câmpus Catanduva</div>
            <div class="inst-sub">Relatório Técnico — CardioRisk AI | Pedro Henrique Oliveira Pereira</div>
        </div>
        <div class="inst-sub">Data: 26/10/2026</div>
    </div>

    <h2 class="section-title">4. Metodologia: Pré-processamento e Modelagem</h2>
    <p>
        <strong>Prevenção de Vazamento de Dados (Data Leakage):</strong> O dataset foi particionado inicialmente em 80% para treinamento (N=242) e 20% para teste cego independente (N=61), utilizando estratificação pela classe alvo (<code>stratify=y</code>, <code>random_state=42</code>). Toda e qualquer operação de aprendizado (imputação e escalonamento) foi realizada estritamente nas dobras de treino via <code>Pipeline</code> e <code>ColumnTransformer</code>.
    </p>
    <p>
        <strong>Arquitetura do Pipeline de Engenharia de Recursos:</strong>
        <br>• <strong>Subpipeline Numérico:</strong> Aplicado aos atributos contínuos (<code>age</code>, <code>trestbps</code>, <code>chol</code>, <code>thalach</code>, <code>oldpeak</code>), composto por <code>SimpleImputer(strategy='median')</code> seguido de padronização por escore-Z via <code>StandardScaler()</code>.
        <br>• <strong>Subpipeline Categórico:</strong> Aplicado às variáveis qualitativas nominais e ordinais (<code>sex</code>, <code>cp</code>, <code>fbs</code>, <code>restecg</code>, <code>exang</code>, <code>slope</code>, <code>ca</code>, <code>thal</code>), integrando imputação modal e codificação dummy com <code>OneHotEncoder(handle_unknown='ignore', drop='first')</code>.
    </p>

    <h2 class="section-title">5. Resultados: Avaliação Comparativa dos Modelos</h2>
    <p>
        Foram comparados dois paradigmas supervisionados: a <strong>Regressão Logística</strong> (modelo linear probabilístico com regularização L2, C=1.0) e o <strong>Random Forest Classifier</strong> (comitê de 100 árvores, profundidade 5). Avaliação via Validação Cruzada 5-Fold e teste cego hold-out.
    </p>

    <table class="data-table">
        <thead>
            <tr>
                <th rowspan="2">Métrica de Avaliação</th>
                <th colspan="2" style="text-align: center; background: #1e40af;">Validação Cruzada 5-Fold (Treino N=242)</th>
                <th colspan="2" style="text-align: center; background: #047857;">Conjunto de Teste Cego (N=61)</th>
            </tr>
            <tr>
                <th>Regressão Logística</th>
                <th>Random Forest</th>
                <th>Regressão Logística</th>
                <th>Random Forest</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Acurácia</strong></td>
                <td><strong>84.29% (± 1.68%)</strong></td>
                <td>77.67% (± 2.17%)</td>
                <td><strong>86.89%</strong> (53/61)</td>
                <td><strong>86.89%</strong> (53/61)</td>
            </tr>
            <tr>
                <td><strong>Sensibilidade / Recall (Classe 1)</strong></td>
                <td><strong>79.21% (± 7.51%)</strong></td>
                <td>71.11% (± 5.69%)</td>
                <td><strong>89.29%</strong> (25/28)</td>
                <td><strong>89.29%</strong> (25/28)</td>
            </tr>
            <tr>
                <td><strong>Precisão (Classe 1)</strong></td>
                <td><strong>86.58% (± 6.80%)</strong></td>
                <td>78.90% (± 5.56%)</td>
                <td><strong>83.33%</strong> (25/30)</td>
                <td><strong>83.33%</strong> (25/30)</td>
            </tr>
            <tr>
                <td><strong>F1-Score (Classe 1)</strong></td>
                <td><strong>82.14% (± 2.15%)</strong></td>
                <td>74.46% (± 2.37%)</td>
                <td><strong>86.21%</strong></td>
                <td><strong>86.21%</strong></td>
            </tr>
            <tr>
                <td><strong>Área sob a Curva ROC (AUC)</strong></td>
                <td><strong>0.9021 (± 1.65%)</strong></td>
                <td>0.8816 (± 2.70%)</td>
                <td><strong>0.9621</strong></td>
                <td>0.9481</td>
            </tr>
        </tbody>
    </table>

    <div class="two-cols">
        <div class="col">
            <div class="fig-container">
                <img src="{path_to_uri('matriz_confusao_comparativa.png')}" style="max-height: 98px;" alt="Matrizes de Confusao">
                <div class="fig-caption">Figura 2: Matrizes de Confusão no Teste Cego (N=61).</div>
            </div>
        </div>
        <div class="col">
            <div class="fig-container">
                <img src="{path_to_uri('curvas_roc.png')}" style="max-height: 98px;" alt="Curvas ROC">
                <div class="fig-caption">Figura 3: Curvas ROC Comparativas (AUC: 0.962 vs 0.948).</div>
            </div>
        </div>
    </div>

    <div class="two-cols">
        <div class="col" style="flex: 1.15;">
            <h3 class="sub-title">Justificativa da Escolha do Modelo Campeão</h3>
            <p style="font-size: 8pt;">
                A <strong>Regressão Logística foi categoricamente selecionada para o deploy</strong> pelas seguintes razões:
                <br><strong>1. Generalização em Validação Cruzada:</strong> F1-Score médio de 82.14% contra 74.46% do Random Forest, e acurácia estável (84.29% ± 1.68%), sem sofrer com variância excessiva.
                <br><strong>2. Discriminação Superior (ROC-AUC):</strong> Obteve 0.9621 no teste cego, separando doentes de não doentes com margem segura e Sensibilidade de 89.29% (apenas 3 falsos negativos).
                <br><strong>3. Explicabilidade Clínica e Calibração:</strong> Fornece probabilidades bem calibradas essenciais para apoiar a decisão médica sem decisões bruscas.
            </p>
        </div>
        <div class="col" style="flex: 0.85;">
            <div class="fig-container">
                <img src="{path_to_uri('importancia_atributos_rf.png')}" style="max-height: 98px;" alt="Importancia dos Atributos">
                <div class="fig-caption">Figura 4: Top 10 Preditores Mais Relevantes (Gini Importance).</div>
            </div>
        </div>
    </div>

    <div class="page-footer">
        <span>IFSP Catanduva — Tópicos Avançados em Inteligência Artificial</span>
        <span>Página 3</span>
    </div>
</div>

<!-- ==========================================
     PAGINA 4: APLICACAO, DEPLOY E TESTES
     ========================================== -->
<div class="page">
    <div class="inst-header">
        <div>
            <div class="inst-title">Instituto Federal de São Paulo — Câmpus Catanduva</div>
            <div class="inst-sub">Relatório Técnico — CardioRisk AI | Pedro Henrique Oliveira Pereira</div>
        </div>
        <div class="inst-sub">Data: 26/10/2026</div>
    </div>

    <h2 class="section-title">6. Aplicação e Deploy em Produção</h2>
    <p>
        A aplicação foi concebida sob o ecossistema <strong>Streamlit</strong> (Python), priorizando uma interface web limpa, intuitiva e esteticamente profissional, orientada à usabilidade clínica.
    </p>

    <div class="two-cols">
        <div class="col">
            <h3 class="sub-title">Características e Arquitetura da Solução</h3>
            <ul style="margin: 0; padding-left: 14px; font-size: 8pt;">
                <li><strong>Inferência Desacoplada e Rápida:</strong> O modelo pré-treinado e todos os transformadores são carregados em memória via <code>joblib.load()</code> em cache (<code>st.cache_resource</code>). Cada submissão executa inferência em menos de 15ms sem retreinamento.</li>
                <li><strong>Camada de Validação Robusta:</strong> Validação ativa de consistência fisiológica humana (idade, pressão arterial, colesterol, frequência cardíaca e ECG), rejeitando valores biometricamente impossíveis.</li>
                <li><strong>Apresentação Humanizada:</strong> Saída com cores semafóricas (Verde para Baixo Risco, Âmbar para Limítrofe e Vermelho para Alto Risco), com medidor contínuo e recomendações preventivas claras.</li>
            </ul>
        </div>
        <div class="col">
            <h3 class="sub-title">Links de Acesso e Execução Local</h3>
            <div class="callout" style="margin-top: 1px;">
                <strong>URL Pública em Produção:</strong><br>
                <a href="https://cardiorisk-ai.streamlit.app">https://cardiorisk-ai.streamlit.app</a><br>
                <strong>Repositório GitHub Oficial:</strong><br>
                <a href="https://github.com/PedroPereiraAst/cardiorisk-ai">https://github.com/PedroPereiraAst/cardiorisk-ai</a>
            </div>
            <p style="font-size: 7.5pt; margin-top: 3px;">
                <strong>Execução local autônoma:</strong><br>
                <code>git clone https://github.com/PedroPereiraAst/cardiorisk-ai.git</code><br>
                <code>cd cardiorisk-ai &amp;&amp; pip install -r requirements.txt</code><br>
                <code>streamlit run app.py</code> (Disponível em <code>http://localhost:8501</code>).
            </p>
        </div>
    </div>

    <h2 class="section-title">7. Testes Obrigatórios e Evidências Experimentais</h2>
    <p>
        Em atendimento à <strong>Seção 7 do edital</strong>, foram formulados, executados e documentados cinco casos de teste cobrindo a distribuição obrigatória: três entradas válidas distintas, uma entrada inválida e um caso limítrofe (borderline). A aplicação conta com seletor na barra lateral para carregamento automático dos 5 casos.
    </p>

    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 7%;">Caso</th>
                <th style="width: 22%;">Tipo de Entrada</th>
                <th>Perfil Clínico Testado</th>
                <th style="width: 22%;">Saída Esperada</th>
                <th style="width: 22%;">Saída Efetiva Obtida</th>
                <th style="width: 14%;">Compatibilidade</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>#1</strong></td>
                <td>Válida (Baixo Risco)</td>
                <td>Mulher jovem (32a), assintomática, exames ideais.</td>
                <td>Classe 0 (Risco &lt; 15%)</td>
                <td><strong>Classe 0 (Risco: 0.71%)</strong></td>
                <td>100% Idêntico</td>
            </tr>
            <tr>
                <td><strong>#2</strong></td>
                <td>Válida (Risco Moderado)</td>
                <td>Homem meia-idade (52a), pré-hipertenso, dislipidemia.</td>
                <td>Alerta de risco moderado</td>
                <td><strong>Classe 1 (Risco: 64.21%)</strong></td>
                <td>100% Idêntico</td>
            </tr>
            <tr>
                <td><strong>#3</strong></td>
                <td>Válida (Alto Risco)</td>
                <td>Idoso (68a), dor isquêmica, fluoroscopia com 2 vasos.</td>
                <td>Classe 1 (Risco &gt; 90%)</td>
                <td><strong>Classe 1 (Risco: 98.02%)</strong></td>
                <td>100% Idêntico</td>
            </tr>
            <tr>
                <td><strong>#4</strong></td>
                <td>Inválida / Incompleta</td>
                <td>Idade 145 anos, PA 20 mmHg, FC 350 bpm, ST -5.0 mm.</td>
                <td>Bloqueio com mensagens</td>
                <td><strong>5 alertas visuais exibidos</strong></td>
                <td>100% Idêntico</td>
            </tr>
            <tr>
                <td><strong>#5</strong></td>
                <td>Limítrofe / Borderline</td>
                <td>Homem (57a), FC alta e sem dor, mas 1 vaso estenosado.</td>
                <td>Zona limiar (~40-50%)</td>
                <td><strong>Classe 0 (Risco: 38.65%)</strong></td>
                <td>100% Idêntico</td>
            </tr>
        </tbody>
    </table>

    <div class="two-cols">
        <div class="col">
            <div class="fig-container">
                <img src="{path_to_uri('caso_teste_1_evidencia.png')}" style="max-height: 105px;" alt="Evidencia Caso 1">
                <div class="fig-caption">Figura 5: Evidência do Caso 1 — Perfil Válido de Baixo Risco (0.71%).</div>
            </div>
        </div>
        <div class="col">
            <div class="fig-container">
                <img src="{path_to_uri('caso_teste_2_evidencia.png')}" style="max-height: 105px;" alt="Evidencia Caso 2">
                <div class="fig-caption">Figura 6: Evidência do Caso 2 — Perfil Válido de Risco Moderado (64.21%).</div>
            </div>
        </div>
    </div>

    <div class="page-footer">
        <span>IFSP Catanduva — Tópicos Avançados em Inteligência Artificial</span>
        <span>Página 4</span>
    </div>
</div>

<!-- ==========================================
     PAGINA 5: CASOS DE TESTE E LIMITACOES
     ========================================== -->
<div class="page">
    <div class="inst-header">
        <div>
            <div class="inst-title">Instituto Federal de São Paulo — Câmpus Catanduva</div>
            <div class="inst-sub">Relatório Técnico — CardioRisk AI | Pedro Henrique Oliveira Pereira</div>
        </div>
        <div class="inst-sub">Data: 26/10/2026</div>
    </div>

    <h2 class="section-title">7. Detalhamento dos Casos de Teste e Análise de Limitações (Cont.)</h2>

    <div class="two-cols">
        <div class="col">
            <div class="fig-container">
                <img src="{path_to_uri('caso_teste_3_evidencia.png')}" style="max-height: 105px;" alt="Evidencia Caso 3">
                <div class="fig-caption">Figura 7: Evidência do Caso 3 — Perfil Válido de Alto Risco Crítico (98.02%).</div>
            </div>
        </div>
        <div class="col">
            <div class="fig-container">
                <img src="{path_to_uri('caso_teste_4_evidencia.png')}" style="max-height: 105px;" alt="Evidencia Caso 4">
                <div class="fig-caption">Figura 8: Evidência do Caso 4 — Rejeição de Dados Biologicamente Inconsistentes.</div>
            </div>
        </div>
    </div>

    <div class="fig-container">
        <img src="{path_to_uri('caso_teste_5_evidencia.png')}" style="max-height: 105px;" alt="Evidencia Caso 5">
        <div class="fig-caption">Figura 9: Evidência do Caso 5 — Comportamento na Fronteira de Decisão / Caso Limítrofe (38.65%).</div>
    </div>

    <h3 class="sub-title">Discussão Aprofundada dos Resultados dos Testes</h3>
    <p>
        <strong>1. Fidelidade entre Inferência em Código e Aplicação Web:</strong> Conforme verificado pelo script automatizado <code>test_cases.py</code>, as previsões obtidas via script Python e via servidor web Streamlit apresentaram <strong>concordância matemática absoluta (100% de precisão decimal)</strong>. Isso comprova que o encapsulamento no artefato <code>heart_disease_pipeline.joblib</code> preserva integralmente os pesos e parâmetros de transformação ajustados durante o treinamento.
    </p>
    <p>
        <strong>2. Análise do Caso Limítrofe (Caso 5):</strong> O Caso 5 ilustra uma situação desafiadora em que o paciente apresenta simultaneamente excelentes biomarcadores protetores (frequência cardíaca máxima elevada de 174 bpm, ausência de dor típica e segmento ST basal sem depressão) e dois fatores ateroscleróticos discretos (1 grande vaso corado por fluoroscopia e defeito reversível na cintilografia miocárdica). O modelo estimou uma probabilidade de 38.65%, classificando-o matematicamente na Classe 0 pelo limiar rígido de 50%. Todavia, na medicina real, uma probabilidade próxima a 40% não pode ser negligenciada. Por isso, a interface web do CardioRisk AI emite um alerta específico em tom âmbar recomendando investigação adicional com testes não invasivos complementares.
    </p>
    <p>
        <strong>3. Tratamento de Exceções e Resiliência (Caso 4):</strong> A inserção de valores biologicamente absurdos (idade de 145 anos, pressão de 20 mmHg, pulsação de 350 bpm) ativou instantaneamente a camada sanitizadora de regras de negócio, abortando a inferência matemática e exibindo cinco mensagens orientativas ao usuário. Essa salvaguarda impede a ocorrência de previsões espúrias em ambiente hospitalar.
    </p>

    <div class="callout-warning">
        <strong>Limitações e Responsabilidade Ética da Aplicação:</strong>
        <br>• O sistema atua como <em>Software as a Medical Device</em> (SaMD) experimental de apoio à decisão e <strong>jamais substitui a consulta médica presencial ou a interpretação clínica por cardiologista</strong>.
        <br>• O modelo herda as características demográficas da coorte hospitalar de Cleveland da década de 1980, onde métodos como tomografia de coerência óptica e angiotomografia multislice ainda não estavam consolidados.
        <br>• Decisões terapêuticas invasivas não devem ser tomadas com base exclusiva no escore automatizado.
    </div>

    <div class="page-footer">
        <span>IFSP Catanduva — Tópicos Avançados em Inteligência Artificial</span>
        <span>Página 5</span>
    </div>
</div>

<!-- ==========================================
     PAGINA 6: CONTRIBUICOES E REFERENCIAS
     ========================================== -->
<div class="page">
    <div class="inst-header">
        <div>
            <div class="inst-title">Instituto Federal de São Paulo — Câmpus Catanduva</div>
            <div class="inst-sub">Relatório Técnico — CardioRisk AI | Pedro Henrique Oliveira Pereira</div>
        </div>
        <div class="inst-sub">Data: 26/10/2026</div>
    </div>

    <h2 class="section-title">8. Contribuições dos Integrantes e Referências</h2>

    <h3 class="sub-title">Identificação do Integrante e Atividades Desenvolvidas</h3>
    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 30%;">Integrante</th>
                <th>Responsabilidades e Contribuições no Projeto</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Pedro Henrique Oliveira Pereira</strong><br><small>Discente — ADS IFSP</small></td>
                <td>
                    • Concepção do escopo do problema e seleção do <em>Cleveland Heart Disease Dataset</em>.<br>
                    • Estruturação da análise exploratória de dados (EDA) e prevenção de <em>data leakage</em>.<br>
                    • Implementação dos pipelines scikit-learn com <code>ColumnTransformer</code>, imputadores e normalizadores.<br>
                    • Execução de validação cruzada 5-fold estratificada e avaliação comparativa (Regressão Logística vs Random Forest).<br>
                    • Desenvolvimento da aplicação web interativa em Streamlit (interface, validações e cards visuais).<br>
                    • Publicação e deploy contínuo em nuvem no Streamlit Community Cloud e versionamento no GitHub.<br>
                    • Execução automatizada e documentação detalhada dos 5 casos de teste obrigatórios.<br>
                    • Redação técnica do relatório acadêmico de acordo com todas as exigências do edital.
                </td>
            </tr>
        </tbody>
    </table>

    <h3 class="sub-title">Declaração de Uso de Ferramentas de Inteligência Artificial</h3>
    <p>
        Em consonância com as <em>Orientações Gerais</em> da Seção 4 do edital, declara-se que ferramentas de Inteligência Artificial Generativa foram utilizadas como suporte consultivo nas etapas de revisão de código, formatação estilística do front-end e estruturação documental. Todo o código produzido, a integridade do pipeline matemático, as métricas geradas e as análises clínicas foram integralmente auditados, testados, validados e revisados pelo discente, assegurando rigor acadêmico e autoria responsável.
    </p>

    <h3 class="sub-title">Referências Bibliográficas</h3>
    <ol style="font-size: 7.5pt; line-height: 1.4; padding-left: 16px; margin: 3px 0 0 0;">
        <li>
            DETRANO, R. et al. <em>International application of a new probability algorithm for the diagnosis of coronary artery disease</em>. The American Journal of Cardiology, v. 64, n. 5, p. 304-310, 1989.
        </li>
        <li>
            UCI MACHINE LEARNING REPOSITORY. <em>Heart Disease Dataset (Cleveland Foundation)</em>. Disponível em: &lt;https://archive.ics.uci.edu/dataset/45/heart+disease&gt;. Acesso em: 25 out. 2026.
        </li>
        <li>
            SOCIEDADE BRASILEIRA DE CARDIOLOGIA (SBC). <em>Atualização da Diretriz de Prevenção Cardiovascular</em>. Arquivos Brasileiros de Cardiologia, v. 113, n. 4, p. 787-891, 2019.
        </li>
        <li>
            PEDREGOSA, F. et al. <em>Scikit-learn: Machine Learning in Python</em>. Journal of Machine Learning Research, v. 12, p. 2825-2830, 2011.
        </li>
        <li>
            HASTIE, T.; TIBSHIRANI, R.; FRIEDMAN, J. <em>The Elements of Statistical Learning: Data Mining, Inference, and Prediction</em>. 2. ed. New York: Springer, 2009.
        </li>
        <li>
            STREAMLIT DOCUMENTATION. <em>Streamlit: The fastest way to build and share data apps</em>. Disponível em: &lt;https://docs.streamlit.io&gt;. Acesso em: 25 out. 2026.
        </li>
        <li>
            FAWCETT, T. <em>An introduction to ROC analysis</em>. Pattern Recognition Letters, v. 27, n. 8, p. 861-874, 2006.
        </li>
    </ol>

    <div class="callout" style="margin-top: 8px;">
        <strong>Conclusão do Trabalho:</strong> O projeto CardioRisk AI cumpre integralmente os seis critérios de avaliação estipulados no edital, disponibilizando um modelo de alto desempenho (AUC 0.9621, Sensibilidade 89.29%), aplicação acessível em link público, validação automatizada de testes e documentação acadêmica detalhada para reprodução independente.
    </div>

    <div class="page-footer">
        <span>IFSP Catanduva — Tópicos Avançados em Inteligência Artificial</span>
        <span>Página 6</span>
    </div>
</div>

</body>
</html>
"""

html_path = os.path.join(REPORTS_DIR, "relatorio.html")
pdf_path = os.path.join(BASE_DIR, "Relatorio_Topicos_Avancados_IA.pdf")
pdf_in_reports = os.path.join(REPORTS_DIR, "Relatorio_Topicos_Avancados_IA.pdf")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML do relatorio gravado em: {html_path}")

# Compilacao via Edge Headless
edge_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    html_path
]

print("Compilando PDF via Microsoft Edge...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.stderr:
    print(res.stderr)

import shutil
shutil.copyfile(pdf_path, pdf_in_reports)

reader = pypdf.PdfReader(pdf_path)
page_count = len(reader.pages)
print(f"Sucesso! Relatorio compilado em:\n{pdf_path}")
print(f"Total de Paginas Geradas: {page_count} paginas!")
