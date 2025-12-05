#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests d'Installation TensorFlow
================================

Tests automatisés pour vérifier l'installation de TensorFlow
sur SUSE 15 SP7 avec GPU A100.

Auteur: Mickael Angel
Version: 1.0.0
"""

import sys
import unittest
import subprocess


class TestSystemRequirements(unittest.TestCase):
    """Tests des prérequis système"""
    
    def test_python_version(self):
        """Vérifie que la version Python est compatible"""
        version = sys.version_info
        self.assertGreaterEqual(version.major, 3)
        self.assertGreaterEqual(version.minor, 8)
        self.assertLessEqual(version.minor, 11)
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    
    def test_nvidia_driver(self):
        """Vérifie que le driver NVIDIA est installé"""
        try:
            result = subprocess.run(['nvidia-smi'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            self.assertEqual(result.returncode, 0)
            print("✓ Driver NVIDIA détecté")
        except FileNotFoundError:
            self.fail("nvidia-smi non trouvé - driver NVIDIA non installé")
    
    def test_cuda_available(self):
        """Vérifie que CUDA est disponible"""
        try:
            result = subprocess.run(['nvcc', '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            self.assertEqual(result.returncode, 0)
            self.assertIn('11.8', result.stdout)
            print("✓ CUDA 11.8 détecté")
        except FileNotFoundError:
            self.fail("nvcc non trouvé - CUDA non installé")


class TestTensorFlowInstallation(unittest.TestCase):
    """Tests de l'installation TensorFlow"""
    
    def test_tensorflow_import(self):
        """Vérifie que TensorFlow peut être importé"""
        try:
            import tensorflow as tf
            print(f"✓ TensorFlow {tf.__version__} importé")
        except ImportError as e:
            self.fail(f"Impossible d'importer TensorFlow: {e}")
    
    def test_tensorflow_version(self):
        """Vérifie la version de TensorFlow"""
        import tensorflow as tf
        version = tf.__version__
        self.assertTrue(version.startswith('2.'))
        print(f"✓ TensorFlow version {version}")
    
    def test_gpu_detection(self):
        """Vérifie que les GPU sont détectés"""
        import tensorflow as tf
        gpus = tf.config.list_physical_devices('GPU')
        self.assertGreater(len(gpus), 0, "Aucun GPU détecté")
        print(f"✓ {len(gpus)} GPU(s) détecté(s)")
        for i, gpu in enumerate(gpus):
            print(f"  GPU {i}: {gpu.name}")
    
    def test_cuda_build(self):
        """Vérifie que TensorFlow est compilé avec CUDA"""
        import tensorflow as tf
        self.assertTrue(tf.test.is_built_with_cuda())
        print("✓ TensorFlow compilé avec CUDA")
    
    def test_gpu_support(self):
        """Vérifie le support GPU"""
        import tensorflow as tf
        self.assertTrue(tf.test.is_built_with_gpu_support())
        print("✓ Support GPU activé")


class TestGPUComputation(unittest.TestCase):
    """Tests de calcul sur GPU"""
    
    def test_simple_computation(self):
        """Test un calcul simple sur GPU"""
        import tensorflow as tf
        
        with tf.device('/GPU:0'):
            a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
            b = tf.constant([[1.0, 1.0], [0.0, 1.0]])
            c = tf.matmul(a, b)
            result = c.numpy()
        
        expected = [[1.0, 3.0], [3.0, 7.0]]
        self.assertTrue((result == expected).all())
        print("✓ Calcul GPU réussi")
    
    def test_memory_growth(self):
        """Vérifie la configuration de croissance mémoire"""
        import tensorflow as tf
        
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                print("✓ Croissance mémoire GPU configurée")
            except RuntimeError as e:
                self.fail(f"Erreur configuration mémoire: {e}")


class TestPerformance(unittest.TestCase):
    """Tests de performance"""
    
    def test_mixed_precision(self):
        """Vérifie le support mixed precision"""
        import tensorflow as tf
        from tensorflow.keras import mixed_precision
        
        try:
            policy = mixed_precision.Policy('mixed_float16')
            mixed_precision.set_global_policy(policy)
            print(f"✓ Mixed precision configuré: {policy.name}")
        except Exception as e:
            self.fail(f"Erreur mixed precision: {e}")
    
    def test_xla_compilation(self):
        """Vérifie le support XLA"""
        import tensorflow as tf
        
        @tf.function(jit_compile=True)
        def test_function(x):
            return x * x
        
        try:
            result = test_function(tf.constant(2.0))
            self.assertEqual(result.numpy(), 4.0)
            print("✓ Compilation XLA fonctionnelle")
        except Exception as e:
            self.fail(f"Erreur XLA: {e}")


def run_tests():
    """Exécute tous les tests"""
    print("=" * 70)
    print("TESTS D'INSTALLATION TENSORFLOW")
    print("=" * 70)
    print()
    
    # Créer la suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Ajouter les tests
    suite.addTests(loader.loadTestsFromTestCase(TestSystemRequirements))
    suite.addTests(loader.loadTestsFromTestCase(TestTensorFlowInstallation))
    suite.addTests(loader.loadTestsFromTestCase(TestGPUComputation))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Résumé
    print()
    print("=" * 70)
    print("RÉSUMÉ")
    print("=" * 70)
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Réussis: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")
    
    if result.wasSuccessful():
        print()
        print("✅ TOUS LES TESTS SONT PASSÉS!")
        print("Installation TensorFlow validée avec succès")
        return 0
    else:
        print()
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("Consultez TROUBLESHOOTING.fr.md pour l'aide")
        return 1


if __name__ == '__main__':
    sys.exit(run_tests())

