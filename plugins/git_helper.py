import os
import subprocess
import requests
from utils.logger import get_logger

logger = get_logger("git_helper")

class GitHelperPlugin:
    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        if not args:
            return "Available commands: clone <repo_url> [dir], commit <message>, push, latest <repo_url>"
            
        command = args[0].lower()
        try:
            if command == "clone" and len(args) > 1:
                clone_dir = args[2] if len(args) > 2 else ""
                return self.clone_repo(args[1], clone_dir)
            elif command == "commit" and len(args) > 1:
                return self.commit_changes(" ".join(args[1:]))
            elif command == "push":
                return self.push_changes()
            elif command == "latest" and len(args) > 1:
                return self.get_latest_commit_info(args[1])
            else:
                return f"Unknown command: {command}"
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {str(e)}")
            return f"Git operation failed: {str(e)}"
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return f"Error: {str(e)}"

    def clone_repo(self, repo_url, clone_dir=""):
        command = f"git clone {repo_url} {clone_dir}" if clone_dir else f"git clone {repo_url}"
        subprocess.run(command, shell=True, check=True)
        logger.info(f"Cloned repository: {repo_url} to {clone_dir or 'current directory'}")
        return f"Cloned repository from {repo_url}"

    def commit_changes(self, commit_message):
        subprocess.run(f"git add .", shell=True, check=True)
        subprocess.run(f"git commit -m '{commit_message}'", shell=True, check=True)
        logger.info(f"Committed changes: {commit_message}")
        return f"Changes committed with message: {commit_message}"

    def push_changes(self):
        subprocess.run("git push", shell=True, check=True)
        logger.info("Pushed changes to remote repository")
        return "Pushed changes to the remote repository."

    def get_latest_commit_info(self, repo_url):
        api_url = f"https://api.github.com/repos/{repo_url}/commits"
        response = requests.get(api_url)
        if response.status_code == 200:
            commits = response.json()
            latest_commit = commits[0]
            info = f"Latest commit: {latest_commit['commit']['message']} by {latest_commit['commit']['author']['name']}"
            logger.info(f"Fetched latest commit info: {info}")
            return info
        else:
            logger.error(f"Failed to fetch commits for {repo_url}")
            return "Unable to fetch the latest commit."

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    git_helper = GitHelperPlugin()
    return git_helper.run(*args, **kwargs)
