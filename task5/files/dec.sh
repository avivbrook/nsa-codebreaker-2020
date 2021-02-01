#!/usr/bin/bash

FILE=$1
LIST=${2:-keyivlist}

date=${FILE%.log}
name=${date##*/}
echo -n "-> Cracking $name.log "
while read K iv; do
    openssl enc -in $FILE -d -aes-128-cbc -K $K -iv $iv -out $name.dec &> /dev/null
    if [ "$(head -c3 $name.dec)" == '$GN' ]; then
        printf "\nSUCCESS: K=$K, iv=$iv\n"
        exit 0
    else
        echo -n '.'
    fi
done < $LIST
printf "\nFAILED\n"
exit 1
