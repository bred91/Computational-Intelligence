## Notes
In this second lab, the aim is to solve the Lab1 problem through an EA. 
Unfortunately, It was "Crunch Time" at  work, so I had very little time to do everything. :/

The results were very close to the A* algorithm for small N values.
For larger Ns, where A* became computationally unsustainable, this algorithm performed very well, with a very good level of "purity" of the solution and very short calculation times (for N = 1000 it took just under 3 minutes!!! ).

| N | W(Cost) | Bloat | Elapsed Time |
| --| ------- | ----- | ----------- |
| 5 | 5 | 0 % | 0.1370 s |
| 10 | 12 | 20 % | 0.1920 s |
| 50 | 68 | 36 % | 1.0620 s |
| 100 | 149 | 49 % | 2.6230 s |
| 200 | 318 | 59 % | 8.1200 s |
| 500 | 679 | 36 % | 46.8120 s |
| 1000 | 1401 | 40 % | 173.4312 s |

### What's next
A further improvement could be to try to play with the Population Size and the Offspring Size in a dynamic way: make them change as the generations go by.
The current values were found experimentally.


NB: the code is partially inspired by the one developed by Prof Squillero.
<div dir="rtl"> Raffaele Pane </div>
