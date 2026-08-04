from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sigma-machine",
    version="2.0.0",
    author="Sigma Machine Research Group",
    description="Universal Computational Architecture for the Isomorphism Principle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chepin-ai/sigma-machine",
    project_urls={
        "Documentation": "https://chepin-ai.github.io/sigma-machine",
        "Bug Tracker": "https://github.com/chepin-ai/sigma-machine/issues",
        "Discussions": "https://github.com/chepin-ai/sigma-machine/discussions",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-benchmark>=4.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "black>=23.0.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.0.0",
            "pymdown-extensions>=10.0.0",
        ],
        "quantum": [
            "qiskit>=0.44.0",
            "cirq>=1.3.0",
            "pennylane>=0.32.0",
        ],
        "ml": [
            "torch>=2.0.0",
            "jax>=0.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sigma-machine=sigma_machine.core.sigma_machine:main_cli",
        ],
    },
)
