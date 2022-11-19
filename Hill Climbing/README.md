## Notes
I resolved, using a Vanilla Hill Climber, both the Sphere and the Rastrigin problem.

I consider the problem solved when the distance from 0 is less than 10^-5 (for me, it is reasonably near to zero! ;) )

For Rastrigin, I added some lines to escape from a local maxima. 
First, I always keep a variable with the best solution. 
If I have the same solution unbeated for 100 iteration, I start from an other random point of the space.

### Sphere
Solution: [-0.00050693  0.00240757]<br>
Peak: -6.05336806868649e-06<br>
Iterations: 1434<br>

### Rastrigin
Solution: [ 3.87523565e-06 -2.22163573e-04]<br>
Peak: -9.794947238476994e-06<br>
Iterations: 349029

<br><br><br>
NB: the code is partially inspired by the one developed by Prof Squillero.
<div dir="rtl"> Raffaele Pane </div>
