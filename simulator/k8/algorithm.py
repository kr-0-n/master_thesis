from random import Random
import itertools
from k8.evaluator import evaluate, evaluate_step
from visualizer import draw_graph
import conf
import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np
from metrics import update_metric
from utils import *
import hashlib

rnd: Random = Random()
rnd.seed(10)

def random(graph: nx.Graph, pod=None, debug=False, visualize=False):
    """
    A function that adds a node to the graph and attaches it to a randomly chosen existing node.
    Takes input parameters node and graph, with optional debug and visualize flags. 
    Returns the updated graph after adding the node and edge.
    """
    global rnd
    if pod is None:
        pod = rnd.choice(get_pod_ids(graph))
        # get node with all attributes
        pod = (pod, graph.nodes[pod])
        graph.remove_node(pod[0])
    #add node to graph
    # print(pod)
    graph.add_node(pod[0], **pod[1])
    #attach new node to random existing node
    graph.add_edge(pod[0], rnd.choice(get_node_ids(graph)),  type="assign")
    #graph.add_edge(1 , node[0])
    # update_metric("num_eval_func_calls", 0)
    return graph

def assign_pods_to_nodes(nodes, pods):
    # Generate all possible assignments (with repetition) of pods to nodes
    assignments = list(itertools.product(nodes, repeat=len(pods)))

    # Pair the pods with their corresponding node assignments
    result = []
    for assignment in assignments:
        result.append(list(zip(pods, assignment)))

    return result

def perfect_solve(graph, pods=None, debug=False, visualize=False):
    """
    A function that adds a node to the graph and tries all possible connections.
    Takes input parameters node and graph, with optional debug and visualize flags. 
    Returns the best graph after adding the node and edge.
    """
    if pods != None:
        for pod in pods:
            graph.add_node(pod[0], **pod[1])
    #try all node-pod connections
    set_of_nodes = list(node for node in graph.nodes if graph.nodes[node]["type"] == "node")
    set_of_pods = list(pod for pod in graph.nodes if graph.nodes[pod]["type"] == "pod")
    
    assignments = assign_pods_to_nodes( set_of_nodes, set_of_pods)
    # print(assignments)
    solutions_checked = 0
 
    current_best = (evaluate(graph), graph)
    print(f"now checking {len(set_of_nodes)} ^ {len(set_of_pods)} assginments")
    for combination in assignments:
        solutions_checked += 1
        # create new graph
        new_graph = graph.copy()
        # remove all assignmentscalc
        new_graph.remove_edges_from((edge for edge in new_graph.edges if new_graph.edges[edge]["type"] == "assign"))
        assigned_pods = []
        if debug:
            print("#"*50)
            print(f"combination: {combination}")
        for assignment in combination:
            new_graph.add_edge(assignment[1], assignment[0], type="assign")
        
        evaluation = evaluate_step(graph, new_graph, debug=False)
        if evaluation < current_best[0]:
            current_best = (evaluation, new_graph)
            if visualize:
                draw_graph(new_graph, conf.graph, "Evaluation: " + str(evaluation))
            if debug:
                print(f"new best: {current_best[0]}")
            if evaluation == 0:
                print(f"checked {solutions_checked} combinations")
                update_metric("num_eval_func_calls", solutions_checked)
                return current_best[1]
        else:
            if debug:
                print(f"evaluation: {evaluation}")

    print(f"checked {solutions_checked} combinations")
    update_metric("num_eval_func_calls", solutions_checked)
    return current_best[1]

