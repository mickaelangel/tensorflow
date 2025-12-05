#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests de Performance GPU
========================

Benchmarks de performance pour TensorFlow sur GPU A100.

Auteur: Mickael Angel
Version: 1.0.0
"""

import time
import numpy as np
import tensorflow as tf


def test_matrix_multiplication():
    """Benchmark multiplication matricielle"""
    print("\n" + "=" * 70)
    print("Test: Multiplication Matricielle")
    print("=" * 70)
    
    sizes = [1000, 2000, 4000, 8000]
    
    for size in sizes:
        # Créer des matrices aléatoires
        a = tf.random.normal([size, size])
        b = tf.random.normal([size, size])
        
        # Warmup
        _ = tf.matmul(a, b)
        
        # Benchmark
        start = time.time()
        for _ in range(10):
            _ = tf.matmul(a, b)
        end = time.time()
        
        elapsed = (end - start) / 10
        gflops = (2 * size ** 3) / (elapsed * 1e9)
        
        print(f"  Taille {size}x{size}: {elapsed*1000:.2f} ms/iteration, {gflops:.2f} GFLOPS")


def test_convolution():
    """Benchmark convolution 2D"""
    print("\n" + "=" * 70)
    print("Test: Convolution 2D")
    print("=" * 70)
    
    batch_sizes = [32, 64, 128]
    image_size = 224
    
    for batch_size in batch_sizes:
        # Créer des images aléatoires
        images = tf.random.normal([batch_size, image_size, image_size, 3])
        
        # Créer une couche de convolution
        conv = tf.keras.layers.Conv2D(64, 3, padding='same')
        
        # Warmup
        _ = conv(images)
        
        # Benchmark
        start = time.time()
        for _ in range(50):
            _ = conv(images)
        end = time.time()
        
        elapsed = (end - start) / 50
        throughput = batch_size / elapsed
        
        print(f"  Batch size {batch_size}: {elapsed*1000:.2f} ms/batch, {throughput:.2f} images/sec")


def test_mixed_precision():
    """Benchmark mixed precision"""
    print("\n" + "=" * 70)
    print("Test: Mixed Precision (FP16 vs FP32)")
    print("=" * 70)
    
    size = 4096
    iterations = 100
    
    # Test FP32
    tf.keras.backend.set_floatx('float32')
    a_fp32 = tf.random.normal([size, size], dtype=tf.float32)
    b_fp32 = tf.random.normal([size, size], dtype=tf.float32)
    
    _ = tf.matmul(a_fp32, b_fp32)  # Warmup
    
    start = time.time()
    for _ in range(iterations):
        _ = tf.matmul(a_fp32, b_fp32)
    time_fp32 = time.time() - start
    
    # Test FP16
    from tensorflow.keras import mixed_precision
    policy = mixed_precision.Policy('mixed_float16')
    mixed_precision.set_global_policy(policy)
    
    a_fp16 = tf.random.normal([size, size], dtype=tf.float16)
    b_fp16 = tf.random.normal([size, size], dtype=tf.float16)
    
    _ = tf.matmul(a_fp16, b_fp16)  # Warmup
    
    start = time.time()
    for _ in range(iterations):
        _ = tf.matmul(a_fp16, b_fp16)
    time_fp16 = time.time() - start
    
    speedup = time_fp32 / time_fp16
    
    print(f"  FP32: {time_fp32:.2f}s pour {iterations} itérations")
    print(f"  FP16: {time_fp16:.2f}s pour {iterations} itérations")
    print(f"  Accélération: {speedup:.2f}x")


def test_memory_usage():
    """Test utilisation mémoire GPU"""
    print("\n" + "=" * 70)
    print("Test: Utilisation Mémoire GPU")
    print("=" * 70)
    
    gpus = tf.config.list_physical_devices('GPU')
    
    if gpus:
        # Allouer des tenseurs de différentes tailles
        sizes_mb = [100, 500, 1000, 2000]
        
        for size_mb in sizes_mb:
            # Calculer la taille du tenseur
            elements = (size_mb * 1024 * 1024) // 4  # 4 bytes par float32
            tensor = tf.random.normal([elements])
            
            print(f"  Tenseur alloué: ~{size_mb} MB")
            
            # Libérer
            del tensor
            tf.keras.backend.clear_session()


def main():
    """Fonction principale"""
    print("=" * 70)
    print("BENCHMARKS DE PERFORMANCE GPU")
    print("TensorFlow sur NVIDIA A100")
    print("=" * 70)
    
    # Informations GPU
    gpus = tf.config.list_physical_devices('GPU')
    print(f"\nGPU détectés: {len(gpus)}")
    for i, gpu in enumerate(gpus):
        print(f"  GPU {i}: {gpu.name}")
    
    print(f"\nTensorFlow version: {tf.__version__}")
    print(f"CUDA disponible: {tf.test.is_built_with_cuda()}")
    print(f"Support GPU: {tf.test.is_built_with_gpu_support()}")
    
    # Exécuter les benchmarks
    try:
        test_matrix_multiplication()
        test_convolution()
        test_mixed_precision()
        test_memory_usage()
        
        print("\n" + "=" * 70)
        print("✅ TOUS LES BENCHMARKS TERMINÉS")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erreur pendant les benchmarks: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

