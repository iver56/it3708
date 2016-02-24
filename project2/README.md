# Example commands

## One max

40 bits, full generational replacement, fitness proportionate, population size 300:
`pypy main.py --problem onemax --genotype-size 40 --population-size 300 --adult-selection-method full_generational_replacement --parent-selection-method fitness_proportionate --num-generations 100 --num-runs 100 > log && python plot.py --average --answer-found --legend --output plot.png`

## Surprising sequences
`pypy main.py --problem ss --genotype-size 12 --alphabet-size 5 --num-generations 150 --population-size 100`
