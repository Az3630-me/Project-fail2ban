import sys
import time
import json
from collections import defaultdict
from fail2ban.log_parser import process_log_file
from fail2ban.scenario import detect_brute_force, ban_ips, get_banned_ips, print_table, load_banned_ips, save_banned_ips

BANNED_IPS_FILE = 'banned_ips.json' # Nom du fichier servant à stocker les IP bannies

def print_help():
    print("""
Utilisation: python3 main.py [OPTIONS]

Options:
  -h, --help         : Affiche l'aide avec des informations sur les options disponibles.
  -d, --ban-duration : l'utilisateur peut choisir la durée du bannissement de l'IP voulu (ex : -d 3600)
  -s, --status       : Cette option affiche le statut des IP bannis (durée du bannissement, temps restant du bannissement)
""")

def main():
    logfile_path = '/var/log/auth.log' # Chemin des logs SSH
    ban_duration = 3600 # Durée par défaut du bannissement

    load_banned_ips(BANNED_IPS_FILE)

    if len(sys.argv) > 1:
        if sys.argv[1] in ('-h', '--help'):
            print_help()
            return
        elif sys.argv[1] in ('-d', '--ban-duration'):
            ban_duration = int(sys.argv[2])
        elif sys.argv[1] in ('-s', '--status'):
            banned_ips = get_banned_ips()  # Récupération des IP bannies
            print_table(banned_ips) # Affichage du tableau des IP bannies
            return
        else:
            logfile_path = sys.argv[1]

    try:
        while True:
            failed_attempts = process_log_file(logfile_path)
            malicious_ips, ports, source_ports = detect_brute_force(failed_attempts)
            ban_ips(malicious_ips, ports, source_ports, ban_duration)
            save_banned_ips(BANNED_IPS_FILE)
            time.sleep(5)  
    except KeyboardInterrupt:
        print("\nProgramme arrêté.")

if __name__ == "__main__":
    main()
