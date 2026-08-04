#!/usr/bin/env python3
"""
Sigma Machine - GitHub Push Script (Python Version)
===================================================
Alternative to the bash script for Windows users or those
who prefer Python.

Usage:
    python push_to_github.py --token YOUR_GITHUB_TOKEN [--username YOUR_USERNAME]

Or set environment variables:
    export GITHUB_TOKEN=your_token
    export GITHUB_USERNAME=your_username
    python push_to_github.py
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error


def api_request(url, method="GET", data=None, headers=None, token=None):
    """Make a GitHub API request."""
    if headers is None:
        headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    headers["Accept"] = "application/vnd.github.v3+json"

    req = urllib.request.Request(url, method=method)
    for key, val in headers.items():
        req.add_header(key, val)

    if data:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(data).encode("utf-8")

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"API Error: {e.code} - {e.reason}")
        try:
            body = json.loads(e.read().decode("utf-8"))
            print(f"Details: {body.get('message', 'Unknown error')}")
        except:
            pass
        return None


def get_username(token):
    """Get GitHub username from API."""
    data = api_request("https://api.github.com/user", token=token)
    return data.get("login") if data else None


def create_repo(token, username, repo_name, description):
    """Create a new GitHub repository."""
    url = "https://api.github.com/user/repos"
    data = {
        "name": repo_name,
        "description": description,
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True,
        "has_discussions": True,
        "auto_init": False
    }
    return api_request(url, method="POST", data=data, token=token)


def repo_exists(token, username, repo_name):
    """Check if repository already exists."""
    url = f"https://api.github.com/repos/{username}/{repo_name}"
    data = api_request(url, token=token)
    return data is not None


def create_discussion(token, username, repo_name, title, body, category="General"):
    """Create a discussion post."""
    url = f"https://api.github.com/repos/{username}/{repo_name}/discussions"
    data = {
        "title": title,
        "body": body,
        "category": category
    }
    return api_request(url, method="POST", data=data, token=token)


def create_label(token, username, repo_name, name, description, color):
    """Create a repository label."""
    url = f"https://api.github.com/repos/{username}/{repo_name}/labels"
    data = {
        "name": name,
        "description": description,
        "color": color
    }
    return api_request(url, method="POST", data=data, token=token)


def main():
    parser = argparse.ArgumentParser(description="Push Sigma Machine to GitHub")
    parser.add_argument("--token", help="GitHub personal access token")
    parser.add_argument("--username", help="GitHub username")
    parser.add_argument("--repo-name", default="sigma-machine", help="Repository name")
    args = parser.parse_args()

    # Get token from args or environment
    token = args.token or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ Error: GitHub token required.")
        print("Use --token or set GITHUB_TOKEN environment variable.")
        sys.exit(1)

    # Get username
    username = args.username or os.environ.get("GITHUB_USERNAME")
    if not username:
        username = get_username(token)
        if not username:
            print("❌ Error: Could not determine GitHub username.")
            print("Use --username or set GITHUB_USERNAME environment variable.")
            sys.exit(1)

    repo_name = args.repo_name
    description = "Universal Computational Architecture for the Isomorphism Principle"

    print("=" * 50)
    print("  Sigma Machine GitHub Deployment")
    print("=" * 50)
    print(f"\nRepository: {repo_name}")
    print(f"Username:   {username}\n")

    # Step 1: Check if repo exists
    print("🔍 Step 1: Checking repository...")
    exists = repo_exists(token, username, repo_name)

    if exists:
        print("   ⚠️  Repository exists. Will push to existing repo.")
    else:
        print("   ✅ Creating new repository...")
        repo = create_repo(token, username, repo_name, description)
        if repo:
            print(f"   ✅ Created: {repo['html_url']}")
        else:
            print("   ❌ Failed to create repository")
            sys.exit(1)

    # Step 2: Git push
    print("\n🚀 Step 2: Pushing codebase...")

    if not os.path.exists(".git"):
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", 
            "Initial commit: Sigma Machine v1.0.0\n\n"
            "Universal Computational Architecture for the Isomorphism Principle."],
            check=True)

    remote_url = f"https://github.com/{username}/{repo_name}.git"
    subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)
    subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)
    subprocess.run(["git", "branch", "-M", "main"], check=True)

    try:
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        print("   ✅ Codebase pushed successfully!")
    except subprocess.CalledProcessError:
        print("   ⚠️  Push may have failed. Check credentials.")

    # Step 3: Create discussions
    print("\n💬 Step 3: Creating Discussion posts...")

    discussions = [
        {
            "title": "Welcome to Sigma Machine - Introduction & Roadmap",
            "body": "# Welcome!\n\nThis is the main welcome thread...",
            "category": "General"
        },
        {
            "title": "Theory Discussion: The Isomorphism Principle",
            "body": "# Theory Discussion\n\nOpen questions about the Isomorphism Principle...",
            "category": "General"
        },
        {
            "title": "Experimental Collaboration: Physical Platforms",
            "body": "# Experimental Collaboration\n\nCoordinating physical zero detection experiments...",
            "category": "General"
        },
        {
            "title": "Breakthrough Directions: Which Path to Pursue?",
            "body": "# Breakthrough Directions\n\nDiscussing the 5 research directions...",
            "category": "General"
        }
    ]

    for disc in discussions:
        result = create_discussion(token, username, repo_name, 
                                   disc["title"], disc["body"], disc["category"])
        if result:
            print(f"   ✅ Created: {disc['title']}")
        else:
            print(f"   ⚠️  Could not create: {disc['title']}")

    # Step 4: Create labels
    print("\n🏷️  Step 4: Creating labels...")

    labels = [
        ("theory", "Theory contributions and proofs", "1d76db"),
        ("experiment", "Experimental results", "28a745"),
        ("isomorphism", "New isomorphism discoveries", "e99695"),
        ("criticality", "Criticality principle", "d93f0b"),
        ("breakthrough", "Breakthrough research", "5319e7"),
        ("documentation", "Documentation", "0075ca"),
        ("performance", "Performance", "84b6eb"),
        ("platform", "Physical platforms", "fbca04")
    ]

    for name, desc, color in labels:
        create_label(token, username, repo_name, name, desc, color)

    print("   ✅ Labels created.")

    # Summary
    print("\n" + "=" * 50)
    print("  ✅ DEPLOYMENT COMPLETE!")
    print("=" * 50)
    print(f"\nRepository:  https://github.com/{username}/{repo_name}")
    print(f"Discussions: https://github.com/{username}/{repo_name}/discussions")
    print(f"Issues:      https://github.com/{username}/{repo_name}/issues")
    print("\nNext: Visit Discussions to engage with the community!")


if __name__ == "__main__":
    main()
