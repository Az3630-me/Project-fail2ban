from datetime import datetime, timedelta
from collections import defaultdict
import os
import subprocess
import json
import sys
import time

# Configurations
attack_time_window = timedelta(minutes=5)  # Fenêtre de temps pour détecter les attaques
max_attempts = 3  # Nombre maximum de tentatives avant de considérer une IP comme malveillante
BANNED_IPS_FILE = 'banned_ips.json'  # Chemin relatif vers le fichier des IP bannies
banned_ips = []  # Liste des IP bannies

# Fonction permettant de configurer nftables
def configure_nftables():
    try:
        subprocess.run(['sudo', 'nft', 'add', 'table', 'inet', 'filter'], check=True)
        subprocess.run(['sudo', 'nft', 'add', 'chain', 'inet', 'filter', 'input', '{', 'type', 'filter', 'hook', 'input', 'priority', '0', ';', '}'], check=True)
    except subprocess.CalledProcessError as e:
        if "File exists" not in str(e):
            print(f"Erreur de configuration nftables: {e}")

# Fonction permettant de détecter les attaques par brute force
def detect_brute_force(failed_attempts):
    attempts_by_ip = defaultdict(list)  # Dictionnaire pour stocker les tentatives par IP
    ports = defaultdict(list)  # Dictionnaire pour stocker les ports par IP
    source_ports = defaultdict(list)  # Dictionnaire pour stocker les ports source par IP

    for date, user, ip, source_port in failed_attempts:
        attempts_by_ip[ip].append((date, source_port))
        ports[ip] = 22  # Port SSH par défaut
        source_ports[ip] = source_port  # Port source

    malicious_ips = set()
    for ip, attempts in attempts_by_ip.items():
        attempts.sort()  # Trie des tentatives par date
        for i in range(len(attempts)):
            window_attempts = [attempt for attempt in attempts if attempt[0] - attempts[i][0] <= attack_time_window]
            if len(window_attempts) >= max_attempts:
                malicious_ips.add(ip)
                break

    return malicious_ips, ports, source_ports

# Fonction pour bannir les IP malveillantes
def ban_ips(malicious_ips, ports, source_ports, ban_duration):
    for ip in malicious_ips:
        if not any(ban['IP'] == ip for ban in banned_ips):
            ban_start_time = datetime.now()
            ban_end_time = ban_start_time + timedelta(seconds=ban_duration)
            ban_ip(ip, ports[ip], source_ports[ip], ban_start_time, ban_end_time)

# Fonction pour appliquer le ban sur une IP
def ban_ip(ip, port, source_port, ban_start_time, ban_end_time):
    print(f"3 tentatives de connexions SSH échoué detecté")
    print(f"Adresse IP à bannir: {ip}")
    try:
        configure_nftables()
        subprocess.run(['sudo', 'nft', 'add', 'rule', 'inet', 'filter', 'input', 'ip', 'saddr', ip, 'counter', 'drop'], check=True)
        print(f"[statut] Adresse IP {ip} bloquée avec succès.")
        banned_ips.append({'IP': ip, 'Source Port': source_port, 'Port': port, 'Date': ban_start_time, 'End Time': ban_end_time, 'Time Left': (ban_end_time - datetime.now()).total_seconds()})
        print_table(banned_ips)
        print_detailed_table(banned_ips)
    except subprocess.CalledProcessError as e:
        print(f"[statut] Erreur lors du bannissement de l'IP {ip}: {e}")

# Fonction pour obtenir les IP bannies
def get_banned_ips():
    current_time = datetime.now()
    for ban in banned_ips:
        time_left = (ban['End Time'] - current_time).total_seconds()
        ban['Time Left'] = time_left
    return banned_ips

# Affichage du tableau principal des IP bannies
def print_table(data):
    print("+-----------------+---------------+------+----------------------------+")
    print("| Adresse IP      | Port source   | Port | Date                       |")
    print("+-----------------+---------------+------+----------------------------+")
    for entry in data:
        print(f"| {entry['IP']:15} | {entry['Source Port']:13} | {entry['Port']:4} | {entry['Date']} |")
    print("+-----------------+---------------+------+----------------------------+")

# Affichage du tableau des détails des IP bannies
def print_detailed_table(data):
    print("+-----------------+---------------------+------------------+")
    print("| Adresse IP      | Fin du ban          | Temps restant       |")
    print("+-----------------+---------------------+------------------+")
    for entry in data:
        time_left = entry['Time Left']
        print(f"| {entry['IP']:15} | {entry['End Time']} | {int(time_left)}s           |")
    print("+-----------------+---------------------+------------------+")

# Fonction pour charger les IP bannies depuis un fichier
def load_banned_ips(filename):
    global banned_ips
    try:
        with open(filename, 'r') as file:
            banned_ips = json.load(file)
            for ban in banned_ips:
                ban['Date'] = datetime.fromisoformat(ban['Date'])
                ban['End Time'] = datetime.fromisoformat(ban['End Time'])
    except FileNotFoundError:
        banned_ips = []

# Fonction pour sauvegarder les IP bannies dans un fichier
def save_banned_ips(filename):
    with open(filename, 'w') as file:
        json.dump(banned_ips, file, default=str)
