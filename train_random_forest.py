import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import joblib

# === 1. Carregar a base de dados com separador ";" e converter vírgulas decimais ===
df = pd.read_csv("dados_misturados_para_randomforest_trafego_variado.csv", sep=';', decimal=',')

# === 2. Selecionar as features e o rótulo ===
features = [
    'Flow Duration',
    'Total Fwd Packets',
    'Packet Length Mean',
    'Flow Bytes/s',
    'Fwd Packet Length Max'
]

X = df[features].copy()
y = df['Label']

# === 3. Pré-processar os dados ===
X = X.replace([np.inf, -np.inf], np.nan)
X = X.fillna(X.mean())
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# === 4. Dividir em treino e teste ===
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# === 5. Criar e treinar o modelo Random Forest ===
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# === 6. Avaliar o modelo ===
y_pred = modelo.predict(X_test)
print("Relatório de Classificação:\n")
print(classification_report(y_test, y_pred))

# === 7. Salvar o modelo e o scaler ===
joblib.dump(modelo, "modelo_random_forest.joblib")
joblib.dump(scaler, "scaler_random_forest.joblib")
print("\n✅ Modelo e scaler salvos com sucesso!")
