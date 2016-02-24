# Example commands

## One max

population 20, adult size 10:
`pypy main.py --problem onemax --genotype-size 40 --population-size 20 --adult-pool-size 10 --adult-selection-method fgr --parent-selection-method fitness_proportionate -g 100 --num-runs 30 > log && python plot.py --average --output onemax_p20.png`

population 80, adult size 40:
`pypy main.py --problem onemax --genotype-size 40 --population-size 80 --adult-pool-size 40 --adult-selection-method fgr --parent-selection-method fitness_proportionate -g 100 --num-runs 30 > log && python plot.py --average --output onemax_p80.png`

population 320, adult size 160:
`pypy main.py --problem onemax --genotype-size 40 --population-size 320 --adult-pool-size 160 --adult-selection-method fgr --parent-selection-method fitness_proportionate -g 100 --num-runs 30 > log && python plot.py --average --output onemax_p320.png`


## Surprising sequences
`python main.py --problem ss --genotype-size 12 --alphabet-size 5 --num-generations 150 --population-size 100`
