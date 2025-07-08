import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd



# Utility Function

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y-30}")

def select_goal(goal):
    global selected_goal
    selected_goal = goal
    for button in goal_buttons:
        if button[0] == goal:
            button[1].config(bg="#00ffdd", fg="black")
        else:
            button[1].config(bg="#ddf2c4", fg="black")

def calculate_bmi():
    try:
        height = float(height_entry.get()) / 100
        weight = float(weight_entry.get())
        bmi = weight / (height**2)
        bmi_label.config(text=f"{bmi:.2f}")
    except ValueError:
        bmi_label.config(text="")

# Main Output Logic 

def get_output():
    user_age = age_entry.get()
    user_height = height_entry.get()
    user_weight = weight_entry.get()
    user_bmi_text = bmi_label.cget("text")
    user_diet_type = diet_type.get()
    user_diet_preference = diet_type_preference.get()
    user_health_condition = diet_type_health_conditions.get()
    user_diet_goal = selected_goal if selected_goal else "None"

    if not (user_age and user_height and user_weight and user_bmi_text):
        messagebox.showwarning("Input Error", "Please fill in all the required fields!")
        return
    if int(user_age) > 80 or int(user_age) < 5:
        messagebox.showwarning("Age Value Error", "Please provide age between 5 and 80")
        return
    if int(user_height) > 300 or int(user_height) < 60:
        messagebox.showwarning("Height Value Error", "Please provide height (in cm) between 60 and 300")
        return
    if int(user_weight) > 500 or int(user_weight) < 30:
        messagebox.showwarning("Weight Value Error", "Please provide weight between 30 and 500")
        return

    try:
        user_bmi = float(user_bmi_text)
        user_weight = float(user_weight)
    except ValueError:
        messagebox.showwarning("Input Error", "Invalid numerical values entered!")
        return

    try:
        df = pd.read_csv("food_data.csv")
    except Exception as e:
        messagebox.showerror("File Error", f"Error reading food_data.csv: {e}")
        return

    def contains_value(cell_value, target):
        if pd.isna(cell_value):
            return False
        return target.lower() in str(cell_value).lower().split(", ")

    if user_diet_type != "All":
        df = df[df["Category"].str.lower() == user_diet_type.lower()]

    if user_health_condition == "High cholesterol":
        df = df[(df["Fats"] < 15) & (df["Fibre"] > 2) & (df["Sugar"] < 5)]
    elif user_health_condition == "Diabetes":
        df = df[(df["Sugar"] < 5) & (df["Fibre"] > 4)]
    elif user_health_condition == "Hypertension":
        df = df[df["Sodium"] < 400]
    elif user_health_condition == "Iron Deficiency":
        df = df[df["Iron"] > 2]

    # Apply Goal & Preference Filters
    if user_diet_goal == "Weight Loss":
        df = df[df["Calories"] <= 300]
    elif user_diet_goal == "Muscle Gain":
        df = df[df["Calories"] >= 300]
    elif user_diet_goal == "Healthy":
        df = df[(df["Calories"] > 100) & (df["Calories"] < 300)]

    if user_diet_preference == "High-Protein":
        df = df.sort_values("Protein", ascending=False)
    elif user_diet_preference == "Keto":
        df = df.sort_values("Carbohydrates", ascending=True).sort_values("Fats", ascending=False)

    # Organize meal plan
    meal_plan = {"breakfast": [], "lunch": [], "snack": [], "dinner": []}
    for meal in meal_plan.keys():
        df_meal = df[df["Meal Type"].apply(lambda x: contains_value(x, meal))]
        meal_plan[meal] = df_meal["Food_items"].head(4).tolist()



    # Output popup
    output_window = tk.Toplevel(root, bg=app_bg)
    output_window.title("Meal Plan Recommendation")
    output_window.geometry(f"1300x590")

    def display_meal(title, meal_list, x_pos):
        tk.Label(output_window, text=title, font=(app_font_family, 19), bg=app_bg, fg="#1f1cb5").place(x=x_pos, y=180)
        frame = tk.Frame(output_window, bg=app_text_bg, pady=10)
        frame.place(x=x_pos, y=230, height=250)
        for item in meal_list:
            tk.Label(frame, text=item.capitalize(), font=(app_bg, 14), bg=app_text_bg, fg="#070a03", 
            padx=5, pady=5).pack(anchor="w", padx=15)

    # Display all meals
    tk.Label(output_window, text="NutriMate", font=(app_font_family, 32, "bold"), bg=app_bg, fg="blue").place(x=x_value, y=33)
    tk.Label(output_window, text="Your Personalized Diet ",
            font=(app_font_family, app_font_size), bg=app_text_bg,fg="black" , pady=7, padx=15).place(x=x_value, y=95)
 
    display_meal("Breakfast", meal_plan["breakfast"], 40)
    display_meal("Lunch", meal_plan["lunch"], 340)
    display_meal("Snack", meal_plan["snack"], 620)
    display_meal("Dinner", meal_plan["dinner"], 900)

   
