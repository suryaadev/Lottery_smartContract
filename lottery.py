import smartpy as sp

class Lottery(sp.Contract):

    def __init__(self):
        self.init(
            players = sp.map(l = {}, tkey = sp.TNat, tvalue = sp.TAddress),
            ticket_cost = sp.tez(1),
            ticket_ava = sp.nat(2),
            max_tickets = sp.nat(5)
        )

    @sp.entry_point
    def buyTicket(self):
        sp.verify(self.data.ticket_ava > 0, "SORRY :) TICKETS sold out")
        sp.verify(sp.amount >= self.data.ticket_cost, "Invalid amount")

        self.data.players[sp.len(self.data.players)] = sp.sender
        self.data.ticket_ava = sp.as_nat(self.data.ticket_ava - 1)

        extra = sp.amount - self.data.ticket_cost

        sp.if extra > sp.mutez(0):
            sp.send(sp.sender, extra)

    @sp.entry_point
    def findWinner(self):
        sp.verify(self.data.ticket_ava == 0, "GAME is still on")

        winner_id = sp.as_nat(sp.now - sp.timestamp(0)) % self.data.max_tickets
        winner_add = self.data.players[winner_id]

        sp.send(winner_add, sp.balance)
        
        self.data.players = {}
        self.data.ticket_ava = self.data.max_tickets

@sp.add_test(name = "main")
def test():
    rohit = sp.test_account("rohit")
    sanket = sp.test_account("sanket")

    scenario = sp.test_scenario()
    l = Lottery()
    scenario.h1("Lottery Game")
    scenario += l
    scenario += l.buyTicket().run(amount = sp.tez(2), sender = rohit)
    scenario += l.findWinner().run(valid = False)
    scenario += l.buyTicket().run(amount = sp.tez(2), sender = sanket)
    scenario += l.findWinner()
    
