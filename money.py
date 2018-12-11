try:
    from abc import ABC, abstractmethod
except ImportError as err:
    ABC = ABC or None
    abstractmethod = abstractmethod = None
    print('Couldn\'t load module. %s' % err)
    exit(1)


class Money(ABC):
    """ Abstract class Money defined for handling Coin and Bill subclasses """

    def __init__(self, value=0):
        self._value = value

    @abstractmethod
    def possible_value(self, value):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

    def get_value(self):
        return self._value

    def __repr__(self):
        return MoneyStore.convert(self._value)

    def __str__(self):
        return MoneyStore.convert(self._value)


class Coin(Money):
    def __init__(self, value=0.01):
        super().__init__(value)
        if self.possible_value(value):
            self._value = int(value * 100)
        else:
            raise Exception("Invaild value in Coin class")

    def __add__(self, other):
        return self._value + other

    def possible_value(self, value):
        values = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]
        return value in values


class Bill(Money):
    def __init__(self, value = 10):
        super().__init__(value)
        if self.possible_value(value):
            self._value = value * 100
        else:
            raise Exception("Invalid value in Bill class")

    def __add__(self, other):
        return self._value + other

    def possible_value(self, value):
        values = [10, 20, 50, 100, 200, 500]
        return value in values


class MoneyStore:
    def __init__(self):
        self._values = dict()
        self._total = 0

    def add_another(self, store):
        if isinstance(store, MoneyStore):
            for money, amount in store._values.items():
                if money in self._values.keys():
                    self._values[money] += amount
                else:
                    self._values[money] = amount

    def add(self, value):
        if issubclass(value.__class__, Money):
            key = value.get_value()
            if key in self._values:
                self._values[key] += 1
                self._total += key
            else:
                self._values[key] = 1
                self._total += key

        else:
            raise Exception("Value is not from Money class")

    def add_few(self, value, how_many):
        if issubclass(value.__class__, Money):
            key = value.get_value()
            if key in self._values.keys():
                self._values[key] += how_many
                self._total += key*how_many
            else:
                self._values[key] = how_many
                self._total += key*how_many
        else:
            raise Exception("Value is not from Money class")

    def remove(self, value):
        if issubclass(value.__class__, Money):
            key = value.get_value()
            if key in self._values:
                if self._values[key] == 1:
                    del self._values[key]
                    self._total -= key
                else:
                    self._values[key] -= 1
                    self._total -= key
            else:
                raise Exception("Cannot remove this value")
        else:
            raise Exception("Value is not from Money class")

    def remainder(self, user_money, rest):
        if isinstance(user_money, MoneyStore):
            R = rest

            if R >= 0:
                values_before_remainder = dict(self._values)

                self.add_another(user_money)

                values = sorted(self._values.keys(), reverse=True)

                coins_or_bills = MoneyStore()   # to return

                i = 0

                while R > 0:
                    if i > len(values) - 1:
                        self._values = values_before_remainder
                        raise Exception("MoneyStore doesnt have nominal to give remainder")
                        # or Break
                        # return rest
                    else:
                        L = R // values[i]
                        if L > 0:
                            if L >= self._values[values[i]]:
                                L = self._values[values[i]]
                            R = R - L * values[i]
                            if values[i] // 100 <= 5:
                                coins_or_bills.add_few(Coin(values[i] / 100), L)
                            else:
                                coins_or_bills.add_few(Bill(values[i] // 100), L)

                            if L >= self._values[values[i]]:
                                del self._values[values[i]]
                            else:
                                self._values[values[i]] -= L

                        i = i + 1
                return coins_or_bills
            else:
                raise Exception("Rest is too high that MoneyStore actually has")
        else:
            raise Exception("Rest is not from MoneyStore class")

    def get(self):
        return self._values

    def get_total(self):
        return self._total

    def __repr__(self):
        _str = ""
        for key, value in self._values.items():
            _str += str(value)+"x "+MoneyStore.convert(int(key))+" "
        else:
            return _str

    @staticmethod
    def convert(value):
        _str = ""
        div = value // 100
        if div > 0:
            _str += str(div)+" zl"
            rem = value - div*100
            if rem > 0:
                _str += " "+str(rem)+" gr"
        else:
            rem = value
            _str += str(rem)+" gr"
        return _str
