# Package d'Installation Hors Ligne TensorFlow pour SUSE 15 SP7

[![Licence](https://img.shields.io/badge/licence-MIT-blue.svg)](LICENSE)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20.0-orange.svg)](https://www.tensorflow.org/)
[![Python](https://img.shields.io/badge/Python-3.8--3.11-blue.svg)](https://www.python.org/)
[![CUDA](https://img.shields.io/badge/CUDA-11.8-green.svg)](https://developer.nvidia.com/cuda-toolkit)

> **Package complet d'installation hors ligne pour TensorFlow avec support GPU A100 sur SUSE Linux Enterprise Server 15 SP7**

[English](README.md) | [Français](README.fr.md)

## 📋 Vue d'Ensemble

Ce dépôt contient un package complet et prêt à déployer pour installer TensorFlow avec accélération GPU sur des systèmes SUSE 15 SP7 isolés (sans connexion Internet). Conçu pour les environnements d'entreprise nécessitant des installations sécurisées et hors ligne avec support GPU NVIDIA A100.

## ✨ Fonctionnalités

- **🔒 Entièrement Hors Ligne** : Aucune connexion Internet requise sur le système cible
- **🚀 Optimisé GPU** : Configuré pour NVIDIA A100 avec CUDA 11.8 et cuDNN 8.6
- **📦 Package Complet** : Toutes les dépendances incluses en fichiers sources
- **🛠️ Installation Automatisée** : Scripts de déploiement simples
- **✅ Testé et Vérifié** : Configuration prête pour la production
- **📊 Surveillance des Performances** : TensorBoard et outils de test intégrés

## 🎯 Environnement Cible

- **OS** : SUSE Linux Enterprise Server 15 SP7
- **GPU** : NVIDIA A100
- **Python** : 3.8, 3.9, 3.10 ou 3.11
- **CUDA** : 11.8
- **cuDNN** : 8.6

## 📦 Contenu du Package

### Composants Principaux
- **TensorFlow 2.20.0** (source)
- **29 packages de dépendances** (tous en fichiers sources .tar.gz)
- **Scripts d'installation** (déploiement automatisé)
- **Configuration GPU** (optimisée pour A100)
- **Suite de tests** (outils de validation)

### Structure du Package
```
tensorflow_offline_packages/
├── install_suse.sh              # Script d'installation principal
├── deploy.sh                    # Script de déploiement rapide
├── gpu_a100_config.sh           # Configuration GPU A100
├── test_tensorflow_gpu.py       # Script de test GPU
├── requirements.txt             # Liste des dépendances
├── README.md                    # Documentation du package
└── [packages sources]           # Tous les fichiers .tar.gz
```

## 🚀 Démarrage Rapide

### Prérequis sur le Système Cible

```bash
# Installer les outils de compilation
sudo zypper install -y gcc gcc-c++ python3-devel make cmake

# Vérifier la version Python (doit être 3.8-3.11)
python3 --version

# Vérifier le driver NVIDIA
nvidia-smi

# Vérifier CUDA 11.8
nvcc --version
```

### Étapes d'Installation

1. **Transférer le package** sur votre système SUSE 15 SP7 (USB, SCP ou réseau)

2. **Extraire l'archive** :
```bash
cd /tmp
tar -xzf tensorflow_suse15sp7_a100_FINAL.tar.gz
cd tensorflow_offline_packages
```

3. **Lancer le script de déploiement** :
```bash
chmod +x deploy.sh install_suse.sh gpu_a100_config.sh
./deploy.sh
```

4. **Vérifier l'installation** :
```bash
python3 -c "import tensorflow as tf; print('TensorFlow:', tf.__version__)"
python3 -c "import tensorflow as tf; print('GPUs:', tf.config.list_physical_devices('GPU'))"
python3 test_tensorflow_gpu.py
```

## 📖 Documentation Détaillée

### Guide d'Installation
Voir [INSTALLATION.fr.md](INSTALLATION.fr.md) pour les instructions détaillées.

### Dépannage
Voir [TROUBLESHOOTING.fr.md](TROUBLESHOOTING.fr.md) pour les problèmes courants et solutions.

### Configuration
Voir [CONFIGURATION.fr.md](CONFIGURATION.fr.md) pour les options de configuration avancées.

## 🔧 Exigences Système

### Exigences Minimales
- **Espace Disque** : 15 GB libre
- **RAM** : 16 GB
- **Python** : 3.8+
- **GCC** : 7.0+

### Exigences Recommandées
- **Espace Disque** : 50 GB libre
- **RAM** : 32 GB+
- **Python** : 3.11
- **GCC** : 11.0+

## 🎯 Optimisation des Performances

Le package inclut des optimisations pour :
- **Mixed Precision Training** : Utilisation des Tensor Cores A100
- **Compilation XLA** : Accelerated Linear Algebra
- **Support Multi-GPU** : Capacités d'entraînement distribué
- **Optimisation Mémoire** : Gestion efficace de la mémoire

## 📊 Benchmarks

Performances attendues sur NVIDIA A100 :
- **Classification d'Images (ResNet-50)** : ~900 images/sec
- **Détection d'Objets (YOLOv5)** : ~60 FPS
- **Modèle de Langage (BERT-base)** : ~120 séquences/sec
- **Mixed Precision** : Accélération 2-3x par rapport à FP32

## 🛠️ Compiler depuis la Source

Pour créer votre propre package hors ligne :

```bash
# Sur une machine avec accès Internet
python download_packages.py

# Créer l'archive
tar -czf tensorflow_suse15sp7_a100_FINAL.tar.gz tensorflow_offline_packages/
```

Voir [BUILD.fr.md](BUILD.fr.md) pour les instructions de compilation détaillées.

## 🧪 Tests

Exécuter la suite de tests complète :

```bash
# Test de fonctionnalité de base
python3 test_tensorflow_gpu.py

# Benchmark de performance
python3 benchmark_gpu.py

# Test d'entraînement de modèle
python3 test_training.py
```

## 📚 Exemples

Consultez le répertoire `examples/` pour :
- Classification d'images avec CNN
- Détection d'objets avec YOLO
- Traitement du langage naturel avec Transformers
- Prévision de séries temporelles
- Apprentissage par renforcement

## 🤝 Contribuer

Ceci est un dépôt de package de déploiement. Pour les contributions à TensorFlow lui-même, visitez le [dépôt officiel TensorFlow](https://github.com/tensorflow/tensorflow).

Pour contribuer à ce projet, voir [CONTRIBUTING.fr.md](CONTRIBUTING.fr.md).

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

TensorFlow est sous licence Apache License 2.0.

## 👤 Auteur

**Mickael Angel**
- GitHub : [@mickaelangel](https://github.com/mickaelangel)
- Projet : Package d'Installation Hors Ligne TensorFlow

## 🙏 Remerciements

- L'équipe Google TensorFlow pour le framework extraordinaire
- NVIDIA pour le support GPU et l'optimisation
- SUSE pour l'excellente distribution Linux d'entreprise
- La communauté open-source pour les améliorations continues

## 📞 Support

Pour les problèmes et questions :
1. Consulter [TROUBLESHOOTING.fr.md](TROUBLESHOOTING.fr.md)
2. Consulter les [issues fermées](https://github.com/mickaelangel/tensorflow/issues?q=is%3Aissue+is%3Aclosed)
3. Ouvrir une [nouvelle issue](https://github.com/mickaelangel/tensorflow/issues/new)

## 🔄 Mises à Jour

Consulter [CHANGELOG.fr.md](CHANGELOG.fr.md) pour l'historique des versions et mises à jour.

## ⚠️ Notes Importantes

- Ce package est conçu pour les environnements **hors ligne/isolés**
- Assurez-vous que **CUDA 11.8** et **cuDNN 8.6** sont installés avant le déploiement
- La compilation peut prendre **15-45 minutes** selon les ressources système
- Testé sur **SUSE 15 SP7** - compatibilité avec d'autres versions non garantie

## 🌟 Feuille de Route

- [ ] Support pour TensorFlow 2.21+
- [ ] Support GPU AMD ROCm
- [ ] Configuration d'entraînement multi-nœuds
- [ ] Déploiement conteneurisé Docker
- [ ] Templates d'orchestration Kubernetes

---

**Fait avec ❤️ pour la communauté ML/AI**

*Dernière mise à jour : Décembre 2025*

