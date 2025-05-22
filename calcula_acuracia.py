import pandas as pd
from sklearn.metrics import classification_report, accuracy_score

# === 1. Carregar o arquivo com predições feitas pelo modelo ===
df_predito = pd.read_csv("resultado_predito_randomforest.csv", sep=';', decimal=',')

# === 2. Carregar o gabarito (arquivo com a coluna Label real) ===
df_gabarito = pd.read_csv("dados_misturados_para_teste_da_randomforest_labeled_trafego_variado_v2.csv", sep=';', decimal=',')

# === 3. Garantir que as linhas estão alinhadas ===
if len(df_predito) != len(df_gabarito):
    raise ValueError("❌ Os arquivos têm quantidade diferente de linhas!")

# === 4. Comparar as predições com o gabarito ===
y_true = df_gabarito['Label']
y_pred = df_predito['is_attack?']

# === 5. Exibir resultado ===
print("✅ Relatório de Classificação (Comparando com Gabarito):\n")
print(classification_report(y_true, y_pred))

# Acurácia bruta
print(f"🎯 Acurácia: {accuracy_score(y_true, y_pred) * 100:.2f}%")
