# Contributing to TensorFlow Offline Installation Package

Thank you for your interest in contributing to this project!

## About This Project

This repository provides an offline installation package for TensorFlow on SUSE 15 SP7 with NVIDIA A100 GPU support. It is designed for air-gapped enterprise environments.

## How to Contribute

### Reporting Issues

If you encounter problems:

1. **Search existing issues** to avoid duplicates
2. **Create a new issue** with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, CUDA version)
   - Error messages and logs

### Suggesting Enhancements

We welcome suggestions for:
- Performance improvements
- Additional platform support
- Documentation enhancements
- Script optimizations
- New features

Please open an issue with the "enhancement" label.

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**: `git commit -m "Add: description of changes"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Open a Pull Request**

### Coding Standards

- Follow PEP 8 for Python code
- Use clear, descriptive variable names
- Comment complex logic
- Update documentation as needed
- Test on SUSE 15 SP7 when possible

### Commit Message Guidelines

Format: `Type: Short description`

Types:
- `Add`: New features or files
- `Fix`: Bug fixes
- `Update`: Updates to existing features
- `Docs`: Documentation changes
- `Refactor`: Code refactoring
- `Test`: Adding or updating tests

Examples:
```
Add: Support for Python 3.12
Fix: GPU detection issue on multi-GPU systems
Update: Installation script with better error handling
Docs: Improve troubleshooting guide
```

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/tensorflow.git
cd tensorflow

# Set up remote
git remote add upstream https://github.com/mickaelangel/tensorflow.git

# Create development branch
git checkout -b dev/your-feature
```

## Testing

Before submitting a PR:

```bash
# Run tests
python3 test_tensorflow_gpu.py

# Verify installation
./deploy.sh

# Check documentation
# Ensure all links work and formatting is correct
```

## Documentation

When adding features:
- Update README.md
- Add/update relevant documentation files
- Include code examples
- Update CHANGELOG.md

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the issue, not the person
- Help others learn and grow

## Questions?

Feel free to:
- Open an issue for discussion
- Comment on existing issues
- Reach out via GitHub

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Author**: Mickael Angel  
**Project**: TensorFlow Offline Installation Package for SUSE 15 SP7

