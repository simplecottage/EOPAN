from tkinter import Tk, Label, Entry, Button, Frame
from SimConnect import SimConnect, AircraftRequests
import threading, time, random

# init simconnect
sm = SimConnect()
requests = AircraftRequests(sm)

# phase duration in ms
PHASE_DURATION = 60000
phase_active = True

# global vars for arithmetic, digit seq, image count
current_arithmetic_answer = None
digit_sequence = []
target_count = 0

# flight data update (runs every 500ms)
def update_flight_data():
    try:
        alt = requests.get("PLANE_ALTITUDE")
        vario = requests.get("VERTICAL_SPEED")
        rpm = requests.get("GENERAL_ENG_RPM:1")
    except Exception as e:
        alt = vario = rpm = 0
    # determine flight regime based on vertical speed thresholds
    if vario < -50:
        regime = "descente"
        rec_engine = "700 rpm"
        rec_knob = "54"
    elif vario > 50:
        regime = "montée"
        rec_engine = "PLEIN GAZ"
        rec_knob = "98"
    else:
        regime = "palier"
        rec_engine = "1200 rpm"
        rec_knob = "NN"
    fd_text = f"alt: {alt:.1f} | var: {vario:.1f} | rpm: {rpm:.0f}\nregime: {regime} | rec engine: {rec_engine} | rec knob: {rec_knob}"
    flight_label.config(text=fd_text)
    root.after(500, update_flight_data)

# mental arithmetic task: generate new problem every 30 sec
def new_arithmetic_problem():
    global current_arithmetic_answer
    if not phase_active:
        arithmetic_label.config(text="")
        return
    op = random.choice(["+", "-", "*", "/"])
    a = random.randint(1,20)
    b = random.randint(1,20)
    if op == "/":
        a = a * b  # ensure integer division
    problem = f"{a} {op} {b} = ?"
    if op == "+":
        current_arithmetic_answer = a + b
    elif op == "-":
        current_arithmetic_answer = a - b
    elif op == "*":
        current_arithmetic_answer = a * b
    elif op == "/":
        current_arithmetic_answer = a // b
    arithmetic_label.config(text=problem)
    arithmetic_entry.delete(0, "end")
    root.after(30000, new_arithmetic_problem)

def check_arithmetic(event):
    try:
        ans = int(arithmetic_entry.get())
        if ans == current_arithmetic_answer:
            arithmetic_feedback.config(text="correct", fg="green")
        else:
            arithmetic_feedback.config(text="wrong", fg="red")
    except:
        arithmetic_feedback.config(text="invalid", fg="red")
    root.after(2000, lambda: arithmetic_feedback.config(text=""))

# digit sequence task: generate a random 4-5 digit sequence at phase start and schedule displays
def start_digit_sequence():
    global digit_sequence
    length = random.choice([4,5])
    digit_sequence = [str(random.randint(0,9)) for _ in range(length)]
    delay = 5000  # start after 5 sec
    for d in digit_sequence:
        root.after(delay, lambda digit=d: show_digit(digit))
        delay += random.randint(5000,15000)

def show_digit(d):
    digit_label.config(text=d)
    root.after(1000, lambda: digit_label.config(text=""))

# image counting task: schedule 10 random image events; count only target images
def start_image_counting():
    global target_count
    target_count = 0
    target_image_label.config(text="TARGET", bg="blue", fg="white")
    for _ in range(10):
        delay = random.randint(5000, PHASE_DURATION-5000)
        root.after(delay, show_random_image)

def show_random_image():
    global target_count
    is_target = random.choice([True, False])
    img_text = "TARGET" if is_target else "DECOY"
    if is_target:
        target_count += 1
    image_popup.config(text=img_text, bg="blue" if is_target else "gray", fg="white")
    root.after(500, lambda: image_popup.config(text=""))

# phase end: enable user inputs for digit seq and image count answers
def end_phase():
    global phase_active
    phase_active = False
    phase_status.config(text="phase ended. enter digit seq & image count.")
    digit_entry_frame.pack(pady=5)
    image_entry_frame.pack(pady=5)

def check_digit_sequence():
    entered = digit_entry.get()
    correct = "".join(digit_sequence)
    if entered == correct:
        digit_result.config(text="digit sequence correct", fg="green")
    else:
        digit_result.config(text=f"wrong (was {correct})", fg="red")

def check_image_count():
    try:
        entered = int(image_entry.get())
        if entered == target_count:
            image_result.config(text="image count correct", fg="green")
        else:
            image_result.config(text=f"wrong (was {target_count})", fg="red")
    except:
        image_result.config(text="invalid", fg="red")

# setup tkinter ui
root = Tk()
root.geometry("600x400+100+100")
root.title("overlay msfs2024")
root.attributes("-topmost", True)
root.overrideredirect(True)
root.config(bg="black")

# flight data frame
flight_frame = Frame(root, bg="black")
flight_frame.pack(fill="x", pady=5)
flight_label = Label(flight_frame, text="connexion à msfs...", font=("arial",16), bg="black", fg="white")
flight_label.pack()

# arithmetic frame
arithmetic_frame = Frame(root, bg="black")
arithmetic_frame.pack(fill="x", pady=5)
arithmetic_label = Label(arithmetic_frame, text="", font=("arial",14), bg="black", fg="yellow")
arithmetic_label.pack(side="left", padx=5)
arithmetic_entry = Entry(arithmetic_frame, font=("arial",14))
arithmetic_entry.pack(side="left", padx=5)
arithmetic_feedback = Label(arithmetic_frame, text="", font=("arial",14), bg="black", fg="white")
arithmetic_feedback.pack(side="left", padx=5)
arithmetic_entry.bind("<Return>", check_arithmetic)

# digit sequence display frame
digit_frame = Frame(root, bg="black")
digit_frame.pack(fill="x", pady=5)
digit_label = Label(digit_frame, text="", font=("arial",16), bg="black", fg="cyan")
digit_label.pack()

# hidden digit answer entry frame (shown at phase end)
digit_entry_frame = Frame(root, bg="black")
digit_entry = Entry(digit_entry_frame, font=("arial",16))
digit_entry.pack(side="left", padx=5)
Button(digit_entry_frame, text="check digit seq", command=check_digit_sequence).pack(side="left", padx=5)
digit_result = Label(digit_entry_frame, text="", font=("arial",14), bg="black", fg="white")
digit_result.pack(side="left", padx=5)

# image counting frame
image_frame = Frame(root, bg="black")
image_frame.pack(fill="x", pady=5)
target_image_label = Label(image_frame, text="", font=("arial",14), bg="black", fg="white")
target_image_label.pack(side="left", padx=5)
image_popup = Label(image_frame, text="", font=("arial",14), bg="black", fg="white")
image_popup.pack(side="left", padx=5)

# hidden image answer entry frame (shown at phase end)
image_entry_frame = Frame(root, bg="black")
image_entry = Entry(image_entry_frame, font=("arial",16))
image_entry.pack(side="left", padx=5)
Button(image_entry_frame, text="check image count", command=check_image_count).pack(side="left", padx=5)
image_result = Label(image_entry_frame, text="", font=("arial",14), bg="black", fg="white")
image_result.pack(side="left", padx=5)

# phase status label
phase_status = Label(root, text="phase in progress...", font=("arial",16), bg="black", fg="white")
phase_status.pack(pady=5)

# start tasks
root.after(0, update_flight_data)
root.after(0, new_arithmetic_problem)
start_digit_sequence()
start_image_counting()
root.after(PHASE_DURATION, end_phase)

root.mainloop()
