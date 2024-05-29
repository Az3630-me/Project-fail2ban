import re
from datetime import datetime
import subprocess

# Regex pour le parsing des logs de connexion ssh
ssh_fail_pattern = re.compile(
    r'(?P<date>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}) .* sshd\[.*\]: Failed password for (invalid user )?(?P<user>\S*) from (?P<ip>\S*) port (?P<source_port>\d+) ssh2'
)

def parse_log_line(line): # Cette fonction analyse une ligne de journal pour extraire les informations d'échec de connexion SSH
    match = ssh_fail_pattern.match(line)
    if match:
        date_str = match.group('date')
        user = match.group('user')
        ip = match.group('ip')
        source_port = int(match.group('source_port'))
        date = datetime.fromisoformat(date_str)
        return date, user, ip, source_port
    return None

def process_log_file(logfile_path): # Cette fonction traite le fichier de log pour trouver toutes les tentatives d'échec de connexion SSH
    failed_attempts = []
    try:
        result = subprocess.run(['sudo', 'cat', logfile_path], capture_output=True, text=True, check=True)  # Exécution d'une commande shell pour lire le fichier de log avec des privilèges sudo
        for line in result.stdout.splitlines():  # On analyse chaque ligne du fichier de log
            result = parse_log_line(line)
            if result:
                failed_attempts.append(result)
    except subprocess.CalledProcessError as e:
        # On affiche un message d'erreur si la lecture du fichier de log échoue
        print(f"Erreur lors de la lecture du fichier de log {logfile_path}: {e}")

    return failed_attempts
