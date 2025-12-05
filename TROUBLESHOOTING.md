# Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### Issue: "python3-devel not found"

**Solution**:
```bash
sudo zypper refresh
sudo zypper install python3-devel python311-devel
```

#### Issue: "gcc: command not found"

**Solution**:
```bash
sudo zypper install gcc gcc-c++ make cmake
```

#### Issue: "Permission denied" during installation

**Solution**:
```bash
# Add user to necessary groups
sudo usermod -aG video $USER
sudo usermod -aG render $USER

# Logout and login again for changes to take effect
```

### CUDA and GPU Issues

#### Issue: "CUDA not found" or "nvcc: command not found"

**Solution**:
```bash
# Check CUDA installation
ls /usr/local/cuda-11.8/

# Set environment variables
export CUDA_HOME=/usr/local/cuda-11.8
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
export PATH=$CUDA_HOME/bin:$PATH

# Make permanent
echo 'export CUDA_HOME=/usr/local/cuda-11.8' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
echo 'export PATH=$CUDA_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

#### Issue: "Could not load dynamic library 'libcudart.so.11.0'"

**Solution**:
```bash
# Verify CUDA libraries
ldconfig -p | grep cuda

# If not found, add to library path
sudo sh -c 'echo "/usr/local/cuda-11.8/lib64" > /etc/ld.so.conf.d/cuda.conf'
sudo ldconfig
```

#### Issue: "Could not load dynamic library 'libcudnn.so.8'"

**Solution**:
```bash
# Check cuDNN installation
ls /usr/local/cuda-11.8/lib64/libcudnn*

# Verify cuDNN version
cat /usr/local/cuda-11.8/include/cudnn_version.h | grep CUDNN_MAJOR -A 2

# If not installed, cuDNN 8.6 must be installed separately
```

#### Issue: "No GPU devices found" despite nvidia-smi working

**Solution**:
```bash
# Check if GPU is visible to TensorFlow
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

# Verify CUDA libraries are loaded
python3 -c "import tensorflow as tf; print(tf.sysconfig.get_build_info())"

# Check for conflicting installations
pip3 list | grep tensorflow

# Ensure only one TensorFlow installation
pip3 uninstall tensorflow tensorflow-gpu
# Then reinstall from local package
```

### Compilation Issues

#### Issue: Compilation takes too long or freezes

**Solution**:
```bash
# Check available memory
free -h

# Check CPU usage
top

# If memory is low, add swap space
sudo dd if=/dev/zero of=/swapfile bs=1M count=8192
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### Issue: "Out of memory" during compilation

**Solution**:
```bash
# Reduce parallel compilation jobs
export BAZEL_OPTS="--jobs=2"

# Or compile with limited resources
./install_suse.sh --jobs=1
```

### Runtime Issues

#### Issue: "ImportError: No module named 'tensorflow'"

**Solution**:
```bash
# Check Python path
python3 -c "import sys; print(sys.path)"

# Verify installation location
pip3 show tensorflow

# Add user site-packages to path
export PYTHONPATH=$HOME/.local/lib/python3.11/site-packages:$PYTHONPATH
```

#### Issue: "GPU memory allocation error"

**Solution**:
```python
import tensorflow as tf

# Enable memory growth
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

# Or set memory limit
tf.config.set_logical_device_configuration(
    gpus[0],
    [tf.config.LogicalDeviceConfiguration(memory_limit=10240)]
)
```

#### Issue: "Blas GEMM launch failed"

**Solution**:
```python
# Reduce batch size
# Or enable memory growth as shown above

# Check GPU memory usage
import subprocess
subprocess.run(['nvidia-smi'])
```

### Performance Issues

#### Issue: Training is slow on GPU

**Solution**:
```python
# Enable XLA compilation
import tensorflow as tf

@tf.function(jit_compile=True)
def train_step(x, y):
    # Your training logic
    pass

# Use mixed precision
from tensorflow.keras import mixed_precision
policy = mixed_precision.Policy('mixed_float16')
mixed_precision.set_global_policy(policy)

# Optimize data pipeline
dataset = dataset.prefetch(tf.data.AUTOTUNE)
dataset = dataset.cache()
```

#### Issue: CPU is being used instead of GPU

**Solution**:
```python
# Force GPU usage
with tf.device('/GPU:0'):
    # Your model operations
    pass

# Check device placement
tf.debugging.set_log_device_placement(True)
```

### Version Compatibility Issues

#### Issue: "Version mismatch between TensorFlow and CUDA"

**Solution**:
```bash
# Verify versions
python3 -c "import tensorflow as tf; print(tf.sysconfig.get_build_info())"

# This package requires:
# - CUDA 11.8
# - cuDNN 8.6
# - Python 3.8-3.11

# Do not use with Python 3.12 or CUDA 12.x
```

## Diagnostic Commands

### System Information
```bash
# OS version
cat /etc/os-release

# Kernel version
uname -r

# Python version
python3 --version

# GCC version
gcc --version
```

### GPU and CUDA
```bash
# NVIDIA driver
nvidia-smi

# CUDA version
nvcc --version

# CUDA libraries
ldconfig -p | grep cuda | grep so

# GPU architecture
nvidia-smi --query-gpu=compute_cap --format=csv
```

### TensorFlow
```bash
# Installation location
pip3 show tensorflow

# Verify build info
python3 -c "import tensorflow as tf; print(tf.sysconfig.get_build_info())"

# Test GPU
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

## Getting Help

If the issue persists:

1. **Check System Logs**:
```bash
dmesg | grep -i error
journalctl -xe
```

2. **Create Diagnostic Report**:
```bash
python3 test_tensorflow_gpu.py > diagnostic_report.txt 2>&1
nvidia-smi >> diagnostic_report.txt
```

3. **Open an Issue**: Include:
   - OS version
   - Python version
   - CUDA/cuDNN versions
   - Error messages
   - Diagnostic report

---

**Author**: Mickael Angel  
**Last Updated**: December 2025

