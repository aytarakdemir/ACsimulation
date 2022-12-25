
''' Classes are named according to the Wikipedia definition of the petri nets.
Examine https://en.wikipedia.org/wiki/Petri_net to understand what each class does.
'''
import random
from enum import Enum

infinity = 1000

class Place:
    def __init__(self, name, token, token_limit = infinity): # Assume has no limit for default value
        self.name = name
        self.token = token
        self.token_limit = token_limit

    def setTokenLimit(self, token_limit):
        self.token_limit = token_limit


class Transition:
    def __init__(self, name, input_places, output_places):
        self.name = name
        self.input_places = input_places
        self.output_places = output_places

    class fireOutMsg(Enum):
        FIRED = 0
        FIRED_UNCONDITIONALLY = 1
        COULD_NOT_BE_FIRED = 2
        # Below values are only possible if the check_mode is True
        CAN_BE_FIRED = 3
        CANNOT_BE_FIRED = 4

    def fire(self, fire_unconditionally = False, check_mode = False):
        could_not_finish = False
        input_performed = False
        if (all(i.tokenIsSufficient() for i in self.input_places)):
            for input in self.input_places:
                input.trigger()
            input_performed = True
        else:
            if (check_mode):
                return self.fireOutMsg.CANNOT_BE_FIRED
        if (input_performed):
            if (all(j.tokenWithinLimit() for j in self.output_places)):
                if (check_mode): 
                    for input in self.input_places:
                        input.revert()
                    could_not_finish = True
                    return self.fireOutMsg.CAN_BE_FIRED
                else:
                    for output in self.output_places:
                        output.trigger()
                    return self.fireOutMsg.FIRED
            else:
                for input in self.input_places:
                    input.revert()
                could_not_finish = True
                return self.fireOutMsg.CANNOT_BE_FIRED

        if (could_not_finish):
            if (fire_unconditionally):
                for output in self.output_places:
                    output.trigger()
                return self.fireOutMsg.FIRED_UNCONDITIONALLY
            else:
                return self.fireOutMsg.COULD_NOT_BE_FIRED


# Arc that goes  place --> transition
class InputPlace:
    def __init__(self, id, place, tokens_to_be_inputted = 1):
        self.id = id
        self.place = place
        self.tokens_to_be_inputted = tokens_to_be_inputted 

    def tokenIsSufficient(self):
        return self.place.token >= self.tokens_to_be_inputted
    
    def trigger(self):
        self.place.token -= self.tokens_to_be_inputted
    
    def revert(self):
        self.place.token += self.tokens_to_be_inputted


# Arc that goes  transition --> place
class OutputPlace:
    def __init__(self, id, place, tokens_to_be_outputted = 1):
        self.id = id
        self.place = place
        self.tokens_to_be_outputted = tokens_to_be_outputted

    def tokenWithinLimit(self):
        #print(str(self.place.token) + " + " + str(self.tokens_to_be_outputted) + " <= " + str(self.place.token_limit))
        return self.place.token + self.tokens_to_be_outputted <= self.place.token_limit

    def trigger(self):
        self.place.token += self.tokens_to_be_outputted


