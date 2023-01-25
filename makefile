SHELL = /usr/bin/env bash -o pipefail
.SHELLFLAGS = -ec

.PHONY: get
get: get-source get-prereqs

.PHONY: get-source
get-source:
	if [ ! -d "./cpython" ]; then \
		git clone --branch 3.9 https://github.com/python/cpython; \
	fi;

.PHONY: get-prereqs
get-prereqs:
	OS=$$(cat /etc/os-release | grep -Po '(?<=^ID=).*'); \
	if [ "$${OS}" == "arch" ]; then \
		sudo pacman -S libssl-dev zlib1g-dev libncurses5-dev \
		libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev \
		libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev libffi-dev; \
	else \
		sudo apt install libssl-dev zlib1g-dev libncurses5-dev \
		libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev \
		libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev libffi-dev; \
	fi;

.PHONY: cpython
cpython:
	cd cpython; \
	make -j2 -s; \
	cd ..; 