# GUI Configuration

root = tk.Tk()
root.title("NutriMate – Personalized Diet Recommendation System")
window_width, window_height = 950, 630
center_window(root, window_width, window_height)
app_bg = "#8CB8E1"         # Background blue
app_text_bg = "#4169E1"    # Better than dark blue, vibrant
button_hover_bg = "#27408B"
entry_bg = "white"
label_fg = "#1a1a1a"
app_font_family = "Arial"
app_font_size = 14
app_label_fsize = 13
x_value = 60
y_spacing = 80
root.configure(bg=app_bg)
root.resizable(False, False)
root.iconbitmap("dieticon.ico") #GUI Icon

# GUI bakcground Image

image = Image.open("dietremovedbg.png").resize((250, 250))  # Replace with your image
photo = ImageTk.PhotoImage(image)

image_label = tk.Label(root, image=photo, bg="#8CB8E1")
image_label.image = photo  # Prevent garbage collection
image_label.place(x=650, y=200)


# GUI Form Elements

# Title
tk.Label(root, text="NutriMate", font=(app_font_family, 32, "bold"), bg=app_bg, fg="blue").place(x=x_value, y=33)
tk.Label(root, text="Eat Right. Feel Bright 🔥.", font=(app_font_family, 12, "bold",),
         bg=app_bg, fg="Blue").place(x=x_value + 260, y=50)

tk.Label(root, text="A PERSONALIZED DIET RECOMMENDATION SYSTEM", 
         font=(app_font_family, 13,), 
         bg="#8CB8E1", pady=8, padx=5).place(x=x_value, y=80)

# Input Fields
def place_label_and_entry(label_text, x, y, var):
    tk.Label(root, text=label_text, font=(app_font_family, app_label_fsize, "bold"), bg=app_bg, fg="black").place(x=x, y=y)
    var.place(x=x, y=y + 33)

age_entry = tk.Entry(root, font=(app_font_family, app_font_size), bg="white", border=0)
place_label_and_entry("AGE", x_value, 170, age_entry)

height_entry = tk.Entry(root, font=(app_font_family, app_font_size), border=0)
place_label_and_entry("HEIGHT IN CM", x_value, 250, height_entry)

weight_entry = tk.Entry(root, font=(app_font_family, app_font_size), border=0)
place_label_and_entry("WEIGHT IN KG", x_value, 330, weight_entry)

height_entry.bind("<KeyRelease>", lambda e: calculate_bmi())
weight_entry.bind("<KeyRelease>", lambda e: calculate_bmi())

diet_type = ttk.Combobox(root, values=["All", "Veg", "Non-Veg","Vegan"], state="readonly",
                         font=(app_font_family, app_font_size))
diet_type.current(0)
place_label_and_entry("DIET TYPE", 330, 170, diet_type)

diet_type_preference = ttk.Combobox(root, values=["None", "High-Protein", "Keto"], state="readonly",
                                    font=(app_font_family, app_font_size))
diet_type_preference.current(0)
place_label_and_entry("DIET PREFERENCES", 330, 250, diet_type_preference)

diet_type_health_conditions = ttk.Combobox(root,
                                           values=["None", "High cholesterol", "Diabetes", "Cancer", "Iron Deficiency","Any other"],
                                           state="readonly", font=(app_font_family, app_font_size))
diet_type_health_conditions.current(0)
place_label_and_entry("HEALTH CONDITIONS", 330, 330, diet_type_health_conditions)

bmi_label = tk.Label(root, text="BMI : ", font=(app_font_family, app_font_size), bg="white", width=19, anchor="w", padx=5, pady=1, border=0)
tk.Label(root, text="BMI", font=(app_font_family, app_label_fsize, "bold"), bg=app_bg, fg="black").place(x=x_value, y=410)
bmi_label.place(x=x_value, y=440)

# Goal Selection
selected_goal = None
goal_buttons = []

tk.Label(root, text="FITNESS GOAL", font=(app_font_family, app_label_fsize, "bold"), bg=app_bg, fg="black").place(x=x_value, y=490)

frame = tk.Frame(root, bg=app_bg)
frame.place(x=x_value, y=520)

for goal in ["Weight Loss", "Muscle Gain", "Healthy"]:
    btn = tk.Button(frame, text=goal, font=(app_font_family, app_font_size), width=13, bg="white", 
                    command=lambda g=goal: select_goal(g), border=0)
    btn.pack(side="right", padx=10)
    goal_buttons.append((goal, btn))

# Submit Button

tk.Button(root, font=(app_font_family, app_label_fsize, "bold"), bg="#336499", text="Get My Diet Plan", 
          command=get_output, width=16, pady=5, border=0).place(x=x_value + 300, y=590)


root.mainloop()
