import os
import subprocess

def git_commit_and_push(repo_url, local_path, commit_message, branch="main"):
    try:
        # Check if the repository already exists locally
        if not os.path.exists(local_path):
            print("Cloning the repository...")
            subprocess.run(["git", "clone", repo_url, local_path], check=True)
        else:
            print("Repository already exists locally.")

        # Change directory to the repository
        os.chdir(local_path)

        # Check if the branch exists locally
        branches = subprocess.run(["git", "branch"], capture_output=True, text=True)
        if branch not in branches.stdout:
            print(f"Branch '{branch}' not found locally. Attempting to switch or create it...")
            # Try checking out the branch if it exists remotely
            try:
                subprocess.run(["git", "checkout", branch], check=True)
            except subprocess.CalledProcessError:
                # Create the branch if it doesn't exist
                print(f"Creating branch '{branch}' locally...")
                subprocess.run(["git", "checkout", "-b", branch], check=True)
        else:
            print(f"Switching to branch '{branch}'...")
            subprocess.run(["git", "checkout", branch], check=True)

        # Check if the repository is empty
        if not os.listdir(local_path):
            print("Repository is empty. Adding a README.md file...")
            with open("README.md", "w") as f:
                f.write("# New Repository\nThis is an initial README file.")
            subprocess.run(["git", "add", "README.md"], check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)

        # Stage all changes
        print("Staging all changes...")
        subprocess.run(["git", "add", "."], check=True)

        # Commit changes
        print("Committing changes...")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push changes to the remote repository
        print("Pushing changes to the remote repository...")
        subprocess.run(["git", "push", "--set-upstream", "origin", branch], check=True)

        print("Changes committed and pushed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")

# Example usage
repo_url = "https://github.com/IOOLOKUNOLA/gehgeh.git"  # Your new repository URL
local_path = "/Users/user/gehgeh"  # Replace with your desired local path
commit_message = "Initial commit or update"  # Replace with your commit message
branch_name = "main"  # Replace with the branch you want to push to

git_commit_and_push(repo_url, local_path, commit_message, branch_name)
