## Notes
In this second lab, the aim is to solve the Lab1 problem through an EA. 
```diff
- Unfortunately, It was "Crunch Time" at  work, so I had very little time to do everything. :/
```
```diff
+ Below you can find some upgrades made after the lab week, expecially thanks to a deeper study, more time and the showdown lessons
```

The results were very close to the A* algorithm for small N values.
For larger Ns, where A* became computationally unsustainable, this algorithm performed very well, with a very good level of "purity" of the solution and very short calculation times.

| N | W | Bloat | Time |
| -- | ------ | ----- | ----------- |
| 5 | 5 | 0 % | 0.1670 s |
| 10 | 12 | 20 % | 0.2330 s |
| 20 | 27 | 35 % | 0.9530 s |
| 50 | 94 | 88 % | 5.7710 s |
| 100 | 223 | 123 % | 15.6456 s |
| 200 | 597 | 198 % | 52.1165 s |
| 500 | 1739 | 248 % | 281.0598 s |
| 1000 | 4100 | 310 % | 1003.7821 s |

### What's next
A further improvement could be to try to play with the Mutation Rate, the Population Size and the Offspring Size in a dynamic way: make them change as the generations go by.
The current values were found experimentally.

An other idea could be to add an exit point when the population is the same for several generations (I made a little try, but I saw no great improvements).

## Upgraded Version (2022/11/18)
Thanks to the fact that I had a few hours of free time, I was able to implement and test some of the things I had skipped to do when writing the solution for this lab.

In details:
- I added a variable mutation rate, which allows for more exploration in the early stages and more exploitation in the later ones
- the Fitness Hole trick
- a stop condition when the best individual is always the same for n generations (and coverage has already been reached)
- a control for possible clones in the offspring insertion phase into the population
- CallCounter

### What's next p2: the revenge
Again, the values of population_SIZE, offspring_SIZE and num_GENERATIONS were chosen experimentally. 
Ideally, given enough time, one could think of performing a sort of Grid Search, for each N, to find the optimal values.

Surely I should replace the use of lists for genes with tuples, perhaps even constructing the sort of bitmap I saw some colleagues use during their presentation.


<br><br><br>
NB: the code is partially inspired by the one developed by Prof Squillero.
<div dir="rtl"> Raffaele Pane </div>
