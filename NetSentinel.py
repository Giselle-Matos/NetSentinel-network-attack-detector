import pyshark
import csv
import os
import numpy as np
from datetime import datetime

INTERFACE = 'enp0s3'  # Atualize se necessário (ex: 'eth0', 'wlan0', etc.)
ARQUIVO_SAIDA = "trafego_benigno_capturado.csv"
PACOTES_POR_FLOW = 10

# Criar cabeçalho CSV se o arquivo ainda não existe
if not os.path.exists(ARQUIVO_SAIDA):
    with open(ARQUIVO_SAIDA, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Flow Duration',
            'Total Fwd Packets',
            'Packet Length Mean',
            'Flow Bytes/s',
            'Fwd Packet Length Max',
            'Label'  # Sempre 0 para benigno
        ])

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
        fwd_packet_length_max,
        0  # label = 0 (benigno)
    ]

print(f"📡 Iniciando captura de tráfego benigno na interface: {INTERFACE}")
janela = []

try:
    captura = pyshark.LiveCapture(interface=INTERFACE)

    for pkt in captura.sniff_continuously():
        janela.append(pkt)

        if len(janela) >= PACOTES_POR_FLOW:
            features = extrair_features(janela)
            janela = []

            if features:
                with open(ARQUIVO_SAIDA, mode='a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(features)
                print(f"✅ Flow salvo às {datetime.now().strftime('%H:%M:%S')}")

except KeyboardInterrupt:
    print("\n🛑 Captura encerrada pelo usuário.")
except Exception as e:
    print(f"❌ Erro: {e}")