def evolutionary_solve(graph, pods=None, debug=False, visualize=False):
    """
    A function that performs an evolutionary solve on the input graph.
    Parameters:
        pod: The pod to be used in the evolutionary solve.
        graph: The graph on which the evolutionary solve will be performed.
        debug: A flag to enable/disable debugging information (default is False).
    Returns:
        The best graph after performing the evolutionary solve.
    """
    global rnd
    generations = 100
    chilren_per_parent = 35
    survivors_per_generation = 22

    initial_unassigned = graph.copy()

    # connect new pod to the same node as its wanted connection pod
    first_solution = graph.copy()
    if pods != None:
        # This is a questionable approach which decreases the performance.
        # # choose random connection from the wanted connections
        # if len(pod[1]["network"]) > 0:
        #     first_solution.add_node(pod[0], **pod[1])
        #     connection = rnd.choice(pod[1]["network"])
        #     if connection[0] in first_solution.nodes and connection[1] in first_solution.nodes:
        #         first_solution.add_edge(connection[0], connection[1], type="assign")
        # else:
        for pod in pods:
            random(first_solution, pod, debug=debug, visualize=visualize)

    initial_best = (evaluate_step(initial_unassigned, first_solution, debug=False), first_solution)
    current_best = initial_best


    survivors = [initial_best for i in range(survivors_per_generation)]
    for generation in range(generations):
        if debug:
            print(f"Generation {generation}: {survivors}")
        children = []
        for parent in range(survivors_per_generation):
            if debug:
                print(f"Parent {parent}")
            for i in range(chilren_per_parent):
                if debug:
                    print(f"Child {i}")
                rand_index = rnd.randint(0, number_neighbour_states(survivors[parent][1]) - 1)
                # print(f"pick neihgbor number {rand_index}")
                new_graph = get_neighbour_at_index(survivors[parent][1], rand_index)
                # neighbors = list(generate_neighbour_states(survivors[parent][1]))
                # print(f"number neighbors {len(neighbors)}")
                
                # new_graph = neighbors[rand_index]
                # draw_graph(new_graph, conf.small_deployment, "Generation: " + str(generation) + " Parent: " + str(parent) + " Child: " + str(i))
                children.append((evaluate_step(graph, new_graph, debug=False), new_graph))
        children.sort(key=lambda x: x[0])
        survivors = children[:survivors_per_generation]
        if survivors[0][0] < current_best[0]:
            current_best = survivors[0]

        if debug:
            print(f"Generation {generation}: {survivors}")
    #print(f"checked {generations * chilren_per_parent * survivors_per_generation} combinations")
    update_metric("num_eval_func_calls", generations * chilren_per_parent * survivors_per_generation)
    return current_best[1]

def graph_hash(graph: nx.DiGraph) -> int:
    hash_string = ""
    hash_string += str(sorted(list(graph.nodes)))
    hash_string += str(sorted(list(graph.edges)))
    return int(hashlib.md5(hash_string.encode()).hexdigest(), 16)

def number_neighbour_states(graph: nx.DiGraph) -> int:
    return len(get_pod_ids(graph)) * (len(get_node_ids(graph)) + 1)

