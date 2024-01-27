#!/bin/bash

set -eux

for FILE_DIR in "$@"; do

    if [ "${CHECK_ONLY}" = "true" ];
    then
        black "${FILE_DIR}" --check --diff
        isort "${FILE_DIR}" --check-only
    else
        black "${FILE_DIR}"
        isort "${FILE_DIR}"
    fi
    
    flake8 --max-line-length 88 "${FILE_DIR}"
done
