#!/bin/sh
wget http://nodejs.org/dist/v8.11.1/node-v8.11.1-linux-x64.tar.gz
tar xf node-v8.11.1-linux-x64.tar.gz -C /usr/local/
cd /usr/local/
mv node-v8.11.1-linux-x64/ nodejs
ln -s /usr/local/nodejs/bin/node /usr/local/bin
ln -s /usr/local/nodejs/bin/npm /usr/local/bin
echo -e "\033[32;49;1mEND\033[39;49;0m"!
