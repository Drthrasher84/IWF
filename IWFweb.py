from flask import Flask, request, render_template, redirect, url_for
import random
import json

app = Flask(__name__)

# Wrestler class and functions
class Wrestler:
    def __init__(self, name, strength, agility, charisma):
        self.name = name
        self.strength = strength
        self.agility = agility
        self.charisma = charisma
        self.health = 100

    def take_damage(self, damage):
        self.health -= damage
        self.health = max(self.health, 0)

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
        damage = max(damage, 0)
        defender.take_damage(damage)
        return move, damage

def save_wrestlers(wrestlers, filename="wrestlers.json"):
    data = [
        {"name": w.name, "strength": w.strength, "agility": w.agility, "charisma": w.charisma}
        for w in wrestlers
    ]
    with open(filename, "w") as file:
        json.dump(data, file)

def load_wrestlers(filename="wrestlers.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return [Wrestler(d["name"], d["strength"], d["agility"], d["charisma"]) for d in data]
    except FileNotFoundError:
        return []

# Flask routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create", methods=["GET", "POST"])
def create_wrestler():
    if request.method == "POST":
        name1 = request.form["name1"]
        strength1 = int(request.form["strength1"])
        agility1 = int(request.form["agility1"])
        charisma1 = int(request.form["charisma1"])
        wrestler1 = Wrestler(name1, strength1, agility1, charisma1)

        name2 = request.form["name2"]
        strength2 = int(request.form["strength2"])
        agility2 = int(request.form["agility2"])
        charisma2 = int(request.form["charisma2"])
        wrestler2 = Wrestler(name2, strength2, agility2, charisma2)

        # Save wrestlers and start the match
        save_wrestlers([wrestler1, wrestler2])
        return redirect(url_for("match"))
    return render_template("create_wrestler.html")

@app.route("/match")
def match():
    wrestlers = load_wrestlers()
    if len(wrestlers) < 2:
        return "Error: Not enough wrestlers created!"
    wrestler1, wrestler2 = wrestlers[0], wrestlers[1]
    match = WrestlingMatch(wrestler1, wrestler2)
    result = []

    while not wrestler1.is_knocked_out() and not wrestler2.is_knocked_out():
        attacker, defender = random.choice([(wrestler1, wrestler2), (wrestler2, wrestler1)])
        move, damage = match.simulate_move(attacker, defender)
        result.append(f"{move} ({defender.name} takes {damage} damage!)")
        result.append(f"{defender.name}'s health: {defender.health}")
    
    winner = wrestler1 if not wrestler1.is_knocked_out() else wrestler2
    result.append(f"{winner.name} wins the match!")
    return render_template("match_result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
