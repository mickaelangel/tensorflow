#!/bin/bash
# Script d'installation complète de TensorFlow pour SUSE 15 SP7 avec GPU A100
# Ce script doit être exécuté sur le serveur SUSE cible

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$SCRIPT_DIR/tensorflow_offline_packages"

echo "=========================================="
echo "Installation TensorFlow pour SUSE 15 SP7"
echo "GPU: NVIDIA A100"
echo "=========================================="

# Vérifier que nous sommes sur SUSE
if [ ! -f /etc/os-release ]; then
    echo "Erreur: Impossible de détecter la distribution"
    exit 1
fi

source /etc/os-release
if [[ "$ID" != "sles" && "$ID" != "opensuse-leap" ]]; then
    echo "Attention: Ce script est conçu pour SUSE Linux Enterprise Server ou openSUSE Leap"
    read -p "Continuer quand même? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Vérifier les privilèges root pour certaines opérations
if [ "$EUID" -ne 0 ]; then
    echo "Attention: Certaines opérations nécessitent les privilèges root"
    echo "Vous devrez peut-être exécuter certaines commandes avec sudo"
fi

# Vérifier Python3
if ! command -v python3 &> /dev/null; then
    echo "Python3 n'est pas installé. Installation..."
    sudo zypper install -y python3 python3-pip
fi

# Vérifier pip3
if ! command -v pip3 &> /dev/null; then
    echo "pip3 n'est pas installé. Installation..."
    sudo zypper install -y python3-pip
fi

# Vérifier la GPU NVIDIA
echo ""
echo "=== Vérification de la GPU NVIDIA ==="
if command -v nvidia-smi &> /dev/null; then
    echo "Driver NVIDIA détecté:"
    nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
else
    echo "ATTENTION: nvidia-smi n'est pas disponible"
    echo "Assurez-vous que le driver NVIDIA est installé"
    echo "Pour installer: zypper install nvidia-computeG06 (ou version appropriée)"
fi

# Vérifier CUDA
echo ""
echo "=== Vérification de CUDA ==="
if command -v nvcc &> /dev/null; then
    echo "CUDA détecté:"
    nvcc --version
else
    echo "ATTENTION: CUDA n'est pas détecté dans le PATH"
    echo "Assurez-vous que CUDA 11.8 est installé"
    echo "Vous pouvez définir les variables d'environnement:"
    echo "  export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:\$LD_LIBRARY_PATH"
    echo "  export CUDA_HOME=/usr/local/cuda-11.8"
    echo "  export PATH=/usr/local/cuda-11.8/bin:\$PATH"
fi

# Vérifier que le répertoire des packages existe
if [ ! -d "$PACKAGE_DIR" ]; then
    echo "Erreur: Répertoire des packages introuvable: $PACKAGE_DIR"
    echo "Assurez-vous d'avoir copié le dossier tensorflow_offline_packages"
    exit 1
fi

# Installer les packages Python
echo ""
echo "=== Installation des packages Python ==="
echo "Répertoire des packages: $PACKAGE_DIR"

# Mettre à jour pip
python3 -m pip install --upgrade pip --no-index --find-links "$PACKAGE_DIR" || true

# Installer depuis le répertoire local
if [ -f "$PACKAGE_DIR/requirements.txt" ]; then
    echo "Installation depuis requirements.txt..."
    pip3 install --no-index --find-links "$PACKAGE_DIR" -r "$PACKAGE_DIR/requirements.txt" --user
else
    echo "Installation de tous les packages dans le répertoire..."
    pip3 install --no-index --find-links "$PACKAGE_DIR" tensorflow[and-cuda] --user
fi

# Vérifier l'installation
echo ""
echo "=== Vérification de l'installation ==="
python3 -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)" 2>/dev/null && {
    echo "TensorFlow installé avec succès!"
    echo ""
    echo "Test de détection GPU:"
    python3 -c "import tensorflow as tf; gpus = tf.config.list_physical_devices('GPU'); print('GPU détectées:', len(gpus)); [print(f'  - {gpu}') for gpu in gpus]" 2>/dev/null || echo "  (Vérifiez la configuration CUDA)"
} || {
    echo "Erreur lors de la vérification de TensorFlow"
    exit 1
}

echo ""
echo "=========================================="
echo "Installation terminée!"
echo "=========================================="
echo ""
echo "Pour tester TensorFlow:"
echo "  python3 -c \"import tensorflow as tf; print(tf.__version__)\""
echo ""
echo "Pour tester la GPU:"
echo "  python3 -c \"import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))\""
echo ""

