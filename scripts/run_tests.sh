#!/bin/sh

cd $( dirname $0 )/../

_cmd_exists() {
    which $1 &>/dev/null
}

_install_rsa() {
    apt-get install python-m2crypto
}

_install_pip() {
    # Mac都自带了
    if ! _cmd_exists pip
    then
        apt-get install -y python-pip
    fi

}

_install_tox() {
    pip install tox
}

_install_deps() {
    _install_pip
    _install_tox
    _install_rsa
}

# 安装Tox和RSA库
_install_deps &> /dev/null

tox -c misc/tox.ini "$@"
