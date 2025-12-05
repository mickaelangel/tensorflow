# Installation Guide

## Table of Contents
- [Prerequisites](#prerequisites)
- [Step-by-Step Installation](#step-by-step-installation)
- [Post-Installation Verification](#post-installation-verification)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Hardware Requirements
- **CPU**: x86_64 architecture
- **GPU**: NVIDIA A100 (or compatible)
- **RAM**: Minimum 16 GB, recommended 32 GB+
- **Disk**: 15 GB free space minimum

### Software Requirements

#### SUSE 15 SP7
```bash
# Verify SUSE version
cat /etc/os-release
```

#### Python 3.8-3.11
```bash
# Check Python version
python3 --version

# If Python 3.11 is not installed
sudo zypper install python311 python311-pip python311-devel
```

#### Compilation Tools
```bash
sudo zypper install -y gcc gcc-c++ make cmake python3-devel
```

#### NVIDIA Driver
```bash
# Check driver
nvidia-smi

# If not installed
sudo zypper install nvidia-computeG06
```

#### CUDA 11.8
```bash
# Check CUDA
nvcc --version

# Configure environment variables
export CUDA_HOME=/usr/local/cuda-11.8
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
export PATH=$CUDA_HOME/bin:$PATH

# Make permanent
echo 'export CUDA_HOME=/usr/local/cuda-11.8' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
echo 'export PATH=$CUDA_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

#### cuDNN 8.6
Ensure cuDNN 8.6 is installed in `/usr/local/cuda-11.8/`

## Step-by-Step Installation

### 1. Transfer the Package

**Option A: USB Transfer**
```bash
# Mount USB
sudo mount /dev/sdb1 /mnt/usb

# Copy package
cp /mnt/usb/tensorflow_suse15sp7_a100_FINAL.tar.gz /tmp/

# Unmount
sudo umount /mnt/usb
```

**Option B: SCP Transfer**
```bash
scp tensorflow_suse15sp7_a100_FINAL.tar.gz user@suse-server:/tmp/
```

### 2. Extract the Package

```bash
cd /tmp
tar -xzf tensorflow_suse15sp7_a100_FINAL.tar.gz
cd tensorflow_offline_packages
```

### 3. Verify Contents

```bash
# List source packages
ls -lh *.tar.gz

# Check scripts
ls -lh *.sh

# Verify requirements
cat requirements.txt
```

### 4. Run Installation

**Quick Installation (Recommended)**:
```bash
chmod +x deploy.sh install_suse.sh gpu_a100_config.sh
./deploy.sh
```

**Manual Installation**:
```bash
# Load GPU configuration
source gpu_a100_config.sh

# Run installation script
chmod +x install_suse.sh
./install_suse.sh
```

### 5. Installation Process

The installation will:
1. Verify system prerequisites
2. Check NVIDIA driver and CUDA
3. Install Python packages from source
4. Compile TensorFlow (15-45 minutes)
5. Configure GPU settings
6. Run verification tests

## Post-Installation Verification

### Basic Verification

```bash
# Test TensorFlow import
python3 -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"

# Expected output: TensorFlow version: 2.20.0
```

### GPU Detection

```bash
# Check GPU availability
python3 -c "import tensorflow as tf; print('GPUs:', tf.config.list_physical_devices('GPU'))"

# Expected output: GPUs: [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
```

### Comprehensive Test

```bash
# Run full test suite
python3 test_tensorflow_gpu.py
```

Expected output:
```
============================================================
Test d'installation TensorFlow pour GPU A100
============================================================
✓ TensorFlow importé avec succès
  Version: 2.20.0

=== Détection des GPU ===
✓ 1 GPU détectée(s):
  GPU 0: /physical_device:GPU:0

=== Fonctionnalités TensorFlow ===
✓ CUDA version: 11.8
✓ cuDNN version: 8.6
  Built with CUDA: True
  Built with GPU support: True

=== Test de calcul sur GPU ===
✓ Calcul sur GPU réussi
  Résultat:
[[22. 28.]
 [49. 64.]]

============================================================
✓ Tous les tests sont passés avec succès!
  TensorFlow est correctement configuré pour utiliser la GPU A100
============================================================
```

## Configuration

### GPU Memory Growth

```python
import tensorflow as tf

# Enable memory growth
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
```

### Mixed Precision

```python
from tensorflow.keras import mixed_precision

# Enable mixed precision for A100 Tensor Cores
policy = mixed_precision.Policy('mixed_float16')
mixed_precision.set_global_policy(policy)
```

### Multi-GPU Strategy

```python
strategy = tf.distribute.MirroredStrategy()

with strategy.scope():
    # Build and compile model here
    model = create_model()
    model.compile(...)
```

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

---

**Author**: Mickael Angel  
**Last Updated**: December 2025

