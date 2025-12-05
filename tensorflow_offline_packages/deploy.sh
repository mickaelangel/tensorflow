#!/bin/bash
# Script de déploiement rapide
# Exécute toutes les étapes nécessaires pour installer TensorFlow

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Déploiement de TensorFlow sur SUSE 15 SP7"
echo "=========================================="

# Charger la configuration GPU
if [ -f "$SCRIPT_DIR/gpu_a100_config.sh" ]; then
    source "$SCRIPT_DIR/gpu_a100_config.sh"
fi

# Exécuter l'installation
bash "$SCRIPT_DIR/install_suse.sh"

# Tester l'installation
echo ""
echo "Test de l'installation..."
python3 "$SCRIPT_DIR/test_tensorflow_gpu.py"

echo ""
echo "Déploiement terminé!"
