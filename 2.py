import random
import json
from time import sleep

class Human:
    def __init__(self, name, place=None):
        self.name = name
        self.gladness = 50
        self.money = 20
        self.location = None
        try:
            self.travel(place)
        except:
            print("Передайте локацию в конструктор")
    def work(self):
        self.money += random.randint(5, 10)
        self.gladness -= random.randint(2, 5)
    def rest(self):
        self.money -= random.randint(1, 10)
        self.gladness += random.randint(2, 5)
        try:
            self.money -= self.location.money
            self.gladness += self.location.gladness
        except:
            pass
    def travel(self, place):
        if not hasattr(self, "car"):
            self.money -= 2
        if self.location:
            self.location.remove(self)
        self.location = place
        self.location.add(self)

class Car:
    def __init__(self, name, year, price):
        self.name = name
        self.year = year
        self.price = price
    def buy(self, human):
        if human.money >= self.price:
            human.car = self
            self.owner = human
            human.money -= self.price
            print(f"{human.name} купил {self.name}")

#==============================
class Place:
    def __init__(self, name, g, m):
        self.name = name
        self.humans = []
        self.gladness = g
        self.money = m
    def add(self, human):
        if not human in self.humans:
            self.humans.append(human)
    def remove(self, human):
        if human in self.humans:
            self.humans.remove(human)
    def near(self):
        human_info = []
        for human in self.humans:
            human_info.append({"name": human.name, "human": human})
        return human_info

#==============================

class NPCs:
    def __init__(self):
        self.players = []
    def add(self, human):
        if not human in self.players:
            self.players.append(human)
    def add(self, human):
        if human in self.players:
            self.players.remove(human)
    def get(self):
        #Возвращает всех плееров по одному через yield, когда плееры кончаются выдает ошибку StopIteration
        for player in self.players:
            yield player
        raise StopIteration

class NPC(Human):
    def __init__(self, name, place=None):
        super().__init__(name, place)
        self.relationship = 0

class Player(Human):
    def __init__(self, name, h, w):
        super().__init__(name, home)
        self.height = h
        self.weight = w
    def save(self):
        with open('./save.json', 'w') as f:
            data = {}
            data["name"] = self.name
            data["h"] = self.height
            data["w"] = self.weight
            json.dump(data, f)
    def actions(self):
        print("Выберите действие: ")
        print("1. Отдохнуть")
        print("2. Пойти на работу")
        print("3. Купить машину")
        print("4. Баланс")
        print("5. Перейти в локацию")
        print("6. Люди рядом")
    def day(self):
        choice = int(input("-> "))
        if choice == 1:
            self.rest()
        elif choice == 2:
            self.work()
        elif choice == 3:
            print("Машины: ")
            for i in range(len(autopark)):
                print(f"{i + 1}. {autopark[i].name}")
            choice = int(input("-> "))
            if choice >= 0 and choice < len(autopark):
                autopark[choice - 1].buy(self)
            else:
                self.day()
        elif choice == 4:
            print(f"Баланс: {self.money}")
            self.day()
        elif choice == 5:
            print("Локации: ")
            for i in range(len(places)):
                print(f"{i + 1}. {places[i].name}")
            choice = int(input("-> "))
            if choice >= 0 and choice <= len(places):
                self.travel(places[choice - 1])
            else:
                self.day()
        elif choice == 6:
            humans = self.location.humans
            humans.remove(self)
            print("Люди: ")
            for i in range(len(humans)):
                print(f"{i + 1}. {humans[i].name}")
            choice = int(input("-> "))
            if choice >= 0 and choice < len(humans) + 1:
                self.npcsActions(humans[choice - 1])
            else:
                self.day()
        else:
            self.day()
    def npcsActions(self, human):
        print("Дейсвтия: ")
        for i in range(len(npcs_actions)):
            print(f"{i + 1}. {npcs_actions[i].name}")
        choice = int(input("-> "))
        npcs_actions[choice - 1].do(self, human)

