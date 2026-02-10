#!/usr/bin/env bash

# ensure user has their own python venv (required by python these days)
if [ ! -d ~/pbl-venv ]; then
    # create python environment
    echo "creating environment"
    python3 -m venv ~/pbl-venv

    # ensure bash terminals automatically use the virtual environment
    echo "adding 'source ~/pbl-venv/bin/activate to .bashrc"
    grep -v "# managed by PBL" ~/.bashrc > ~/.bashrc.tmp && mv ~/.bashrc.tmp ~/.bashrc
    echo "source ~/pbl-venv/bin/activate # managed by PBL" >> ~/.bashrc
else
    echo "skipping creation: ~/pbl-env already exists"
fi

