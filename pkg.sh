#!/bin/bash

origin_dir="$(dirname "$(readlink -f "$0")")"
cd $origin_dir

# build tools
./build_tools.sh

# install requirements
if [ -d venv ]; then
	rm -rf venv
fi
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# package
pyinstaller \
    -F main.py \
    --add-binary=tools/mysqldef:tools \
    --onefile \
    --distpath dist/bin -n dbver
