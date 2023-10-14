# run "bash setting_up.sh" to execute this script

#!/bin/bash

# Detect the operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    my_string="I dont want to do this yet lmao"
    echo $my_string
elif [[ "$OSTYPE" == "darwin"* ]]; then
    pip install -r requirements.txt
elif [[ "$OSTYPE" == "win32" ]]; then
    pip install -r requirements.txt
else
    echo "Unsupported OS"
fi