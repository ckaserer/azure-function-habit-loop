#!/bin/bash

set -euo pipefail

# Make sure these values are correct for your environment
resourceGroup="habit-loop-python-rest-api"
appName="habit-loop-python-rest-api"
location="westeurope" 

# Change this if you are using your own github repository
gitSource="https://github.com/ckaserer/azure-function-habit-loop.git"

az group create \
    -n $resourceGroup \
    -l $location

az appservice plan create \
    -g $resourceGroup \
    -n "linux-plan" \
    --sku B1 \
    --is-linux

az webapp create \
    -g $resourceGroup \
    -n $appName \
    --plan "linux-plan" \
    --runtime "PYTHON|3.7" \
    --deployment-source-url $gitSource \
    --deployment-source-branch master

az webapp config appsettings set \
    -g $resourceGroup \
    -n $appName \
    --settings WWIF="$SQLAZURECONNSTR_WWIF"
