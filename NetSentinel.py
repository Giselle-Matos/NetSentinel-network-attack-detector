import pyshark
import joblib
import numpy as np
from datetime import datetime

# Carrega modelo e scaler treinados
modelo = joblib.load('modelo_random_forest.joblib')
scaler = joblib.load('scaler_random_forest.joblib')

# === Função para extrair features de um pacote de rede ===
def extrair_features(pacote):
    try:
        flow_duration = float(pacote.sniff_time.timestamp() * 1000)  # tempo em ms
        total_fwd_packets = 1  # cada pacote individual
        packet_length_mean = float(pacote.length)
        flow_bytes_per_sec = float(pacote.length) / 1.0  # simplificado como "1 segundo"
        fwd_packet_length_max = float(pacote.length)

        return [
            flow_duration,
            total_fwd_packets,
            packet_length_mean,
            flow_bytes_per_sec,
            fwd_packet_length_max
        ]
    except Exception as e:
        print(f"[⚠️] Erro ao extrair dados do pacote: {e}")
        return None

# Interface de rede a ser monitorada (ajuste com 'ip a' se necessário)
interface = 'enp0s3'

print(f"📡 Monitorando tráfego na interface: {interface} (pressione CTRL+C para parar)\n")

# === Captura contínua ===
try:
    captura = pyshark.LiveCapture(interface=interface)

    for pacote in captura.sniff_continuously():
        features = extrair_features(pacote)
        if features:
            # Mostra os dados extraídos para análise comparativa
            print(f"\n📥 Pacote capturado - Features extraídas:")
            print(f"Flow Duration: {features[0]}")
            print(f"Total Fwd Packets: {features[1]}")
            print(f"Packet Length Mean: {features[2]}")
            print(f"Flow Bytes/s: {features[3]}")
            print(f"Fwd Packet Length Max: {features[4]}")

            # Prepara para predição
            features = np.array(features).reshape(1, -1)
            features_padronizadas = scaler.transform(features)
            predicao = modelo.predict(features_padronizadas)[0]

            # Resultado da classificação
            tipo = "🔥 MALIGNO" if predicao == 1 else "✅ BENIGNO"
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {tipo} - Tamanho: {features[0][2]} bytes")

except KeyboardInterrupt:
    print("\n🛑 Captura interrompida pelo usuário.")
except Exception as e:
    print(f"[ERRO FATAL] Erro durante a captura: {e}")
