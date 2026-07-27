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

This section will be completed after practicing the first pull request.
