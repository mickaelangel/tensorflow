# Package TensorFlow Hors Ligne pour SUSE 15 SP7 - GPU A100

Ce package permet d'installer TensorFlow avec support GPU A100 sur un serveur SUSE 15 SP7 sans connexion Internet.

## Prérequis

### Sur la machine de téléchargement (avec Internet)
- **Windows**: Python 3.8+ et pip (voir `INSTRUCTIONS_WINDOWS.md` pour les détails)
- **Linux**: Python 3.8+ et pip
- Connexion Internet

### Sur le serveur SUSE 15 SP7 (sans Internet)
- SUSE Linux Enterprise Server 15 SP7 ou openSUSE Leap 15.x
- Python 3.8 ou supérieur
- pip3 installé
- Driver NVIDIA installé (version >= 525.60.13 pour A100)
- CUDA Toolkit 11.8 installé
- cuDNN 8.6 installé

## Étape 1: Téléchargement des packages (machine avec Internet)

1. Clonez ou téléchargez ce répertoire sur une machine avec Internet

2. Exécutez le script de téléchargement:
```bash
python3 download_tensorflow_offline.py
```

Ce script va:
- Créer un dossier `tensorflow_offline_packages` contenant tous les packages Python nécessaires
- Générer un fichier `requirements.txt` avec toutes les dépendances
- Créer un script d'installation pour SUSE

3. Vérifiez que le dossier `tensorflow_offline_packages` contient tous les fichiers `.whl` et `.tar.gz`

## Étape 2: Transfert vers le serveur SUSE

1. Compressez le dossier `tensorflow_offline_packages`:
```bash
tar -czf tensorflow_offline_packages.tar.gz tensorflow_offline_packages/
```

2. Transférez l'archive et le script `install_suse.sh` vers le serveur SUSE:
```bash
scp tensorflow_offline_packages.tar.gz install_suse.sh user@serveur-suse:/chemin/destination/
```

3. Sur le serveur SUSE, décompressez l'archive:
```bash
tar -xzf tensorflow_offline_packages.tar.gz
```

## Étape 3: Installation sur le serveur SUSE

### Préparation du système

1. Installez Python3 et pip3 si nécessaire:
```bash
sudo zypper install python3 python3-pip
```

2. Vérifiez que le driver NVIDIA est installé:
```bash
nvidia-smi
```

Si `nvidia-smi` n'est pas disponible, installez le driver:
```bash
sudo zypper install nvidia-computeG06
# ou la version appropriée pour votre système
```

3. Vérifiez que CUDA 11.8 est installé:
```bash
nvcc --version
```

Si CUDA n'est pas dans le PATH, configurez les variables d'environnement:
```bash
export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH
export CUDA_HOME=/usr/local/cuda-11.8
export PATH=/usr/local/cuda-11.8/bin:$PATH
```

Pour rendre ces variables permanentes, ajoutez-les à `~/.bashrc` ou `/etc/profile`.

### Installation de TensorFlow

1. Rendez le script d'installation exécutable:
```bash
chmod +x install_suse.sh
```

2. Exécutez le script d'installation:
```bash
./install_suse.sh
```

Le script va:
- Vérifier les prérequis système
- Installer tous les packages Python depuis le répertoire local
- Vérifier que TensorFlow est correctement installé

## Vérification de l'installation

1. Vérifiez la version de TensorFlow:
```bash
python3 -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"
```

2. Vérifiez que la GPU est détectée:
```bash
python3 -c "import tensorflow as tf; print('GPU disponibles:', tf.config.list_physical_devices('GPU'))"
```

3. Testez un calcul simple sur GPU:
```python
import tensorflow as tf

# Vérifier les GPU disponibles
print("GPU disponibles:", tf.config.list_physical_devices('GPU'))

# Créer un tenseur et le placer sur GPU
with tf.device('/GPU:0'):
    a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
    b = tf.constant([[1.0, 1.0], [0.0, 1.0]])
    c = tf.matmul(a, b)
    print("Résultat du calcul GPU:", c.numpy())
```

## Dépannage

### Erreur: "Could not load dynamic library 'libcudart.so.11.0'"
- Vérifiez que CUDA 11.8 est installé et dans le LD_LIBRARY_PATH
- Vérifiez: `ldconfig -p | grep cudart`

### Erreur: "Could not load dynamic library 'libcudnn.so.8'"
- Vérifiez que cuDNN 8.6 est installé
- Assurez-vous que les bibliothèques cuDNN sont dans le LD_LIBRARY_PATH

### Erreur: "No GPU devices found"
- Vérifiez avec `nvidia-smi` que la GPU est détectée
- Vérifiez que le driver NVIDIA est compatible avec l'A100
- Vérifiez les logs: `dmesg | grep -i nvidia`

### Erreur lors de l'installation pip
- Vérifiez que tous les fichiers `.whl` sont présents dans `tensorflow_offline_packages`
- Essayez d'installer manuellement: `pip3 install --no-index --find-links ./tensorflow_offline_packages tensorflow[and-cuda] --user`

## Structure des fichiers

```
.
├── download_tensorflow_offline.py  # Script de téléchargement (machine avec Internet)
├── install_suse.sh                 # Script d'installation (serveur SUSE)
├── README.md                       # Ce fichier
└── tensorflow_offline_packages/    # Dossier avec tous les packages (généré)
    ├── requirements.txt
    ├── install_offline.sh
    ├── gpu_config.txt
    └── [fichiers .whl et .tar.gz]
```

## Notes importantes

- **Version Python**: Assurez-vous que la version Python sur le serveur SUSE correspond à celle utilisée pour télécharger les packages
- **Architecture**: Les packages sont compilés pour l'architecture x86_64
- **CUDA**: TensorFlow avec support GPU nécessite CUDA 11.8 et cuDNN 8.6
- **Espace disque**: Le dossier `tensorflow_offline_packages` peut occuper plusieurs centaines de Mo

## Support

Pour plus d'informations sur TensorFlow et la GPU A100:
- Documentation TensorFlow: https://www.tensorflow.org/install/gpu
- Documentation NVIDIA A100: https://www.nvidia.com/en-us/data-center/a100/

