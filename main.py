try:
    import helpers
    import machine
    import _data
    import money
    from pubsub import pub
    import tkinter as tk
except ImportError as err:
    helpers = helpers or None
    machine = machine or None
    _data = _data or None
    money = money or None
    pub = pub or None
    tk = tk or None
    print('Couldn\'t load module. %s' % err)
    exit(1)

path = "data/images/"
ticket_files = ["20.gif", "40.gif", "60.gif", "20ulg.gif", "40ulg.gif", "60ulg.gif"]
coin_files = ["1.png", "2.png", "5.png", "10.png", "20.png", "50.png", "100.png", "200.png", "500.png"]
bill_files = ["10zl.png", "20zl.png", "50zl.png", "100zl.png", "200zl.png"]


class BillFrame(tk.Toplevel):
    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master=master)
        self.init_window()

        self.machine = master.machine
        self.init_money_buttons()
        self.paid = self.paid_label()

    def init_window(self):
        self.geometry("+%d+%d" % (
                                  self.master.winfo_rootx() + 50,
                                  self.master.winfo_rooty() + 50
                                  )
                      )
        self.title("Pay for tickets")
        self.show()

    def init_money_buttons(self):
        self.load_coins()
        self.load_bills()

    def pay(self, value):
        self.machine.pay(value)
        self.update_paid()
        if self.machine.bought:
            helpers.show_info("You bought tickets\nYour remainder : "+str(self.machine.get_remainder()))
            self.machine.new_user()
            self.withdraw()
            pub.sendMessage("bought", arg1="xd")

    def paid_label(self):
        info_label = tk.Label(self.master, text="Paid")
        info_label.grid()
        value = self.machine.user_money.get_total()
        value = self.machine.machineMoney.convert(value)
        paid = helpers.new_label(self.master, value)
        paid.grid()
        return paid

    def update_paid(self):
        val = self.machine.user_money.get_total()
        val = self.machine.machineMoney.convert(val)
        self.paid['text'] = val

    def show(self):
        self.update()
        self.deiconify()

    def load_coins(self):
        for file in coin_files:
            file_path = path+file
            coin = helpers.btn_with_img(self, file_path, lambda val=helpers.coin_val(file): self.pay(money.Coin(val)))
            coin.pack(side=tk.LEFT)

    def load_bills(self):
        for file in bill_files:
            file_path = path+file
            bill = helpers.btn_with_img(self, file_path, lambda val=helpers.bill_val(file): self.pay(money.Bill(val)))
            bill.pack(side=tk.LEFT)


class TicketSelector(tk.Toplevel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master=master)
        self.inputs = []
        self.init_frame()
        self.machine = master.machine
        self.init_button_tickets()

        self.to_pay = self.to_pay_label()

        btn = tk.Button(self, text="Go back", command=self.on_back)
        btn.grid(column=2)

        self.money_window = BillFrame(self)

        pub.subscribe(self.listener, "bought")

    # ----------------------------------------------------------------------

    def init_frame(self):
        self.geometry("600x400")
        self.title("Ticket Selector")
        self.maxsize(600, 400)
        self.minsize(600, 400)

    def to_pay_label(self):
        info_label = tk.Label(self, text="To pay")
        info_label.grid()
        value = self.machine.selected_tickets.value()
        value = self.machine.machineMoney.convert(value)
        to_pay = helpers.new_label(self, value)
        to_pay.grid()
        return to_pay

    def change_to_pay(self):
        to_pay = self.machine.selected_tickets.value()
        to_pay = self.machine.machineMoney.convert(to_pay)
        self.to_pay['text'] = to_pay

    def on_back(self):
        self.machine.selected_to_machines()
        self.machine.new_user_space()
        self.destroy()
        pub.unsubscribe(self.listener, "bought")
        pub.sendMessage("other_frame_destroyed", arg1="data")

    def on_close(self):
        self.withdraw()
        pub.sendMessage("other_frame_closed", arg1="data")

    def init_button_tickets(self):
        row = 0
        column = 0
        i = 1
        for file in ticket_files:
            button = helpers.btn_with_img(self, path+file, lambda j=i: self.select_ticket(j))
            button.grid(row=row, column=column, padx=35, pady=10)
            self.init_input(i, column, row)
            column = column + 1
            if column % 3 == 0:
                row = row + 2
                column = 0
            i = i + 1

    def init_input(self, _type, column, row):
        a = helpers.entry(self, column=column, row=row + 1)
        a.bind("<Return>", lambda x, y=a, j=_type: self.select_tickets(j, y))
        self.inputs.append(a)

    def select_ticket(self, index):
        self.machine.select_ticket(index)
        self.update_input(index, len(self.machine.selected_tickets.get_ticket_type(index)))
        self.change_to_pay()

    def update_input(self, j, _val):
        value = self.inputs[j-1]
        value.delete(0, tk.END)
        value.insert(0, _val)

    def select_tickets(self, ticket_type, count):
        try:
            val = count.get()
            self.machine.select_few(ticket_type, val)
            self.change_to_pay()
            self.update_input(ticket_type, val)
        except Exception:
            # transaction
            raise

    def on_destroy(self):
        self.destroy()
        self.unsub_from_event()
        self.send_msg_to_listener(text="other_frame_destroyed", arg1="data")

    def send_msg_to_listener(self, text, arg1):
        pub.sendMessage(text, arg1=arg1)

    def unsub_from_event(self):
        pub.unsubscribe(self.listener, "bought")

    # ----------------------------------------------------------------------
    def listener(self, arg1, arg2=None):
        """
        pubsub listener - opens main frame when otherFrame closes
        """
        self.on_destroy()


    # ----------------------------------------------------------------


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.init_frame()

        self.machine = machine.Machine()
        self.init_data()

        pub.subscribe(self.listener, "other_frame_destroyed")

    # ----------------------------------------------------------------------
    def listener(self, arg1, arg2=None):
        """
        pubsub listener - opens main frame when otherFrame closes
        """
        self.show()

    # ----------------------------------------------------------------

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Ticket selector"
        self.hi_there["command"] = self.open_window
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def init_frame(self):
        self.set_fixed_resolution(800, 600)
        self.set_title("Ticket Machine")

    def set_fixed_resolution(self, width,  height):
        self.master.minsize(width, height)
        self.master.maxsize(width, height)

    def set_title(self, title):
        self.master.title(title)

    def show(self):
        self.master.update()
        self.master.deiconify()

    def open_window(self):
        self.hide()
        self.sub_frame = TicketSelector(self)

    def on_close_other_frame(self, other_frame):
        other_frame.destroy()
        self.show()

    def hide(self):
        self.master.withdraw()

    def exit(self):
        self.master.destroy()

    def init_data(self):
        _data.add_money(self.machine)
        _data.add_tickets(self.machine)

if __name__ == '__main__':
    root = tk.Tk()
    tk.Tk.report_callback_exception = helpers.show_error
    app = Application(master=root)
    app.mainloop()
