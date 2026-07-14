## What I Learned
- 14 July Tuesday
- Today I learned the basic Git workflow: checking repository status, staging changes, creating commits, connecting a local repository to GitHub, renaming the main branch, and pushing local commits to a remote repository.

git status : 
    Shows the current state of the repository. It checks which files have been modified, which are staged, if there is anything to commit, and the status of the branch. It indirectly performs an "Is Git initialized?" check; it will throw an error anyway if it is not a repository.

git add . : 
    Adds the modified files to the preparation area called the staging area. This essentially means, "I want to include these changes in the next commit."

git commit -m "..." : 
    Records the changes from the staging area into the local Git history. The message part should briefly and meaningfully explain why this change was made.

git remote add origin "address" : 
    Establishes a connection between the local repository and the remote repository on GitHub. origin is the traditional name given to the remote repository.

git branch -M main : 
    Changes the name of the active branch to main. The branch command is used to manage branches, and the -M flag forces the renaming.

git push -u origin main : 
    Sends the local main branch to the origin repository on GitHub. Thanks to the -u flag, just typing git push will be enough for future pushes.

touch : 
    Used to create a new empty file.

echo : 
    Used to write text to a file from the terminal. Example: echo "text" > file.md