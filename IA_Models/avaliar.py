#@title 4.2. Impressão das métricas de qualidade do modelo
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from data_train import y_test


def avaliar_modelo(modelo, y_pred):
    """
    Avaliação do modelo para problemas de classificação e regressão.
    Fornece métricas, relatório de classificação e gráficos de avaliação.

    Parâmetros:
    - modelo: o modelo treinado (ex.: LinearRegression, RandomForestClassifier, etc.)
    - y_pred: valores previstos pelo modelo
    """
    print("======= Avaliação do Modelo =======\n")

    # Identificar o tipo de problema (classificação ou regressão)

    print("Modelo Identificado: Classificação\n")

    # Acurácia
    acuracia = accuracy_score(y_test, y_pred)
    print(f"Acurácia: {acuracia:.4f}")


    # Relatório de Classificação
    print("\nRelatório de Classificação:")
    print(classification_report(y_test, y_pred))

    # Matriz de Confusão
    plt.figure(figsize=(6, 5))
    matriz_confusao = confusion_matrix(y_test, y_pred)
    sns.heatmap(matriz_confusao, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.xlabel("Previsto")
    plt.ylabel("Real")
    plt.title("Matriz de Confusão")
    plt.show()


    print("\n======= Avaliação Finalizada =======")