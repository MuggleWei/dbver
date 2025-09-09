#!/bin/bash

origin_dir="$(dirname "$(readlink -f "$0")")"
cd $origin_dir

if [ -d _deps ]; then
	rm -rf _deps
fi
mkdir -p _deps

if [ -d tools ]; then
	rm -rf tools
fi
mkdir -p tools

cd _deps
git clone https://github.com/sqldef/sqldef.git --depth=1 --branch=v2.3.0

cd sqldef
make
cp -r build/*/mysqldef $origin_dir/tools
