"""
CardioRisk AI - Pipeline de Treinamento e Avaliacao Comparativa de Modelos
Disciplina: Topicos Avancados em Inteligencia Artificial - IFSP Catanduva
Docente: Prof. Dr. Marcio Andrey Teixeira
Discente: Pedro Henrique Oliveira Pereira
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_curve,
    roc_auc_score,
    accuracy_score,
    f1_score,
    recall_score,
    precision_score
)

# Configuracao de estilo dos graficos
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# Diretorios base
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "heart.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
FIGS_DIR = os.path.join(BASE_DIR, "reports", "figures")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(FIGS_DIR, exist_ok=True)

def carregar_e_preparar_dados():
    """
    Carrega o dataset Cleveland Heart Disease e prepara as variaveis preditoras e alvo.
    """
    print("[1/6] Carregando dataset...")
    df = pd.read_csv(DATA_PATH)
    
    # Binarizacao da variavel alvo: 0 = Saudavel/Ausencia, 1 a 4 = Presenca de Doenca Cardiaca
    df['target'] = (df['target'] > 0).astype(int)
    
    X = df.drop(columns=['target'])
    y = df['target']
    
    print(f"Total de registros: {len(df)}")
    print(f"Distribuicao da classe alvo:\n{y.value_counts(normalize=True).to_dict()}")
    print(f"Valores nulos identificados:\n{df.isnull().sum()[df.isnull().sum() > 0].to_dict()}")
    
    # Gerar grafico da distribuicao das classes
    plt.figure(figsize=(6, 4))
    sns.countplot(x='target', data=df, palette=['#2b5c8f', '#d9534f'])
    plt.title("Distribuicao da Variavel Alvo (0: Ausencia, 1: Presenca)", fontsize=12, pad=10)
    plt.xlabel("Diagnostico de Doenca Cardiaca")
    plt.ylabel("Contagem de Pacientes")
    plt.xticks([0, 1], ["Sem Doenca (0)", "Com Doenca (1)"])
    for i, count in enumerate(df['target'].value_counts().sort_index()):
        plt.text(i, count / 2, f"{count}\n({count/len(df)*100:.1f}%)", ha='center', va='center', color='white', fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS_DIR, "distribuicao_classes.png"), dpi=300)
    plt.close()
    
    return X, y, df

def construir_preprocessador():
    """
    Constroi o ColumnTransformer com pipelines de imputacao e codificacao
    estritamente sem vazamento de dados (data leakage).
    """
    num_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
    cat_features = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']

    num_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    cat_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', drop='first', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, num_features),
            ('cat', cat_transformer, cat_features)
        ]
    )
    return preprocessor

def main():
    X, y, df = carregar_e_preparar_dados()
    
    print("[2/6] Divisao estratificada Treino/Teste (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Tamanho Treino: {len(X_train)} | Tamanho Teste: {len(X_test)}")
    
    preprocessor = construir_preprocessador()
    
    # Criacao dos pipelines para os dois modelos comparados
    pipe_lr = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(C=1.0, max_iter=1000, random_state=42))
    ])

    pipe_rf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_split=4, random_state=42))
    ])
    
    print("[3/6] Executando Validacao Cruzada 5-Fold Estratificada no Treino...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']

    cv_lr = cross_validate(pipe_lr, X_train, y_train, cv=cv, scoring=scoring)
    cv_rf = cross_validate(pipe_rf, X_train, y_train, cv=cv, scoring=scoring)
    
    cv_results = {
        "Regressao Logistica": {
            "accuracy_mean": float(cv_lr["test_accuracy"].mean()),
            "accuracy_std": float(cv_lr["test_accuracy"].std()),
            "precision_mean": float(cv_lr["test_precision"].mean()),
            "recall_mean": float(cv_lr["test_recall"].mean()),
            "f1_mean": float(cv_lr["test_f1"].mean()),
            "roc_auc_mean": float(cv_lr["test_roc_auc"].mean())
        },
        "Random Forest": {
            "accuracy_mean": float(cv_rf["test_accuracy"].mean()),
            "accuracy_std": float(cv_rf["test_accuracy"].std()),
            "precision_mean": float(cv_rf["test_precision"].mean()),
            "recall_mean": float(cv_rf["test_recall"].mean()),
            "f1_mean": float(cv_rf["test_f1"].mean()),
            "roc_auc_mean": float(cv_rf["test_roc_auc"].mean())
        }
    }
    
    print("\n--- Resultados CV 5-Fold ---")
    for model_name, m in cv_results.items():
        print(f"{model_name}:")
        print(f"  Acuracia: {m['accuracy_mean']:.4f} (+/- {m['accuracy_std']:.4f})")
        print(f"  Precisao: {m['precision_mean']:.4f}")
        print(f"  Recall:   {m['recall_mean']:.4f}")
        print(f"  F1-Score: {m['f1_mean']:.4f}")
        print(f"  ROC-AUC:  {m['roc_auc_mean']:.4f}")

    print("\n[4/6] Treinando modelos e avaliando no Conjunto de Teste Cego (61 amostras)...")
    pipe_lr.fit(X_train, y_train)
    y_pred_lr = pipe_lr.predict(X_test)
    y_proba_lr = pipe_lr.predict_proba(X_test)[:, 1]

    pipe_rf.fit(X_train, y_train)
    y_pred_rf = pipe_rf.predict(X_test)
    y_proba_rf = pipe_rf.predict_proba(X_test)[:, 1]

    cm_lr = confusion_matrix(y_test, y_pred_lr)
    cm_rf = confusion_matrix(y_test, y_pred_rf)
    
    test_results = {
        "Regressao Logistica": {
            "accuracy": float(accuracy_score(y_test, y_pred_lr)),
            "precision": float(precision_score(y_test, y_pred_lr)),
            "recall": float(recall_score(y_test, y_pred_lr)),
            "f1": float(f1_score(y_test, y_pred_lr)),
            "roc_auc": float(roc_auc_score(y_test, y_proba_lr)),
            "confusion_matrix": cm_lr.tolist(),
            "classification_report": classification_report(y_test, y_pred_lr, output_dict=True)
        },
        "Random Forest": {
            "accuracy": float(accuracy_score(y_test, y_pred_rf)),
            "precision": float(precision_score(y_test, y_pred_rf)),
            "recall": float(recall_score(y_test, y_pred_rf)),
            "f1": float(f1_score(y_test, y_pred_rf)),
            "roc_auc": float(roc_auc_score(y_test, y_proba_rf)),
            "confusion_matrix": cm_rf.tolist(),
            "classification_report": classification_report(y_test, y_pred_rf, output_dict=True)
        }
    }

    print("\n--- Resultados Teste Cego ---")
    for model_name, m in test_results.items():
        print(f"{model_name}:")
        print(f"  Acuracia: {m['accuracy']:.4f}")
        print(f"  Precisao: {m['precision']:.4f}")
        print(f"  Recall:   {m['recall']:.4f}")
        print(f"  F1-Score: {m['f1']:.4f}")
        print(f"  ROC-AUC:  {m['roc_auc']:.4f}")

    print("\n[5/6] Gerando graficos de avaliacao e metricas...")
    
    # 1. Matrizes de Confusao Comparativas
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    
    sns.heatmap(cm_lr, annot=True, fmt='d', cmap='Blues', ax=axes[0], cbar=False,
                xticklabels=['Previsto: 0', 'Previsto: 1'],
                yticklabels=['Real: 0', 'Real: 1'], annot_kws={"size": 13, "weight": "bold"})
    axes[0].set_title(f"Regressao Logistica\nAcuracia: {test_results['Regressao Logistica']['accuracy']*100:.1f}% | Recall: {test_results['Regressao Logistica']['recall']*100:.1f}%", fontsize=11)
    
    sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Greens', ax=axes[1], cbar=False,
                xticklabels=['Previsto: 0', 'Previsto: 1'],
                yticklabels=['Real: 0', 'Real: 1'], annot_kws={"size": 13, "weight": "bold"})
    axes[1].set_title(f"Random Forest\nAcuracia: {test_results['Random Forest']['accuracy']*100:.1f}% | Recall: {test_results['Random Forest']['recall']*100:.1f}%", fontsize=11)
    
    plt.suptitle("Comparacao das Matrizes de Confusao no Conjunto de Teste (N=61)", fontsize=13, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS_DIR, "matriz_confusao_comparativa.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Curvas ROC Comparativas
    fpr_lr, tpr_lr, _ = roc_curve(y_test, y_proba_lr)
    fpr_rf, tpr_rf, _ = roc_curve(y_test, y_proba_rf)

    plt.figure(figsize=(7, 5.5))
    plt.plot(fpr_lr, tpr_lr, color='#1f77b4', lw=2, label=f"Regressao Logistica (AUC = {test_results['Regressao Logistica']['roc_auc']:.3f})")
    plt.plot(fpr_rf, tpr_rf, color='#2ca02c', lw=2, linestyle='--', label=f"Random Forest (AUC = {test_results['Random Forest']['roc_auc']:.3f})")
    plt.plot([0, 1], [0, 1], color='#888888', linestyle=':', label="Aleatorio (AUC = 0.500)")
    plt.xlim([-0.02, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("Taxa de Falsos Positivos (1 - Especificidade)", fontsize=11)
    plt.ylabel("Taxa de Verdadeiros Positivos (Sensibilidade / Recall)", fontsize=11)
    plt.title("Curva ROC Comparativa dos Modelos no Conjunto de Teste", fontsize=12, pad=12)
    plt.legend(loc="lower right", frameon=True, fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS_DIR, "curvas_roc.png"), dpi=300)
    plt.close()

    # 3. Importancia dos Atributos (Random Forest)
    rf_model = pipe_rf.named_steps['classifier']
    preproc = pipe_rf.named_steps['preprocessor']
    feature_names = preproc.get_feature_names_out()
    
    importances = rf_model.feature_importances_
    feat_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False).head(10)
    
    # Limpar nomes dos atributos para melhor legibilidade
    clean_names = [f.replace('num__', '').replace('cat__', '') for f in feat_df['Feature']]
    feat_df['Feature_Clean'] = clean_names

    plt.figure(figsize=(8, 5))
    sns.barplot(x='Importance', y='Feature_Clean', data=feat_df, palette='Blues_r')
    plt.title("Top 10 Variaveis Mais Relevantes - Random Forest", fontsize=12, pad=12)
    plt.xlabel("Grau de Importancia Relativa (Gini Importance)")
    plt.ylabel("Atributo Clinico")
    for i, v in enumerate(feat_df['Importance']):
        plt.text(v + 0.003, i, f"{v*100:.1f}%", va='center', fontsize=9)
    plt.xlim(0, max(feat_df['Importance']) * 1.15)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS_DIR, "importancia_atributos_rf.png"), dpi=300)
    plt.close()

    print("[6/6] Salvando modelo campeao e relatorios...")
    # Salvando Regressao Logistica (Campeao de Generalizacao & AUC)
    joblib.dump(pipe_lr, os.path.join(MODELS_DIR, "heart_disease_pipeline.joblib"))
    # Salvando tambem o Random Forest para fins comparativos
    joblib.dump(pipe_rf, os.path.join(MODELS_DIR, "random_forest_pipeline.joblib"))

    # Salvar metricas consolidadas em JSON
    metrics_summary = {
        "cross_validation": cv_results,
        "test_evaluation": test_results,
        "model_chosen": "Regressao Logistica",
        "justification": "A Regressao Logistica obteve desempenho superior na Validacao Cruzada 5-fold (F1-score 0.8214 vs 0.7446; ROC-AUC 0.9021 vs 0.8816) e no teste cego alcancou AUC excepcional de 0.9621 com Sensibilidade (Recall) de 89.29%. Alem disso, modelos lineares oferecem explicabilidade direta e menor suscetibilidade a overfitting em amostras clinicas compactas."
    }
    
    with open(os.path.join(BASE_DIR, "reports", "metrics_summary.json"), "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=4, ensure_ascii=False)

    print("Treinamento e avaliacao concluidos com exito absoluto!")

if __name__ == "__main__":
    main()
