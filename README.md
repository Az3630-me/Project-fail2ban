# Project-fail2ban

Fail2Ban est un script Python conçu pour surveiller les tentatives de connexion SSH et bannir les adresses IP malveillantes après 3 tentatives échouées. Ce projet utilise nftables pour implémenter le bannissement des IP et rsyslog pour la gestion des logs.

Prérequis :

Python 3.x

nftables installé et configuré sur le système

rsyslog configuré pour la gestion des logs SSH

Installation

Cloner le dépôt :

sudo git clone https://github.com/Az3630-me/Project-fail2ban.git

cd Project-fail2ban

Installer les dépendances Python :

sudo sh install.sh

Assurez-vous que nftables et rsyslog sont correctement configurés et fonctionnent sur votre système.

sudo python3 -m fail2ban.main

Utilisation

Le script Fail2Ban peut être exécuté avec différentes options pour définir la durée du bannissement et afficher le statut des IP bannies.
Tous les bannissements effectués sont répertoriés dans un fichier json présent dans le dossier fail2ban

Options disponibles :

-h, --help : Affiche l'aide et les options disponibles.

-s, --statut : Affiche la durée du banissement 

-d, --ban-duration : Défini la durée du bannissement en secondes (ex : -d 3600).

Exemples :

Démarrer le script avec une durée de bannissement de 60 secondes :

cd Project-fail2ban/fail2ban/ 

sudo PYTHONPATH=.. python3 main.py -d 60
