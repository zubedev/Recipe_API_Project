#!/bin/bash

STATUS=$1
OWNER=$2
REPO=$3
TOKEN=$4
COMMIT=$5
URL=$6

curl "https://api.github.com/repos/$OWNER/$REPO/statuses/$COMMIT" \
      -H "Authorization: token $TOKEN" -X POST \
      -d "{\"state\": \"$STATUS\", \"context\": \"continuous-integration/jenkins\", \"description\": \"$STATUS\", \"target_url\": \"$URL\"}"