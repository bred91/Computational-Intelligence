## Notes
In this third lab, the aim is to create some agents capable of playing Nim. 

NOTE: 
>since I wrote most of the code before the professor's specifications about the testing and the rules, there are some things that are a bit different from the expected ones. For example, I wrote some cells in which a human can play with the agent! ;D

Task 3.1 , 3.2 and 3.3 are all made in weeks 9/10, so before december 4th.
Task 3.4 was made in week 11, so before december 12th
<br><br>


### Task 3.1: An agent using fixed rules based on *nim-sum* (i.e., an *expert system*)
For the first task my idea is to write a basic agent based on rules that is able to play randomly in the first stage and then wisely in the latest ones. 
In fact, by keeping track of the number of columns with only 1 object and those with several objects, the agent is able to understand whether it is convenient for him to take all values from one row or N-1 (or k if there is that limit).
![image](https://user-images.githubusercontent.com/58046025/205091367-9c7acd59-ec6b-4366-bace-f7d4f36e80bf.png)

Since it is very simple and the idea it is not so clever, comparing it with a random agent it show us that is barely better.
![image](https://user-images.githubusercontent.com/58046025/205091978-7a80747d-f2cc-417e-9449-2220f68ca17b.png)


### Task 3.2: An agent using evolved rules
Starting from the agent of task 3.1, I tried to parameterise the conditions that trigger actions. 
Once this was done, I used a GA algorithm to find the optimal values of the 3 parameters I had selected. The idea was to use a list of the 3 values (initially random) as the genome, as fitness the percentage of matches won against the random agent, mutation is the replacement of one of the values with any other from the search space and crossover is the classic one.
Once N generations had passed, I took the best individual and used the values within its genome to test against the random agent. The result shows a good improvement in the number of matches won.
![image](https://user-images.githubusercontent.com/58046025/205097037-dc13ad0f-98b5-4462-b7f3-c30c749a5ac2.png)

### Task 3.3: An agent using minmax
In this task, I developed two versions of Minmax: (a) a Vanilla version, which is quite computationally heavy, and a version using Alpha-Beta Pruning (b), which is much lighter.
In both cases, the algorithm will be unbeatable! :(

### Task 4.4: An agent using reinforcement learning
For this task I trained 2 agents using a Q-learning approch, one against a random player, the other against minsum (optimal).
In both cases the agent was capable to learn how to beat the adversarial and win a good rate of matches (>95%)
![image](https://user-images.githubusercontent.com/58046025/206915904-775c2278-8f1e-42b8-bd7a-6ad52f187e2b.png)

VS Random - **97 %**<br>
![image](https://user-images.githubusercontent.com/58046025/206916026-eb0863b3-cf60-4598-8710-2e5507f18320.png)

VS Optimal - **97 %**<br>
![image](https://user-images.githubusercontent.com/58046025/206916044-98eff11a-955c-4975-a0bb-df39bb07f05d.png)

Obviously, there is room for improvements. 
I implemented several parametes, but for lack of time I used them in a fixed way. Probably, playing a little bit with them, and changing them during the epochs, will lead to better results.

Note:
In a couple of occations I was stuck and I took ispiration from this code made by the user [abelmariam](https://github.com/abelmariam/nimPy)

<br><br><br>
<div dir="rtl"> Raffaele Pane </div>
