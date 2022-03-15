
''' Classes are named according to the Wikipedia definition of the petri nets.
Examine https://en.wikipedia.org/wiki/Petri_net to undestand what classes do.
'''
class Place:
    def __init__(self, token):
        self.token = token


class Transition:
    def __init__(self, input_places, output_places):
        self.input_places = input_places
        self.output_places = output_places

    def fire(self):
        if all(i.tokenIsSufficient for i in self.input_places):
            for input in self.input_places:
                input.trigger()
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
        self.place -= self.tokens_to_be_inputted

# Arc that goes  transition --> place
class OutputPlace:
    def __init__(self, place, tokens_to_be_outputted = 1):
        self.place = place
        self.tokens_to_be_outputted = tokens_to_be_outputted

    def trigger(self):
        self.place.token += self.tokens_to_be_outputted




#class PetriNet: