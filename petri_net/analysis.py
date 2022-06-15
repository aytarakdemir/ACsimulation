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

#def fireAllComprehensive(steps):



steps = 4
print("Trigger History: \n" + str(fireAllRandom(steps)))