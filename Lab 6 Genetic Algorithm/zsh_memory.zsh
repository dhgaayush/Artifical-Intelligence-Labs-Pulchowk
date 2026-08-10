#!/bin/zsh

# Make a file executable
chmod +x setup_venv.zsh

# Run an executable script
./setup_venv.zsh

# Run/source a script in the current shell
source setup_venv.zsh

# Create a Python virtual environment
python3 -m venv .venv

# Activate a Python virtual environment
source .venv/bin/activate

# Deactivate the virtual environment
deactivate


: <<'COMMENT'
==========================================
ZSH MEMORY NOTES
==========================================

This file is my personal command notebook.

I can open it whenever I forget a command.

COMMENT


: <<'COMMENT'
==========================================
FILE PERMISSIONS
==========================================

chmod +x filename

This gives the file execute permission.

The permission persists until it is changed
or the file is replaced/recreated.

COMMENT

# One caveat: this isn't technically a comment in Zsh. 
# ts a no-op (:) receiving a multiline here-document. 
# The shell effectively does nothing with the text, so it's commonly useful for 
# multiline notes.