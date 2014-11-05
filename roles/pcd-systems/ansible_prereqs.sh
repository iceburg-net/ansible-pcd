#!/bin/sh

# installed ansible managed node requirements (python >= 2.5)

if [ ! -f /root/.ansible_prereqs_installed ]; then

    if [ -n "$(command -v yum)" ]; then
      yum -y install python
    elif [ -n "$(command -v apt-get)" ]; then
      apt-get -y install python
    elif [ -n "$(command -v pacman)" ]; then
      pacman -S --noconfirm python
    else
      echo "FAILURE - unsupported package manager"
      exit 99;
    fi
    
    if [ "$?" -ne "0" ]; then
      echo "FAILURE - package manager failed to install python"
      exit 1
    fi
    
    echo "SUCCESS - installed"
    touch /root/.ansible_prereqs_installed
fi