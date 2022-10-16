## Notes
Algorithm **A*** was chosen to solve the problem.
The reason is that, under the right assumptions, it is optimal and complete.
I tried other algorithms, but this one performed best in the tests.

For N equal:
- **5**: w=5 (bloat=0%) and a solution was found in 3 steps, visiting 32 states
- **10**: w=10 (bloat=0%) and a solution was found in 3 steps, visiting 692 states
- **20**: w=23 (bloat=15%) and a solution was found in 5 steps, visiting 15,595 states

For higher Ns, my configuration was unable to run it.

A further improvement could be to try to implement some king of optimizations, like Python Generators (I am quite new to the topic).
