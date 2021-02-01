#!/usr/bin/bash

if [ $# -ne 3 ]; then
   echo "USAGE: $0 infile outfile wordlist"
   exit 1
fi

rm -f $2

while read password; do
   echo -n "Trying: $password... "
   gpg --batch --no-tty -o $2 --cipher-algo AES256 --passphrase $password -d $1 &> /dev/null
   if [ $? -eq 0 ]; then
      echo 'SUCCESS'
      exit 0
   else
      echo 'FAILED'
   fi
done < $3
exit 1