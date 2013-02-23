#!/bin/bash

#!/bin/bash
cd "$(dirname "$0")"

while [ 1 ];
do

  python data.py
  echo ""
  echo "Press ENTER to exit"
  read x

done