#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    echo "Format: $0 <file_to_upload> <ID> <SUBIECT>"
    exit 1
fi

FILE=$1
ID=$2
SUBIECT=$3
if [ "$FILE" == "done" ]; then
    curl -X POST -d "link=$FILE&id=$ID&subiect=$SUBIECT" http://192.168.1.7/api/rezultate
    exit 0
fi
RESPONSE=$(curl -s -T "$FILE" https://bashupload.com)

echo "Response from bashupload.com:"
echo "$RESPONSE"

if echo "$RESPONSE" | grep -q "Uploaded"; then
    LINK=$(echo "$RESPONSE" | grep -Eo "(http|https)://[a-zA-Z0-9./?=_%:-]*")

    if [ -n "$LINK" ]; then
        echo "Link: $LINK"  

        curl -X POST -d "link=$LINK&id=$ID&subiect=$SUBIECT" http://192.168.1.7/api/rezultate
    else
        echo "Nu am putut extrage link-ul!"
        exit 1
    fi
else
    echo "Fisierul nu a putut fi uploadat!"
    exit 1
fi
