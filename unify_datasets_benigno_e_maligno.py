import pandas as pd

# Arquivos CSV
arquivos_csv = [
    ("dados_misturados_para_teste_da_randomforest_labeled_trafego_variado.csv", ";", ","),
    ("synthetic_ddos_dataset_20k_para_teste_com_label.csv", ";", ","),
]

dfs = []

for arquivo, separador, decimal in arquivos_csv:
    print(f"\n🔍 Lendo {arquivo} com sep='{separador}' e decimal='{decimal}'...")

    try:
        df = pd.read_csv(arquivo, sep=separador, decimal=decimal, engine='python')
        df.columns = [col.strip() for col in df.columns]
        print(f"Colunas encontradas: {df.columns.tolist()}")

        # Confere se todas as colunas esperadas estão presentes
        colunas_esperadas = [
            'Flow Duration',
            'Total Fwd Packets',
            'Packet Length Mean',
            'Flow Bytes/s',
            'Fwd Packet Length Max',
            'Label'
        ]

        if all(col in df.columns for col in colunas_esperadas):
            df = df[colunas_esperadas]
            dfs.append(df)
        else:
            print(f"⚠️ Colunas incompatíveis. Ignorando {arquivo}.")

    except Exception as e:
        print(f"❌ Erro ao processar {arquivo}: {e}")

# Junta e salva
if dfs:
    df_final = pd.concat(dfs, ignore_index=True).sample(frac=1, random_state=42)
    df_final.to_csv("dados_misturados_para_teste_da_randomforest_labeled_trafego_variado_v2.csv", index=False, sep=';', decimal=',')
    print("\n✅ Arquivo 'dados_unificados_para_randomforest.csv' salvo com sucesso!")
else:
    print("\n❌ Nenhum dataset pôde ser processado.")
