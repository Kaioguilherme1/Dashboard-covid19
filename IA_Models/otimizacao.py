#@title 4.3. Utilização de técnica para identificação dos melhores hiperparâmetros
import os, sys

# Adiciona a referencia da pasta IA_Models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import RandomizedSearchCV

from IA_Models.data_train import X_train, y_train, X_test, y_test

# 1. Definir o modelo_hiper
modelo_hiper = RandomForestClassifier(random_state=42)

# 2. Melhorar as faixas de parâmetros para RandomizedSearchCV
param_dist = {
    'n_estimators': [60, 80, 100, 150, 200],
    'max_depth': [40, None],
    'min_samples_split': [2, 5, 10, 15, 20, 30, 40],
    'min_samples_leaf': [1, 2, 4, 6, 8, 10, 12],
    'max_features': ['sqrt', 'log2', None],
    'bootstrap': [True, False],
    'class_weight': [
        'balanced',
        {0: 1, 1: 2},
    ]
}

# 3. Configurar RandomizedSearchCV
random_search = RandomizedSearchCV(
    modelo_hiper,
    param_distributions=param_dist,
    n_iter=50,  # Número de combinações aleatórias a serem testadas
    cv=5,  # Validação cruzada com 5 dobras
    scoring="accuracy",  # Métrica para avaliar cada modelo_hiper
    verbose=1,  # Nível de detalhamento no console
    random_state=42,
    n_jobs=-1  # Paralelismo para acelerar a busca
)

# 4. Realizar a busca pelos melhores hiperparâmetros
print("Otimizando os hiperparâmetros...")
random_search.fit(X_train, y_train)

# 5. Melhor modelo_hiper encontrado
print(f"\nMelhor combinação de parâmetros: {random_search.best_params_}")
best_model = random_search.best_estimator_

# Avaliar o melhor modelo_hiper nos dados de teste
y_pred = best_model.predict(X_test)

# 6. Avaliação do modelo_hiper
print("\n=== Avaliação do Modelo ===")
print(f"Acurácia no conjunto de teste: {accuracy_score(y_test, y_pred):.4f}")
print("\nRelatório de Classificação:")
print(classification_report(y_test, y_pred))

# Matriz de confusão
plt.figure(figsize=(6, 5))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt="d", cmap="Blues", cbar=False)
plt.xlabel("Previsto")
plt.ylabel("Real")
plt.title("Matriz de Confusão")
plt.show()