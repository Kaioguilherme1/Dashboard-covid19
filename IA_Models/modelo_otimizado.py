#@title 4.4. Treinamento do modelo com os melhores hiperparâmetros
from sklearn.ensemble import RandomForestClassifier
import os, sys
# from avaliar import avaliar_modelo

# Adiciona o diretório pai ao caminho para importar corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from IA_Models.data_train import X_train, y_train, X_test
# from avaliar import avaliar_modelo
modelo_otimizado = RandomForestClassifier(
    n_estimators=60,
    max_depth=40,
    min_samples_split=2,
    min_samples_leaf=1,
    max_features=None,
    bootstrap=True,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

# Treinando o modelo_otimizado com os dados de treino
modelo_otimizado.fit(X_train, y_train)
# Fazendo previsões no conjunto de teste
# y_pred_2 = modelo_otimizado.predict(X_test)
# avaliar_modelo(modelo_otimizado, y_pred_2)
#68.24