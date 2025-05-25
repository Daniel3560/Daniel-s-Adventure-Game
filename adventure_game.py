# Daniel's Adventure Game

def clear_screen():
    """Clears the console screen for better readability."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Game Setup ---
# Define rooms/locations using a dictionary
rooms = {
    'start_clearing': {
        'name': "Forest Clearing",
        'description': "You are in a quiet forest clearing. Sunlight filters through the leaves. There's a path leading NORTH and a faint glimmer to the EAST.",
        'exits': {'north': 'dark_cave', 'east': 'shimmering_pool'},
        'items': ['old_key'],
        'required_item_for_exit': None
    },
    'dark_cave': {
        'name': "Dark Cave Entrance",
        'description': "The entrance to a dark cave. You can hear a faint dripping sound. The forest clearing is to the SOUTH.",
        'exits': {'south': 'start_clearing', 'inside': 'deep_cave'},
        'items': [],
        'required_item_for_exit': {'inside': 'torch'} # Need a torch to go deeper
    },
    'deep_cave': {
        'name': "Deep Cave",
        'description': "It's pitch black and damp in here. You can barely see a thing! You came from the EXIT. A strange GLOW emanates from deeper within.",
        'exits': {'exit': 'dark_cave', 'glow': 'treasure_chamber'},
        'items': ['ancient_scroll'],
        'required_item_for_exit': None # No item needed once inside deep cave
    },
    'shimmering_pool': {
        'name': "Shimmering Pool",
        'description': "A small pool of water shimmers with an ethereal light. You can see your reflection. The clearing is to the WEST.",
        'exits': {'west': 'start_clearing'},
        'items': ['glowing_orb'],
        'required_item_for_exit': None
    },
    'treasure_chamber': {
        'name': "Ancient Treasure Chamber",
        'description': "You've found it! A chamber filled with glittering gold and ancient artifacts! This looks like the end of your adventure... for now.",
        'exits': {}, # No exits, this is an ending room
        'items': [],
        'required_item_for_exit': None
    }
}

# Player state
player_location = 'start_clearing'
player_inventory = []
game_over = False

# --- Game Functions ---

def display_room():
    """Prints the current room's name, description, exits, and items."""
    current_room = rooms[player_location]
    print(f"\n--- {current_room['name']} ---")
    print(current_room['description'])

    # Display items in the room
    if current_room['items']:
        print("You see the following items here:")
        for item in current_room['items']:
            print(f"- {item.replace('_', ' ').title()}")

    # Display available exits
    exits = ", ".join(current_room['exits'].keys()).upper()
    print(f"Exits: {exits}")

def get_player_choice():
    """Gets and processes player input."""
    global player_location, game_over

    choice = input("\nWhat do you do? (e.g., 'go north', 'take key', 'inventory', 'quit') ").lower().strip()
    action_words = choice.split()

    if not action_words:
        print("Please enter a command.")
        return

    command = action_words[0]

    if command == 'go':
        if len(action_words) < 2:
            print("Go where? (e.g., 'go north')")
            return
        direction = action_words[1]
        move_player(direction)
    elif command == 'take':
        if len(action_words) < 2:
            print("Take what?")
            return
        item_to_take = "_".join(action_words[1:])
        take_item(item_to_take)
    elif command == 'inventory' or command == 'i':
        display_inventory()
    elif command == 'quit' or command == 'exit':
        print("Thanks for playing Daniel's Adventure Game! Goodbye.")
        game_over = True
    else:
        print("I don't understand that command. Try 'go [direction]', 'take [item]', 'inventory', or 'quit'.")

def move_player(direction):
    """Attempts to move the player to a new room."""
    global player_location, game_over

    current_room = rooms[player_location]
    new_location = current_room['exits'].get(direction)

    if new_location:
        # Check for required items for specific exits
        required_items = current_room['required_item_for_exit']
        if required_items and direction in required_items:
            item_needed = required_items[direction]
            if item_needed not in player_inventory:
                print(f"You need a {item_needed.replace('_', ' ')} to go that way.")
                return

        player_location = new_location
        # Check for game end condition
        if player_location == 'treasure_chamber':
            print("\n!!! CONGRATULATIONS !!!")
            print("You have successfully found the Ancient Treasure Chamber and completed your adventure!")
            display_inventory()
            global game_over
            game_over = True
        else:
            clear_screen() # Clear screen after a successful move
    else:
        print("You can't go that way.")

def take_item(item_name):
    """Allows the player to pick up an item from the current room."""
    current_room = rooms[player_location]
    if item_name in current_room['items']:
        player_inventory.append(item_name)
        current_room['items'].remove(item_name)
        print(f"You picked up the {item_name.replace('_', ' ')}.")
    else:
        print(f"There's no {item_name.replace('_', ' ')} here.")

def display_inventory():
    """Shows the player's current inventory."""
    print("\n--- Your Inventory ---")
    if player_inventory:
        for item in player_inventory:
            print(f"- {item.replace('_', ' ').title()}")
    else:
        print("Your inventory is empty.")
    print("--------------------")

# --- Game Loop ---
def play_game():
    clear_screen()
    print("Welcome to Daniel's Adventure Game!")
    print("Your goal is to find the Ancient Treasure Chamber.")
    print("Type 'go [direction]' to move, 'take [item]' to pick things up, 'inventory' to check your items, or 'quit' to exit.")

    while not game_over:
        display_room()
        get_player_choice()

# Start the game
if __name__ == "__main__":
    play_game()