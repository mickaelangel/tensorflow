# Configuration TensorFlow pour SUSE 15 SP7 avec GPU A100

Guide de configuration avancée pour optimiser TensorFlow sur NVIDIA A100.

## 🎯 Configuration GPU de Base

### Variables d'Environnement CUDA

```bash
# Configuration CUDA 11.8
export CUDA_HOME=/usr/local/cuda-11.8
export CUDA_PATH=${CUDA_HOME}
export LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${CUDA_HOME}/extras/CUPTI/lib64:${LD_LIBRARY_PATH}
export PATH=${CUDA_HOME}/bin:${PATH}

# Rendre permanent
echo 'export CUDA_HOME=/usr/local/cuda-11.8' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}' >> ~/.bashrc
echo 'export PATH=${CUDA_HOME}/bin:${PATH}' >> ~/.bashrc
source ~/.bashrc
```

### Configuration TensorFlow

```bash
# Croissance mémoire GPU
export TF_FORCE_GPU_ALLOW_GROWTH=true

# Mode threading GPU
export TF_GPU_THREAD_MODE=gpu_private

# Désactiver les warnings
export TF_CPP_MIN_LOG_LEVEL=2
```

## 🚀 Optimisations Python

### 1. Croissance Mémoire GPU

```python
import tensorflow as tf

# Activer la croissance mémoire pour éviter l'allocation complète
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"Croissance mémoire activée pour {len(gpus)} GPU(s)")
    except RuntimeError as e:
        print(f"Erreur: {e}")
```

### 2. Limiter la Mémoire GPU

```python
import tensorflow as tf

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    # Limiter à 40 GB (pour A100 80GB)
    tf.config.set_logical_device_configuration(
        gpus[0],
        [tf.config.LogicalDeviceConfiguration(memory_limit=40960)]
    )
```

### 3. Mixed Precision Training (Tensor Cores)

```python
from tensorflow.keras import mixed_precision

# Activer mixed precision pour utiliser les Tensor Cores
policy = mixed_precision.Policy('mixed_float16')
mixed_precision.set_global_policy(policy)

print(f'Politique de calcul: {policy}')
print(f'Compute dtype: {policy.compute_dtype}')
print(f'Variable dtype: {policy.variable_dtype}')
```

**Avantages** :
- ✅ 2-3x plus rapide sur A100
- ✅ 50% de mémoire en moins
- ✅ Utilise les Tensor Cores

### 4. XLA Compilation

```python
import tensorflow as tf

# Activer XLA globalement
tf.config.optimizer.set_jit(True)

# Ou pour une fonction spécifique
@tf.function(jit_compile=True)
def train_step(x, y):
    with tf.GradientTape() as tape:
        predictions = model(x, training=True)
        loss = loss_fn(y, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss
```

**Avantages** :
- ✅ 20-30% plus rapide
- ✅ Optimisations automatiques
- ✅ Fusion d'opérations

### 5. TF32 (Automatique sur A100)

```python
import tensorflow as tf

# TF32 est activé par défaut sur A100
# Pour vérifier ou désactiver si nécessaire
print(f"TF32 activé: {tf.config.experimental.tensor_float_32_execution_enabled()}")

# Désactiver si besoin de précision maximale
# tf.config.experimental.enable_tensor_float_32_execution(False)
```

## 🎮 Configuration Multi-GPU

### Stratégie Mirrored (GPU multiples sur un serveur)

```python
import tensorflow as tf

strategy = tf.distribute.MirroredStrategy()

print(f'Nombre de devices: {strategy.num_replicas_in_sync}')

with strategy.scope():
    # Créer et compiler le modèle
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10)
    ])
    
    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )

# Entraîner normalement
model.fit(dataset, epochs=10)
```

### Sélectionner des GPU Spécifiques

```bash
# Utiliser uniquement GPU 0
export CUDA_VISIBLE_DEVICES=0

# Utiliser GPU 0 et 1
export CUDA_VISIBLE_DEVICES=0,1

# Masquer tous les GPU (forcer CPU)
export CUDA_VISIBLE_DEVICES=-1
```

