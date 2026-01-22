#!/bin/bash

set -Euo pipefail

if [[ "${BASH_SOURCE[0]}" = "$0" ]]; then
    echo "This script should be sourced, not run directly."
    exit 1
fi

cur_dir=$(pwd)

# find what python version is installed
if command -v python3 &>/dev/null; then
    pyth=python3
elif command -v python &>/dev/null; then
    pyth=python
else
    echo "python is not installed."
    exit 1
fi

# find what type of bash/zsh settings file is being used
if [ -e ~/.bash_profile ]; then
    rc_file=.bash_profile
elif [ -e ~/.bashrc ]; then
    rc_file=.bashrc
elif [ -e ~/.zshrc ]; then
    rc_file=.zshrc
else
    echo "Neither .bash_profile, .bashrc nor .zshrc. exists."
    exit 1
fi

# add the alias to the bash/zsh settings file
echo "alias grades='$pyth $cur_dir/main.py'" >> ~/$rc_file
. ~/$rc_file
echo "successfully added alias 'grades' to $rc_file and sourced it."
echo "you can now run 'grades' from anywhere to start the program."





