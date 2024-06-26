#!/bin/bash

sudo apt-get update

# Installation de Python 3
sudo apt-get install -y python3

# Installation des prérequis
sudo apt-get install -y rsyslog nftables
sudo apt-get install -y openssh-server

# Configuration de nftables
sudo nft add table inet filter
sudo nft add chain inet filter input { type filter hook input priority 0 \; }

echo "Installation et configuration terminées."