En Python :
```python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import tensorflow as tf
```

## 📊 Monitoring et Profiling

### TensorBoard

```python
import tensorflow as tf
import datetime

# Créer callback TensorBoard
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir=log_dir,
    histogram_freq=1,
    profile_batch='10,20'
)

# Utiliser lors de l'entraînement
model.fit(
    dataset,
    epochs=10,
    callbacks=[tensorboard_callback]
)
```

Lancer TensorBoard :
```bash
tensorboard --logdir logs/fit
```

### Profiling GPU

```python
import tensorflow as tf

# Démarrer le profiler
tf.profiler.experimental.start('logdir')

# Code à profiler
model.fit(dataset, epochs=1)

# Arrêter le profiler
tf.profiler.experimental.stop()
```

### Monitoring en Temps Réel

```bash
# Terminal 1: Surveiller GPU
watch -n 1 nvidia-smi

# Terminal 2: Logs détaillés GPU
nvidia-smi --query-gpu=timestamp,name,utilization.gpu,utilization.memory,memory.used,memory.free,temperature.gpu --format=csv -l 1

# Terminal 3: Entraînement
python train.py
```

## 🔧 Configuration Avancée

### Placement de Device

```python
import tensorflow as tf

# Activer le logging de placement
tf.debugging.set_log_device_placement(True)

# Forcer placement sur GPU
with tf.device('/GPU:0'):
    a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
    b = tf.constant([[1.0, 1.0], [0.0, 1.0]])
    c = tf.matmul(a, b)
```

### Pipeline de Données Optimisé

```python
import tensorflow as tf

# Optimiser le chargement de données
dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
dataset = dataset.cache()                    # Mettre en cache
dataset = dataset.shuffle(buffer_size=10000)
dataset = dataset.batch(32)
dataset = dataset.prefetch(tf.data.AUTOTUNE) # Préchargement automatique

# Utiliser
model.fit(dataset, epochs=10)
```

### Callbacks Utiles

```python
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

callbacks = [
    # Sauvegarder le meilleur modèle
    ModelCheckpoint(
        'best_model.h5',
        monitor='val_loss',
        save_best_only=True
    ),
    
    # Arrêter si pas d'amélioration
    EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    ),
    
    # Réduire learning rate
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3
    )
]

model.fit(dataset, epochs=100, callbacks=callbacks)
```

## 🐛 Débogage et Diagnostics

### Vérifier la Configuration

```python
import tensorflow as tf

print("TensorFlow version:", tf.__version__)
print("GPU disponibles:", tf.config.list_physical_devices('GPU'))
print("Built with CUDA:", tf.test.is_built_with_cuda())
print("Built with GPU support:", tf.test.is_built_with_gpu_support())

# Informations de build
build_info = tf.sysconfig.get_build_info()
print("CUDA version:", build_info.get('cuda_version'))
print("cuDNN version:", build_info.get('cudnn_version'))
```

### Tester les Performances

```python
import tensorflow as tf
import time

# Test simple
size = 4096
a = tf.random.normal([size, size])
b = tf.random.normal([size, size])

# Warmup
_ = tf.matmul(a, b)

# Benchmark
start = time.time()
for _ in range(100):
    _ = tf.matmul(a, b)
elapsed = time.time() - start

print(f"Temps: {elapsed:.2f}s pour 100 itérations")
print(f"GFLOPS: {(2 * size**3 * 100) / (elapsed * 1e9):.2f}")
```

## 📚 Ressources

- [TensorFlow GPU Guide](https://www.tensorflow.org/guide/gpu)
- [Mixed Precision Guide](https://www.tensorflow.org/guide/mixed_precision)
- [TensorFlow Performance Guide](https://www.tensorflow.org/guide/profiler)
- [NVIDIA A100 Documentation](https://www.nvidia.com/en-us/data-center/a100/)

---

**Auteur** : Mickael Angel  
**Version** : 1.0.0  
**Dernière mise à jour** : Décembre 2025

