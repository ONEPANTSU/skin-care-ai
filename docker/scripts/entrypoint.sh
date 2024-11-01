#!/bin/bash

PORT=${PORT:-8000}

while getopts "p:" opt; do
  case ${opt} in
    p )
      PORT=$OPTARG
      ;;
    \? )
      echo "Usage: cmd [-p port]"
      exit 1
      ;;
  esac
done

python -m src.server -m "$MODEL" -p $PORT