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

Utilisation
Le script Fail2Ban peut être exécuté avec différentes options pour définir la durée du bannissement et afficher le statut des IP bannies.
Tout les bannissements effectués sont répertoriés dans un fichier json présent dans le dossier fail2ban

Options disponibles :

-h, --help : Affiche l'aide et les options disponibles.
-d, --ban-duration : Définit la durée du bannissement en secondes (ex : -d 3600).
-s, --status : Affiche le statut des IP bannies.

Exemples :

Démarrer le script avec une durée de bannissement de 60 secondes :
python3 main.py -d 60

Afficher le statut des IP bannies :
python3 main.py -s
