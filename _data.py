try:
    import money
    import ticket
except ImportError as err:
    money = money or None
    ticket = ticket or None
    print('Couldn\'t load module. %s' % err)
    exit(1)


def add_tickets(machine):
    for i in range(2):
        tickets1 = ticket.Ticket(time=20, discount=False, cost=280)
        tickets2 = ticket.Ticket(time=40, discount=False, cost=380)
        tickets3 = ticket.Ticket(time=60, discount=False, cost=500)
        tickets4 = ticket.Ticket(time=20, discount=True, cost=140)
        tickets5 = ticket.Ticket(time=40, discount=True, cost=190)
        tickets6 = ticket.Ticket(time=60, discount=True, cost=250)
        machine.add_tickets(tickets1, tickets2, tickets3, tickets4, tickets5, tickets6)


def add_money(machine):
    for i in range(100):
        coin1 = money.Coin(0.01)
        coin2 = money.Coin(0.02)
        coin3 = money.Coin(0.05)
        coin4 = money.Coin(0.1)
        coin5 = money.Coin(0.2)
        coin6 = money.Coin(0.5)
        coin7 = money.Coin(1)
        coin8 = money.Coin(2)
        coin9 = money.Coin(5)
        bill1 = money.Bill(10)
        bill2 = money.Bill(20)
        bill3 = money.Bill(50)
        bill4 = money.Bill(100)
        bill5 = money.Bill(200)
        bill6 = money.Bill(500)
        machine.add_money(coin1, coin2, coin3, coin4, coin5, coin6, coin7, coin8, coin9,
                          bill1, bill2, bill3, bill4, bill5, bill6)
