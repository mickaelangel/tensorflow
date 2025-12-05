# TensorFlow Offline Installation Package for SUSE 15 SP7

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20.0-orange.svg)](https://www.tensorflow.org/)
[![Python](https://img.shields.io/badge/Python-3.8--3.11-blue.svg)](https://www.python.org/)
[![CUDA](https://img.shields.io/badge/CUDA-11.8-green.svg)](https://developer.nvidia.com/cuda-toolkit)

> **Complete offline installation package for TensorFlow with GPU A100 support on SUSE Linux Enterprise Server 15 SP7**

## 📋 Overview

This repository contains a comprehensive, ready-to-deploy package for installing TensorFlow with GPU acceleration on air-gapped SUSE 15 SP7 systems. Designed for enterprise environments requiring secure, offline installations with NVIDIA A100 GPU support.

## ✨ Features

- **🔒 Fully Offline**: No internet connection required on target system
- **🚀 GPU Optimized**: Configured for NVIDIA A100 with CUDA 11.8 and cuDNN 8.6
- **📦 Complete Package**: All dependencies included as source files
- **🛠️ Automated Installation**: Simple deployment scripts
- **✅ Tested & Verified**: Production-ready configuration
- **📊 Performance Monitoring**: Integrated TensorBoard and testing tools

## 🎯 Target Environment

- **OS**: SUSE Linux Enterprise Server 15 SP7
- **GPU**: NVIDIA A100
- **Python**: 3.8, 3.9, 3.10, or 3.11
- **CUDA**: 11.8
- **cuDNN**: 8.6

## 📦 Package Contents

### Core Components
- **TensorFlow 2.20.0** (source)
- **29 dependency packages** (all as source .tar.gz files)
- **Installation scripts** (automated deployment)
- **GPU configuration** (optimized for A100)
- **Testing suite** (validation tools)

### Package Structure
```
tensorflow_offline_packages/
├── install_suse.sh              # Main installation script
├── deploy.sh                    # Quick deployment script
├── gpu_a100_config.sh           # GPU A100 configuration
├── test_tensorflow_gpu.py       # GPU testing script
├── requirements.txt             # Dependency list
├── README.md                    # Package documentation
└── [source packages]            # All .tar.gz files
```

## 🚀 Quick Start

### Prerequisites on Target System

```bash
# Install compilation tools
sudo zypper install -y gcc gcc-c++ python3-devel make cmake

# Verify Python version (must be 3.8-3.11)
python3 --version

# Verify NVIDIA driver
nvidia-smi

# Verify CUDA 11.8
nvcc --version
```

### Installation Steps

1. **Transfer the package** to your SUSE 15 SP7 system (USB, SCP, or network)

2. **Extract the archive**:
```bash
cd /tmp
tar -xzf tensorflow_suse15sp7_a100_FINAL.tar.gz
cd tensorflow_offline_packages
```

3. **Run the deployment script**:
```bash
chmod +x deploy.sh install_suse.sh gpu_a100_config.sh
./deploy.sh
```

4. **Verify installation**:
```bash
python3 -c "import tensorflow as tf; print('TensorFlow:', tf.__version__)"
python3 -c "import tensorflow as tf; print('GPUs:', tf.config.list_physical_devices('GPU'))"
python3 test_tensorflow_gpu.py
```

## 📖 Detailed Documentation

### Installation Guide
See [INSTALLATION.md](INSTALLATION.md) for detailed installation instructions.

### Troubleshooting
See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

### Configuration
See [CONFIGURATION.md](CONFIGURATION.md) for advanced configuration options.

## 🔧 System Requirements

### Minimum Requirements
- **Disk Space**: 15 GB free
- **RAM**: 16 GB
- **Python**: 3.8+
- **GCC**: 7.0+

### Recommended Requirements
- **Disk Space**: 50 GB free
- **RAM**: 32 GB+
- **Python**: 3.11
- **GCC**: 11.0+

## 🎯 Performance Optimization

The package includes optimizations for:
- **Mixed Precision Training**: Utilizing A100 Tensor Cores
- **XLA Compilation**: Accelerated Linear Algebra
- **Multi-GPU Support**: Distributed training capabilities
- **Memory Optimization**: Efficient memory management

## 📊 Benchmarks

Expected performance on NVIDIA A100:
- **Image Classification (ResNet-50)**: ~900 images/sec
- **Object Detection (YOLOv5)**: ~60 FPS
- **Language Model (BERT-base)**: ~120 sequences/sec
- **Mixed Precision**: 2-3x speedup over FP32

## 🛠️ Building from Source

To create your own offline package:

```bash
# On a machine with internet access
python download_packages.py

# Create the archive
tar -czf tensorflow_suse15sp7_a100_FINAL.tar.gz tensorflow_offline_packages/
```

See [BUILD.md](BUILD.md) for detailed build instructions.

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Basic functionality test
python3 test_tensorflow_gpu.py

# Performance benchmark
python3 benchmark_gpu.py

# Model training test
python3 test_training.py
```

## 📚 Examples

Check the `examples/` directory for:
- Image classification with CNNs
- Object detection with YOLO
- Natural Language Processing with Transformers
- Time series forecasting
- Reinforcement learning

## 🤝 Contributing

This is a deployment package repository. For contributions to TensorFlow itself, please visit the [official TensorFlow repository](https://github.com/tensorflow/tensorflow).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

TensorFlow is licensed under the Apache License 2.0.

## 👤 Author

**Mickael Angel**
- GitHub: [@mickaelangel](https://github.com/mickaelangel)
- Project: TensorFlow Offline Installation Package

## 🙏 Acknowledgments

- Google TensorFlow Team for the amazing framework
- NVIDIA for GPU support and optimization
- SUSE for the excellent enterprise Linux distribution
- Open-source community for continuous improvements

## 📞 Support

For issues and questions:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review [closed issues](https://github.com/mickaelangel/tensorflow/issues?q=is%3Aissue+is%3Aclosed)
3. Open a [new issue](https://github.com/mickaelangel/tensorflow/issues/new)

## 🔄 Updates

Check [CHANGELOG.md](CHANGELOG.md) for version history and updates.

## ⚠️ Important Notes

- This package is designed for **offline/air-gapped** environments
- Ensure **CUDA 11.8** and **cuDNN 8.6** are installed before deployment
- Compilation may take **15-45 minutes** depending on system resources
- Tested on **SUSE 15 SP7** - compatibility with other versions not guaranteed

## 🌟 Features Roadmap

- [ ] Support for TensorFlow 2.21+
- [ ] AMD ROCm GPU support
- [ ] Multi-node distributed training setup
- [ ] Docker containerized deployment
- [ ] Kubernetes orchestration templates

---

**Made with ❤️ for the ML/AI community**

*Last updated: December 2025*
