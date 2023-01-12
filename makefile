SHELL = /usr/bin/env bash -o pipefail
.SHELLFLAGS = -ec

.PHONY: get
get: get-source get-prereqs

.PHONY: get-source
get-source:
	[ ! -d "./cpython" ] && \
		git clone --branch 3.9 https://github.com/python/cpython

.PHONY: get-prereqs
get-prereqs:
	sudo apt install libssl-dev zlib1g-dev libncurses5-dev \
	libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev \
	libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev libffi-dev

.PHONY: cpython
cpython:
	cd cpython 
	make -j2 -s
	cd ..