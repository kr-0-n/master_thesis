# Evolutionary Solve
If a pod gets scheduled on Node 3, all pods will end up there (performance penalty on nodes is lower than on the network)

On Network Change the network_administration triggers the optimize function of the scheduler. I am not sure if this is the right separation of concerns

- This is a problem for all algorithms
TODO: FIX NETWORK SEGMENTATION
TODO: Introduce network calculus