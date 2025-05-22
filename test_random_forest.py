import pandas as pd
import numpy as np
import joblib

# === 1. Carregar a base de dados sem label ===
df = pd.read_csv("dados_misturados_para_teste_da_randomforest_no_label_trafego_variado.csv", sep=';', decimal=',')

# === 2. Selecionar as mesmas features usadas no treinamento ===
features = [
    'Flow Duration',
    'Total Fwd Packets',
    'Packet Length Mean',
    'Flow Bytes/s',
    'Fwd Packet Length Max'
]

X = df[features].copy()

# === 3. Tratar dados inválidos ===
X = X.replace([np.inf, -np.inf], np.nan)
X = X.fillna(X.mean())

# === 4. Carregar modelo e scaler treinados ===
modelo = joblib.load("modelo_random_forest.joblib")
scaler = joblib.load("scaler_random_forest.joblib")
X_scaled = scaler.transform(X)

# === 5. Fazer previsões ===
y_pred = modelo.predict(X_scaled)

# === 6. Adicionar resultado ao dataframe original
df['is_attack?'] = y_pred  # 1 = ataque, 0 = benigno

# === 7. Salvar novo CSV com predição ===
df.to_csv("resultado_predito_randomforest.csv", index=False, sep=';', decimal=',')
print("✅ Predições adicionadas e arquivo salvo como 'resultado_predito_randomforest.csv'.")

# === 8. Exemplo de print individual ===
print("\n🔍 Exemplo de primeira linha classificada:")
print("Resultado:", "ATAQUE" if y_pred[0] == 1 else "BENIGNO")
