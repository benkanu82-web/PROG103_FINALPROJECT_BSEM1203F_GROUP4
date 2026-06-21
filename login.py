import tkinter as tk
from tkinter import messagebox

# ─────────────────────────────────────────────
#  CREDENTIALS
#  Username : admin        (letters only)
#  Password : Admin1234    (must have letters AND numbers)
# ─────────────────────────────────────────────
VALID_USERNAME = "admin"
VALID_PASSWORD = "Admin1234"
MAX_ATTEMPTS   = 3
attempts_made  = 0

# ─────────────────────────────────────────────
#  THEME COLOURS
#  Light mode  →  cream white background, deep forest green, gold accent
#  Dark  mode  →  deep charcoal background, bright mint green, gold accent
# ─────────────────────────────────────────────
THEMES = {
    "light": {
        "bg":           "#F5F0E8",
        "card":         "#FFFFFF",
        "primary":      "#1B4332",
        "accent":       "#D4A017",
        "text":         "#1A1A1A",
        "subtext":      "#555555",
        "entry_bg":     "#EDEAE2",
        "entry_fg":     "#1A1A1A",
        "btn_fg":       "#FFFFFF",
        "error":        "#C0392B",
        "toggle_text":  "🌙  Dark Mode",
    },
    "dark": {
        "bg":           "#1A1A2E",
        "card":         "#16213E",
        "primary":      "#2ECC71",
        "accent":       "#D4A017",
        "text":         "#E8E8E8",
        "subtext":      "#A0A0A0",
        "entry_bg":     "#0F3460",
        "entry_fg":     "#E8E8E8",
        "btn_fg":       "#1A1A2E",
        "error":        "#FF6B6B",
        "toggle_text":  "☀️  Light Mode",
    },
}

current_theme = "light"


# ─────────────────────────────────────────────
#  VALIDATION HELPERS
# ─────────────────────────────────────────────

def is_letters_only(text):
    """Username must contain letters only — no digits or symbols."""
    if text.strip() == "":
        return False
    for char in text.strip():
        if not char.isalpha():
            return False
    return True


def has_letter_and_number(text):
    """
    Password must have at least one letter AND at least one digit.
    Uses a loop to inspect every character.
    """
    found_letter = False
    found_digit  = False
    for char in text:
        if char.isalpha():
            found_letter = True
        if char.isdigit():
            found_digit = True
    return found_letter and found_digit


# ─────────────────────────────────────────────
#  LOGIN LOGIC
# ─────────────────────────────────────────────

def check_login():
    global attempts_made

    username = username_entry.get().strip()
    password = password_entry.get().strip()

    # Step 1 — nothing left empty
    if username == "" or password == "":
        show_error("Username and password cannot be left empty.")
        return

    # Step 2 — username: letters only
    if not is_letters_only(username):
        show_error("Username must contain letters only (no numbers or symbols).")
        return

    # Step 3 — password: must have at least one letter AND one number
    if not has_letter_and_number(password):
        show_error("Password must contain both letters and numbers (e.g. Admin1234).")
        return

    # Step 4 — check against stored credentials
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        show_error("")
        messagebox.showinfo("Access Granted", f"Welcome back, {username}!\nOpening SRMS Dashboard…")
        login_window.destroy()
        open_dashboard()
        return

    # Step 5 — wrong credentials: count attempt and warn or lock
    attempts_made += 1
    remaining = MAX_ATTEMPTS - attempts_made

    if remaining > 0:
        show_error(f"Invalid username or password.  {remaining} attempt(s) remaining.")
    else:
        show_error("Account locked — too many failed attempts.\nPlease restart the application.")
        lock_form()


def show_error(message):
    error_label.config(text=message)


def lock_form():
    username_entry.config(state="disabled")
    password_entry.config(state="disabled")
    login_button.config(state="disabled")


def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        show_hide_btn.config(text="Hide")
    else:
        password_entry.config(show="*")
        show_hide_btn.config(text="Show")


# ─────────────────────────────────────────────
#  THEME TOGGLE
# ─────────────────────────────────────────────

