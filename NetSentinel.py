import pyshark
import joblib
import numpy as np
import time
from datetime import datetime
from statistics import mean

# === Carregamento do modelo e scaler ===
modelo = joblib.load('modelo_random_forest.joblib')
scaler = joblib.load('scaler_random_forest.joblib')

# === Parâmetros da captura ===
interface = 'enp0s3'
janela_segundos = 3  # Intervalo de tempo para agrupar pacotes

print(f"📡 Monitorando tráfego na interface: {interface} (em janelas de {janela_segundos}s)\n")

def extrair_features_fluxo(pacotes):
    if not pacotes:
        return None

    duracoes = [float(pkt.sniff_timestamp) for pkt in pacotes]
    tamanhos = [int(pkt.length) for pkt in pacotes]

    flow_duration = (max(duracoes) - min(duracoes)) * 1000  # em ms
    total_fwd_packets = len(pacotes)
    packet_length_mean = mean(tamanhos)
    flow_bytes_per_sec = sum(tamanhos) / janela_segundos
    fwd_packet_length_max = max(tamanhos)

    return [
        flow_duration,
        total_fwd_packets,
        packet_length_mean,
        flow_bytes_per_sec,
        fwd_packet_length_max
    ]

try:
    captura = pyshark.LiveCapture(interface=interface)
    buffer = []
    inicio_janela = time.time()

    for pacote in captura.sniff_continuously():
        buffer.append(pacote)
        if (time.time() - inicio_janela) >= janela_segundos:
            features = extrair_features_fluxo(buffer)
            buffer.clear()
            inicio_janela = time.time()

            if features:
                print("\n📦 Janela de pacotes - Features extraídas:")
                print(f"Flow Duration: {features[0]:.2f} ms")
                print(f"Total Fwd Packets: {features[1]}")
                print(f"Packet Length Mean: {features[2]:.2f}")
                print(f"Flow Bytes/s: {features[3]:.2f}")
                print(f"Fwd Packet Length Max: {features[4]:.2f}")

                entrada = np.array(features).reshape(1, -1)
                entrada_pad = scaler.transform(entrada)
                pred = modelo.predict(entrada_pad)[0]

                status = "🔥 MALIGNO" if pred == 1 else "✅ BENIGNO"
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {status}")
except KeyboardInterrupt:
    print("\n🛑 Captura encerrada pelo usuário.")
except Exception as e:
    print(f"⚠️ Erro durante execução: {e}")
