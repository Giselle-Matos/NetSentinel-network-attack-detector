import joblib
import pyshark
import numpy as np
from datetime import datetime

# === Carregamento do modelo treinado e scaler ===
modelo = joblib.load("modelo_random_forest.pkl")
scaler = joblib.load("scaler.pkl")

# === Interface de rede a ser monitorada ===
INTERFACE = "enp0s3"  # Substitua conforme o nome da interface da VM alvo (use `ifconfig` ou `ip a`)

# === Função para extrair características do pacote ===
def extrair_caracteristicas(pacote):
    try:
        duracao = float(pacote.frame_info.time_delta)  # Tempo entre este e o último pacote
        total_fwd_packets = 1  # Supondo 1 por fluxo; adaptável se usar agrupamento posterior
        packet_length = int(pacote.length)
        packet_length_mean = packet_length  # Igual ao tamanho se fluxo for de 1 pacote
        flow_bytes_s = packet_length / duracao if duracao > 0 else 0
        fwd_packet_length_max = packet_length  # Valor máximo para esse fluxo único

        return [
            duracao,
            total_fwd_packets,
            packet_length_mean,
            flow_bytes_s,
            fwd_packet_length_max,
            0  # Label fictício, ignorado na predição
        ]
    except Exception as e:
        print(f"[⚠️] Erro ao extrair características: {e}")
        return None

# === Função de predição e saída formatada ===
def prever_trafego(modelo, scaler, dados_pacote):
    if len(dados_pacote) != 6:
        print(f"[⚠️] Pacote ignorado. Dados incompletos: {dados_pacote}")
        return

    # Convertendo para numpy array e ajustando formato para scaler e modelo
    entrada = np.array(dados_pacote[:-1], dtype=float).reshape(1, -1)

    # 🔎 Mostra os dados brutos
    print(f"\n📦 Dados brutos capturados: {entrada}")

    # Aplica o mesmo scaler usado no treinamento
    entrada_normalizada = scaler.transform(entrada)

    # 🔎 Mostra os dados padronizados (input real da IA)
    print(f"📏 Dados normalizados (input do modelo): {entrada_normalizada}")

    # Predição
    predicao = modelo.predict(entrada_normalizada)[0]
    label = "🔥 MALIGNO" if predicao == 1 else "✅ BENIGNO"

    # Output
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {label} - Tamanho: {entrada[0][3]} bytes\n")

# === Início do monitoramento ===
print(f"📡 Monitorando tráfego na interface: {INTERFACE} (pressione CTRL+C para parar)")

# Captura contínua usando pyshark
try:
    captura = pyshark.LiveCapture(interface=INTERFACE)

    for pacote in captura.sniff_continuously():
        dados = extrair_caracteristicas(pacote)
        if dados:
            prever_trafego(modelo, scaler, dados)

except KeyboardInterrupt:
    print("\n🛑 Captura finalizada pelo usuário.")
except Exception as e:
    print(f"[❌] Erro durante a captura: {e}")
