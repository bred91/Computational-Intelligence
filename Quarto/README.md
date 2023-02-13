# Final Project
In this branch there is my final project of the Computational Intelligence 2022/2023 course.<br>
The aim is to write an agent that can play (and possibly be very strong) in playing the game Quarto.

To achieve this, I developed an agent based mainly on the MinMax algorithm, with Alpha-Beta Pruning and maximum depth.
In order to optimise performance, making it faster in choices and stronger in game skills, I also applied some customisations, such as:
- variable maximum depth
- fixed rules
- a more advanced scoring system
- time-based breaks
- not symmetric parameters 

<br>
With these additions, the agent is able to win an average of **98%** of the matches, with a fluctuation of +/- 2%. <br>
It tends to be able to finish a match in less than a second, with a maximum decision time for a single round of 5 seconds (although it very rarely reaches that point).
These statistics were collected by running a group of 100 matches 10 times (so, a total of 1000 matches). In one half the agent was the first player, in the other the second. The opponent for these tests has always been the random agent, but in general it has also been tried against humans and simple rule-based agents.<br>

<br> 
Overall, I think it has reached an all-round satisfying level of performance.
<br>

Of course, there is still room for improvement. Below are some ideas that I have left open, but which would be interesting to explore further.
-	Optimize the values of the maximum depth
-	Explore Symmetries
-	Explore the “not winning” matches
-	More complex starting rules
-	Code Optimization

<br>
For more details, I recommend you take a look at the report I compiled, where I explain everything thoroughly. <br><br>

Note: in the [discarded agents](https://github.com/bred91/Computational_Intelligence_2022-2023/tree/main/Quarto/discarded%20agents) directory there is the RL agent that I developed, but at the end discarded. I uploaded it just for reference.

<br><br><br>
<div dir="rtl"> Raffaele Pane </div>
