#@title 4.4. Treinamento do modelo com os melhores hiperparâmetros
from sklearn.ensemble import RandomForestClassifier

from IA_Models.data_train import X_train, y_train, X_test

modelo_otimizado = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=4,
    min_samples_leaf=2,
    max_features="sqrt",
    bootstrap=True,
    class_weight=None,
    random_state=42,
    n_jobs=-1
)

# Treinando o modelo_otimizado com os dados de treino
modelo_otimizado.fit(X_train, y_train)
# Fazendo previsões no conjunto de teste
y_pred_2 = modelo_otimizado.predict(X_test)
# avaliar_modelo(modelo_otimizado, y_pred_2)