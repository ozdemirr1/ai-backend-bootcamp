# Week 01 Report

## Date

14 July - 17 July

## Main Focus

- Bootcamp repository setup
- Git/GitHub workflow
- Terminal basics
- Markdown notes
- HTTP/REST introduction
- Codex workflow setup

## What I Completed

- [x] Created bootcamp folder structure
- [x] Created README.md
- [x] Created ROADMAP.md
- [x] Created DECISIONS.md
- [x] Created AGENTS.md
- [x] Practiced terminal commands
- [x] Practiced Git commands
- [x] Wrote HTTP basics notes
- [x] Wrote REST API design notes
- [x] Created OpsDesk ticket API design notes
- [x] Pushed changes to GitHub

## What I Learned

- I learned the basic Git workflow: status, add, commit, push, log, and diff.
- I learned that git status shows the current repository state.
- I learned that git diff helps review changes before committing.
- I learned that git log shows the commit history.
- I learned basic terminal commands such as pwd, ls, cd, mkdir, touch, echo, cat, rm, and rmdir.
- I learned the basics of HTTP request and response structure.
- I learned the difference between common HTTP methods such as GET, POST, PUT, PATCH, and DELETE.
- I learned that 401 means unauthenticated, while 403 means authenticated but not authorized.
- I learned that 204 No Content means the request succeeded but the server does not return a response body.
- I learned how to think about REST API endpoint design using resources and HTTP methods.
- I practiced choosing HTTP status codes for backend API scenarios.
- I created a first API design draft for the OpsDesk ticket system.

## Problems I Faced

- I accidentally created `https-basics.md` instead of `http-basics.md`.
- I accidentally committed a personal `.rtf` context file.
- I confused `204 No Content` with `404 Not Found`.
- I saw that `git diff` does not show untracked file contents before staging.
- I made small Markdown formatting mistakes while writing notes.

## How I Solved Them

- I renamed `https-basics.md` to `http-basics.md`.
- I removed the personal `.rtf` file from Git tracking and added `*.rtf` to `.gitignore`.
- I learned that `204` means successful request with no response body, while `404` means resource not found.
- I used `git diff --staged` to review staged new files.
- I cleaned up Markdown formatting in the notes.

## Interview Questions I Can Answer

- What is Git?
- What is a Git commit?
- What is a Git branch?
- What is the difference between commit and push?
- What is HTTP?
- What is the difference between request and response?
- What is the difference between GET and POST?
- What is the difference between PUT and PATCH?
- What is the difference between 401 and 403?
- What is the difference between 204 and 404?
- What is REST API design?
- Why should REST endpoints use nouns instead of verbs?

## Next Week Goals

- Python fundamentals
- Virtual environment
- Functions
- Data structures
- File handling
- Basic CLI project