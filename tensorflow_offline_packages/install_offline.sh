#!/bin/bash
# Script d'installation hors ligne de TensorFlow pour SUSE 15 SP7 avec GPU A100

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$SCRIPT_DIR"

echo "=== Installation hors ligne de TensorFlow ==="
echo "Répertoire des packages: $PACKAGE_DIR"

# Vérifier que pip est installé
if ! command -v pip3 &> /dev/null; then
    echo "Erreur: pip3 n'est pas installé"
    echo "Installez pip3 avec: zypper install python3-pip"
    exit 1
fi

# Installer les packages depuis le répertoire local
echo "Installation des packages Python..."
pip3 install --no-index --find-links "$PACKAGE_DIR" -r "$PACKAGE_DIR/requirements.txt"

echo ""
echo "=== Installation terminée ==="
echo "Vérifiez l'installation avec: python3 -c 'import tensorflow as tf; print(tf.__version__)'"
