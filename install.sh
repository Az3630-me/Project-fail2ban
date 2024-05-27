#!/bin/bash

sudo apt-get update

# Installation des prérequis
sudo apt-get install -y rsyslog nftables

# Configuration de nftables
sudo nft add table inet filter
sudo nft add chain inet filter input { type filter hook input priority 0 \; }

echo "Installation et configuration terminées."
