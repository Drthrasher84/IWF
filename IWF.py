import random
import time
import json

class Wrestler:
    def __init__(self, name, strength, agility, charisma):
        self.name = name
        self.strength = strength
        self.agility = agility
        self.charisma = charisma
        self.health = 100

    def take_damage(self, damage):
        self.health -= damage
        self.health = max(self.health, 0)  # Ensure health doesn't go below 0

    def is_knocked_out(self):
        return self.health <= 0

class WrestlingMatch:
    def __init__(self, wrestler1, wrestler2):
        self.wrestler1 = wrestler1
        self.wrestler2 = wrestler2

    def simulate_move(self, attacker, defender):
        move = random.choice([
            f"{attacker.name} delivers a powerful suplex to {defender.name}!",
            f"{attacker.name} lands a high-flying dropkick on {defender.name}!",
            f"{attacker.name} executes a devastating clothesline on {defender.name}!",
            f"{attacker.name} slams {defender.name} into the mat with a body slam!",
            f"{attacker.name} locks {defender.name} into a submission hold!",
        ])

        damage = random.randint(5, 15) + attacker.strength - defender.agility // 2
        damage = max(damage, 0)  # Ensure damage is not negative
        defender.take_damage(damage)

        return move, damage

    def announce(self, message):
        print(message)
        time.sleep(1)  # Add a dramatic pause

    def start_match(self):
        self.announce("The match begins!")
        while not self.wrestler1.is_knocked_out() and not self.wrestler2.is_knocked_out():
            attacker, defender = random.choice([
                (self.wrestler1, self.wrestler2),
                (self.wrestler2, self.wrestler1),
            ])
            move, damage = self.simulate_move(attacker, defender)
            self.announce(f"{move} ({defender.name} takes {damage} damage!)")
            self.announce(f"{defender.name}'s health: {defender.health}")

        winner = self.wrestler1 if not self.wrestler1.is_knocked_out() else self.wrestler2
        self.announce(f"{winner.name} wins the match!")

def save_wrestlers(wrestlers, filename="wrestlers.json"):
    """Save wrestler information to a file."""
    data = [
        {"name": w.name, "strength": w.strength, "agility": w.agility, "charisma": w.charisma}
        for w in wrestlers
    ]
    with open(filename, "w") as file:
        json.dump(data, file)

def load_wrestlers(filename="wrestlers.json"):
    """Load wrestler information from a file."""
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return [Wrestler(d["name"], d["strength"], d["agility"], d["charisma"]) for d in data]
    except FileNotFoundError:
        return []

def create_or_load_wrestlers():
    """Give the option to create new wrestlers or load existing ones."""
    wrestlers = load_wrestlers()
    if wrestlers:
        print("Saved wrestlers found! Do you want to use them?")
        choice = input("Enter 'yes' to use saved wrestlers or 'no' to create new ones: ").strip().lower()
        if choice == "yes":
            return wrestlers
    print("No saved wrestlers found or new ones being created.")
    wrestler1 = create_wrestler()
    wrestler2 = create_wrestler()
    save_wrestlers([wrestler1, wrestler2])
    return [wrestler1, wrestler2]

def create_wrestler():
    print("Create your wrestler:")
    name = input("Enter wrestler's name: ")
    strength = int(input("Enter strength (1-20): "))
    agility = int(input("Enter agility (1-20): "))
    charisma = int(input("Enter charisma (1-20): "))
    return Wrestler(name, strength, agility, charisma)

if __name__ == "__main__":
    print("Welcome to the Wrestling Simulator!")
    player1, player2 = create_or_load_wrestlers()

    # Start the match
    match = WrestlingMatch(player1, player2)
    match.start_match()
