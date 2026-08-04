# Sigma Machine - Quick GitHub Push Reference

## Option 1: Bash Script (Linux/Mac/Git Bash)
```bash
cd /mnt/agents/output/sigma_machine
./push_to_github.sh YOUR_GITHUB_TOKEN [YOUR_USERNAME]
```

## Option 2: Python Script (Cross-platform)
```bash
cd /mnt/agents/output/sigma_machine
python push_to_github.py --token YOUR_GITHUB_TOKEN [--username YOUR_USERNAME]
```

## Option 3: Manual Steps
```bash
cd /mnt/agents/output/sigma_machine
git init
git add .
git commit -m "Initial commit: Sigma Machine v1.0.0"
# Create repo at https://github.com/new
git remote add origin https://github.com/YOUR_USERNAME/sigma-machine.git
git branch -M main
git push -u origin main
```

## Environment Variables (Recommended)
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
export GITHUB_USERNAME="your_username"
./push_to_github.sh  # reads from env
```

## What Gets Created
- ✅ Repository with full codebase
- ✅ Discussions enabled with 4 initial posts
- ✅ Issue templates (Bug, Feature, Theory)
- ✅ 8 custom labels
- ✅ MIT License
- ✅ CITATION.cff

## After Push
1. Visit https://github.com/YOUR_USERNAME/sigma-machine/discussions
2. Engage with the 4 initial discussion threads
3. Share with collaborators
4. Set up GitHub Actions CI/CD (optional)
5. Enable GitHub Pages for docs (optional)

## Security
⚠️  NEVER commit API keys to the repository!
The .gitignore is pre-configured to exclude secrets.
Always use environment variables or GitHub Secrets.
