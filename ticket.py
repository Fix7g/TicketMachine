try:
    import helpers
except ImportError as err:
    helpers = helpers or None
    print('Couldn\'t load module. %s' % err)
    exit(1)


class Ticket:
    def __init__(self, time=20, discount=False, cost=200):
        self._discount = discount
        self._time = time
        self._cost = cost

    def get_cost(self):
        return self._cost

    def get_time(self):
        return self._time

    def has_discount(self):
        return self._discount

    def __repr__(self):
        _str = str(self._time)+" minutes"
        _str += " N" if self._discount else " D"
        return _str


class TicketStore:
    def __init__(self):
        self.tickets = []

    def add(self, *args):
        for arg in args:
            if isinstance(arg, Ticket):
                self.tickets.append(arg)
            else:
                raise Exception("Some argument is not from Ticket class")

    def remove(self, discount, time):
        for ticket in self.tickets:
            if ticket.has_discount() == discount and ticket.get_time() == time:
                self.tickets.remove(ticket)
                break
        else:
            raise Exception("Ticket not found")

    def remove(self, *tickets):
        for ticket in tickets:
            if isinstance(ticket, Ticket):
                self.tickets.remove(ticket)
            else:
                raise Exception("Some argument is not from Ticket class")

    def get_tickets_with_discount(self):
        tickets = [ticket for ticket in self.tickets if ticket.has_discount()]
        return tickets

    def get_tickets_without_discount(self):
        tickets = [ticket for ticket in self.tickets if not ticket.has_discount()]
        return tickets

    def remove_from(self, store):
        if isinstance(store, TicketStore):
            tickets = store.get_tickets()
            tic = helpers.ListHelper.list_sub(self.tickets, tickets)
            self.tickets = tic
        else:
            raise Exception("Tickets are not from TicketStore")

    def get_tickets(self):
        return self.tickets

    def value(self):
        val = 0
        for ticket in self.tickets:
            val += ticket.get_cost()
        return val

    def get_ticket_type(self, _type):
        types = [20, 40, 60, 20, 40, 60]
        result = {
            '1': lambda: self.get_tickets_without_discount(),
            '2': lambda: self.get_tickets_without_discount(),
            '3': lambda: self.get_tickets_without_discount(),
            '4': lambda: self.get_tickets_with_discount(),
            '5': lambda: self.get_tickets_with_discount(),
            '6': lambda: self.get_tickets_with_discount()
        }[str(_type)]()
        _to_return = []
        for tic in result:
            if tic.get_time() == types[int(_type)-1]:
                _to_return.append(tic)
        return _to_return
