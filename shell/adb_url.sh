#!/bin/bash

BASEDIR=$(dirname "$0")

FILE=$(basename "$1")

EXTENSION="${FILE##*.}"

if [[ $EXTENSION == "apk" ]]; then

    find "${BASEDIR}/temp" -maxdepth 1 -name "*.apk" -type f -delete
    wget -N $1 --no-check-certificate -P "${BASEDIR}/temp"
    adb install -f "${BASEDIR}/temp/${FILE}"

else
    echo -e "\e[01;31mThe URL does not contain .apk\e[0m"
fi