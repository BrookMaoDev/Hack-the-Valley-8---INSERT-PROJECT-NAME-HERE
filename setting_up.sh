# run "bash setting_up.sh" to execute this script

#!/bin/bash

# Detect the operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    pip install -r requirements.txt

elif [[ "$OSTYPE" == "darwin"* ]]; then
    my_string="I dont want to do this yet lmao"
    echo $my_string

elif [[ "$OSTYPE" == "win32" ]]; then
    pip install -r requirements.txt
    pip install cython
    pip install git+https://github.com/philferriere/cocoapi.git
else
    echo "Unsupported OS"
fi