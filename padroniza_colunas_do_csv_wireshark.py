import pandas as pd

# Carrega o CSV benigno
df = pd.read_csv("saida_dados_malignos_wireshark.csv")

# Preenche vazios com 0
df = df.fillna(0)

# Cria colunas para combinar com o ataque filtrado
df['Flow Duration'] = df['frame.time_relative']  # aproximação
df['Total Fwd Packets'] = 1  # cada linha é 1 pacote
df['Packet Length Mean'] = df['frame.len']
df['Flow Bytes/s'] = df['frame.len'] / (df['frame.time_relative'] + 0.000001)  # para evitar divisão por zero
df['Fwd Packet Length Max'] = df['udp.length']  # se for 0, sem problema
df['Label'] = 0  # benigno

# Mantém apenas as colunas compatíveis
df_benigno_final = df[['Flow Duration', 'Total Fwd Packets', 'Packet Length Mean',
                       'Flow Bytes/s', 'Fwd Packet Length Max', 'Label']]

df_benigno_final.to_csv("benigno_padronizado.csv", index=False)
