# 🚀 Guide de Démarrage Rapide

Installation de TensorFlow en moins de 10 minutes sur SUSE 15 SP7.

## ⚡ Installation Express

### Étape 1 : Prérequis (2 minutes)

```bash
# Installer les outils de compilation
sudo zypper install -y gcc gcc-c++ python3-devel make cmake

# Vérifier Python
python3 --version  # Doit afficher 3.8-3.11
```

### Étape 2 : Extraction (1 minute)

```bash
cd /tmp
tar -xzf tensorflow_suse15sp7_a100_FINAL.tar.gz
cd tensorflow_offline_packages
```

### Étape 3 : Installation (5-30 minutes)

```bash
chmod +x deploy.sh
./deploy.sh
```

Le script va :
- ✅ Vérifier les prérequis
- ✅ Installer TensorFlow
- ✅ Configurer le GPU
- ✅ Tester l'installation

### Étape 4 : Vérification (1 minute)

```bash
python3 -c "import tensorflow as tf; print(tf.__version__)"
python3 test_tensorflow_gpu.py
```

## ✅ Premier Test

Créez un fichier `test.py` :

```python
import tensorflow as tf

# Vérifier les GPU
print("GPUs disponibles:", tf.config.list_physical_devices('GPU'))

# Test simple
with tf.device('/GPU:0'):
    a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
    b = tf.constant([[1.0, 1.0], [0.0, 1.0]])
    c = tf.matmul(a, b)
    print("Résultat:", c.numpy())
```

Exécutez :
```bash
python3 test.py
```

## 🎯 Résultat Attendu

```
GPUs disponibles: [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
Résultat: [[1. 3.]
 [3. 7.]]
```

## ⚠️ Problèmes Courants

### GPU non détecté
```bash
# Vérifier le driver
nvidia-smi

# Configurer CUDA
export CUDA_HOME=/usr/local/cuda-11.8
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
```

### ImportError
```bash
# Vérifier l'installation
pip3 list | grep tensorflow

# Réinstaller si nécessaire
./install_suse.sh
```

## 📚 Prochaines Étapes

- [Configuration Avancée](Configuration-Avancee)
- [Optimisation Performances](Optimisation-Performances)
- [Premier Modèle](Premier-Modele)

---

**Temps total : ~10-35 minutes**

