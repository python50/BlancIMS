#!/bin/bash

#!/bin/bash
cd "$(dirname "$0")"

while [ 1 ]
do

python dbwiz.py

echo "PRESS ENTER TO RESTART"
read x
clear

done
