from petri import PetriNet
import random
from anytree import Node, RenderTree

petri = PetriNet('net_config/pull_request_review.txt')

def fireAllRandom(steps):
    trigger_history = []
    for i in range(steps):
        print("Iteration: " + str(i))
        transition_names_list = petri.transitionNames()
        random.shuffle(transition_names_list)
        triggers_fired_this_iteration = []
        for transition_name in transition_names_list:
            result = petri.fire(transition_name)
            if (result[1]):
                triggers_fired_this_iteration.append(result[0])
        trigger_history.append(triggers_fired_this_iteration)

        petri.printPlaceTokens()
    return trigger_history


queue = []

def fireAllBFS(depth):
    trigger_history = []
    queue = []
    transition_names_list = petri.transitionNames()
    #print(transition_names_list)

    queue.append(petri.saveState())



    for level in range(depth):
        print("LEVEL: " + str(level))
        petri.setState(queue[0])
        print("QQQQQQQQQQQ:" + str(queue[0]))
        transitions_this_depth = []
        #number_of_branches = 0
        for transition_name in transition_names_list:
            print(transition_name)
            if (petri.transitionFirable(transition_name)):
                #number_of_branches += 1
                petri.fire(transition_name)
                trigger_history.append(transition_name)
                queue.append(petri.saveState())
                petri.setState(queue[-1])
        trigger_history.append("*")
        queue.pop(0)

    print(trigger_history)



    triggers_flat = []
    temp = []
    id = 0
    for item in trigger_history:
        if (item != '*'):
            temp.append(item)
        else:
            triggers_flat.append(temp)
            temp = []
        id += 1

    print(triggers_flat)
    return triggers_flat




def createTree(triggers_flat):
    root = Node("Root")
    temp_fork_length = 0
    for i in range(len(triggers_flat)):
        if (i == 0):
            for item in triggers_flat[i]:
                a = Node(item, root)
        else:
            for item in triggers_flat[i]:
                b = Node(item, root)


    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))







depth = 9
# print("Trigger History: \n" + str(fireAllRandom(steps)))

createTree(fireAllBFS(depth))