def apply_theme(mode):
    t = THEMES[mode]

    login_window.config(bg=t["bg"])
    outer_frame.config(bg=t["bg"])
    card.config(bg=t["card"])

    header_label.config(bg=t["card"],   fg=t["primary"])
    subtitle_label.config(bg=t["card"], fg=t["accent"])
    divider.config(bg=t["accent"])

    username_label.config(bg=t["card"], fg=t["text"])
    username_entry.config(bg=t["entry_bg"], fg=t["entry_fg"],
                          insertbackground=t["entry_fg"])

    password_label.config(bg=t["card"], fg=t["text"])
    pw_row.config(bg=t["entry_bg"])
    password_entry.config(bg=t["entry_bg"], fg=t["entry_fg"],
                          insertbackground=t["entry_fg"])
    show_hide_btn.config(bg=t["entry_bg"], fg=t["subtext"],
                         activebackground=t["entry_bg"])

    error_label.config(bg=t["card"], fg=t["error"])
    hint_label.config(bg=t["card"],  fg=t["subtext"])

    login_button.config(bg=t["primary"], fg=t["btn_fg"],
                        activebackground=t["accent"])

    toggle_btn.config(bg=t["bg"], fg=t["subtext"],
                      activebackground=t["bg"],
                      text=t["toggle_text"])


def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme(current_theme)


# ─────────────────────────────────────────────
#  OPEN THE REAL DASHBOARD
#  (defined in dashboard.py — sidebar, stats, charts, etc.)
# ─────────────────────────────────────────────

def open_dashboard():
    import dashboard
    dashboard.launch_dashboard()


# ─────────────────────────────────────────────
#  BUILD THE LOGIN WINDOW
# ─────────────────────────────────────────────

login_window = tk.Tk()
login_window.title("SRMS — Login")
login_window.geometry("420x530")
login_window.resizable(False, False)

outer_frame = tk.Frame(login_window)
outer_frame.pack(fill="both", expand=True)

# Centred card
card = tk.Frame(outer_frame, bd=0, relief="flat", padx=30, pady=30)
card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=470)

# Header
header_label = tk.Label(card, text="SRMS", font=("Georgia", 34, "bold"))
header_label.pack(pady=(0, 0))

subtitle_label = tk.Label(
    card,
    text="Student Record Management System",
    font=("Arial", 9)
)
subtitle_label.pack()

divider = tk.Frame(card, height=2, width=260)
divider.pack(pady=14)

# Username
username_label = tk.Label(card, text="Username", font=("Arial", 10, "bold"), anchor="w")
username_label.pack(fill="x")
username_entry = tk.Entry(card, font=("Arial", 11), relief="flat", bd=6)
username_entry.pack(fill="x", ipady=7, pady=(2, 14))

# Password
password_label = tk.Label(card, text="Password", font=("Arial", 10, "bold"), anchor="w")
password_label.pack(fill="x")

pw_row = tk.Frame(card)
pw_row.pack(fill="x", pady=(2, 4))

password_entry = tk.Entry(pw_row, font=("Arial", 11), relief="flat", bd=6, show="*")
password_entry.pack(side="left", fill="x", expand=True, ipady=7)

show_hide_btn = tk.Button(
    pw_row, text="Show", font=("Arial", 8),
    relief="flat", cursor="hand2",
    command=toggle_password
)
show_hide_btn.pack(side="right", padx=(4, 0))

# Hint text
hint_label = tk.Label(
    card,
    text="Username: letters only  |  Password: letters + numbers",
    font=("Arial", 7), anchor="w"
)
hint_label.pack(fill="x", pady=(2, 12))

# Error / status label
error_label = tk.Label(card, text="", font=("Arial", 9), wraplength=300, justify="left")
error_label.pack(fill="x", pady=(0, 12))

# Login button
login_button = tk.Button(
    card,
    text="Log  In",
    font=("Arial", 12, "bold"),
    relief="flat",
    cursor="hand2",
    pady=9,
    command=check_login
)
login_button.pack(fill="x", pady=(0, 0))

# Press Enter to login
login_window.bind("<Return>", lambda event: check_login())

# Dark / Light mode toggle — top right corner
toggle_btn = tk.Button(
    login_window,
    font=("Arial", 9),
    relief="flat",
    cursor="hand2",
    bd=0,
    command=toggle_theme
)
toggle_btn.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

# Apply starting theme
apply_theme(current_theme)

login_window.mainloop()
