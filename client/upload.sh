#!/bin/bash

if [ -z "$1" ]; then
    echo "Format: $0 <file_to_upload>"
    exit 1
fi

FILE=$1

if [ ! -f "$FILE" ]; then
    echo "Fisierul $FILE nu exista!"
    exit 1
fi

RESPONSE=$(curl -s bashupload.com -T "$FILE")

if echo "$RESPONSE" | grep -q "Uploaded"; then
    LINK=$(echo "$RESPONSE" | grep -o 'http://bashupload.com/[A-Za-z0-9]*/'"$(basename "$FILE")")
        python3 "$LINK"
    else
    echo "Fisierul nu a putut fi uploadat!"
    exit 1
fi
