# ⚙️ Configuration GPU A100

Guide de configuration optimale pour GPU NVIDIA A100.

## 🎯 Vue d'Ensemble

Le A100 est un GPU de centre de données avec :
- **80 GB HBM2** (ou 40 GB selon modèle)
- **Tensor Cores** (génération 3)
- **Multi-Instance GPU (MIG)**
- **Support FP64, TF32, FP16, INT8**

## 🔧 Configuration de Base

### Variables d'Environnement

Le script `gpu_a100_config.sh` configure automatiquement :

```bash
# Charger la configuration
source gpu_a100_config.sh
```

Contenu :
```bash
export CUDA_VERSION="11.8"
export CUDA_HOME="/usr/local/cuda-${CUDA_VERSION}"
export LD_LIBRARY_PATH="${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}"
export PATH="${CUDA_HOME}/bin:${PATH}"
export TF_FORCE_GPU_ALLOW_GROWTH="true"
export TF_GPU_THREAD_MODE="gpu_private"
```

## 🚀 Optimisations TensorFlow

### 1. Croissance Mémoire GPU

```python
import tensorflow as tf

gpus = tf.config.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
```

### 2. Mixed Precision (Tensor Cores)

```python
from tensorflow.keras import mixed_precision

policy = mixed_precision.Policy('mixed_float16')
mixed_precision.set_global_policy(policy)
```

**Bénéfices** :
- ✅ 2-3x plus rapide
- ✅ 50% moins de mémoire
- ✅ Utilise les Tensor Cores

### 3. XLA Compilation

```python
@tf.function(jit_compile=True)
def train_step(x, y):
    # Votre logique d'entraînement
    pass
```

**Bénéfices** :
- ✅ 20-30% plus rapide
- ✅ Optimisations automatiques

### 4. TF32 (Automatique sur A100)

Par défaut activé sur A100. Pour désactiver si nécessaire :

```python
tf.config.experimental.enable_tensor_float_32_execution(False)
```

## 🎮 Multi-GPU

### Configuration 2+ GPU

```python
strategy = tf.distribute.MirroredStrategy()

with strategy.scope():
    model = create_model()
    model.compile(...)
```

## 📊 Monitoring GPU

### Utilisation Mémoire

```bash
# En temps réel
watch -n 1 nvidia-smi

# Logs
nvidia-smi --query-gpu=timestamp,name,utilization.gpu,utilization.memory,memory.used,memory.free --format=csv -l 1
```

### Dans Python

```python
import tensorflow as tf

# Info GPU
gpus = tf.config.list_physical_devices('GPU')
for gpu in gpus:
    details = tf.config.experimental.get_device_details(gpu)
    print(f"GPU: {gpu.name}")
    print(f"Compute Capability: {details.get('compute_capability')}")
```

## 🔧 Configuration Avancée

### Limiter la Mémoire GPU

```python
gpus = tf.config.list_physical_devices('GPU')
tf.config.set_logical_device_configuration(
    gpus[0],
    [tf.config.LogicalDeviceConfiguration(memory_limit=40960)]  # 40 GB
)
```

### GPU Spécifique

```bash
# Utiliser seulement GPU 0
export CUDA_VISIBLE_DEVICES=0

# Utiliser GPU 0 et 1
export CUDA_VISIBLE_DEVICES=0,1
```

### Profiling

```python
# Activer le profiling
tf.profiler.experimental.start('logdir')

# Votre code ici

tf.profiler.experimental.stop()
```

## 📈 Benchmarks Typiques

### ResNet-50 (Batch 32)
- **FP32** : ~300 images/sec
- **Mixed Precision** : ~900 images/sec

### BERT-base (Seq 128)
- **FP32** : ~40 seq/sec
- **Mixed Precision** : ~120 seq/sec

### Matmul 8K×8K
- **FP32** : ~3.5 TFLOPS
- **FP16** : ~10 TFLOPS (Tensor Cores)
- **TF32** : ~6 TFLOPS (Tensor Cores)

## 🐛 Dépannage

### GPU non utilisé

```python
# Vérifier placement
tf.debugging.set_log_device_placement(True)
```

### Out of Memory

```python
# Activer croissance mémoire
for gpu in tf.config.list_physical_devices('GPU'):
    tf.config.experimental.set_memory_growth(gpu, True)
```

### Performances faibles

```python
# Activer toutes optimisations
from tensorflow.keras import mixed_precision
mixed_precision.set_global_policy('mixed_float16')

@tf.function(jit_compile=True)
def optimized_function(x):
    return x * x
```

## 📚 Ressources

- [NVIDIA A100 Datasheet](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/nvidia-a100-datasheet-us-nvidia-1758950-r4-web.pdf)
- [TensorFlow GPU Guide](https://www.tensorflow.org/guide/gpu)
- [Mixed Precision Guide](https://www.tensorflow.org/guide/mixed_precision)

---

**Auteur** : Mickael Angel  
**Dernière mise à jour** : Décembre 2025

