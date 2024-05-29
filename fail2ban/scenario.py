from datetime import datetime, timedelta
from collections import defaultdict
import os
import subprocess
import json

# Configurations
attack_time_window = timedelta(minutes=5)
max_attempts = 3
banned_ips = []

def configure_nftables():
    try:
        subprocess.run(['sudo', 'nft', 'add', 'table', 'inet', 'filter'], check=True)
        subprocess.run(['sudo', 'nft', 'add', 'chain', 'inet', 'filter', 'input', '{', 'type', 'filter', 'hook', 'input', 'priority', '0', ';', '}'], check=True)
    except subprocess.CalledProcessError as e:
        if "File exists" not in str(e):
            print(f"Error configuring nftables: {e}")

def detect_brute_force(failed_attempts):
    attempts_by_ip = defaultdict(list)
    ports = defaultdict(list)
    source_ports = defaultdict(list)

    for date, user, ip, source_port in failed_attempts:
        attempts_by_ip[ip].append((date, source_port))
        ports[ip] = 22 
        source_ports[ip] = source_port 

    malicious_ips = set()
    for ip, attempts in attempts_by_ip.items():
        attempts.sort()
        for i in range(len(attempts)):
            window_attempts = [attempt for attempt in attempts if attempt[0] - attempts[i][0] <= attack_time_window]
            if len(window_attempts) >= max_attempts:
                malicious_ips.add(ip)
                break

    return malicious_ips, ports, source_ports

def ban_ips(malicious_ips, ports, source_ports, ban_duration):
    for ip in malicious_ips:
        if not any(ban['IP'] == ip for ban in banned_ips):
            ban_start_time = datetime.now()
            ban_end_time = ban_start_time + timedelta(seconds=ban_duration)
            ban_ip(ip, ports[ip], source_ports[ip], ban_start_time, ban_end_time)

def ban_ip(ip, port, source_port, ban_start_time, ban_end_time):
    print(f"Banning IP: {ip}, Source Port: {source_port}, Port: {port}, Date: {ban_start_time}")
    try:
        configure_nftables()
        subprocess.run(['sudo', 'nft', 'add', 'rule', 'inet', 'filter', 'input', 'ip', 'saddr', ip, 'counter', 'drop'], check=True)
        print(f"IP {ip} bloquée avec succès.")
        banned_ips.append({'IP': ip, 'Source Port': source_port, 'Port': port, 'Date': ban_start_time, 'End Time': ban_end_time, 'Time Left': (ban_end_time - datetime.now()).total_seconds()})
        print_table(banned_ips)
    except subprocess.CalledProcessError as e:
        print(f"Error banning IP {ip}: {e}")

def get_banned_ips():
    current_time = datetime.now()
    for ban in banned_ips:
        time_left = (ban['End Time'] - current_time).total_seconds()
        ban['Time Left'] = time_left
    return banned_ips
def print_table(data):
    print("+-----------------+---------------+------+---------------------+---------------------+--------------+")
    print("| Adresse IP      | Port source   | Port | Date                | Fin du ban          | Temps restant |")
    print("+-----------------+---------------+------+---------------------+---------------------+--------------+")
    for entry in data:
        time_left = entry['Time Left']
        print(f"| {entry['IP']:15} | {entry['Source Port']:13} | {entry['Port']:4} | {entry['Date']} | {entry['End Time']} | {int(time_left)}s |")
    print("+-----------------+---------------+------+---------------------+---------------------+--------------+")

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

def save_banned_ips(filename):
    with open(filename, 'w') as file:
        json.dump(banned_ips, file, default=str)
