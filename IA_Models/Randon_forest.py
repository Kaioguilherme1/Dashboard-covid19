from IA_Models.data_train import X_train, X_test, y_train, y_test
from sklearn.ensemble import RandomForestClassifier
from avaliar import avaliar_modelo

#@title 4.1. Treinamento do modelo sem ajustes de hiperparâmetros
# Criar e treinar o modelo Random Forest
modelo = RandomForestClassifier()
modelo.fit(X_train, y_train)

# Fazer previsões no conjunto de teste
y_pred = modelo.predict(X_test)

avaliar_modelo(modelo, y_pred)