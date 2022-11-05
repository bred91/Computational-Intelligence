## Notes
In this second lab, the aim is to solve the Lab1 problem through an EA. 
```diff
- Unfortunately, It was "Crunch Time" at  work, so I had very little time to do everything. :/
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
A further improvement could be to try to play with the Population Size and the Offspring Size in a dynamic way: make them change as the generations go by.
The current values were found experimentally.

An other idea could be to add an exit point when the population is the same for several generations (I made a little try, but I saw no great improvements).


NB: the code is partially inspired by the one developed by Prof Squillero.
<div dir="rtl"> Raffaele Pane </div>
