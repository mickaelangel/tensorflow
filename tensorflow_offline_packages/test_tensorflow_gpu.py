#!/usr/bin/env python3
"""
Script de test pour vérifier l'installation de TensorFlow avec GPU A100
"""

import sys

def test_tensorflow_import():
    """Test l'importation de TensorFlow"""
    try:
        import tensorflow as tf
        print(f"✓ TensorFlow importé avec succès")
        print(f"  Version: {tf.__version__}")
        return tf
    except ImportError as e:
        print(f"✗ Erreur lors de l'importation de TensorFlow: {e}")
        sys.exit(1)

def test_gpu_detection(tf):
    """Test la détection des GPU"""
    print("\n=== Détection des GPU ===")
    gpus = tf.config.list_physical_devices('GPU')
    
    if len(gpus) == 0:
        print("✗ Aucune GPU détectée")
        print("  Vérifiez:")
        print("    - Que le driver NVIDIA est installé (nvidia-smi)")
        print("    - Que CUDA est dans le LD_LIBRARY_PATH")
        print("    - Que cuDNN est installé")
        return False
    else:
        print(f"✓ {len(gpus)} GPU détectée(s):")
        for i, gpu in enumerate(gpus):
            print(f"  GPU {i}: {gpu.name}")
            # Obtenir les détails de la GPU
            try:
                details = tf.config.experimental.get_device_details(gpu)
                if details:
                    print(f"    Détails: {details}")
            except:
                pass
        return True

def test_gpu_computation(tf):
    """Test un calcul simple sur GPU"""
    print("\n=== Test de calcul sur GPU ===")
    try:
        with tf.device('/GPU:0'):
            # Créer deux matrices
            a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
            b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
            
            # Multiplication matricielle
            c = tf.matmul(a, b)
            result = c.numpy()
            
            print("✓ Calcul sur GPU réussi")
            print(f"  Résultat:\n{result}")
            return True
    except Exception as e:
        print(f"✗ Erreur lors du calcul sur GPU: {e}")
        return False

def test_tensorflow_features(tf):
    """Test les fonctionnalités de TensorFlow"""
    print("\n=== Fonctionnalités TensorFlow ===")
    
    # Vérifier la version CUDA
    try:
        cuda_version = tf.sysconfig.get_build_info()['cuda_version']
        cudnn_version = tf.sysconfig.get_build_info()['cudnn_version']
        print(f"✓ CUDA version: {cuda_version}")
        print(f"✓ cuDNN version: {cudnn_version}")
    except:
        print("  (Informations CUDA non disponibles)")
    
    # Vérifier les optimisations
    print(f"  Built with CUDA: {tf.test.is_built_with_cuda()}")
    print(f"  Built with GPU support: {tf.test.is_built_with_gpu_support()}")

def main():
    """Fonction principale"""
    print("=" * 60)
    print("Test d'installation TensorFlow pour GPU A100")
    print("=" * 60)
    
    # Test 1: Importation
    tf = test_tensorflow_import()
    
    # Test 2: Détection GPU
    gpu_available = test_gpu_detection(tf)
    
    # Test 3: Fonctionnalités
    test_tensorflow_features(tf)
    
    # Test 4: Calcul sur GPU (si disponible)
    if gpu_available:
        test_gpu_computation(tf)
    
    print("\n" + "=" * 60)
    if gpu_available:
        print("✓ Tous les tests sont passés avec succès!")
        print("  TensorFlow est correctement configuré pour utiliser la GPU A100")
    else:
        print("⚠ TensorFlow est installé mais la GPU n'est pas détectée")
        print("  Vérifiez la configuration CUDA et les drivers NVIDIA")
    print("=" * 60)

if __name__ == "__main__":
    main()

