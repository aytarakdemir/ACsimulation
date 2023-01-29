from petri import PetriNet
import random

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
        for transition_name in transition_names_list:
            print(transition_name)
            if (petri.transitionFirable(transition_name)):
                petri.fire(transition_name)
                trigger_history.append(transition_name)
                queue.append(petri.saveState())
                petri.setState(queue[-1])
        queue.pop(0)

    print(trigger_history)


    # petri.fire("createPR")
    # petri.fire("approvePR")
    # queue.append(petri.saveState())
    # petri.fire("approvePR")
    # queue.append(petri.saveState())
    # petri.fire("approvePR")
    # petri.fire("push")
    # petri.printPlaceTokens()
    # petri.setState(queue.pop())
    # petri.printPlaceTokens()


    # for i in range(steps):
    #     print("Iteration: " + str(i))
    #     firablesArray = []
    #     for transition_name in transition_names_list:
    #         firablesArray.append(petri.transitionFirable(transition_name))
    #     print(firablesArray)
    #     transitionFirableStatus = {transition_names_list[i]: firablesArray[i] for i in range(len(transition_names_list))}
    #     print(transitionFirableStatus)


depth = 9
# print("Trigger History: \n" + str(fireAllRandom(steps)))

fireAllBFS(depth)