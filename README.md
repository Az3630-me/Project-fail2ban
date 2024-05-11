# Project-fail2ban
Projet BSI Linux 23/24 
le script analyse les logs d'authentification et scrute les lignes correspondants aux motifs prédéfinis concernant les erreurs de login SSH en s'appuyant sur des expressions rationnelles.
En cas d'erreur répétées, il bannit l'IP ayant envoyé les requêtes pendant une durée configurable avec nftables.