class PetriNet:
    def __init__(self, filename, random_privilege_escalation_probability = 0.0):
        self.places_from_txt = []
        self.inputs_from_txt = []
        self.outputs_from_txt = []
        self.transitions_from_txt = []
        self.random_privilege_escalation_probability = random_privilege_escalation_probability   
        self.readStateAndSet(filename, self.random_privilege_escalation_probability)


    def transitionFirable(self, transition_name):
        for i in self.transitions:
            if (i.name == transition_name):
                return i.fire(fire_unconditionally = False, check_mode = True) == i.fireOutMsg.CAN_BE_FIRED
        return -1


    def fire(self, transition_name, fire_unconditionally = False):
        
        if (random.random() < self.random_privilege_escalation_probability):
            fire_unconditionally = True
            
        for i in self.transitions:
            if (i.name == transition_name):
                if (i.fire(fire_unconditionally) == i.fireOutMsg.FIRED):
                    print("'" + transition_name + "': Fired transition")
                    return (i.name, True)
                elif (i.fire(fire_unconditionally) == i.fireOutMsg.FIRED_UNCONDITIONALLY):
                    print("'" + transition_name + "': Fired transition with unauthorized privilege escalation")
                else:
                    print("'" + transition_name + "': Transition could not be fired.")
                return (i.name, False)


    def printPlaceTokens(self):
        print("---------")
        for i in self.places:
            print("Place: " + str(i.name) + " -> " + str(i.token) + " tokens, Limit: " + str(i.token_limit))
        print("---------")


    def transitionNames(self):
        transition_names = []
        for i in self.transitions:
            transition_names.append(i.name)
        return transition_names


    def readCurrentStateFromFile(self, filename):
        with open(filename) as f:    
            lines = f.readlines()
            id = 0
            for cur_line in lines:
                cur_line.replace(" ", "")
                if (cur_line[-1] != '\n'):
                    cur_line += '\n' 
                if (cur_line[0] == '/'):
                    if(cur_line[1:6] == "place"):
                        inside = cur_line[7:-2].split(",")
                        place_info = {
                            "name": inside[0],
                            "token": int(inside[1])
                        }
                        self.places_from_txt.append(place_info)
                    elif(cur_line[1:11] == "transition"):
                        inside = cur_line[12:-2].split(",")
                        transition_info = {
                            "name": inside[0],
                        }
                        self.transitions_from_txt.append(transition_info)
                    elif(cur_line[1:5] == "PtoT"):
                        inside = cur_line[6:-2].split(",")
                        input_info = {
                            "id": id,
                            "P": inside[0],
                            "T": inside[1],
                            "token_minus": int(inside[2])
                        }
                        id += 1
                        self.inputs_from_txt.append(input_info)
                    elif(cur_line[1:5] == "TtoP"): 
                        inside = cur_line[6:-2].split(",")
                        output_info = {
                            "id": id,
                            "T": inside[0],
                            "P": inside[1],
                            "token_plus": int(inside[2])
                        }
                        id += 1
                        self.outputs_from_txt.append(output_info)
                    else:
                        print("Error: Undefined command")

            print("Places:", self.places_from_txt)
            print(self.inputs_from_txt)
            print(self.outputs_from_txt)
            print(self.transitions_from_txt)

    def readStateAndSet(self, filename, random_privilege_escalation_probability = 0.0):
            self.readCurrentStateFromFile(filename)

            # Set token
            self.places = []
            for i in range(len(self.places_from_txt)):
                place_instance = Place(self.places_from_txt[i]["name"], self.places_from_txt[i]["token"])
                self.places.append(place_instance)


            self.input = []
            for i in range(len(self.inputs_from_txt)):
                for a in range(len(self.places)):
                    if (self.places[a].name == self.inputs_from_txt[i]['P']):
                        input_instance = InputPlace(self.inputs_from_txt[i]['id'], self.places[a], self.inputs_from_txt[i]['token_minus'])
                        self.input.append(input_instance)


            self.output = []
            for i in range(len(self.outputs_from_txt)):
                for a in range(len(self.places)):
                    if (self.places[a].name == self.outputs_from_txt[i]['P']):
                        output_instance = OutputPlace(self.outputs_from_txt[i]['id'], self.places[a], self.outputs_from_txt[i]['token_plus'])
                        self.output.append(output_instance)


            self.transitions = []

            for i in range(len(self.transitions_from_txt)):
                temp_input = []
                temp_output = []
                
                for z in self.inputs_from_txt:
                    if (z['T'] == self.transitions_from_txt[i]['name']):
                        for j in self.input:
                            if (j.id == z['id']):
                                temp_input.append(j)
                for z in self.outputs_from_txt:        
                    if (z['T']  == self.transitions_from_txt[i]['name']):
                        for j in self.output:
                            if (j.id == z['id']):
                                temp_output.append(j)

                transition_instance = Transition(self.transitions_from_txt[i]['name'], temp_input, temp_output)
                self.transitions.append(transition_instance)

            for a in self.places:
                for i in self.input:
                    if (i.place.name == a.name):
                        if (a.token_limit < i.tokens_to_be_inputted or a.token_limit == infinity):
                            a.setTokenLimit(i.tokens_to_be_inputted)
                for i in self.output:
                    if (i.place.name == a.name):
                        if (a.token_limit < i.tokens_to_be_outputted or a.token_limit == infinity):
                            a.setTokenLimit(i.tokens_to_be_outputted)


    def writeCurrentStateToFile(self, filename):
        f = open(filename, "w")
        state_out = ""
        for i in self.places:
            place_out = "/place{" + i.name + "," + str(i.token) + "}\n"
            state_out += place_out

        state_out += "\n"

        for i in self.transitions:
            transition_out = "/transition{" + i.name + "}\n"
            state_out += transition_out

        state_out += "\n"

        for i in self.input:
            for j in self.transitions:
                for k in j.input_places:
                    if (i.id == k.id):
                        input_out = "/PtoT{" + i.place.name + "," + str(j.name) + "," + str(i.tokens_to_be_inputted) + "}\n"
                        state_out += input_out

        state_out += "\n"

        for i in self.output:
            for j in self.transitions:
                for k in j.output_places:
                    if (i.id == k.id):
                        output_out = "/TtoP{" + i.place.name + "," + str(j.name) + "," + str(i.tokens_to_be_outputted) + "}\n"
                        state_out += output_out

        f.write(state_out)
        f.close()

        

if __name__ == "__main__":

    petri = PetriNet('net_config/pull_request_review.txt')
    petri.printPlaceTokens()
    print(petri.transitionFirable("createPR"))
    petri.printPlaceTokens()
    petri.fire("createPR")
    petri.printPlaceTokens()
    petri.fire("approvePR")
    petri.fire("push")
    petri.fire("approvePR")
    petri.fire("approvePR")
    petri.fire("push")

