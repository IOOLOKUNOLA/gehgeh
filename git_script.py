import os
import subprocess

def git_commit_and_push(repo_url, local_path, commit_message, branch="main", commit_count=103):
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

        # Loop for making and pushing commits
        for i in range(1, commit_count + 1):
            # Create or modify a file for each commit
            with open(f"file_{i}.txt", "w") as f:
                f.write(f"Content for commit {i}")

            # Stage the new file
            print(f"Staging file_{i}.txt for commit {i}...")
            subprocess.run(["git", "add", f"file_{i}.txt"], check=True)

            # Commit the change
            commit_msg = f"{commit_message} {i}"
            print(f"Committing changes for commit {i}...")
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)

            # Push the commit to the remote repository
            print(f"Pushing commit {i} to the remote repository...")
            subprocess.run(["git", "push", "--set-upstream", "origin", branch], check=True)

            print(f"Commit {i} pushed successfully!")

        print("All commits have been made and pushed successfully!")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")

# Example usage
repo_url = "https://github.com/IOOLOKUNOLA/gehgeh.git"  # Your repository URL
local_path = "/Users/user/gehgeh"  # Replace with your desired local path
commit_message = "Automated commit"  # Replace with your commit message
branch_name = "main"  # Replace with the branch you want to push to

git_commit_and_push(repo_url, local_path, commit_message, branch_name)
