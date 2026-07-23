
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, average_precision_score, confusion_matrix
from sklearn.preprocessing import StandardScaler


def calcular_tss(y_true, y_pred_proba, umbral=0.5):
    """True Skill Statistic = sensibilidad + especificidad - 1"""
    y_pred = (y_pred_proba >= umbral).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    sensibilidad = tp / (tp + fn) if (tp + fn) > 0 else 0
    especificidad = tn / (tn + fp) if (tn + fp) > 0 else 0
    return sensibilidad + especificidad - 1


def evaluar_modelo_cv(modelo_fn, X, y, n_splits=5, escalar=False, random_state=42):
    """
    Evalúa un modelo con k-fold estratificado.
    modelo_fn: función que retorna una instancia NUEVA del modelo (sin entrenar) cada vez que se llama.
    """
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    resultados = {"auc_roc": [], "auc_pr": [], "tss": []}

    for train_idx, test_idx in skf.split(X, y):
        X_train, X_test = X.iloc[train_idx].copy(), X.iloc[test_idx].copy()
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        if escalar:
            scaler = StandardScaler()
            X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
            X_test = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)

        modelo = modelo_fn()
        modelo.fit(X_train, y_train)

        y_pred_proba = modelo.predict_proba(X_test)[:, 1]

        resultados["auc_roc"].append(roc_auc_score(y_test, y_pred_proba))
        resultados["auc_pr"].append(average_precision_score(y_test, y_pred_proba))
        resultados["tss"].append(calcular_tss(y_test.values, y_pred_proba))

    return {
        "auc_roc_mean": np.mean(resultados["auc_roc"]), "auc_roc_std": np.std(resultados["auc_roc"]),
        "auc_pr_mean": np.mean(resultados["auc_pr"]), "auc_pr_std": np.std(resultados["auc_pr"]),
        "tss_mean": np.mean(resultados["tss"]), "tss_std": np.std(resultados["tss"]),
    }
