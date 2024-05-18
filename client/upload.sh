#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Format: $0 <file_to_upload> <ID>"
    exit 1
fi

FILE=$1
ID=$2

if [ ! -f "$FILE" ]; then
    echo "Fisierul $FILE nu exista!"
    exit 1
fi

RESPONSE=$(curl -s bashupload.com -T "$FILE")

if echo "$RESPONSE" | grep -q "Uploaded"; then
    LINK=$(echo "$RESPONSE" | grep -o 'http://bashupload.com/[A-Za-z0-9]/[A-Za-z0-9].[A-Za-z0-9]')
    echo "Link: $LINK$FILE"  # Print the link

    # Post the link and ID to a web server
    curl -X POST -d "link=$LINK&id=$ID" http://192.168.1.7/api/rezultate

else
    echo "Fisierul nu a putut fi uploadat!"
    exit 1
fi
