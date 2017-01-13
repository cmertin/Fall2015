#!/bin/bash

# Install iPython and all that cool stuff
sudo yum install -y ncurses-devel
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
sudo rpm -Uvh epel-release-latest-7.noarch.rpm
sudo yum update
sudo yum -y install emacs emacs-auctex texlive-wrapfig expect-devel
sudo yum -y libpng-devel freetype-devel graphviz graphviz-python graphviz-devel
sudo yum install -y python-pip
sudo pip install ipython[all]
sudo pip install matplotlib
sudo pip install pygraphviz

# Install flash player
sudo rpm -ivh http://linuxdownload.adobe.com/adobe-release/adobe-release-x86_64-1.0-1.noarch.rpm
sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-adobe-linux
yum -y install flash-plugin nspluginwrapper alsa-plugins-pulseaudio libcurl

# Install org-mode
mkdir git
cd git
git clone git://orgmode.org/org-mode.git
cd org-mode
make
sudo make install
cd
wget http://www.emacswiki.org/emacs/download/htmlize.el
mkdir ~/.emacs.d/lisp/
mv htmlize.el ~/.emacs.d/lisp/htmlize.el
sed -i "1i(require 'htmlize)" ~/.emacs
sed -i "1i(load \"htmlize\")" ~/.emacs
sed -i "1i(add-to-list 'load-path \"~/.emacs.d/lisp/\")" ~/.emacs

# Install all of LaTeX
wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
tar -xvzf install-tl.unx.tar.gz
cd install-tl-*
expect -c "spawn -nottyinit sudo ./install-tl; expect -re \".*command:.*\"; send I\r; interact"
