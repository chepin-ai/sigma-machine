# Contributing to Sigma Machine

## How to Contribute

### Reporting Issues
- Use GitHub Issues for bugs or feature requests
- Include minimal reproducible examples
- Tag with appropriate labels

### Submitting Code
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Open Pull Request

### Code Standards
- Follow PEP 8
- Include docstrings for public functions
- Add tests for new features
- Maintain backward compatibility

### Theoretical Contributions
- Submit proofs as LaTeX in `docs/theory/`
- Computational experiments as Jupyter notebooks
- Literature reviews as Markdown

## Development Setup

```bash
git clone https://github.com/chepin-ai/sigma-machine.git
cd sigma-machine
pip install -e ".[dev]"
pytest tests/ -v
```
