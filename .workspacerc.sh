#!/usr/bin/env bash

#Add ". '.workspacerc.sh'" to .bashrc
alias workspace=python workspace.py
function toworkspace(){
cd `workspace $1`
}
function openworkspace(){
nautilus `workspace`
cd `workspace`
}
function towork(){
	cd `workspace work $1`
}
function workon(){
	nautilus `workspace work $1`
	cd `workspace work $1`
}

