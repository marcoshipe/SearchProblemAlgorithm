# Search Problem Algorithm (State space search)

## The idea:
Present a generic algorithm to resolve Search Problems like Senku, labyrinth games, puzzle games, etc.  
You can solve problems where you can define a state (like a photo of the game) and how you go from one state to another.  
You do that, specify your initial state and the goal states (one or many), configure some options and you are done.  
This idea has many names, the more accurated that i found is [State Space Search](https://en.wikipedia.org/wiki/State_space_search) 

## The algorithm:
The main idea of the algorithm is generate the reachable states from the initial state in "one step" (let call them the **neighbors**), 
then choose one of them and genere its neighbors, and so on until a solution state is reached.  
To do that, the algorithm keep a set of states that it know that can reach from the start state (let's call this set the **frontier**).  
So, the algorithm choose one state from the frontier, check if it is a goal state, if not, then generate its neighbors and add them to the frontier, and start over.

## Configuration:
Some of the options you can configure is how you choose a state from the frontier, if it keep the states that were visited (the states that were selected from the frontier, generated its neighbors and discarted), if the algorithm search for the first solution or all of them, etc.

## TODO:
- Documentation
- Extend the VisitedMode and FrontierMode with more options
- Use the algorithm to get more game solutions
- clean the code a little
- play with cython?