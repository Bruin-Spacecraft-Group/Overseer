# Overseer 2021-22

## Installation

Ensure you have a terminal available (recommended for MacOS/Linux).

Clone the repository into your system.
```bash
git clone https://github.com/Bruin-Spacecraft-Group/Overseer.git
```

## Developing your first feature

Create your own branch for individual development:
```bash
cd Overseer
git checkout -b '<insert development-First_Last>'
```
For example:
```bash
cd Overseer
git checkout -b development-John_Smith
```

## Uploading your feature

To push your local feature in your branch to the remote repository:
```bash
git add .                                                 # add all modified files to commit 
git status                                                # check what files are modified
git commit -am '<your message here>'                      # create a commit + message about feature
git push --set-upstream origin '<development-First_Last>' # push commit to remote repository
```
For example:
```bash
git push --set-upstream origin development-John_Smith
```

## Creating and submitting a pull request

All commits into our remote repository must be first reviewed as a pull request (PR) before the feature can be merged with our main branch. On visiting the repository after your push, click 'Create a new pull request', and add your feature name, description, and other related information. 

To see all pull requests, click ![here](https://github.com/Bruin-Spacecraft-Group/Overseer/pulls). 

## Viewing archive

To view old files in Overseer, click ![here](https://github.com/Bruin-Spacecraft-Group/Overseer/tree/1de8b506c905792a38530c1407036a0f964ff9db.
)
