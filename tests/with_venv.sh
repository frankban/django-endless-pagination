#!/bin/bash

TESTS=`dirname $0`
VENV=$TESTS/../.venv
source $VENV/bin/activate && $@
