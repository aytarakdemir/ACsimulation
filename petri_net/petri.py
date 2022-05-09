
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
                # if (input.place.index == 0):
                #     print("Changed from: " + str(input.place.token))
                input.trigger()
                # if (input.place.index == 0):
                #     print("To: " + str(input.place.token))
            for output in self.output_places:
                output.trigger()


# Arc that goes  place --> transition
class InputPlace:
    def __init__(self, place, tokens_to_be_inputted = 1):
        self.place = place
        self.tokens_to_be_inputted = tokens_to_be_inputted 

    def tokenIsSufficient(self):
        return self.place.token >= self.tokens_to_be_inputted
    
    def trigger(self):
        # if (self.place.index == 0):
        #     print("Changed from: " + str(self.place.token))
        self.place.token -= self.tokens_to_be_inputted
        # if (self.place.index == 0):
        #     print("To: " + str(self.place.token))


# Arc that goes  transition --> place
class OutputPlace:
    def __init__(self, place, tokens_to_be_outputted = 1):
        self.place = place
        self.tokens_to_be_outputted = tokens_to_be_outputted

    def trigger(self):
        self.place.token += self.tokens_to_be_outputted
        # print("Token:")
        # print(self.place.token)





#class PetriNet:
#    def __init__(self, places, transitions):



if __name__ == "__main__":

    # Set token
    places = []
    place_tokens = [5, 5, 5, 5]
    for i in range(len(place_tokens)):
        place_instance = Place(i, place_tokens[i])
        places.append(place_instance)

    print("---")
    for i in places:
        print(str(i.index) + " - " + str(i.token))
    print("---")


    input = []
    input_req_token = [2, 1, 2]
    place_list = [0, 1, 2]
    for i in range(len(input_req_token)):
        input_instance = InputPlace(places[place_list[i]], input_req_token[i])
        input.append(input_instance)




    output = []
    output_out_token = [1, 1, 2, 1]
    place_list = [1, 2, 3, 0]
    for i in range(len(output_out_token)):
        output_instance = OutputPlace(places[place_list[i]], output_out_token[i])
        output.append(output_instance)


    transitions = []
    transition_input_count = [1, 2]
    transition_output_count = [2, 2]


    temp_input = []
    i = 0
    a = 0 
    while i < len(transition_input_count):
        temp_input.append(input[a:a+transition_input_count[i]])
        a = a + transition_input_count[i]
        i += 1


    temp_output = []
    j = 0
    b = 0
    while j < len(transition_output_count):
        temp_output.append(output[b: b+transition_output_count[j]])
        b = b + transition_output_count[j]
        j += 1


    for i in range(len(temp_input)):
        transition_instance = Transition(temp_input[i], temp_output[i])
        transitions.append(transition_instance)


    # print(transitions[0].output_places[0].tokens_to_be_outputted)


    # print("Place 0 token: " + str(output[0].place.token))
    transitions[0].fire()
    print("Fired transition")

    print("---")
    for i in places:
        print(str(i.index) + " - " + str(i.token))
    print("---")


    # print("Place0 token: " + str(output[0].place.token))
    # transitions[1].fire()
    # print("Fired transition")

    # print("Place0 token: " + str(output[0].place.token))
    # transitions[1].fire()
    # print("Fired transition")



    # print("Input arc list: ")
    # print(input)
    # print("Output arc list: ")
    # print(output)
    # print("Transition list: ")
    # print(transitions)


