# Meeting Prep
## Simulation tool
Goal: Learn about algorithms and test feasability\
Sart with random algorithm
### Network Graph
1. Pods
2. Nodes
3. Links
4. Wanted Connections in Green
### Evaluation Function
Not very mature right now. Penalizes unconnected pods, overloaded nodes and overloaded links. Searches for shortest connections between pods.
### Algorithms
#### Random
Just for testing reasons, no significance

#### Perfect Solve
A perfect solver which tries every single possible configuration and evaluates them. Terminates early of perfect configuration was found (evaluation of 0).

#### Evolutionary Solve
Is able to mutate solutions, generate multiple generations and always select the best candidates. Cross Mixing of solutions is not supported (yet)

#### Ant Colony Solve
Used ant colony optimization to solve. Ants can only advance to 1-Step neighbours. Pheromone update routine could be improved. (Activate visualizer here to see how Ants advance)

#### Simulated annealing Solve
I was not certain if this actually makes sense. I created a full function evaluation graph and measured its entropy. Looks like Simulated annealing could make sense.

## Essay/Thesis
### Taxonomy
I learned a lot during the last weeks and my current approach is narrow and incomplete - The taxonomy would be as well. All but one of the suggested methods are to be categorized as mathematical optimization. We could potentially leave it like this, but its harder to introduce a taxonomy here.
### Papers
I did not have time to read through

## Misc
I will be gone the next 3 weeks\
Will miss the first few sessions in performance analysis :grr: