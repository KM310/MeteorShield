import tkinter as tk
from selenium import webdriver
from selenium.webdriver.edge.service import Service

# Edge WebDriver starten
service = Service("msedgedriver.exe")
driver = webdriver.Edge(service=service)
driver.get("https://chromedino.com/")

# -------------------------
# JS EXECUTE
# -------------------------
def js(code):
    try:
        driver.execute_script(code)
    except Exception as e:
        print("Fehler:", e)

# -------------------------
# Hacks
# -------------------------

# Speedhack toggle + slider
speed_slider_visible = False
def toggle_speed_slider():
    global speed_slider_visible
    if not speed_slider_visible:
        speed_slider.pack(pady=5)
        speed_slider_visible = True
    else:
        speed_slider.pack_forget()
        speed_slider_visible = False

def apply_speed(val):
    js(f"Runner.instance_.setSpeed({val})")

# Unsterblich
def immortal():
    js("Runner.instance_.gameOver = function(){}")

# Autojump
def autojump():
    js("""
        window.autojumpInterval = setInterval(() => {
            if (!Runner.instance_.crashed && !Runner.instance_.tRex.jumping) {
                Runner.instance_.tRex.startJump();
            }
        }, 50);
    """)

def stop_autojump():
    js("clearInterval(window.autojumpInterval)")

# WASD Steuerung
def wasd():
    js("""
        document.addEventListener('keydown', e => {
            if (e.key === 'w') Runner.instance_.tRex.startJump();
            if (e.key === 'a') Runner.instance_.tRex.xPos -= 20;
            if (e.key === 'd') Runner.instance_.tRex.xPos += 20;
            if (e.key === 's') Runner.instance_.tRex.setDuck(true);
        });
        document.addEventListener('keyup', e => {
            if (e.key === 's') Runner.instance_.tRex.setDuck(false);
        });
    """)

# Lustige Hacks
def moon_gravity():
    js("Runner.instance_.gravity = 0.1")

def super_jump():
    js("Runner.instance_.tRex.jumpVelocity = 20")

def slow_motion():
    js("Runner.instance_.setSpeed(1)")

def fly_mode():
    js("""
        document.addEventListener('keydown', e => {
            if (e.key === ' ') Runner.instance_.tRex.yPos -= 20;
            if (e.key === 'Shift') Runner.instance_.tRex.yPos += 20;
        });
    """)

# -------------------------
# GUI
# -------------------------
root = tk.Tk()
root.title("MeteorShield")

# JS Eingabefeld
entry = tk.Entry(root, width=60)
entry.pack(padx=10, pady=10)

tk.Button(root, text="Run JS", command=lambda: js(entry.get())).pack(pady=5)

# Speedhack + Slider
tk.Button(root, text="Speedhack (Slider)", command=toggle_speed_slider).pack(pady=5)
speed_slider = tk.Scale(root, from_=1, to=5000, orient="horizontal", command=apply_speed)

# Unsterblich
tk.Button(root, text="Invincible", command=immortal).pack(pady=5)

# Autojump
tk.Button(root, text="Autojump", command=autojump).pack(pady=5)
tk.Button(root, text="Stop Autojump", command=stop_autojump).pack(pady=5)

# WASD
tk.Button(root, text="WASD Steuerung", command=wasd).pack(pady=5)

# Lustige Hacks
tk.Button(root, text="Mond-Gravitation", command=moon_gravity).pack(pady=5)
tk.Button(root, text="Super Jump", command=super_jump).pack(pady=5)
tk.Button(root, text="Slow Motion", command=slow_motion).pack(pady=5)
tk.Button(root, text="Fly Mode (Space/Shift)", command=fly_mode).pack(pady=5)

root.mainloop()
driver.quit()
