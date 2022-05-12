
''' Classes are named according to the Wikipedia definition of the petri nets.
Examine https://en.wikipedia.org/wiki/Petri_net to undestand what classes do.
'''
class Place:
    def __init__(self, index, token):
        self.index = index
        self.token = token


class Transition:
    def __init__(self, input_places, output_places):
        self.input_places = input_places
        self.output_places = output_places

    def fire(self):
        if all(i.tokenIsSufficient() for i in self.input_places):
            for input in self.input_places:
                input.trigger()
            for output in self.output_places:
                output.trigger()
            return True
        else:
            return False


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
    def __init__(self, filename):
        with open(filename) as f:
            lines = f.readlines()
            a = lines[0][:-1].split(' ')
            a = list(map(int, a))

            bc = lines[1].split('-')
            b = bc[0].split(' ')
            if (b[-1] == ''):
                b = b[:-1]
            c = bc[1][:-1].split(' ')
            if (c[0] == ''):
                c = c[1:]
            b = list(map(int, b))
            c = list(map(int, c))

            de = lines[2].split('-')
            d = de[0].split(' ')
            if (d[-1] == ''):
                d = d[:-1]
            e = de[1][:-1].split(' ')
            if (e[0] == ''):
                e = e[1:]
            d = list(map(int, d))
            e = list(map(int, e))

            f = lines[3][:-1].split(' ')
            f = list(map(int, f))

            g = lines[4][:-1].split(' ')
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


    def fire(self, transition_id):
        if (self.transitions[transition_id].fire()):
            print("Fired transition")
        else:
            print("Transition could not be fired.")


    def printPlaceTokens(self):
        print("---------")
        for i in self.places:
            print("Place " + str(i.index) + " -> " + str(i.token) + " tokens")
        print("---------")
        



if __name__ == "__main__":

    petri = PetriNet('net.txt')
    petri.printPlaceTokens()
    petri.fire(0)
    petri.printPlaceTokens()


