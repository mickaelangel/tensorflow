# Guide de Compilation - Package TensorFlow Offline

Guide pour créer votre propre package d'installation offline de TensorFlow pour SUSE 15 SP7.

## 🎯 Vue d'Ensemble

Ce guide explique comment :
- Télécharger tous les packages nécessaires
- Créer une archive complète
- Préparer le package pour installation offline

## 🖥️ Prérequis

### Sur la Machine de Téléchargement

**Windows** :
- Python 3.8+ installé
- pip installé
- Connexion Internet
- 5-10 GB d'espace disque libre

**Linux** :
- Python 3.8+ installé
- pip installé
- Connexion Internet
- 5-10 GB d'espace disque libre

## 📥 Méthode 1 : Utiliser les Scripts Fournis

### Sur Windows

```bash
# 1. Télécharger tous les packages
python download_tensorflow_offline.py

# 2. Télécharger TensorFlow depuis GitHub
cd tensorflow_offline_packages
curl -L -o tensorflow-2.20.0.tar.gz https://github.com/tensorflow/tensorflow/archive/refs/tags/v2.20.0.tar.gz

# 3. Vérifier les dépendances
cd ..
python verifier_dependances.py

# 4. Créer l'archive
tar -czf tensorflow_suse15sp7_a100_FINAL.tar.gz tensorflow_offline_packages/
```

### Sur Linux (Ubuntu/Debian)

```bash
# 1. Cloner ce dépôt
git clone https://github.com/mickaelangel/tensorflow.git
cd tensorflow

# 2. Télécharger les packages
python3 download_tensorflow_offline.py

# 3. Télécharger TensorFlow source
cd tensorflow_offline_packages
wget https://github.com/tensorflow/tensorflow/archive/refs/tags/v2.20.0.tar.gz -O tensorflow-2.20.0.tar.gz

# 4. Créer l'archive
cd ..
tar -czf tensorflow_suse15sp7_a100_FINAL.tar.gz tensorflow_offline_packages/
```

## 📥 Méthode 2 : Téléchargement Manuel

### Étape 1 : Créer la Structure

```bash
mkdir -p tensorflow_offline_packages
cd tensorflow_offline_packages
```

### Étape 2 : Télécharger TensorFlow

```bash
# Depuis GitHub (source complète)
curl -L -o tensorflow-2.20.0.tar.gz https://github.com/tensorflow/tensorflow/archive/refs/tags/v2.20.0.tar.gz

# Vérifier la taille (doit être ~80 MB)
ls -lh tensorflow-2.20.0.tar.gz
```

### Étape 3 : Télécharger les Dépendances

**Option A : Avec pip download** :
```bash
# Créer fichier requirements.txt
cat > requirements.txt << EOF
numpy>=1.24.0
protobuf>=3.20.0
grpcio>=1.50.0
absl-py>=1.0.0
astunparse>=1.6.3
flatbuffers>=23.1.21
gast>=0.4.0
google-pasta>=0.2.0
h5py>=3.8.0
keras>=2.13.0
libclang>=13.0.0
opt-einsum>=3.3.0
packaging>=20.0
setuptools>=65.0.0
six>=1.15.0
tensorboard>=2.13.0
tensorflow-estimator>=2.13.0
termcolor>=2.0.0
typing-extensions>=4.0.0
wrapt>=1.14.0
wheel>=0.38.0
EOF

# Télécharger toutes les dépendances en source
pip download -r requirements.txt -d . --no-binary :all: --no-deps
```

**Option B : Téléchargement individuel** :

```bash
# Pour chaque package
pip download numpy -d . --no-binary :all: --no-deps
pip download protobuf -d . --no-binary :all: --no-deps
pip download grpcio -d . --no-binary :all: --no-deps
# ... etc
```

### Étape 4 : Copier les Scripts

```bash
# Copier les scripts d'installation
cp ../install_suse.sh .
cp ../deploy.sh .
cp ../gpu_a100_config.sh .
cp ../test_tensorflow_gpu.py .
```

### Étape 5 : Créer l'Archive

```bash
cd ..
tar -czf tensorflow_suse15sp7_a100_FINAL.tar.gz tensorflow_offline_packages/

# Vérifier la taille finale
ls -lh tensorflow_suse15sp7_a100_FINAL.tar.gz
```

## 📦 Versions Recommandées

| Package | Version Recommandée | Notes |
|---------|-------------------|-------|
| TensorFlow | 2.20.0 ou 2.13.0 | 2.20.0 plus récent, 2.13.0 plus stable |
| Python | 3.11 | Meilleur support |
| CUDA | 11.8 | Requis pour A100 |
| cuDNN | 8.6 | Requis pour A100 |

## 🔧 Personnalisation du Package

### Modifier les Versions

Éditez `requirements.txt` pour spécifier des versions précises :

