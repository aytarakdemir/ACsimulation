from petri import PetriNet

# View photo 5 times and no more
petri = PetriNet('net_config/photo_view_limit.txt', 0.5)
petri.printPlaceTokens()
petri.fire(0)
petri.fire(0)
petri.fire(0)
petri.fire(0)
petri.fire(0)
petri.fire(0)
petri.fire(0)
petri.printPlaceTokens()

# Infinite token
petri2 = PetriNet('net_config/infinite_token_loop.txt')
petri2.printPlaceTokens()
petri2.fire(0)
petri2.fire(0)
petri2.fire(0)
petri2.printPlaceTokens()

# Give permission to read for 2 times only
petri3 = PetriNet('net_config/give_permission.txt')
petri3.printPlaceTokens()
petri3.fire(1) # Cannot fire
petri3.printPlaceTokens()
petri3.fire(0) # Give permission for twice
petri3.printPlaceTokens()
petri3.fire(1) # Can read
petri3.printPlaceTokens()
petri3.fire(1) # Can read again
petri3.printPlaceTokens()
petri3.fire(1) # Cannot read anymore


""" Pull request review process: at least 3 people need to approve in order for PR request to be accepted. If the previous PR is not accepted
then the a new PR cannot be created.
"""
petri4 = PetriNet('net_config/pull_request_review.txt')
petri4.printPlaceTokens()
petri4.fire(0)
petri4.printPlaceTokens()
petri4.fire(2)
petri4.fire(2)
petri4.fire(2)
petri4.printPlaceTokens()
petri4.fire(1)
petri4.printPlaceTokens()


# Give permission to write and take away permission (can also grant permission to give others permission)
petri5 = PetriNet('net_config/grant_and_revoke_permission.txt')
petri5.printPlaceTokens()
petri5.fire(1)
petri5.fire(1) # Cannot write
petri5.fire(2) # Cannot revoke since there is no permission anyway
petri5.fire(0) # Give permission to write
petri5.fire(1) # Write
petri5.fire(1) # Write as much as you like :)
petri5.fire(2) # Permission revoked
petri5.fire(1) # Cannot write :(









