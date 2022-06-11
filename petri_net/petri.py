
''' Classes are named according to the Wikipedia definition of the petri nets.
Examine https://en.wikipedia.org/wiki/Petri_net to undestand what classes do.
'''
import random

class Place:
    def __init__(self, name, token):
        self.name = name
        self.token = token


class Transition:
    def __init__(self, name, input_places, output_places):
        self.name = name
        self.input_places = input_places
        self.output_places = output_places

    def fire(self, fire_unconditionally = False):
        if (all(i.tokenIsSufficient() for i in self.input_places)):
            for input in self.input_places:
                input.trigger()
            for output in self.output_places:
                output.trigger()
            return 0
        elif (fire_unconditionally):
            for output in self.output_places:
                output.trigger()
            return 1
        else:
            return 2


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


# Arc that goes  transition --> place
class OutputPlace:
    def __init__(self, id, place, tokens_to_be_outputted = 1):
        self.id = id
        self.place = place
        self.tokens_to_be_outputted = tokens_to_be_outputted

    def trigger(self):
        self.place.token += self.tokens_to_be_outputted


class PetriNet:
    def __init__(self, filename, random_privilege_escalation_probability = 0.0):
        self.random_privilege_escalation_probability = random_privilege_escalation_probability

        places_from_txt = []
        inputs_from_txt = []
        outputs_from_txt = []
        transitions_from_txt = []

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
                        places_from_txt.append(place_info)
                    elif(cur_line[1:11] == "transition"):
                        inside = cur_line[12:-2].split(",")
                        transition_info = {
                            "name": inside[0],
                        }
                        transitions_from_txt.append(transition_info)
                    elif(cur_line[1:5] == "PtoT"):
                        inside = cur_line[6:-2].split(",")
                        input_info = {
                            "id": id,
                            "P": inside[0],
                            "T": inside[1],
                            "token_minus": int(inside[2])
                        }
                        id += 1
                        inputs_from_txt.append(input_info)
                    elif(cur_line[1:5] == "TtoP"): 
                        inside = cur_line[6:-2].split(",")
                        output_info = {
                            "id": id,
                            "T": inside[0],
                            "P": inside[1],
                            "token_plus": int(inside[2])
                        }
                        id += 1
                        outputs_from_txt.append(output_info)
                    else:
                        print("Error: Undefined command")

            

            # Set token
            self.places = []
            for i in range(len(places_from_txt)):
                place_instance = Place(places_from_txt[i]["name"], places_from_txt[i]["token"])
                self.places.append(place_instance)


            self.input = []
            for i in range(len(inputs_from_txt)):
                for a in range(len(self.places)):
                    if (self.places[a].name == inputs_from_txt[i]['P']):
                        input_instance = InputPlace(inputs_from_txt[i]['id'], self.places[a], inputs_from_txt[i]['token_minus'])
                        self.input.append(input_instance)


            self.output = []
            for i in range(len(outputs_from_txt)):
                for a in range(len(self.places)):
                    if (self.places[a].name == outputs_from_txt[i]['P']):
                        output_instance = OutputPlace(outputs_from_txt[i]['id'], self.places[a], outputs_from_txt[i]['token_plus'])
                        self.output.append(output_instance)


            self.transitions = []

            for i in range(len(transitions_from_txt)):
                temp_input = []
                temp_output = []
                
                for z in inputs_from_txt:
                    if (z['T'] == transitions_from_txt[i]['name']):
                        for j in self.input:
                            if (j.id == z['id']):
                                temp_input.append(j)
                for z in outputs_from_txt:        
                    if (z['T']  == transitions_from_txt[i]['name']):
                        for j in self.output:
                            if (j.id == z['id']):
                                temp_output.append(j)
                transition_instance = Transition(transitions_from_txt[i]['name'], temp_input, temp_output)
                self.transitions.append(transition_instance)




            


    def fire(self, transition_name, fire_unconditionally = False):
        
        if (random.random() < self.random_privilege_escalation_probability):
            fire_unconditionally = True
            
        for i in self.transitions:
            if (i.name == transition_name):
                if (i.fire(fire_unconditionally) == 0):
                    print("'" + transition_name + "': Fired transition")
                elif (i.fire(fire_unconditionally) == 1):
                    print("'" + transition_name + "': Fired transition with unauthorized privilege escalation")
                else:
                    print("'" + transition_name + "': Transition could not be fired.")


    def printPlaceTokens(self):
        print("---------")
        for i in self.places:
            print("Place: " + str(i.name) + " -> " + str(i.token) + " tokens")
        print("---------")

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
                        output_out = "/PtoT{" + i.place.name + "," + str(j.name) + "," + str(i.tokens_to_be_outputted) + "}\n"
                        state_out += output_out

        f.write(state_out)
        f.close()

        

if __name__ == "__main__":

    petri = PetriNet('infinite_token_loop.txt')
    petri.printPlaceTokens()
    petri.fire(0)
    petri.printPlaceTokens()

# Example Net
# 5 5 5 5
# 2 1 2 - 0 1 2
# 1 1 2 1 - 1 2 3 0
# 1 2
# 2 2


