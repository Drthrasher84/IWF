from flask import Flask, request, render_template, redirect, url_for
import random
import json
import time

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
        self.match_log = []  # Store the events of the match

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

    def start_match(self):
        self.match_log.append("The match begins!")
        while not self.wrestler1.is_knocked_out() and not self.wrestler2.is_knocked_out():
            attacker, defender = random.choice([
                (self.wrestler1, self.wrestler2),
                (self.wrestler2, self.wrestler1),
            ])
            move, damage = self.simulate_move(attacker, defender)
            self.match_log.append(f"{move} ({defender.name} takes {damage} damage!)")
            self.match_log.append(f"{defender.name}'s health: {defender.health}")

        winner = self.wrestler1 if not self.wrestler1.is_knocked_out() else self.wrestler2
        self.match_log.append(f"{winner.name} wins the match!")
        return self.match_log

class BattleRoyalMatch:
    def __init__(self, wrestlers):
        self.wrestlers = wrestlers  # List of all wrestlers in the match
        self.match_events = []  # Store events for a visual summary

    def simulate_move(self, attacker, defender):
        """Simulate a move from one wrestler to another."""
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
        """Store match events for later display."""
        self.match_events.append(message)

    def start_match(self):
        """Simulate the Battle Royal match."""
        self.announce("The Battle Royal begins!")
        
        while len(self.wrestlers) > 1:
            # Randomly pick an attacker and a defender
            attacker, defender = random.sample(self.wrestlers, 2)
            move, damage = self.simulate_move(attacker, defender)
            
            self.announce(f"{move} ({defender.name} takes {damage} damage!)")
            self.announce(f"{defender.name}'s health: {defender.health}")
            
            if defender.is_knocked_out():
                self.announce(f"{defender.name} is eliminated!")
                self.wrestlers.remove(defender)

        winner = self.wrestlers[0]
        self.announce(f"{winner.name} wins the Battle Royal!")
        return winner, self.match_events




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

def create_or_load_wrestlers():
    """Load existing wrestlers and allow the creation of new ones."""
    wrestlers = load_wrestlers()

    if wrestlers:
        print("Saved wrestlers found!")
        choice = input("Enter 'yes' to use saved wrestlers or 'no' to create new ones: ").strip().lower()
        if choice == "yes":
            add_more = input("Do you want to create additional wrestlers? (yes/no): ").strip().lower()
            if add_more == "yes":
                while True:
                    wrestlers.append(create_wrestler())
                    more = input("Do you want to create another wrestler? (yes/no): ").strip().lower()
                    if more != "yes":
                        break
                save_wrestlers(wrestlers)
            return wrestlers

    print("No saved wrestlers found or new ones being created.")
    while True:
        wrestlers.append(create_wrestler())
        more = input("Do you want to create another wrestler? (yes/no): ").strip().lower()
        if more != "yes":
            break
    save_wrestlers(wrestlers)
    return wrestlers

def save_match_results(winner, events, filename="match_results.json"):
    """Save the results of a match to a file."""
    try:
        with open(filename, "r") as file:
            match_history = json.load(file)
    except FileNotFoundError:
        match_history = []

    match_history.append({
        "winner": winner.name,
        "events": events
    })

    with open(filename, "w") as file:
        json.dump(match_history, file, indent=4)

# Flask routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create_wrestler", methods=["GET", "POST"])
def create_wrestler_page():
    if request.method == "POST":
        name = request.form["name"]
        strength = int(request.form["strength"])
        agility = int(request.form["agility"])
        charisma = int(request.form["charisma"])

        new_wrestler = Wrestler(name, strength, agility, charisma)
        wrestlers = load_wrestlers()
        wrestlers.append(new_wrestler)
        save_wrestlers(wrestlers)

        return redirect("/wrestlers")

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

@app.route("/wrestlers")
def show_wrestlers():
    wrestlers = load_wrestlers()
    return render_template("wrestlers.html", wrestlers=wrestlers)

@app.route("/delete/<name>", methods=["POST"])
def delete_wrestler(name):
    wrestlers = load_wrestlers()
    wrestlers = [w for w in wrestlers if w.name != name]  # Filter out the wrestler to delete
    save_wrestlers(wrestlers)  # Save the updated list
    return redirect(url_for("show_wrestlers"))

@app.route("/edit/<name>", methods=["GET", "POST"])
def edit_wrestler(name):
    wrestlers = load_wrestlers()
    wrestler = next((w for w in wrestlers if w.name == name), None)
    if not wrestler:
        return "Wrestler not found!", 404

    if request.method == "POST":
        # Update wrestler stats from the form
        wrestler.strength = int(request.form["strength"])
        wrestler.agility = int(request.form["agility"])
        wrestler.charisma = int(request.form["charisma"])
        save_wrestlers(wrestlers)
        return redirect(url_for("show_wrestlers"))

    return render_template("edit_wrestler.html", wrestler=wrestler)

@app.route("/profile/<name>")
def profile(name):
    wrestlers = load_wrestlers()
    wrestler = next((w for w in wrestlers if w.name == name), None)
    if not wrestler:
        return "Wrestler not found!", 404
    return render_template("profile.html", wrestler=wrestler)

@app.route("/run_match", methods=["GET", "POST"])
def run_match():
    wrestlers = load_wrestlers()
    
    if request.method == "POST":
        wrestler1_name = request.form["wrestler1"]
        wrestler2_name = request.form["wrestler2"]
        
        wrestler1 = next((w for w in wrestlers if w.name == wrestler1_name), None)
        wrestler2 = next((w for w in wrestlers if w.name == wrestler2_name), None)
        
        if wrestler1 and wrestler2:
            # Start the match with the selected wrestlers
            match = WrestlingMatch(wrestler1, wrestler2)
            match_result = match.start_match()  # Simulate the match
            
            # Redirect to the match result page
            return render_template("match_result.html", match_result=match_result)
    
    return render_template("run_match.html", wrestlers=wrestlers)

@app.route("/battle_royal", methods=["GET", "POST"])
def battle_royal():
    wrestlers = load_wrestlers()

    if request.method == "POST":
        selected_ids = request.form.getlist("wrestlers")
        selected_wrestlers = [wrestlers[int(i)] for i in selected_ids]
        
        if len(selected_wrestlers) < 2:
            return "You need at least 2 wrestlers for a Battle Royal!", 400
        
        # Run the match
        match = BattleRoyalMatch(selected_wrestlers)
        winner, events = match.start_match()
        
        # Save results
        save_match_results(winner, events)

        return redirect("/match_summary")

    return render_template("battle_royal.html", wrestlers=wrestlers)

@app.route("/match_summary")
def match_summary():
    """Display the summary of the last match."""
    try:
        with open("match_results.json", "r") as file:
            match_history = json.load(file)
        last_match = match_history[-1]
    except (FileNotFoundError, IndexError):
        last_match = None

    return render_template("match_summary.html", match=last_match)

@app.route("/past_matches")
def past_matches():
    """Display a list of all past matches."""
    try:
        with open("match_results.json", "r") as file:
            match_history = json.load(file)
    except FileNotFoundError:
        match_history = []

    return render_template("past_matches.html", matches=match_history)


if __name__ == "__main__":
    app.run(debug=True)
