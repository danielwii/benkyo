#!/bin/bash
echo '[x] update assets...'
yarn

rm -rf ui/static/libs ui/static/fonts
mkdir -p ui/static/libs
mkdir -p ui/static/fonts

cp -f node_modules/bulma/css/bulma.css ui/static/libs/bulma.css
cp -f node_modules/font-awesome/css/font-awesome.css ui/static/libs/font-awesome.css

cp -rf node_modules/font-awesome/fonts/ ui/static/fonts/

echo '[x] ^_^ done!'
