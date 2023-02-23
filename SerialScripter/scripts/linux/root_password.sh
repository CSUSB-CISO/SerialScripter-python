#!/bin/bash

# password_scheme=$1
# magic_num=$2
# last_octet=$3

extension=$(($2 * $3))3
if [ $# -ne 3 ]; then
    echo "Need three arguments: "
    echo "Usage: 1 = password scheme"
    echo "Usage: 2 = magic number"
    echo "Usage: 3 = last octet"

  exit 1
fi


echo "Changing password for root user..."
echo "root:$1$extension" | chpasswd
if [ "$?" -eq "0" ]; then
    echo "Password changed successfully."
else
    echo "Failed to change password."
fi