def get_neighbour_at_index(graph: nx.DiGraph, index: int) -> nx.DiGraph:
    if index < 0 or index >= number_neighbour_states(graph): raise Exception("Index out of range")
    if graph == None: raise Exception("Graph is None")

    pod_ids = get_pod_ids(graph)
    node_ids = get_node_ids(graph)

    node_to_pick = (index % (len(node_ids) + 1))-1

    pod_id = pod_ids[index // (len(node_ids) + 1)]
    node_id = node_ids[node_to_pick]

    new_graph = graph.copy()
    new_graph.remove_edges_from(list(graph.out_edges(pod_id)) + list(graph.in_edges(pod_id)))
    if node_to_pick != -1:
        new_graph.add_edge(pod_id, node_id, type="assign")
    return new_graph

def generate_neighbour_states(graph: nx.DiGraph, graph_hash_map: dict[str, nx.Graph] = None) -> list[nx.Graph]:
    """
    Generate a list of neighbor states by removing an existing edge from the graph and adding a new edge connecting a node to the pod.
    Parameters:
        graph (nx.Graph): The graph object representing the problem.
        graph_hash_map (dict, optional): A dictionary mapping graph hashes to graph objects. Defaults to None.
        index_list (list, optional): A list of indices to generate neighbor states for. Defaults to None.
    Returns:
        list: A list of neighbor states represented as new graphs. Each neighbor state is a graph object with the same nodes as the original graph but with a different edge connecting a node to the pod.
    Description:
        This function takes a graph object as input and generates a list of neighbor states. A neighbor state is a graph object with the same nodes as the original graph but with a different edge connecting a node to the pod. The function iterates over the pods in the graph and for each pod, it iterates over the nodes in the graph. For each pod-node pair, it creates a new graph by copying the original graph and removes the existing edge connecting the pod to a neighbor node. It then adds a new edge connecting the node to the pod. The new graph is appended to the list of neighbor states.
    Note:
        The function assumes that the graph is a NetworkX graph object and that the pods and nodes have the "type" attribute set to "pod" and "node", respectively.
    """


    def cache_graph_hash(graph: nx.DiGraph, graph_hash_map: dict[str, nx.Graph]) -> nx.Graph:
        if graph == None or cache_graph_hash_map == None:
            return
        cache_graph_hash_map = graph_hash(graph)
        if cache_graph_hash_map not in graph_hash_map:
            cache_graph_hash_map[graph_hash] = graph.copy()
        return cache_graph_hash_map[graph_hash]
        
    
    set_of_nodes = get_node_ids(graph)
    set_of_pods = get_pod_ids(graph)
    solutions = []
    for i, pod_id in enumerate(set_of_pods):
        pod = graph.nodes[pod_id]
        new_graph = graph.copy()
        try:
            new_graph.remove_edge(pod_id, get_assigned_node_id(new_graph, pod_id))
        except nx.NetworkXError:
            new_graph = new_graph
            # if debug: print(f"Pod {pod_id} has no neighbor")
        if graph_hash_map != None:
            solutions.append(graph_hash(new_graph, graph_hash_map))
        else:
            solutions.append(new_graph)
        for j, node in enumerate(set_of_nodes):
            new_graph = graph.copy()
            try:
                new_graph.remove_edge(pod_id, get_assigned_node_id(new_graph, pod_id))
            except nx.NetworkXError:
                new_graph = new_graph
                # if debug: print(f"Pod {pod_id} has no neighbor")
            new_graph.add_edge(pod_id, node,type="assign")
            if graph_hash_map != None:
                solutions.append(cache_graph_hash(new_graph, graph_hash_map))
            else:
                solutions.append(new_graph)

    # print(f"Generated {len(solutions)} neighbour states")
   
    return solutions
def ant_colony_solve(graph, pods=None, debug=False, visualize=False):
    """
    Solves a graph problem using the Ant Colony Algorithm.
    Args:
        pod (tuple): A tuple representing a pod and its properties.
        graph (nx.Graph): The graph to be solved.
        debug (bool, optional): Flag to enable debug mode. Defaults to False.
        visualize (bool, optional): Flag to enable visualization. Defaults to False.
    Returns:
        nx.Graph: The solved graph.
    Description:
        This function uses the Ant Colony Algorithm to solve a graph problem. It starts by adding a new node to the graph and connecting it to a randomly chosen existing node. It then creates an ant solution graph and adds an initial ant to it. The function generates neighbour states by removing an existing edge from the graph and adding a new edge connecting a node to the pod. It moves the ant to a neighbour node based on a probability distribution. The function continues this process until all ants have reached a solution node. The best solution is then returned.
    Note:
        The function assumes that the graph is a NetworkX graph object and that the pod is a tuple representing a pod and its properties.
    """
    global rnd
    first_solution = graph.copy()
    if pods != None:
        for pod in pods:
            print(f"adding pod {pod}")
            first_solution = random(first_solution, pod, debug=debug, visualize=visualize)
    ant_solution_graph = nx.DiGraph()
    root_node = (evaluate_step(graph, first_solution, debug=False), first_solution) # syntax for an entry in the ant solution graph: (evaluation, graph)
    ant_solution_graph.add_node(root_node, type="solution") 
    amount_of_ants = 5
    moves_per_ant = 10
    pheromone_evaporation = 0.5
    rounds = 10
    graph_hash_map = {}
    pheromone_constant = 50000
    initial_pheromone = 0.1
    alpha = 1
    beta = 1
    heuristic_multiplier_for_worse_solutions = 0
    if debug:
        print(f"ACO configuration: amount_of_ants={amount_of_ants}, moves_per_ant={moves_per_ant}, pheromone_evaporation={pheromone_evaporation}")
    # Add ants to the ant_solution_graph
    for i in range(amount_of_ants):
        ant_solution_graph.add_node(i, type="ant", color='green')
        ant_solution_graph.add_edge(i,root_node, type="sits")


    def heuristic(edge: tuple):
        if edge[1][0] > edge[0][0]:
            return ((edge[1][0]-edge[0][0])/edge[1][0]) * heuristic_multiplier_for_worse_solutions
        return (edge[0][0]-edge[1][0])/edge[0][0]*100


    
    def move_ant(ant):
        global rnd
        assert len(list(ant_solution_graph.out_edges(ant))) == 1
        node = list(ant_solution_graph.neighbors(ant))[0]
        ant_solution_graph.remove_edge(ant,list(ant_solution_graph.out_edges(ant))[0][1])
        out_edges = list(ant_solution_graph.out_edges(node))
        probability = []
        for out_edge in out_edges:
            edge_heuristic = heuristic(out_edge)
            pheromone = ant_solution_graph.edges[out_edge]["pheromone"]
            try:
                numerator = math.pow(pheromone, alpha)*math.pow(edge_heuristic, beta)
                denominator = sum([math.pow(ant_solution_graph.edges[e]["pheromone"], alpha) * math.pow(heuristic(e), beta) for e in out_edges])

                probability.append(numerator/denominator)
                if debug: print("Edge with pheromone", ant_solution_graph.edges[out_edge]["pheromone"], "and heuristic", edge_heuristic, "has probability", probability[-1])

            except(ZeroDivisionError):
                probability.append(0.001)
        # generate random number between 0 and sum(probability)
        # print(probability)
        random = rnd.random()*sum(probability)
        c_p = 0
        for p_i in range(len(probability)) : # move according to probability:
            c_p += probability[p_i]
            if c_p > random:
                new_node = out_edges[p_i][1]
                # if new_node[0] < node[0]:
                #     ant_solution_graph[node][new_node]["pheromone"] += round(1-new_node[0]/node[0],3)
                # actual move
                ant_solution_graph.add_edge(ant, new_node, type="sits")
                assigned = True
                break
                    
    def draw_ant_graph(): 
        dot_file = "aco.dot"
        for edge in ant_solution_graph.edges:
            if ant_solution_graph.edges[edge]["type"] == "solution":
                # print("pheromone:", ant_solution_graph.edges[edge]["pheromone"])
                # ant_solution_graph.edges[edge]["weight"] = ant_solution_graph.edges[edge]["pheromone"] * 10000
                ant_solution_graph.edges[edge]["len"] = 0.0001
                ant_solution_graph.edges[edge]["label"] = str(round(ant_solution_graph.edges[edge]["pheromone"], 2))
                ant_solution_graph.edges[edge]["width"] = min(3, ant_solution_graph.edges[edge]["pheromone"]/100)
            elif ant_solution_graph.edges[edge]["type"] == "sits":
                ant_solution_graph.edges[edge]["len"] = 0.0005
        for node in ant_solution_graph.nodes:
            if ant_solution_graph.nodes[node]["type"] == "ant":
                ant_solution_graph.nodes[node]["label"] = str(node)
                ant_solution_graph.nodes[node]["shape"] = "circle"
                ant_solution_graph.nodes[node]["width"] = 0.5
            elif ant_solution_graph.nodes[node]["type"] == "solution":
                ant_solution_graph.nodes[node]["label"] = str(node[0])
                # ant_solution_graph.nodes[node]["shape"] = "square"
                # ant_solution_graph.nodes[node]["width"] = 0.5
        nx.drawing.nx_pydot.to_pydot(ant_solution_graph).write_raw(dot_file)
        print(f"ACO graph written to {dot_file}")
        input("press enter to continue")

    def attach_solutions(node, solution_list, node_hash_map={}):
        global rnd
        perfect_solution = None

        for solution in solution_list:
            solution_hash = graph_hash(solution)
            if solution_hash not in node_hash_map:
                solution_node = (evaluate_step(graph, solution, debug=False), solution) # syntax for an entry in the ant solution graph: (evaluation, graph)
                node_hash_map[solution_hash] = solution_node
            else:
                solution_node = node_hash_map[solution_hash]

            if(solution_node[0] == 0):
                # best possible solution was found
                perfect_solution = solution_node[1]
            if not ant_solution_graph.has_node(solution_node): 
                ant_solution_graph.add_node(solution_node, type="solution", color='blue')
            if not ant_solution_graph.has_edge(node, solution_node):
                ant_solution_graph.add_edge(node, solution_node, type="solution", pheromone=initial_pheromone)
            # print("attached new solution")
        return perfect_solution

    def update_pheromones():
        ## Build edge lists for the path of each ant
        path_list = [] # the path of ant 0 is at index zero and is a list of edges
        for ant in [ ant for ant in ant_solution_graph.nodes if ant_solution_graph.nodes[ant]["type"] == "ant" ]:
            assert len(list(ant_solution_graph.out_edges(ant))) == 1
            shortes_path = nx.shortest_path(ant_solution_graph, root_node, list(ant_solution_graph.out_edges(ant))[0][1])
            edge_list = []
            for i in range(len(shortes_path)-1):
                edge_list.append((shortes_path[i], shortes_path[i+1]))
            path_list.append(edge_list)

        for edge in ant_solution_graph.edges:
            if "pheromone" in ant_solution_graph.edges[edge]:
                for path in path_list:
                    if edge in path:
                         ant_solution_graph.edges[edge]["pheromone"] += pheromone_constant/path[-1][1][0] # pheromone_constant/the_value_of_the_solution_the_ant_is_on
            else:
                ant_solution_graph.edges[edge]["pheromone"] = initial_pheromone
    
    def reset_ants():
        # Detach ants from their current node
        for ant in [ant for ant in ant_solution_graph.nodes if ant_solution_graph.nodes[ant]["type"] == "ant"]:
            if len(list(ant_solution_graph.out_edges(ant))) == 1:
                ant_solution_graph.remove_edge(ant, list(ant_solution_graph.out_edges(ant))[0][1])

        # Reattach ants to the root node
        for ant in [ant for ant in ant_solution_graph.nodes if ant_solution_graph.nodes[ant]["type"] == "ant"]:
            ant_solution_graph.add_edge(ant, root_node, type="sits")


    def evaporate_pheromones():
        for edge in ant_solution_graph.edges:
            if "pheromone" in ant_solution_graph.edges[edge]:
                ant_solution_graph.edges[edge]["pheromone"] *= pheromone_evaporation


    node_hash_map = {}
    for current_round in range(rounds):
        # print(f"round {current_round}")
        for move in range(moves_per_ant):
            # for every solution node with an ant, generate the neighbour states
            # and attach the solutions to the graph
            nodes_to_generate_neighbours_for = set()
            for node in ant_solution_graph.nodes:
                if "type" in ant_solution_graph.nodes[node] and ant_solution_graph.nodes[node]["type"] == "ant":
                    # draw_ant_graph()
                    assert len(list(ant_solution_graph.out_edges(node))) == 1
                    solution_node_to_generate_neighbors_for = list(ant_solution_graph.out_edges(node))[0][1]
                    if len(ant_solution_graph.out_edges(solution_node_to_generate_neighbors_for)) == 0: # Don't generate neighbours for nodes that already have solutions attached
                        nodes_to_generate_neighbours_for.add(solution_node_to_generate_neighbors_for)
        
            if debug:
                print(f"generating neighbours for {len(nodes_to_generate_neighbours_for)} nodes")
            for node in nodes_to_generate_neighbours_for:
                solutions = generate_neighbour_states(node[1])
                # for solution in solutions:
                #     draw_graph(solution, f"Neighbour {solution}")
                #     input("press enter to continue")

                perfect_solution = attach_solutions(node, solutions, node_hash_map)
                if perfect_solution is not None:
                    if debug:
                        print(f"perfect solution found: {perfect_solution}")
                    if visualize:
                        draw_ant_graph()
                    # print(f"considered {len([node for node in ant_solution_graph.nodes if ant_solution_graph.nodes[node]['type'] == 'solution'])} solutions")
                    update_metric("num_eval_func_calls", len([node for node in ant_solution_graph.nodes if ant_solution_graph.nodes[node]['type'] == 'solution']))
                    return perfect_solution

            for ant in range(amount_of_ants):
                move_ant(ant)
                
                
        update_pheromones()
        evaporate_pheromones()
        # draw_ant_graph()
        reset_ants()
    solution_list = list(node for node in ant_solution_graph.nodes if ant_solution_graph.nodes[node]["type"] == "solution")
    solution_list = sorted(solution_list, key=lambda x: x[0])
    # print("best solution:", solution_list[0][0])
    # print(f"considered {len(solution_list)} solutions")
    update_metric("num_eval_func_calls", len(solution_list))

    if visualize:
        draw_ant_graph()
    return solution_list[0][1]

def simulated_annealing_solve(graph, pods=None, debug=False, visualize=True):
    global rnd
    max_iterations = 77000
    initial_temperature = 1000
    cooling_rate = 0.9997

    
    first_solution = graph.copy()
    if pods != None:
        for pod in pods:
            first_solution = random(first_solution, pod, debug=debug, visualize=visualize)
    current_solution = first_solution
    current_value = evaluate_step(graph, current_solution)
    best_solution = current_solution
    best_value = current_value
    temperature = initial_temperature

    for i in range(max_iterations):
        if temperature <= 0:
            break

        new_solution = rnd.choice(generate_neighbour_states(current_solution))
        new_value = evaluate_step(graph, new_solution)

        delta_value = new_value - current_value
        if delta_value < 0: # new solution is better
            current_solution = new_solution
            current_value = new_value

            if current_value < best_value:
                best_solution = current_solution
                best_value = current_value
        else: # new solution is worse
            acceptance_probability = math.exp(-delta_value / temperature)
            if rnd.random() < acceptance_probability:
                current_solution = new_solution
                current_value = new_value

        temperature *= cooling_rate
    update_metric("num_eval_func_calls", max_iterations)
    return best_solution
        
    

def plot_simulated_anealnealing_solution_space(solution):
    #add node to graph
    graph.add_node(pod[0], **pod[1])
    #try all node-pod connections
 
    assignments = list(itertools.product(get_node_ids(graph), get_pod_ids(graph)))
    solutions_checked = 0
    solution_array = []
    if debug:
        print(assignments)
    combinations = list(itertools.combinations(assignments, len(get_pod_ids(graph))))
    if debug:
        print(combinations)
    
    current_best = (evaluate(graph), graph)
    for combination in combinations:
        solutions_checked += 1
        # create new graph
        new_graph = graph.copy()
        # remove all assignments
        new_graph.remove_edges_from((edge for edge in new_graph.edges if new_graph.edges[edge]["type"] == "assign"))
        assigned_pods = []
        valid=True
        if debug:
            print("#"*50)
            print(f"combination: {combination}")
        for assignment in combination:
            if debug:
                print(f"assignment: {assignment}")
            if assignment[1] in assigned_pods:
                valid=False
                break
            else:
                assigned_pods.append(assignment[1])
                new_graph.add_edge(assignment[1], assignment[0], type="assign")
        if valid:
            evaluation = evaluate(new_graph, debug=debug)
            solution_array.append(evaluation)


            # if evaluation < current_best[0]:
            #     current_best = (evaluation, new_graph)
            #     if visualize:
            #         draw_graph(new_graph, conf.simple_graph, "Evaluation: " + str(evaluation))
            #     if debug:
            #         print(f"new best: {current_best[0]}")
            #     if evaluation == 0:
            #         print(f"checked {solutions_checked} combinations")
            #         return current_best[1]
            # else:
            #     if debug:
            #         print(f"evaluation: {evaluation}")
        else:
            if debug:
                print("invalid combination")

    # calculate entropy of solution array
    # Example data
    data = np.array(solution_array)

    # Calculate the probability distribution
    values, counts = np.unique(data, return_counts=True)
    probabilities = counts / counts.sum()

    # Calculate entropy
    ent = -np.sum(probabilities * np.log2(probabilities))
    print(f'Entropy: {ent:.4f}')
    if True:
        plt.plot(solution_array)
        plt.title("SA")
        # plt.axis('off')
        plt.tight_layout()
        plt.show()

    return graph

def kubernetes_default(graph: nx.DiGraph, pods=None, debug=False, visualize=True):
    graph = graph.copy()
    for pod in pods:
        feasible_nodes = list(node for node in graph.nodes if graph.nodes[node]["type"] == "node")
        ## Stage 1: Filtering
        ## LabelSelector
        for node in [node for node in feasible_nodes]:
            if "labels" not in graph.nodes[node]:
                node_labels = []
            else:
                node_labels = graph.nodes[node]["labels"]

            if "labelSelector" not in pod[1]:
                pod_label_selector = []
            else:
                pod_label_selector = pod[1]["labelSelector"]

            for label_selector in pod_label_selector:
                if label_selector not in node_labels:
                    feasible_nodes.remove(node)
                    break


        ## NodeResourceFit
        for node in [node for node in feasible_nodes]:
            cpu_load = 0
            mem_load = 0
            for pod_id in get_assigned_pod_ids(graph, node):
                    cpu_load += graph.nodes[pod_id]["cpu"]
                    mem_load += graph.nodes[pod_id]["mem"]
            if cpu_load + pod[1]["cpu"] > graph.nodes[node]["cpu"] or mem_load + pod[1]["mem"] > graph.nodes[node]["mem"]:
                feasible_nodes.remove(node)

        ## Stage 2: Scoring
        scored_nodes = [ (node, 0) for node in feasible_nodes ]
        ## Aim for an even distribution
        num_pods = len(get_pod_ids(graph)) + 1
        num_nodes = len(get_node_ids(graph))
        avg_pods_per_node = num_pods / num_nodes
        for node in scored_nodes:
            num_scheduled_pods = len(get_assigned_pod_ids(graph, node[0]))
            if num_scheduled_pods > avg_pods_per_node:
                continue
            else:
                scored_nodes = [(node_name, score + avg_pods_per_node - num_scheduled_pods) if node_name == node[0] else (node_name, score) for node_name, score in scored_nodes]
        
        ## Stage 3: Selection
        if scored_nodes == []:
            graph.add_node(pod[0], **pod[1])
            print("no feasible nodes")
            return graph
        selected_node = max(scored_nodes, key=lambda item: item[1])[0]
        graph.add_node(pod[0], **pod[1])
        graph.add_edge(pod[0], selected_node, type="assign")
        if visualize:
            draw_graph(graph, "Kubernetes Default" + str(evaluate(graph)), conf.mini_graph)
    return graph
