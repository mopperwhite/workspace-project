#!/bin/sh
#You can add following to ~/.bashrc
alias workspace=workspace.py
function toworkspace(){
cd `workspace`
}

function openworkspace(){
nautilus `workspace`
}
