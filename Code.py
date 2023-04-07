import time
from io import BytesIO
from PIL import Image, ImageTk
import requests
import json
import tkinter as tk

class Recipe:
    def __init__(self, id, title, image_url):
        self.id = id
        self.title = title
        self.image_url = image_url
        self.preview_image = None

class RecipeList:
    def __init__(self):
        self.recipes = []

    def search(self, query, number):
        api_key = "YOUR-API-KEY-FOR-SPOOMCULAR"
        url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&query={query}&number={number}"
        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.Timeout:
            print("Error", "Connection timed out.")
            time.sleep(3)
            error()
            self.recipes = []
            return
        except requests.exceptions.RequestException:
            print ("Error, Connection error.")
            time.sleep(3)
            error()
            self.recipes = []
            return
        
        if response.status_code == 200:
            data = json.loads(response.content)
            self.recipes = []
            for result in data["results"]:
                recipe = Recipe(result["id"], result["title"], result["image"])
                self.recipes.append(recipe)
                if recipe.image_url:
                    image_response = requests.get(recipe.image_url)
                    if image_response.status_code == 200:
                        recipe.preview_image = Image.open(BytesIO(image_response.content)).resize((200, 200))
        if len(self.recipes) > 32:
            print ("Error, Too many images requested.")
            time.sleep(3)
            error()
            self.recipes = []

recipe_list = RecipeList()

while True:
    query = input("Enter a recipe search query: ")
    num_images = int(input("Enter the number of images you want to display (max. 32): "))
    print("Wait...")
    recipe_list.search(query, num_images)

    if len(recipe_list.recipes) <= 32:
        break

root = tk.Tk()

for i, recipe in enumerate(recipe_list.recipes):
    if i >= num_images:
        break
    if recipe.preview_image:
        col = i % 8
        row = i // 8
        photo = ImageTk.PhotoImage(recipe.preview_image)
        image_label = tk.Label(root, image=photo)
        image_label.image = photo
        image_label.grid(row=row, column=col)
