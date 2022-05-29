
''' Classes are named according to the Wikipedia definition of the petri nets.
Examine https://en.wikipedia.org/wiki/Petri_net to undestand what classes do.
'''
import random

class Place:
    def __init__(self, index, token):
        self.index = index
        self.token = token


class Transition:
    def __init__(self, input_places, output_places):
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
    def __init__(self, place, tokens_to_be_inputted = 1):
        self.place = place
        self.tokens_to_be_inputted = tokens_to_be_inputted 

    def tokenIsSufficient(self):
        return self.place.token >= self.tokens_to_be_inputted
    
    def trigger(self):
        self.place.token -= self.tokens_to_be_inputted


# Arc that goes  transition --> place
class OutputPlace:
    def __init__(self, place, tokens_to_be_outputted = 1):
        self.place = place
        self.tokens_to_be_outputted = tokens_to_be_outputted

    def trigger(self):
        self.place.token += self.tokens_to_be_outputted


class PetriNet:
    def __init__(self, filename, random_privilege_escalation_probability = 0.0):
        self.random_privilege_escalation_probability = random_privilege_escalation_probability
        with open(filename) as f:    
            lines = f.readlines()
            a = lines[0][:-1].split(' ')
            a = list(map(int, a))


            #inputs
            if(lines[1] != '\n'):
                bc = lines[1].split('-')
                b = bc[0].split(' ')
                if (b[-1] == ''):
                    b = b[:-1]
                c = bc[1][:-1].split(' ')
                if (c[0] == ''):
                    c = c[1:]
                b = list(map(int, b))
                c = list(map(int, c))
            else:
                b = []
                c = []

            # outputs
            if(lines[2] != '\n'):
                de = lines[2].split('-')
                d = de[0].split(' ')
                if (d[-1] == ''):
                    d = d[:-1]
                e = de[1][:-1].split(' ')
                if (e[0] == ''):
                    e = e[1:]
                d = list(map(int, d))
                e = list(map(int, e))
            else:
                d = []
                e = []

            f = lines[3][:-1].split(' ')
            f = list(map(int, f))

            if(lines[4][-1] == '\n'):
                g = lines[4][:-1].split(' ')
            else:
                g = lines[4].split(' ')
            g = list(map(int, g))

            place_tokens = a

            input_req_token = b
            input_place_list = c

            output_out_token = d
            output_place_list = e

            transition_input_count = f
            transition_output_count = g

            # Set token
            self.places = []
            for i in range(len(place_tokens)):
                place_instance = Place(i, place_tokens[i])
                self.places.append(place_instance)


            self.input = []
            for i in range(len(input_req_token)):
                input_instance = InputPlace(self.places[input_place_list[i]], input_req_token[i])
                self.input.append(input_instance)


            self.output = []
            for i in range(len(output_out_token)):
                output_instance = OutputPlace(self.places[output_place_list[i]], output_out_token[i])
                self.output.append(output_instance)


            self.transitions = []
            temp_input = []
            i = 0
            a = 0 
            while i < len(transition_input_count):
                temp_input.append(self.input[a:a+transition_input_count[i]])
                a = a + transition_input_count[i]
                i += 1


            temp_output = []
            j = 0
            b = 0
            while j < len(transition_output_count):
                temp_output.append(self.output[b: b+transition_output_count[j]])
                b = b + transition_output_count[j]
                j += 1


            for i in range(len(temp_input)):
                transition_instance = Transition(temp_input[i], temp_output[i])
                self.transitions.append(transition_instance)


    def fire(self, transition_id, fire_unconditionally = False):
        
        if (random.random() < self.random_privilege_escalation_probability):
            fire_unconditionally = True
            
        if (self.transitions[transition_id].fire(fire_unconditionally) == 0):
            print("Fired transition")
        elif (self.transitions[transition_id].fire(fire_unconditionally) == 1):
            print("Fired transition with unauthorized privilege escalation")
        else:
            print("Transition could not be fired.")


    def printPlaceTokens(self):
        print("---------")
        for i in self.places:
            print("Place " + str(i.index) + " -> " + str(i.token) + " tokens")
        print("---------")
        

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


