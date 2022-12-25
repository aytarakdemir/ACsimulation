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


def fireAllComprehensive(steps):
    trigger_history = []
    stack = []
    transition_names_list = petri.transitionNames()
    print(transition_names_list)
    petri.fire("createPR")
    petri.fire("approvePR")
    stack.append(petri.saveState())
    petri.fire("approvePR")
    stack.append(petri.saveState())
    petri.fire("approvePR")
    petri.fire("push")
    petri.printPlaceTokens()
    petri.setState(stack.pop())
    petri.printPlaceTokens()


    # for i in range(steps):
    #     print("Iteration: " + str(i))
    #     firablesArray = []
    #     for transition_name in transition_names_list:
    #         firablesArray.append(petri.transitionFirable(transition_name))
    #     print(firablesArray)
    #     transitionFirableStatus = {transition_names_list[i]: firablesArray[i] for i in range(len(transition_names_list))}
    #     print(transitionFirableStatus)


steps = 4
# print("Trigger History: \n" + str(fireAllRandom(steps)))

fireAllComprehensive(steps)