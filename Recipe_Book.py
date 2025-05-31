from colorama import init, Fore
init(autoreset=True)
import time
import csv
import os
# This code makes it so even if the user accidentally makes a typo in the recipe name,
# the program will still try to find a close match, similarly to how a search engine
# would do it.
from difflib import get_close_matches

class Ingredient:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def __str__(self):
        return(f"{self.quantity} of {self.name}.")

class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def __str__(self):
        return(f"Recipe: {self.name}\n"
               f"Ingredients: {', '.join(str(ingredient) for ingredient in self.ingredients)}\n"
               f"Instructions: {self.instructions}\n")

class RecipeBook:
    def __init__(self, flip, search, recipes):
        self.flip = flip
        self.search = search
        self.recipes = []

    # This just assigns a string to the recipe book, so that when you print it, it will
    # show how many recipes are in the book.
    def __str__(self):
        return(f"Recipe Book with {len(self.recipes)} recipes.")

    # This function lets you add a recipe to the recipe book.
    def add_recipe(self, recipes):
        self.recipes.append(recipes)
        print(Fore.GREEN + f"Added recipe: {recipes.name}")
        save_recipe_to_csv(recipes)

    # This function lets you "flip" through the recipes in the book,
    # but really it just checks if your input is valid and then prints the recipe assigned
    # to the recipe number you typed in.
    def search_recipe(self, search):
        recipe_names = [recipe.name.lower() for recipe in self.recipes]
        matches = get_close_matches(search.lower(), recipe_names, n=1, cutoff=0.6)
        if matches:
            matched_name = matches[0]
            for recipe in self.recipes:
                if recipe.name.lower() == matched_name:
                    print(Fore.GREEN + f"Found recipe: {recipe.name}")
                    print(recipe)
                    return
        else:
            print(Fore.RED + f"The recipe '{search}' is not in the book.")

# These functions just save the recipe the user inters into a CSV file, so that 
# they're data doesn't get erased when they close the program or re-run it.
def save_recipe_to_csv(recipe):
    with open("recipes.csv", mode="a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        ingredients_str = '|'.join(f"{ing.name}:{ing.quantity}" for ing in recipe.ingredients)
        writer.writerow([recipe.name, ingredients_str, recipe.instructions])

def load_recipes_from_csv():
    if not os.path.exists("recipes.csv"):
        return []
    recipes = []
    with open("recipes.csv", mode="r", newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            name, ingredients_str, instructions = row
            ingredients = []
            for item in ingredients_str.split('|'):
                if ':' in item:
                    ing_name, quantity = item.split(':', 1)
                    ingredients.append(Ingredient(ing_name, quantity))
            recipes.append(Recipe(name, ingredients, instructions))
    return recipes

# In this program I made it so the only recipe in it is a taco one to keep things simple, 
# since this'll just be what will first appear when you run the program and try to 'look'
# for a recipe.
recipe = Recipe("Taco",
    [Ingredient("Taco shell", "3 small"),
     Ingredient("Ground beef", "1/2 lb"),
     Ingredient("Lettuce", "1/2 cup"),
     Ingredient("Salsa", "1 cup"),
     Ingredient("Guacamole", "3 spoonfuls")
    ], 
"""1. Cook the ground beef in a pan until slightly browned.
2. Add 1/4 cup of water and 3 tablespoons of taco seasoning to the pan and stir.
3. Simmer the meat for 5 minutes.
4. Heat up your taco shells in the oven for 5 minutes at 350 degrees Fahrenheit.
5. Fill the warm taco shells with the sizzling meat, adding in order: lettuce, guacamole, and salsa.""")

recipe_book = RecipeBook(flip=0, search="", recipes=[])
for r in load_recipes_from_csv():
    recipe_book.recipes.append(r)
if not any(r.name.lower() == "taco" for r in recipe_book.recipes):
    recipe_book.add_recipe(recipe)

# This asks the user if they want to start the program:
user_start_raw = input("Would you like to start this program? Type 'yes' or 'no': ").strip().lower()
user_start_match = get_close_matches(user_start_raw, ["yes", "no"], n=1, cutoff=0.6)

if user_start_match and user_start_match[0] == 'yes':
    print(Fore.GREEN + "Great! Let's get started.")
    time.sleep(1)

    # This code gets the user's 'intent' based on what they enter:
    user_search = input("Welcome to the Recipe Book! Would you like to add or look for a recipe? Type 'add' or 'look': ").strip().lower()

    # This next section checks if the user's input is similar to 'add' or 'look'
    # in case they make a typo.
    intent = get_close_matches(user_search, ["add", "look"], n=1, cutoff=0.6)

    if intent and intent[0] == 'add':
        name = input("Enter the recipe name: ").strip()
        ingredients = []

        print("Now, add the recipe ingredients! Type 'done' when you're finished.")
        while True:
            ingredient_name = input("Enter the ingredient name or 'done': ").strip()
            if ingredient_name.lower() == 'done':
                break
            quantity = input(f"Enter quantity for {ingredient_name}: ").strip()
            ingredients.append(Ingredient(ingredient_name, quantity))

        instructions = input("Enter the instructions for the recipe: ").strip()
        new_recipe = Recipe(name, ingredients, instructions)
        recipe_book.add_recipe(new_recipe)
        print(Fore.CYAN + f"'{name}' has been added to your recipe book!")

    elif intent and intent[0] == 'look':
        recipe_search = input("Please enter the name of the recipe you want to look for: ")
        recipe_book.search_recipe(recipe_search)
    else:
        print(Fore.RED + "Your input is invalid, please type 'add' or 'look'.")

elif user_start_match and user_start_match[0] == 'no':
    print("Okay, goodbye!")
    time.sleep(1)
    exit()
else:
    print(Fore.RED + "Your input is invalid, please try again.")
    time.sleep(1)
    exit()