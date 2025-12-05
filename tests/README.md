# Tests TensorFlow - Suite de Tests

Suite de tests complète pour valider l'installation TensorFlow sur SUSE 15 SP7 avec GPU A100.

## 📋 Vue d'Ensemble

Cette suite de tests vérifie :
- ✅ Prérequis système
- ✅ Installation TensorFlow
- ✅ Détection et fonctionnalité GPU
- ✅ Performance et benchmarks
- ✅ Configuration optimale

## 🧪 Tests Disponibles

### 1. test_installation.py
Tests d'installation et de configuration de base.

**Ce qui est testé** :
- Version Python compatible
- Driver NVIDIA installé
- CUDA 11.8 disponible
- TensorFlow importable
- GPU détectés
- Support CUDA/GPU
- Calculs sur GPU
- Mixed precision
- Compilation XLA

**Exécution** :
```bash
python3 tests/test_installation.py
```

### 2. test_gpu_performance.py
Benchmarks de performance GPU.

**Ce qui est testé** :
- Multiplication matricielle
- Convolutions 2D
- Mixed precision (FP16 vs FP32)
- Utilisation mémoire GPU

**Exécution** :
```bash
python3 tests/test_gpu_performance.py
```

## 🚀 Exécuter Tous les Tests

### Test Rapide
```bash
# Test d'installation seulement
python3 tests/test_installation.py
```

### Test Complet
```bash
# Tests + Benchmarks
python3 tests/test_installation.py && python3 tests/test_gpu_performance.py
```

### Test avec Rapport Détaillé
```bash
python3 tests/test_installation.py -v > test_report.txt 2>&1
```

## 📊 Résultats Attendus

### Tests d'Installation
```
======================================================================
TESTS D'INSTALLATION TENSORFLOW
======================================================================

test_python_version ✓
test_nvidia_driver ✓
test_cuda_available ✓
test_tensorflow_import ✓
test_tensorflow_version ✓
test_gpu_detection ✓
test_cuda_build ✓
test_gpu_support ✓
test_simple_computation ✓
test_memory_growth ✓
test_mixed_precision ✓
test_xla_compilation ✓

======================================================================
✅ TOUS LES TESTS SONT PASSÉS!
======================================================================
```

### Benchmarks de Performance
```
======================================================================
Test: Multiplication Matricielle
======================================================================
  Taille 1000x1000: 2.34 ms/iteration, 854.70 GFLOPS
  Taille 2000x2000: 8.91 ms/iteration, 1794.28 GFLOPS
  Taille 4000x4000: 45.23 ms/iteration, 2831.45 GFLOPS
  Taille 8000x8000: 289.34 ms/iteration, 3543.12 GFLOPS

======================================================================
Test: Mixed Precision (FP16 vs FP32)
======================================================================
  FP32: 12.45s pour 100 itérations
  FP16: 4.23s pour 100 itérations
  Accélération: 2.94x

✅ TOUS LES BENCHMARKS TERMINÉS
```

## 🔧 Configuration des Tests

### Variables d'Environnement

```bash
# Désactiver les warnings TensorFlow
export TF_CPP_MIN_LOG_LEVEL=2

# Forcer l'utilisation de GPU spécifique
export CUDA_VISIBLE_DEVICES=0

# Activer le mode debug
export TF_CPP_MIN_LOG_LEVEL=0
```

### Options de Test

```python
# Dans le script de test
import tensorflow as tf

# Activer le logging détaillé
tf.debugging.set_log_device_placement(True)

# Limiter la mémoire GPU
gpus = tf.config.list_physical_devices('GPU')
tf.config.set_logical_device_configuration(
    gpus[0],
    [tf.config.LogicalDeviceConfiguration(memory_limit=1024)]
)
```

## ❌ Dépannage

### Test échoue : "nvidia-smi non trouvé"
**Solution** : Installer le driver NVIDIA
```bash
sudo zypper install nvidia-computeG06
```

### Test échoue : "CUDA non disponible"
**Solution** : Configurer les variables d'environnement
```bash
export CUDA_HOME=/usr/local/cuda-11.8
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
export PATH=$CUDA_HOME/bin:$PATH
```

### Test échoue : "Impossible d'importer TensorFlow"
**Solution** : Vérifier l'installation
```bash
pip3 list | grep tensorflow
python3 -m pip install --upgrade tensorflow
```

### Performances faibles
**Solution** : Vérifier les optimisations
```python
# Activer XLA
import tensorflow as tf
tf.config.optimizer.set_jit(True)

# Activer mixed precision
from tensorflow.keras import mixed_precision
policy = mixed_precision.Policy('mixed_float16')
mixed_precision.set_global_policy(policy)
```

## 📝 Ajouter Vos Propres Tests

### Exemple de Test Personnalisé

```python
import unittest
import tensorflow as tf

class TestCustom(unittest.TestCase):
    def test_mon_modele(self):
        """Test votre modèle personnalisé"""
        model = creer_mon_modele()
        self.assertIsNotNone(model)
        
        # Tester la prédiction
        input_data = tf.random.normal([1, 224, 224, 3])
        output = model(input_data)
        self.assertEqual(output.shape[0], 1)

if __name__ == '__main__':
    unittest.main()
```

## 📊 Métriques de Performance

### GPU A100 - Résultats Typiques

| Benchmark | Performance | Notes |
|-----------|-------------|-------|
| ResNet-50 | ~900 img/s | Batch size 32 |
| BERT-base | ~120 seq/s | Sequence length 128 |
| Matmul 8K | ~3.5 TFLOPS | FP32 |
| Matmul 8K | ~10 TFLOPS | FP16 (Tensor Cores) |

### Speedup Mixed Precision

- **Entraînement** : 2-3x plus rapide
- **Inférence** : 2-4x plus rapide
- **Mémoire** : ~50% d'économie

## 🤝 Contribution

Pour ajouter de nouveaux tests :
1. Créer un fichier `test_*.py`
2. Hériter de `unittest.TestCase`
3. Préfixer les méthodes par `test_`
4. Documenter clairement
5. Tester avant de commit

## 📞 Support

Pour les problèmes de tests :
- Consulter [TROUBLESHOOTING.fr.md](../TROUBLESHOOTING.fr.md)
- Ouvrir une issue sur GitHub
- Vérifier les logs détaillés

---

**Auteur** : Mickael Angel  
**Version** : 1.0.0  
**Dernière mise à jour** : Décembre 2025

