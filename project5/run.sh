#! /bin/bash
rm plots/*
pypy main.py -p $1 -g $2
python plot.py --plot-every $3
feh plots/
