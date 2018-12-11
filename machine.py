try:
    import money
    import ticket
    import helpers
except ImportError as err:
    money = money or None
    ticket = ticket or None
    helpers = helpers or None
    print('Couldn\'t load module. %s' % err)
    exit(1)


class Machine:
    def __init__(self):
        self.machineTicket = ticket.TicketStore()
        self.machineMoney = money.MoneyStore()

        self.selected_tickets = ticket.TicketStore()
        self.user_money = money.MoneyStore()

        self.remainder = money.MoneyStore()

        self.bought = False

    def add_tickets(self, *tickets):
        for tic in tickets:
            self.machineTicket.add(tic)

    def add_money(self, *mon):
        for m in mon:
            self.machineMoney.add(m)

    def select_ticket(self, ticket_type):
        tics = self.machineTicket.get_ticket_type(ticket_type)
        if len(tics) == 0:
            raise Exception("Cannot select more of this type of tickets")
        else:
            selected = tics.pop()
            self.selected_tickets.add(selected)
            self.machineTicket.remove(selected)
            print(self.selected_tickets.value())

    def select_few(self, ticket_type, count):
        try:
            if helpers.is_int(count) and int(count) >= 0:
                self.deselect_all(ticket_type)
                tics = self.machineTicket.get_ticket_type(ticket_type)
                if (len(tics) == 0 and len(tics) != int(count)) or int(count) > len(tics):
                    raise Exception("Cannot select more of this type of tickets")
                else:
                    for i in range(int(count)):
                        selected = tics.pop()
                        self.selected_tickets.add(selected)
                        self.machineTicket.remove(selected)
            else:
                raise Exception("Value must be positive integer")
        except Exception:
            raise

    def deselect_ticket(self, ticket_type):
        try:
            tics = self.selected_tickets.get_ticket_type(ticket_type)
            selected = tics.pop()
            self.machineTicket.add(selected)
            self.selected_tickets.remove(selected)
        except Exception:
            print("Cant deselect this ticket")

    def deselect_all(self, ticket_type):
        try:
            tics = self.selected_tickets.get_ticket_type(ticket_type)
            for tic in tics:
                self.machineTicket.add(tic)
                self.selected_tickets.remove(tic)
        except Exception:
            print("Cant deselect those tickets")

    def pay(self, mon):
        if self.selected_tickets.get_tickets():
            self.user_money.add(mon)
            if self.user_money.get_total() >= self.selected_tickets.value():
                self.buy()
        else:
            raise Exception("Select ticket first")

    def buy(self):
        try:
            tickets = self.selected_tickets
            total_cost = tickets.value()
            to_back = self.user_money.get_total() - total_cost

            if len(self.selected_tickets.get_tickets()):
                if total_cost <= self.user_money.get_total():
                    print('Machine money ', self.machineMoney.get())
                    print('Machine tickets ', self.machineTicket.get_tickets())

                    print('User gave ', self.user_money.get())
                    print('Tickets cost ', total_cost)

                    self.remainder = self.machineMoney.remainder(self.user_money, to_back)
                    # self.machineTicket.remove_from(self.selected_tickets)

                    print('Remainder for user', self.remainder.get())
                    print('Machine money after remainder', self.machineMoney.get())
                    print('Machine tickets ', self.machineTicket.get_tickets())
                    self.bought = True
                else:
                    print("Not enough money")
        except Exception:
            pass

    def get_remainder(self):
        return self.remainder

    def new_user(self):
        self.bought = False
        self.new_user_space()

    def selected_to_machines(self):
        sel = self.selected_tickets.get_tickets()
        for tic in sel:
            self.machineTicket.add(tic)
        for tic in sel:
            self.selected_tickets.remove(tic)

    def new_user_space(self):
        self.selected_tickets = ticket.TicketStore()
        self.user_money = money.MoneyStore()
        self.remainder = money.MoneyStore()

