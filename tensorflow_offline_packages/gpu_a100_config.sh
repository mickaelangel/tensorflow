#!/bin/bash
# Configuration des variables d'environnement pour GPU A100 sur SUSE 15 SP7
# Sourcez ce fichier ou ajoutez-le à votre ~/.bashrc

# Version CUDA pour A100 (recommandée: 11.8)
export CUDA_VERSION="11.8"

# Chemins CUDA (ajustez selon votre installation)
export CUDA_HOME="/usr/local/cuda-${CUDA_VERSION}"
export CUDA_PATH="${CUDA_HOME}"

# Bibliothèques CUDA
export LD_LIBRARY_PATH="${CUDA_HOME}/lib64:${CUDA_HOME}/extras/CUPTI/lib64:${LD_LIBRARY_PATH}"

# Binaires CUDA
export PATH="${CUDA_HOME}/bin:${PATH}"

# Configuration TensorFlow pour GPU
export TF_FORCE_GPU_ALLOW_GROWTH="true"
export TF_GPU_THREAD_MODE="gpu_private"

# Optimisations spécifiques A100
# Utilisez les Tensor Cores (TF32) - activé par défaut sur A100
export NVIDIA_TF32_OVERRIDE="0"  # 0 = activé (défaut), 1 = désactivé

# Multi-Instance GPU (MIG) - si configuré
# export CUDA_VISIBLE_DEVICES="0"  # Décommentez pour spécifier une GPU spécifique

echo "Configuration GPU A100 chargée:"
echo "  CUDA_HOME: $CUDA_HOME"
echo "  LD_LIBRARY_PATH: $LD_LIBRARY_PATH"
echo "  TF_FORCE_GPU_ALLOW_GROWTH: $TF_FORCE_GPU_ALLOW_GROWTH"

