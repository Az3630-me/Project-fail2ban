# Project-fail2ban
Projet BSI Linux 23/24 
le script analyse les logs d'authentification et scrute les lignes correspondants aux motifs prédéfinis concernant les erreurs de login SSH en s'appuyant sur des expressions rationnelles.
En cas d'erreur répétées, il bannit l'IP ayant envoyé les requêtes pendant une durée configurable avec nftables.



Script d'analyse de bruteforce (mini-fail2ban)

- Le script analyse les logs d'authentification et scrute les lignes correspondant aux motifs prédéfinis 
concernant les erreurs de login SSH en s'appuyant sur des expressions rationnelles.

- En cas d'erreurs répétées, il bannit l'IP ayant envoyé les requêtes pendant une durée configurable avec nftables


Critères de notation : 
1. Un fichier README au format texte qui doit décrire quels sont les pré-requis et comment les scripts s'installent
2. les scripts doivent proposer une aide en ligne documentant les paramètres qu'ils acceptent, grâce à l'option -h
3. les scripts doivent gérer les cas d'erreur et se terminer sans "crasher". Par exemple en cas de :
- dépendance manquante
- entrée utilisateur invalide
- erreur de connexion réseau...

4. les scripts (notamment ceux SUID root) doivent vérifier que l'utilisateur ne peut pas effectuer une escalade de privilège en passant des paramètres corrompues ou malformés
5. les scripts devrnt être exécutables sans erreur sur une Debian 12 
