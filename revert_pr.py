import requests
import subprocess
import sys
import os

def revert_pr(repo_owner, repo_name, pr_id, github_token):
    # GitHub API URL to get the PR details
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_id}"
    
    # Send the request to GitHub API
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch PR details: {response.status_code}")
        sys.exit(1)
    
    pr_data = response.json()
    print(f'PR_data {pr_data}')
    merge_commit_sha = pr_data.get('merge_commit_sha')
    
    if not merge_commit_sha:
        print(f"Merge commit SHA not found for PR #{pr_id}.")
        sys.exit(1)
    
    print(f"Reverting commit {merge_commit_sha} for PR #{pr_id}")
    
    # Configure Git
    subprocess.run(["git", "config", "user.name", "Jenkins"], check=True)
    subprocess.run(["git", "config", "user.email", "jenkins@yourdomain.com"], check=True)
    
    # Perform git revert
    try:
        subprocess.run(["git", "revert", "-m", "1", "--no-edit", merge_commit_sha], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during git revert: {e}")
        sys.exit(1)
    
    # Commit the revert
    subprocess.run(["git", "commit", "-m", f"Revert PR #{pr_id}"], check=True)
    
    # Push changes to the main branch
    subprocess.run(["git", "push", "origin", "main"], check=True)

if __name__ == "__main__":
    # Get required arguments from the environment
    repo_owner = os.getenv('GITHUB_OWNER')
    repo_name = os.getenv('GITHUB_REPO')
    pr_id = os.getenv('PR_ID')
    github_token = os.getenv('GITHUB_TOKEN')

    if not repo_owner or not repo_name or not pr_id or not github_token:
        print("Required environment variables not set.")
        sys.exit(1)
    
    revert_pr(repo_owner, repo_name, pr_id, github_token)
