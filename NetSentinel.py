import pyshark
import joblib
import numpy as np
from datetime import datetime

# === 1. Carregar modelo e scaler treinados ===
modelo = joblib.load("modelo_random_forest.joblib")
scaler = joblib.load("scaler_random_forest.joblib")

# === 2. Interface a ser monitorada ===
INTERFACE = 'Wi-Fi'  # ou 'Ethernet', 'wlan0', etc. — depende do seu sistema

# === 3. Variáveis para simular as features ===
janela_pacotes = []
pacotes_para_agrupar = 10  # número de pacotes para simular uma "flow"

print(f"🔍 Monitorando tráfego na interface: {INTERFACE} (pressione CTRL+C para parar)\n")

# === 4. Função para extrair features ===
def extrair_features(pacotes):
    if len(pacotes) < 1:
        return None

    duracao = float(pacotes[-1].sniff_timestamp) - float(pacotes[0].sniff_timestamp)
    total_fwd_packets = len(pacotes)
    tamanhos = []

    for pkt in pacotes:
        try:
            tamanhos.append(int(pkt.length))
        except:
            continue

    if len(tamanhos) == 0:
        return None

    packet_length_mean = np.mean(tamanhos)
    flow_bytes_s = np.sum(tamanhos) / duracao if duracao > 0 else 0
    fwd_packet_length_max = np.max(tamanhos)

    return [
        duracao,
        total_fwd_packets,
        packet_length_mean,
        flow_bytes_s,
        fwd_packet_length_max
    ]

# === 5. Captura contínua de pacotes ===
try:
    captura = pyshark.LiveCapture(interface=INTERFACE)

    for pkt in captura.sniff_continuously():
        janela_pacotes.append(pkt)

        if len(janela_pacotes) >= pacotes_para_agrupar:
            features = extrair_features(janela_pacotes)
            janela_pacotes = []  # limpa para próxima janela

            if features:
                X = scaler.transform([features])
                resultado = modelo.predict(X)[0]
                tempo = datetime.now().strftime("%H:%M:%S")
                print(f"[{tempo}] ⚠️ ATAQUE" if resultado == 1 else f"[{tempo}] ✅ Benigno")

except KeyboardInterrupt:
    print("\n🛑 Captura finalizada pelo usuário.")

except Exception as e:
    print(f"❌ Erro durante a captura: {e}")
