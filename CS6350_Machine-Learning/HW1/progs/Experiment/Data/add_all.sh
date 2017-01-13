#!/bin/bash

find . -maxdepth 1 -name ".txt" -exec ./add_definitions.sed {} \;