class Thief(Human):
    def __init__(self, name):
        super().__init__(name, Place("Base", 0, 0))
        self.strenght = random.randint(1, 10)
    def steal(self, human):
        human.money -= self.strenght
        self.money += self.strenght
        print(f"Вор украл деньги у {human.name}")

class Action:
    def __init__(self, name, duo, money, gladness, relation, condition=0):
        self.name = name
        self.duo = duo
        self.money = money
        self.gladness = gladness
        self.relation = relation
        self.condition = condition
    def do(self, initiator, target):
        print()
        if isinstance(initiator, Player) and target.relationship < self.condition:
            return
        if isinstance(initiator, Player) and isinstance(target, NPC):
            target.relationship += self.relation
        if self.duo:
            initiator.money += self.money
            initiator.gladness += self.gladness
            target.money += self.money
            target.gladness += self.gladness
        else:
            initiator.money += self.money
            initiator.gladness += self.gladness
            target.money -= self.money
            target.gladness -= self.gladness

sones = None
autopark = None
player = None
thief = None
places = None
persones = None
npcs = None
npcs_actions = None

def game_start():
    global home
    global autopark
    global thief
    global places
    global persones
    global npcs
    global npcs_actions

    npcs_actions = [
        Action("Украсть деньги", False, 10, 0, -5, 0),
        Action("Поздороваться", True, 0, 1, 1, 0),
        Action("Поговорить о погоде", True, 0, 2, 2, 0),
        Action("Поговорить об общих интересах", True, 0, 5, 5, 0),
        Action("Поцеловать", True, 0, 2, 10, 100),
    ]

    npcs = NPCs()

    home = Place("Home", 0, 0)
    places = [
        home,
        Place("Park", 2, 1),
        Place("Museum", 4, 5),
        Place("Cafe", 6, 10),
    ]

    thief = Thief("Vitaliy")

    #При создании люди появляются в случайных местах
    npcs.add(NPC("Kolya", random.choice(places)))
    npcs.add(NPC("Olya", random.choice(places)))
    npcs.add(NPC("Vadim", random.choice(places)))
    npcs.add(NPC("Nastya", random.choice(places)))
    npcs.add(NPC("Kristina", random.choice(places)))
    npcs.add(NPC("Sergey", random.choice(places)))
    npcs.add(NPC("Andrey", random.choice(places)))
    npcs.add(NPC("Polina", random.choice(places)))

    autopark = [
        Car("BMW", 2019, 200),
        Car("Bentli", 2017, 300),
        Car("Bugatti", 2016, 100),
        Car("Toyota", 2022, 600),
    ]

def create_player():
    global player
    h = input("Введите рост персонажа: ")
    w = input("Введите вес персонажа: ")
    name = input("Введите имя персонажа: ")
    player = Player(name, h, w)
    player.save()

def init_player():
    global player
    try:
        with open('./save.json') as json_file:
            data = json.load(json_file)
            if not data:
                create_player()
            else:
                player = Player(data["name"], data["h"], data["w"])
        npcs.add(player)
    except:
        print("Файл save.json не найден в папке с файлом игры. Добавьте или создайте файл и попробуйте еще раз")
        exit()

game_start()
init_player()

day = 1
while True:
    print("Day: ", day)
    print("Location: ", player.location.name)
    print("Money: ", player.money)
    print("Gladness: ", player.gladness)
    player.actions()
    player.day()
    gen = npcs.get()
    while True:
        try:
            human = next(gen)
        except:
            break
        #Используем генератор вместо for
        if isinstance(human, Player):
            continue
        actions = [human.work, human.rest]
        random.choice(actions)()

        if random.randint(1, 100) <= 5:
            if not hasattr(human, "car"):
                car = random.choice(autopark)
                if not hasattr(car, "owner"):
                    car.buy(human)
    if random.randint(1, 100) <= 20:
        thief.steal(random.choice(persones))
    day += 1
per