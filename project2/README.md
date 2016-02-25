# Example commands

## One-Max

40 bits, full generational replacement, sigma scaling, population size = 320:
`pypy main.py --problem onemax --genotype-size 40 --population-size 320 --adult-selection-method full_generational_replacement --parent-selection-method sigma_scaling --num-generations 100 --num-runs 100 --mutation-rate 0.25 --crossover-rate 0.75 > log && python plot.py --average --solution-found --legend --output plot11_sigma_scaling.png`

## LOLZ
40 bits, zero cap = 21 full generational replacement, sigma scaling, population size = 320:
`pypy main.py --problem lolz --genotype-size 40 --zero-cap 21 --population-size 320 --adult-selection-method full_generational_replacement --parent-selection-method sigma_scaling --num-generations 100 --num-runs 100 --mutation-rate 0.25 --crossover-rate 0.75 > log && python plot.py --average --solution-found --legend --output plot11_sigma_scaling.png`


## Surprising sequences
locally surprising, S = 3:
`pypy main.py --problem ss --genotype-size 2 --alphabet-size 3 --num-generations 150 --population-size 100 --stop-early --surprising-sequences-find-longest --num-runs 15 --silent --surprising-sequences-mode local`

locally surprising, S = 5:
`pypy main.py --problem ss --genotype-size 2 --alphabet-size 5 --num-generations 150 --population-size 100 --stop-early --surprising-sequences-find-longest --num-runs 15 --silent --surprising-sequences-mode local`

globally surprising, S = 3:
`pypy main.py --problem ss --genotype-size 2 --alphabet-size 3 --num-generations 150 --population-size 100 --stop-early --surprising-sequences-find-longest --num-runs 15 --silent --surprising-sequences-mode global`

globally surprising, S = 5:
`pypy main.py --problem ss --genotype-size 2 --alphabet-size 5 --num-generations 150 --population-size 100 --stop-early --surprising-sequences-find-longest --num-runs 15 --silent --surprising-sequences-mode global`
