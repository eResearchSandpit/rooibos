# Vagrant dirs
export HOME_DIR=/home/vagrant
export VAGRANT_DIR=/vagrant
export PROVISION_DIR=$VAGRANT_DIR/.vagrant_provision
# MDID dirs
export MDID_DIR=$HOME_DIR/mdid
export MDID_DATA_DIR=$HOME_DIR/mdid-data
export CONFIG_DIR=$MDID_DIR/config
export ROOIBOS_DIR=$MDID_DIR/rooibos

# virtualenv/wraper defs for MDID
export WORKON_HOME=$HOME_DIR/.virtualenvs
export MDID_PY=$WORKON_HOME/mdid/bin/python
source /usr/local/bin/virtualenvwrapper.sh

# niceties for working on the command line

source $HOME_DIR/.git-prompt
source $HOME_DIR/.mdid-funcs

# source ~/.bash-completion  # replace with apt-get

GIT_PS1_SHOWDIRTYSTATE=true

PS1='\[`[ $? = 0 ] && X=2 || X=1; tput setaf $X`\]\h\[`tput sgr0`\]:$PWD\[\033[31m\]$(__git_ps1)\[`tput sgr0`\]\n\$'

# workon mdid

source /home/vagrant/.virtualenvs/mdid/bin/activate

echo "type 'mdid_help' for a list of mdid specific commands"



