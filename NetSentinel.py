import pyshark
import joblib
import numpy as np
from datetime import datetime

# Carrega modelo e scaler
modelo = joblib.load('modelo_random_forest.joblib')
scaler = joblib.load('scaler_random_forest.joblib')

# Função para extrair características de um pacote
def extrair_features(pacote):
    try:
        flow_duration = float(pacote.sniff_time.timestamp() * 1000)  # simplificado como timestamp para exemplo
        total_fwd_packets = 1  # cada pacote individual
        packet_length_mean = float(pacote.length)
        flow_bytes_per_sec = float(pacote.length) / 1.0  # simplificação
        fwd_packet_length_max = float(pacote.length)

        return [
            flow_duration,
            total_fwd_packets,
            packet_length_mean,
            flow_bytes_per_sec,
            fwd_packet_length_max
        ]
    except Exception as e:
        print(f"Erro ao extrair dados: {e}")
        return None

# Nome da interface de rede
interface = 'enp0s3'  # Ajuste conforme necessário (use `ip a` para ver interfaces)

print(f"📡 Monitorando tráfego na interface: {interface} (pressione CTRL+C para parar)\n")

try:
    captura = pyshark.LiveCapture(interface=interface)
    for pacote in captura.sniff_continuously():
        features = extrair_features(pacote)
        if features:
            features = np.array(features).reshape(1, -1)
            features_padronizadas = scaler.transform(features)
            predicao = modelo.predict(features_padronizadas)[0]
            tipo = "🔥 MALIGNO" if predicao == 1 else "✅ BENIGNO"
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {tipo} - Tamanho: {features[0][2]} bytes")
except KeyboardInterrupt:
    print("\n🛑 Captura interrompida pelo usuário.")
except Exception as e:
    print(f"Erro durante a captura: {e}")