```txt
tensorflow==2.13.0
numpy==1.24.3
protobuf==4.24.0
# etc.
```

### Ajouter des Packages Supplémentaires

```bash
# Ajouter scikit-learn
pip download scikit-learn -d tensorflow_offline_packages/ --no-binary :all: --no-deps

# Ajouter matplotlib
pip download matplotlib -d tensorflow_offline_packages/ --no-binary :all: --no-deps
```

### Créer un Package Minimal

Pour un package plus léger (sans CUDA) :

```bash
# Télécharger TensorFlow CPU uniquement
pip download tensorflow-cpu -d tensorflow_offline_packages/ --no-deps

# Exclure les packages GPU
# Ne pas inclure tensorboard, keras si non nécessaires
```

## 🧪 Tester le Package

### Avant de Créer l'Archive

```bash
# Lister les fichiers
ls -lh tensorflow_offline_packages/

# Compter les packages
ls tensorflow_offline_packages/*.tar.gz | wc -l

# Vérifier les tailles
du -sh tensorflow_offline_packages/
```

### Test d'Installation Locale

```bash
# Créer un environnement virtuel de test
python3 -m venv test_env
source test_env/bin/activate

# Tester l'installation
pip install --no-index --find-links tensorflow_offline_packages/ tensorflow

# Vérifier
python -c "import tensorflow as tf; print(tf.__version__)"

# Nettoyer
deactivate
rm -rf test_env
```

## 📊 Taille du Package

**Tailles typiques** :

| Contenu | Taille |
|---------|--------|
| TensorFlow source | ~80 MB |
| Dépendances sources | ~100-200 MB |
| Scripts et docs | ~1 MB |
| **Total (compressé)** | **~2-2.5 GB** |

## 🔄 Mises à Jour

### Mettre à Jour le Package

```bash
# 1. Supprimer les anciens packages
rm tensorflow_offline_packages/*.tar.gz
rm tensorflow_offline_packages/*.whl

# 2. Télécharger les nouvelles versions
python download_tensorflow_offline.py

# 3. Recréer l'archive
tar -czf tensorflow_suse15sp7_a100_FINAL.tar.gz tensorflow_offline_packages/
```

## ⚠️ Problèmes Courants

### Erreur : "No matching distribution found"

**Cause** : Package n'a pas de version source sur PyPI

**Solution** :
```bash
# Essayer sans --no-binary
pip download package_name -d tensorflow_offline_packages/

# OU télécharger depuis GitHub
wget https://github.com/user/repo/archive/refs/tags/vX.Y.Z.tar.gz
```

### Package Trop Volumineux

**Solution** :
- Exclure les packages optionnels (tensorboard, keras si non utilisés)
- Télécharger uniquement les wheels au lieu des sources
- Créer plusieurs archives plus petites

### Versions Incompatibles

**Solution** :
```bash
# Spécifier les versions exactes
pip download tensorflow==2.13.0 numpy==1.24.3 -d .
```

## 🚀 Automatisation

### Script de Build Complet

```bash
#!/bin/bash
# build_package.sh

set -e

echo "Construction du package TensorFlow offline..."

# Nettoyer
rm -rf tensorflow_offline_packages
mkdir tensorflow_offline_packages

# Télécharger
python3 download_tensorflow_offline.py

# TensorFlow source
cd tensorflow_offline_packages
curl -L -o tensorflow-2.20.0.tar.gz \
  https://github.com/tensorflow/tensorflow/archive/refs/tags/v2.20.0.tar.gz
cd ..

# Copier scripts
cp install_suse.sh tensorflow_offline_packages/
cp deploy.sh tensorflow_offline_packages/
cp gpu_a100_config.sh tensorflow_offline_packages/
cp test_tensorflow_gpu.py tensorflow_offline_packages/

# Créer archive
tar -czf tensorflow_suse15sp7_a100_FINAL.tar.gz tensorflow_offline_packages/

echo "✅ Package créé: tensorflow_suse15sp7_a100_FINAL.tar.gz"
ls -lh tensorflow_suse15sp7_a100_FINAL.tar.gz
```

## 📝 Checklist de Build

Avant de finaliser le package :

- [ ] TensorFlow source téléchargé (> 50 MB)
- [ ] Toutes les dépendances présentes
- [ ] Scripts d'installation copiés
- [ ] README.md inclus
- [ ] requirements.txt à jour
- [ ] Archive créée
- [ ] Taille vérifiée (~2 GB)
- [ ] Test d'installation effectué

## 🔗 Ressources

- [PyPI TensorFlow](https://pypi.org/project/tensorflow/)
- [TensorFlow GitHub](https://github.com/tensorflow/tensorflow)
- [pip documentation](https://pip.pypa.io/en/stable/)

---

**Auteur** : Mickael Angel  
**Version** : 1.0.0  
**Dernière mise à jour** : Décembre 2025

