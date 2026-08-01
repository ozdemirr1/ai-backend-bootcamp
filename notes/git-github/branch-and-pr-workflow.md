# Git Branch and Pull Request Workflow

## Goal

This note explains how to create, switch, and inspect Git branches while keeping new work separate from the stable `main` branch.

## What Is a Branch?

A branch is an independent line of development that points to a commit.

It allows us to develop and review a feature without changing the stable `main` branch directly. A branch does not create a second copy of every project file.

## Creating and Switching to a Branch

The following command creates a new branch and switches to it:

```bash
git switch -c feature/week-03-python-engineering
```

- `git switch` changes the active branch.
- `-c` creates a new branch before switching to it.
- `feature/week-03-python-engineering` describes the purpose of the work.

If the branch already exists, switch to it without `-c`:

```bash
git switch feature/week-03-python-engineering
```

## Checking the Current Branch

List local branches:

```bash
git branch
```

Git marks the active branch with `*`.

Print only the name of the active branch:

```bash
git branch --show-current
```

Show local branches together with their latest commits and upstream branches:

```bash
git branch -vv
```

## Inspecting Branch Pointers

The following command displays recent commits and branch labels:

```bash
git log -3 --oneline --decorate
```

When a feature branch is first created, it usually points to the same commit as `main`. After a new commit is added to the feature branch, its history moves ahead of `main`.

## Working Tree Check

After switching branches, check the repository state:

```bash
git status
```

Before starting new work, confirm that the expected branch is active and the working tree does not contain unrelated changes.

## Pull Request Workflow

A pull request proposes merging changes from one branch into another branch. It provides one place to review the commits, changed files, test results, and discussion before changing `main`.

For the Week 03 work:

- Base branch: `main`
- Compare branch: `feature/week-03-python-engineering`

### 1. Push the Feature Branch

The branch must exist on GitHub before opening a pull request:

```bash
git push -u origin feature/week-03-python-engineering
```

Later commits can be sent with:

```bash
git push
```

An open pull request updates automatically when new commits are pushed to its compare branch.

### 2. Review the Complete Branch Diff

Show all changes introduced by the feature branch:

```bash
git diff main...HEAD
git diff main...HEAD --name-status
git diff main...HEAD --check
```

Show only the commits that are not in `main`:

```bash
git log main..HEAD --oneline
```

The three-dot diff compares the feature branch with the point where it separated from `main`. This makes it useful for reviewing the complete pull request.

### 3. Run Quality Checks

Run the relevant checks before requesting a merge:

```bash
ruff check .
python -m pytest -q
python -m pip check
```

Passing local checks should be recorded in the pull request description. Local results are evidence from the developer's machine; automated GitHub checks require a CI workflow such as GitHub Actions.

If GitHub displays `Checks 0`, it means that no automated pull request checks are configured. It does not mean that a check failed.

### 4. Write a Clear Pull Request

A useful pull request includes:

- a short title that explains the outcome
- a summary of the important changes
- the commands and results used for verification
- review notes about limitations or important decisions

Example title:

```text
week-03: add Python engineering fundamentals and tooling
```

### 5. Review Before Merging

Check the following GitHub sections:

- `Conversation`: description, discussion, and merge status
- `Commits`: the branch history being proposed
- `Files changed`: the exact code and documentation changes
- merge status: conflicts with the base branch
- automated checks, when CI is configured

Do not merge only because GitHub says the branches can be merged. First confirm that the changes are intentional, documented, and tested.

## After the Pull Request Is Merged

Update the local `main` branch after the remote pull request is merged:

```bash
git switch main
git pull --ff-only origin main
```

After confirming that the feature commits are present in `main`, delete the local feature branch:

```bash
git branch -d feature/week-03-python-engineering
```

The remote feature branch can also be deleted after the merge. Branch deletion removes the branch pointer, not the commits that were merged into `main`.
