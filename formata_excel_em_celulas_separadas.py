import pandas as pd

# Ler o novo dataset separando por vírgula e usando ponto como decimal
novo_df = pd.read_csv("synthetic_ddos_dataset_20k.csv", sep=',', decimal='.')

# Remover a coluna 'Attack Type', pois não será usada para treinamento
if 'Attack Type' in novo_df.columns:
    novo_df = novo_df.drop(columns=['Attack Type'])

# Garantir que a coluna Label está como inteiro
novo_df['Label'] = novo_df['Label'].astype(int)

# Salvar padronizado como .xlsx ou .csv (como preferir usar no código de unificação)
novo_df.to_excel("synthetic_ddos_dataset_20k_formatado.xlsx", index=False)
