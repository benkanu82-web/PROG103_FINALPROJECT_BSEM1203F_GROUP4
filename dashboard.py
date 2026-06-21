import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import date, datetime

# ── matplotlib for charts ──────────────────────────────────────────
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_OK = True
except Exception as e:
    MATPLOTLIB_OK = False
    MATPLOTLIB_ERROR = str(e)

DATA_FILE = "students.csv"

# ─────────────────────────────────────────────────────────────────
#  THEME  (same palette as login page)
# ─────────────────────────────────────────────────────────────────
THEMES = {
    "light": {
        "bg":           "#F5F0E8",
        "sidebar":      "#1B4332",
        "sidebar_btn":  "#1B4332",
        "sidebar_fg":   "#FFFFFF",
        "sidebar_hover":"#D4A017",
        "card":         "#FFFFFF",
        "card_border":  "#E0DAD0",
        "primary":      "#1B4332",
        "accent":       "#D4A017",
        "text":         "#1A1A1A",
        "subtext":      "#555555",
        "entry_bg":     "#EDEAE2",
        "entry_fg":     "#1A1A1A",
        "btn_fg":       "#FFFFFF",
        "error":        "#C0392B",
        "success":      "#1B4332",
        "table_bg":     "#FFFFFF",
        "table_alt":    "#F5F0E8",
        "table_head":   "#1B4332",
        "table_head_fg":"#FFFFFF",
        "toggle_text":  "🌙 Dark",
        "chart_bg":     "#FFFFFF",
        "chart_colors": ["#1B4332","#D4A017","#2ECC71","#E74C3C","#3498DB","#9B59B6"],
    },
    "dark": {
        "bg":           "#1A1A2E",
        "sidebar":      "#0F3460",
        "sidebar_btn":  "#0F3460",
        "sidebar_fg":   "#E8E8E8",
        "sidebar_hover":"#D4A017",
        "card":         "#16213E",
        "card_border":  "#0F3460",
        "primary":      "#2ECC71",
        "accent":       "#D4A017",
        "text":         "#E8E8E8",
        "subtext":      "#A0A0A0",
        "entry_bg":     "#0F3460",
        "entry_fg":     "#E8E8E8",
        "btn_fg":       "#1A1A2E",
        "error":        "#FF6B6B",
        "success":      "#2ECC71",
        "table_bg":     "#16213E",
        "table_alt":    "#0F3460",
        "table_head":   "#D4A017",
        "table_head_fg":"#1A1A2E",
        "toggle_text":  "☀️ Light",
        "chart_bg":     "#16213E",
        "chart_colors": ["#2ECC71","#D4A017","#3498DB","#E74C3C","#9B59B6","#F39C12"],
    },
}

current_theme = "light"

# ─────────────────────────────────────────────────────────────────
#  DATA HELPERS
# ─────────────────────────────────────────────────────────────────

def load_students():
    """Load all student rows from CSV into a list of dicts."""
    students = []
    if not os.path.exists(DATA_FILE):
        return students
    with open(DATA_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append(row)
    return students


def calculate_stats(students):
    """Loop through records once and count everything needed."""
    stats = {
        "total":    0,
        "male":     0, "female":   0, "other_gender": 0,
        "active":   0, "inactive": 0, "pending":      0,
        "excellent":0, "good":     0, "average":      0,
        "needs_improvement": 0,
        "monthly":  {},
    }
    for s in students:
        stats["total"] += 1

        gender = s.get("gender", "").strip().lower()
        if gender == "male":
            stats["male"] += 1
        elif gender == "female":
            stats["female"] += 1
        else:
            stats["other_gender"] += 1

        status = s.get("status", "").strip().lower()
        if status == "active":
            stats["active"] += 1
        elif status == "inactive":
            stats["inactive"] += 1
        elif status == "pending":
            stats["pending"] += 1

        remark = s.get("remark", "").strip().lower()
        if remark == "excellent":
            stats["excellent"] += 1
        elif remark == "good":
            stats["good"] += 1
        elif remark == "average":
            stats["average"] += 1
        elif remark == "needs improvement":
            stats["needs_improvement"] += 1

        # Monthly registrations for line graph
        date_str = s.get("date_created", "")
        try:
            month = datetime.strptime(date_str, "%Y-%m-%d").strftime("%b")
            stats["monthly"][month] = stats["monthly"].get(month, 0) + 1
        except ValueError:
            pass

    return stats

# ─────────────────────────────────────────────────────────────────
#  MAIN DASHBOARD WINDOW
# ─────────────────────────────────────────────────────────────────

class SRMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SRMS — Student Record Management System")
        self.root.geometry("1050x660")
        self.root.resizable(True, True)
        self.current_page = None
        self.sidebar_buttons = {}
        self._build_layout()
        self.show_dashboard()

    # ── Layout skeleton ──────────────────────────────────────────

    def _build_layout(self):
        t = THEMES[current_theme]

        # Top bar
        self.topbar = tk.Frame(self.root, height=50)
        self.topbar.pack(side="top", fill="x")
        self.topbar.pack_propagate(False)

        self.top_title = tk.Label(
            self.topbar,
            text="SRMS — Student Record Management System",
            font=("Georgia", 13, "bold")
        )
        self.top_title.pack(side="left", padx=20, pady=10)

        self.theme_btn = tk.Button(
            self.topbar,
            font=("Arial", 9),
            relief="flat",
            cursor="hand2",
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="right", padx=14, pady=10)

        self.top_date = tk.Label(
            self.topbar,
            text=date.today().strftime("%A, %d %B %Y"),
            font=("Arial", 9)
        )
        self.top_date.pack(side="right", padx=10, pady=10)

        # Body (sidebar + content)
        self.body = tk.Frame(self.root)
        self.body.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(self.body, width=190)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.sidebar_logo = tk.Label(
            self.sidebar,
            text="SRMS",
            font=("Georgia", 22, "bold")
        )
        self.sidebar_logo.pack(pady=(20, 4))

        self.sidebar_sub = tk.Label(
            self.sidebar,
            text="Admin Panel",
            font=("Arial", 8)
        )
        self.sidebar_sub.pack(pady=(0, 16))

        tk.Frame(self.sidebar, height=1).pack(fill="x", padx=16, pady=(0, 10))

        pages = [
            ("📊  Dashboard",     self.show_dashboard),
            ("➕  Add Record",    self.show_add_record),
            ("📋  View Records",  self.show_view_records),
            ("🔍  Search & Filter", self.show_search_filter),
            ("📄  PDF Report",    self.show_pdf_report),
        ]

        for label, command in pages:
            btn = tk.Button(
                self.sidebar,
                text=label,
                font=("Arial", 10),
                relief="flat",
                anchor="w",
                padx=18,
                pady=10,
                cursor="hand2",
                command=command
            )
            btn.pack(fill="x", pady=2)
            self.sidebar_buttons[label] = btn

        # Logout at bottom
        self.logout_btn = tk.Button(
            self.sidebar,
            text="🚪  Logout",
            font=("Arial", 10),
            relief="flat",
            anchor="w",
            padx=18,
            pady=10,
            cursor="hand2",
            command=self.logout
        )
        self.logout_btn.pack(side="bottom", fill="x", pady=(0, 10))

        # Main content area
        self.content = tk.Frame(self.body)
        self.content.pack(side="left", fill="both", expand=True)

        self.apply_theme()

    # ── Theme ────────────────────────────────────────────────────

    def apply_theme(self):
        t = THEMES[current_theme]

        self.root.config(bg=t["bg"])
        self.topbar.config(bg=t["card"])
        self.top_title.config(bg=t["card"], fg=t["primary"])
        self.top_date.config(bg=t["card"], fg=t["subtext"])
        self.theme_btn.config(bg=t["card"], fg=t["subtext"],
                              activebackground=t["card"],
                              text=t["toggle_text"])
        self.body.config(bg=t["bg"])
        self.sidebar.config(bg=t["sidebar"])
        self.sidebar_logo.config(bg=t["sidebar"], fg=t["accent"])
        self.sidebar_sub.config(bg=t["sidebar"], fg=t["sidebar_fg"])

        for label, btn in self.sidebar_buttons.items():
            btn.config(bg=t["sidebar_btn"], fg=t["sidebar_fg"],
                       activebackground=t["sidebar_hover"],
                       activeforeground="#FFFFFF")

        self.logout_btn.config(bg=t["sidebar_btn"], fg="#FF6B6B",
                               activebackground=t["sidebar_hover"])
        self.content.config(bg=t["bg"])

    def toggle_theme(self):
        global current_theme
        current_theme = "dark" if current_theme == "light" else "light"
        self.apply_theme()
        # Refresh whatever page is currently showing
        if self.current_page == "dashboard":
            self.show_dashboard()
        elif self.current_page == "view_records":
            self.show_view_records()
        elif self.current_page == "add_record":
            self.show_add_record()
        elif self.current_page == "search_filter":
            self.show_search_filter()
        elif self.current_page == "pdf_report":
            self.show_pdf_report()

    def clear_content(self):
        """Remove all widgets from the content area before loading a new page."""
        for widget in self.content.winfo_children():
            widget.destroy()

    # ── Sidebar active highlight ─────────────────────────────────

    def set_active_btn(self, active_label):
        t = THEMES[current_theme]
        for label, btn in self.sidebar_buttons.items():
            if label == active_label:
                btn.config(bg=t["accent"], fg="#1A1A1A")
            else:
                btn.config(bg=t["sidebar_btn"], fg=t["sidebar_fg"])

    # ─────────────────────────────────────────────────────────────
    #  PAGE 1 — DASHBOARD
    # ─────────────────────────────────────────────────────────────

    def show_dashboard(self):
        self.current_page = "dashboard"
        self.set_active_btn("📊  Dashboard")
        self.clear_content()
        t = THEMES[current_theme]
        students = load_students()
        stats    = calculate_stats(students)

        # Scrollable canvas so charts don't get cut off on small screens
        canvas  = tk.Canvas(self.content, bg=t["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content, orient="vertical",
                                  command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=t["bg"])
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Page heading
        tk.Label(scroll_frame, text="Dashboard Overview",
                 font=("Georgia", 16, "bold"),
                 bg=t["bg"], fg=t["primary"]).pack(anchor="w", padx=24, pady=(18, 4))
        tk.Label(scroll_frame,
                 text=f"Showing statistics for {stats['total']} student records",
                 font=("Arial", 9), bg=t["bg"], fg=t["subtext"]).pack(anchor="w", padx=24)

        # ── Stat cards ───────────────────────────────────────────
        cards_data = [
            ("Total Students", stats["total"],           "#1B4332"),
            ("Male",           stats["male"],            "#2471A3"),
            ("Female",         stats["female"],          "#A93226"),
            ("Active",         stats["active"],          "#1E8449"),
            ("Inactive",       stats["inactive"],        "#784212"),
            ("Pending",        stats["pending"],         "#7D3C98"),
            ("Excellent",      stats["excellent"],       "#D4A017"),
            ("Good",           stats["good"],            "#117A65"),
            ("Needs Improv.",  stats["needs_improvement"],"#CB4335"),
        ]

        card_frame = tk.Frame(scroll_frame, bg=t["bg"])
        card_frame.pack(fill="x", padx=20, pady=16)

        for i, (label, value, color) in enumerate(cards_data):
            col = i % 3
            row = i // 3
            card = tk.Frame(card_frame, bg=color,
                            relief="flat", bd=0)
            card.grid(row=row, column=col, padx=8, pady=8,
                      ipadx=14, ipady=10, sticky="nsew")
            tk.Label(card, text=str(value),
                     font=("Georgia", 26, "bold"),
                     bg=color, fg="#FFFFFF").pack()
            tk.Label(card, text=label,
                     font=("Arial", 9),
                     bg=color, fg="#F0F0F0").pack()

        for col in range(3):
            card_frame.columnconfigure(col, weight=1)

        # ── Charts ───────────────────────────────────────────────
        if not MATPLOTLIB_OK:
            tk.Label(scroll_frame,
                     text="Charts unavailable. Real error below:",
                     font=("Arial", 11, "bold"), bg=t["bg"], fg=t["error"]).pack(pady=(20, 4))
            tk.Label(scroll_frame,
                     text=MATPLOTLIB_ERROR,
                     font=("Arial", 9), bg=t["bg"], fg=t["error"],
                     wraplength=700, justify="left").pack(pady=(0, 20), padx=24)
            return

        chart_bg = t["chart_bg"]
        colors   = t["chart_colors"]
        text_col = t["text"]

        tk.Label(scroll_frame, text="Data Visualisation",
                 font=("Georgia", 14, "bold"),
                 bg=t["bg"], fg=t["primary"]).pack(anchor="w", padx=24, pady=(8, 4))

        chart_row = tk.Frame(scroll_frame, bg=t["bg"])
        chart_row.pack(fill="x", padx=16, pady=8)

        # Bar chart — Gender & Status
        fig1, ax1 = plt.subplots(figsize=(4.0, 3.0))
        fig1.patch.set_facecolor(chart_bg)
        ax1.set_facecolor(chart_bg)
        categories = ["Male", "Female", "Active", "Inactive", "Pending"]
        values     = [stats["male"], stats["female"],
                      stats["active"], stats["inactive"], stats["pending"]]
        bars = ax1.bar(categories, values,
                       color=colors[:5], edgecolor="none", width=0.5)
        ax1.set_title("Gender & Status", color=text_col, fontsize=10, pad=8)
        ax1.tick_params(colors=text_col, labelsize=8)
        for spine in ax1.spines.values():
            spine.set_visible(False)
        ax1.yaxis.grid(True, color="#CCCCCC", linewidth=0.5)
        ax1.set_axisbelow(True)
        for bar, val in zip(bars, values):
            ax1.text(bar.get_x() + bar.get_width()/2,
                     bar.get_height() + 0.1,
                     str(val), ha="center", va="bottom",
                     fontsize=8, color=text_col)
        fig1.tight_layout()

        canvas1 = FigureCanvasTkAgg(fig1, master=chart_row)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", padx=8)
        plt.close(fig1)

        # Pie chart — Status breakdown
        fig2, ax2 = plt.subplots(figsize=(3.6, 3.0))
        fig2.patch.set_facecolor(chart_bg)
        ax2.set_facecolor(chart_bg)
        pie_labels = ["Active", "Inactive", "Pending"]
        pie_values = [stats["active"], stats["inactive"], stats["pending"]]
        pie_values = [v for v in pie_values if v > 0]
        pie_labels = [l for l, v in zip(pie_labels,
                      [stats["active"], stats["inactive"], stats["pending"]]) if v > 0]
        wedge_colors = [colors[3], colors[0], colors[1]][:len(pie_labels)]
        ax2.pie(pie_values, labels=pie_labels, autopct="%1.0f%%",
                colors=wedge_colors,
                textprops={"color": text_col, "fontsize": 8},
                startangle=90, wedgeprops={"edgecolor": chart_bg, "linewidth": 2})
        ax2.set_title("Status Breakdown", color=text_col, fontsize=10, pad=8)
        fig2.tight_layout()

        canvas2 = FigureCanvasTkAgg(fig2, master=chart_row)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="left", padx=8)
        plt.close(fig2)

        # Line graph — Monthly registrations
        month_order = ["Jan","Feb","Mar","Apr","May","Jun",
                       "Jul","Aug","Sep","Oct","Nov","Dec"]
        monthly = stats["monthly"]
        months_present = [m for m in month_order if m in monthly]
        month_counts   = [monthly[m] for m in months_present]

        fig3, ax3 = plt.subplots(figsize=(4.0, 3.0))
        fig3.patch.set_facecolor(chart_bg)
        ax3.set_facecolor(chart_bg)
        ax3.plot(months_present, month_counts,
                 color=colors[0], marker="o",
                 linewidth=2, markersize=6,
                 markerfacecolor=t["accent"])
        ax3.fill_between(months_present, month_counts,
                         alpha=0.15, color=colors[0])
        ax3.set_title("Monthly Registrations", color=text_col, fontsize=10, pad=8)
        ax3.tick_params(colors=text_col, labelsize=8)
        for spine in ax3.spines.values():
            spine.set_visible(False)
        ax3.yaxis.grid(True, color="#CCCCCC", linewidth=0.5)
        ax3.set_axisbelow(True)
        fig3.tight_layout()

        canvas3 = FigureCanvasTkAgg(fig3, master=chart_row)
        canvas3.draw()
        canvas3.get_tk_widget().pack(side="left", padx=8)
        plt.close(fig3)

    # ─────────────────────────────────────────────────────────────
    #  PAGE 2 — ADD RECORD
    # ─────────────────────────────────────────────────────────────

    def show_add_record(self):
        self.current_page = "add_record"
        self.set_active_btn("➕  Add Record")
        self.clear_content()
        t = THEMES[current_theme]

        tk.Label(self.content, text="Add New Student Record",
                 font=("Georgia", 16, "bold"),
                 bg=t["bg"], fg=t["primary"]).pack(anchor="w", padx=24, pady=(18, 14))

        form = tk.Frame(self.content, bg=t["card"], padx=30, pady=24)
        form.pack(padx=24, pady=4, fill="x")

        fields = {}

        def make_field(label_text, widget_type="entry",
                       options=None, row=0, col=0):
            frame = tk.Frame(form, bg=t["card"])
            frame.grid(row=row, column=col, padx=12, pady=8, sticky="w")
            tk.Label(frame, text=label_text,
                     font=("Arial", 9, "bold"),
                     bg=t["card"], fg=t["text"]).pack(anchor="w")
            if widget_type == "entry":
                w = tk.Entry(frame, font=("Arial", 10),
                             bg=t["entry_bg"], fg=t["entry_fg"],
                             relief="flat", bd=4, width=22,
                             insertbackground=t["entry_fg"])
                w.pack(ipady=5, pady=(2, 0))
            else:
                var = tk.StringVar()
                w = ttk.Combobox(frame, textvariable=var,
                                 values=options, state="readonly",
                                 font=("Arial", 10), width=20)
                w.pack(pady=(2, 0))
                fields[label_text] = var
                return var
            fields[label_text] = w
            return w

        make_field("Full Name",           row=0, col=0)
        make_field("Gender", "combo",
                   options=["Male","Female","Other"], row=0, col=1)
        make_field("Class", "combo",
                   options=["JSS1","JSS2","JSS3","SSS1","SSS2","SSS3"],
                   row=1, col=0)
        make_field("Status", "combo",
                   options=["Active","Inactive","Pending"], row=1, col=1)
        make_field("Contact (9 digits)",  row=2, col=0)
        make_field("Grade (0 – 100)",     row=2, col=1)

        error_lbl = tk.Label(form, text="", fg=t["error"],
                             bg=t["card"], font=("Arial", 9))
        error_lbl.grid(row=3, column=0, columnspan=2, pady=(8, 0), sticky="w")

        # ── Validation helpers ────────────────────────────────
        def is_valid_name(name):
            name = name.strip()
            if name == "":
                return False
            for ch in name:
                if not (ch.isalpha() or ch == " "):
                    return False
            return True

        def is_valid_contact(contact):
            contact = contact.strip()
            if len(contact) != 9:
                return False
            for ch in contact:
                if not ch.isdigit():
                    return False
            return True

        def is_valid_grade(grade):
            grade = grade.strip()
            if grade == "":
                return False
            for ch in grade:
                if not (ch.isdigit() or ch == "."):
                    return False
            try:
                v = float(grade)
                return 0 <= v <= 100
            except ValueError:
                return False

        def get_remark(grade):
            v = float(grade)
            if v >= 80:
                return "Excellent"
            elif v >= 60:
                return "Good"
            elif v >= 50:
                return "Average"
            else:
                return "Needs Improvement"

        def get_next_id():
            highest = 0
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", newline="") as f:
                    for row in csv.DictReader(f):
                        try:
                            n = int(row["id"].replace("ST",""))
                            if n > highest:
                                highest = n
                        except (ValueError, KeyError):
                            continue
            return "ST" + str(highest + 1).zfill(3)

        def save():
            name    = fields["Full Name"].get()
            gender  = fields["Gender"].get()
            cls     = fields["Class"].get()
            status  = fields["Status"].get()
            contact = fields["Contact (9 digits)"].get()
            grade   = fields["Grade (0 – 100)"].get()

            if not is_valid_name(name):
                error_lbl.config(text="Name cannot be empty and must contain letters only.")
                return
            if gender == "":
                error_lbl.config(text="Please select a gender.")
                return
            if cls == "":
                error_lbl.config(text="Please select a class.")
                return
            if status == "":
                error_lbl.config(text="Please select a status.")
                return
            if not is_valid_contact(contact):
                error_lbl.config(text="Contact must be exactly 9 digits (numbers only).")
                return
            if not is_valid_grade(grade):
                error_lbl.config(text="Grade must be a number between 0 and 100.")
                return

            new_id = get_next_id()
            remark = get_remark(grade)
            today  = date.today().isoformat()

            file_exists = os.path.exists(DATA_FILE)
            with open(DATA_FILE, "a", newline="") as f:
                w = csv.writer(f)
                if not file_exists:
                    w.writerow(["id","full_name","gender","class",
                                "status","contact","date_created","grade","remark"])
                w.writerow([new_id, name.strip(), gender, cls,
                            status, contact, today, grade, remark])

            error_lbl.config(text="")
            messagebox.showinfo("Saved",
                f"✅  {name.strip()} added as {new_id}\nRemark: {remark}")
            clear()

        def clear():
            for key, widget in fields.items():
                if isinstance(widget, tk.Entry):
                    widget.delete(0, tk.END)
                else:
                    widget.set("")
            error_lbl.config(text="")

        btn_row = tk.Frame(form, bg=t["card"])
        btn_row.grid(row=4, column=0, columnspan=2, pady=(16, 0), sticky="w")

        tk.Button(btn_row, text="Save Record",
                  font=("Arial", 10, "bold"),
                  bg=t["primary"], fg=t["btn_fg"],
                  relief="flat", padx=16, pady=7,
                  cursor="hand2", command=save).pack(side="left", padx=(0, 10))

        tk.Button(btn_row, text="Clear Form",
                  font=("Arial", 10),
                  bg=t["entry_bg"], fg=t["text"],
                  relief="flat", padx=16, pady=7,
                  cursor="hand2", command=clear).pack(side="left")

    # ─────────────────────────────────────────────────────────────
    #  PAGE 3 — VIEW RECORDS
    # ─────────────────────────────────────────────────────────────

    def show_view_records(self, students=None):
        self.current_page = "view_records"
        self.set_active_btn("📋  View Records")
        self.clear_content()
        t = THEMES[current_theme]

        tk.Label(self.content, text="All Student Records",
                 font=("Georgia", 16, "bold"),
                 bg=t["bg"], fg=t["primary"]).pack(anchor="w", padx=24, pady=(18, 14))

        if students is None:
            students = load_students()

        # Table
        cols = ("ID","Full Name","Gender","Class","Status",
                "Contact","Date Created","Grade","Remark")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview",
                        background=t["table_bg"],
                        foreground=t["text"],
                        fieldbackground=t["table_bg"],
                        rowheight=28,
                        font=("Arial", 9))
        style.configure("Custom.Treeview.Heading",
                        background=t["table_head"],
                        foreground=t["table_head_fg"],
                        font=("Arial", 9, "bold"),
                        relief="flat")
        style.map("Custom.Treeview",
                  background=[("selected", t["accent"])],
                  foreground=[("selected", "#1A1A1A")])

        frame = tk.Frame(self.content, bg=t["bg"])
        frame.pack(fill="both", expand=True, padx=16, pady=4)

        tree = ttk.Treeview(frame, columns=cols,
                            show="headings", style="Custom.Treeview")

        widths = [60, 140, 70, 65, 75, 100, 100, 55, 130]
        for col, w in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center")

        # Alternate row colours
        tree.tag_configure("odd",  background=t["table_bg"])
        tree.tag_configure("even", background=t["table_alt"])

        for i, s in enumerate(students):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", "end", tags=(tag,), values=(
                s.get("id",""), s.get("full_name",""),
                s.get("gender",""), s.get("class",""),
                s.get("status",""), s.get("contact",""),
                s.get("date_created",""), s.get("grade",""),
                s.get("remark","")
            ))

        vsb = ttk.Scrollbar(frame, orient="vertical",   command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(self.content,
                 text=f"Total records shown: {len(students)}",
                 font=("Arial", 9), bg=t["bg"], fg=t["subtext"]).pack(pady=6)

    # ─────────────────────────────────────────────────────────────
    #  PAGE 4 — SEARCH & FILTER
    # ─────────────────────────────────────────────────────────────

    def show_search_filter(self):
        self.current_page = "search_filter"
        self.set_active_btn("🔍  Search & Filter")
        self.clear_content()
        t = THEMES[current_theme]

        tk.Label(self.content, text="Search & Filter Records",
                 font=("Georgia", 16, "bold"),
                 bg=t["bg"], fg=t["primary"]).pack(anchor="w", padx=24, pady=(18, 10))

        controls = tk.Frame(self.content, bg=t["card"], padx=20, pady=14)
        controls.pack(fill="x", padx=16, pady=(0, 8))

        # Search box
        tk.Label(controls, text="Search (Name or ID):",
                 font=("Arial", 9, "bold"),
                 bg=t["card"], fg=t["text"]).grid(row=0, column=0, sticky="w", padx=6)
        search_var = tk.StringVar()
        tk.Entry(controls, textvariable=search_var,
                 font=("Arial", 10), bg=t["entry_bg"],
                 fg=t["entry_fg"], relief="flat", bd=4,
                 width=22, insertbackground=t["entry_fg"]
                 ).grid(row=1, column=0, padx=6, ipady=5, sticky="w")

        # Gender filter
        tk.Label(controls, text="Gender:",
                 font=("Arial", 9, "bold"),
                 bg=t["card"], fg=t["text"]).grid(row=0, column=1, sticky="w", padx=6)
        gender_var = tk.StringVar(value="All")
        ttk.Combobox(controls, textvariable=gender_var,
                     values=["All","Male","Female","Other"],
                     state="readonly", width=12
                     ).grid(row=1, column=1, padx=6, sticky="w")

        # Status filter
        tk.Label(controls, text="Status:",
                 font=("Arial", 9, "bold"),
                 bg=t["card"], fg=t["text"]).grid(row=0, column=2, sticky="w", padx=6)
        status_var = tk.StringVar(value="All")
        ttk.Combobox(controls, textvariable=status_var,
                     values=["All","Active","Inactive","Pending"],
                     state="readonly", width=12
                     ).grid(row=1, column=2, padx=6, sticky="w")

        # Remark filter
        tk.Label(controls, text="Remark:",
                 font=("Arial", 9, "bold"),
                 bg=t["card"], fg=t["text"]).grid(row=0, column=3, sticky="w", padx=6)
        remark_var = tk.StringVar(value="All")
        ttk.Combobox(controls, textvariable=remark_var,
                     values=["All","Excellent","Good","Average","Needs Improvement"],
                     state="readonly", width=16
                     ).grid(row=1, column=3, padx=6, sticky="w")

        result_label = tk.Label(self.content, text="",
                                font=("Arial", 9),
                                bg=t["bg"], fg=t["subtext"])
        result_label.pack(anchor="w", padx=24)

        # Table frame placeholder
        table_frame = tk.Frame(self.content, bg=t["bg"])
        table_frame.pack(fill="both", expand=True, padx=16, pady=4)

        cols = ("ID","Full Name","Gender","Class","Status",
                "Contact","Date Created","Grade","Remark")

        style = ttk.Style()
        style.configure("SF.Treeview",
                        background=t["table_bg"],
                        foreground=t["text"],
                        fieldbackground=t["table_bg"],
                        rowheight=27,
                        font=("Arial", 9))
        style.configure("SF.Treeview.Heading",
                        background=t["table_head"],
                        foreground=t["table_head_fg"],
                        font=("Arial", 9, "bold"))
        style.map("SF.Treeview",
                  background=[("selected", t["accent"])],
                  foreground=[("selected", "#1A1A1A")])

        tree = ttk.Treeview(table_frame, columns=cols,
                            show="headings", style="SF.Treeview")
        widths = [60,140,70,65,75,100,100,55,130]
        for col, w in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center")
        tree.tag_configure("odd",  background=t["table_bg"])
        tree.tag_configure("even", background=t["table_alt"])

        vsb = ttk.Scrollbar(table_frame, orient="vertical",   command=tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        def apply_filters(*args):
            """
            Loop through every student record and apply each filter
            in turn. Only records that pass ALL conditions are shown.
            """
            all_students = load_students()
            search  = search_var.get().strip().lower()
            gender  = gender_var.get()
            status  = status_var.get()
            remark  = remark_var.get()

            filtered = []
            for s in all_students:
                # Search filter (name or ID)
                if search != "":
                    name_match = search in s.get("full_name","").lower()
                    id_match   = search in s.get("id","").lower()
                    if not (name_match or id_match):
                        continue
                # Gender filter
                if gender != "All" and s.get("gender","") != gender:
                    continue
                # Status filter
                if status != "All" and s.get("status","") != status:
                    continue
                # Remark filter
                if remark != "All" and s.get("remark","") != remark:
                    continue
                filtered.append(s)

            # Refresh table
            for row in tree.get_children():
                tree.delete(row)
            for i, s in enumerate(filtered):
                tag = "even" if i % 2 == 0 else "odd"
                tree.insert("", "end", tags=(tag,), values=(
                    s.get("id",""), s.get("full_name",""),
                    s.get("gender",""), s.get("class",""),
                    s.get("status",""), s.get("contact",""),
                    s.get("date_created",""), s.get("grade",""),
                    s.get("remark","")
                ))
            result_label.config(text=f"{len(filtered)} record(s) found.")

        # Buttons
        btn_row = tk.Frame(controls, bg=t["card"])
        btn_row.grid(row=1, column=4, padx=12, sticky="w")

        tk.Button(btn_row, text="Apply",
                  font=("Arial", 9, "bold"),
                  bg=t["primary"], fg=t["btn_fg"],
                  relief="flat", padx=12, pady=5,
                  cursor="hand2",
                  command=apply_filters).pack(side="left", padx=(0, 6))

        tk.Button(btn_row, text="Reset",
                  font=("Arial", 9),
                  bg=t["entry_bg"], fg=t["text"],
                  relief="flat", padx=12, pady=5,
                  cursor="hand2",
                  command=lambda: [
                      search_var.set(""),
                      gender_var.set("All"),
                      status_var.set("All"),
                      remark_var.set("All"),
                      apply_filters()
                  ]).pack(side="left")

        # Load all records on first open
        apply_filters()

    # ─────────────────────────────────────────────────────────────
    #  PAGE 5 — PDF REPORT
    # ─────────────────────────────────────────────────────────────

    def show_pdf_report(self):
        self.current_page = "pdf_report"
        self.set_active_btn("📄  PDF Report")
        self.clear_content()
        t = THEMES[current_theme]

        tk.Label(self.content, text="Generate PDF Report",
                 font=("Georgia", 16, "bold"),
                 bg=t["bg"], fg=t["primary"]).pack(anchor="w", padx=24, pady=(18, 6))

        tk.Label(self.content,
                 text="Choose a report period, then click Generate to create a PDF file.",
                 font=("Arial", 10), bg=t["bg"], fg=t["subtext"]
                 ).pack(anchor="w", padx=24, pady=(0, 14))

        box = tk.Frame(self.content, bg=t["card"], padx=24, pady=20)
        box.pack(fill="x", padx=24)

        tk.Label(box, text="Report Period:",
                 font=("Arial", 10, "bold"),
                 bg=t["card"], fg=t["text"]).grid(row=0, column=0, sticky="w", padx=(0, 10))

        period_var = tk.StringVar(value="All Records")
        ttk.Combobox(box, textvariable=period_var,
                     values=["This Week", "This Month", "This Year", "All Records"],
                     state="readonly", width=18
                     ).grid(row=0, column=1, sticky="w")

        status_lbl = tk.Label(box, text="",
                              font=("Arial", 9), bg=t["card"], fg=t["success"])
        status_lbl.grid(row=1, column=0, columnspan=2, sticky="w", pady=(12, 0))

        # ── Helper: figure out which records fall in the chosen period ──
        def filter_by_period(students, period):
            """
            Loops through every student and keeps only the ones whose
            date_created falls inside the chosen period.
            """
            today = date.today()
            filtered = []
            for s in students:
                date_str = s.get("date_created", "")
                try:
                    record_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    continue  # skip rows with a bad/missing date

                if period == "All Records":
                    filtered.append(s)
                elif period == "This Week":
                    days_diff = (today - record_date).days
                    if 0 <= days_diff <= 7:
                        filtered.append(s)
                elif period == "This Month":
                    if record_date.year == today.year and record_date.month == today.month:
                        filtered.append(s)
                elif period == "This Year":
                    if record_date.year == today.year:
                        filtered.append(s)
            return filtered

        def get_date_range_text(students, period):
            """Builds a human-readable date range string for the report header."""
            if period == "All Records" or not students:
                return "All available records"
            dates = []
            for s in students:
                try:
                    dates.append(datetime.strptime(s["date_created"], "%Y-%m-%d").date())
                except (ValueError, KeyError):
                    continue
            if not dates:
                return "No matching dates"
            start = min(dates).strftime("%d %B %Y")
            end   = max(dates).strftime("%d %B %Y")
            return f"{start}  -  {end}"

        # ── Build the actual PDF ─────────────────────────────────
        def generate_pdf():
            try:
                from reportlab.lib.pagesizes import A4
                from reportlab.lib import colors
                from reportlab.lib.units import cm
                from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                                Table, TableStyle)
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            except ImportError:
                status_lbl.config(
                    text="reportlab is not installed. Run:  pip install reportlab",
                    fg=t["error"])
                return

            period = period_var.get()
            all_students = load_students()
            students = filter_by_period(all_students, period)
            stats = calculate_stats(students)

            if not os.path.exists("reports"):
                os.makedirs("reports")

            filename = f"reports/SRMS_Report_{period.replace(' ', '_')}_{date.today().isoformat()}.pdf"

            doc = SimpleDocTemplate(filename, pagesize=A4,
                                    topMargin=1.5*cm, bottomMargin=1.5*cm)
            styles = getSampleStyleSheet()
            story = []

            title_style = ParagraphStyle(
                "TitleStyle", parent=styles["Title"],
                textColor=colors.HexColor("#1B4332"), fontSize=20)
            story.append(Paragraph(f"{period.upper()} STUDENT REPORT", title_style))
            story.append(Spacer(1, 6))

            sub_style = ParagraphStyle(
                "SubStyle", parent=styles["Normal"],
                textColor=colors.HexColor("#555555"), fontSize=10)
            story.append(Paragraph("SRMS — Student Record Management System", sub_style))
            story.append(Spacer(1, 14))

            # Date range
            story.append(Paragraph(f"<b>Date Range:</b> {get_date_range_text(students, period)}",
                                   styles["Normal"]))
            story.append(Spacer(1, 10))

            # Summary statistics table
            story.append(Paragraph("<b>Summary Statistics</b>", styles["Heading3"]))
            summary_data = [
                ["Total Records", str(stats["total"])],
                ["Male", str(stats["male"])],
                ["Female", str(stats["female"])],
                ["Active", str(stats["active"])],
                ["Inactive", str(stats["inactive"])],
                ["Pending", str(stats["pending"])],
                ["Excellent", str(stats["excellent"])],
                ["Good", str(stats["good"])],
                ["Needs Improvement", str(stats["needs_improvement"])],
            ]
            summary_table = Table(summary_data, colWidths=[8*cm, 4*cm])
            summary_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1B4332")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                 [colors.white, colors.HexColor("#F5F0E8")]),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.append(summary_table)
            story.append(Spacer(1, 16))

            # Record table
            story.append(Paragraph("<b>Student Records</b>", styles["Heading3"]))
            table_header = ["ID", "Name", "Gender", "Class", "Status", "Grade", "Remark"]
            table_rows = [table_header]
            for s in students:
                table_rows.append([
                    s.get("id", ""), s.get("full_name", ""), s.get("gender", ""),
                    s.get("class", ""), s.get("status", ""),
                    s.get("grade", ""), s.get("remark", "")
                ])

            if len(table_rows) == 1:
                story.append(Paragraph("No records found for this period.", styles["Normal"]))
            else:
                record_table = Table(table_rows, repeatRows=1)
                record_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D4A017")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                     [colors.white, colors.HexColor("#F5F0E8")]),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]))
                story.append(record_table)

            story.append(Spacer(1, 20))
            generated_style = ParagraphStyle(
                "Generated", parent=styles["Normal"],
                textColor=colors.HexColor("#888888"), fontSize=8)
            story.append(Paragraph(
                f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
                generated_style))

            doc.build(story)

            full_path = os.path.abspath(filename)
            status_lbl.config(
                text=f"PDF created successfully: {full_path}",
                fg=t["success"])
            messagebox.showinfo("Report Generated",
                f"Your {period} report has been saved to:\n\n{full_path}")

        tk.Button(box, text="Generate PDF Report",
                  font=("Arial", 10, "bold"),
                  bg=t["primary"], fg=t["btn_fg"],
                  relief="flat", padx=16, pady=8,
                  cursor="hand2",
                  command=generate_pdf
                  ).grid(row=0, column=2, padx=(20, 0))

        # ── Preview area ─────────────────────────────────────────
        preview_label = tk.Label(self.content, text="",
                                 font=("Arial", 9), bg=t["bg"], fg=t["subtext"],
                                 justify="left", anchor="w")
        preview_label.pack(anchor="w", padx=24, pady=(16, 0))

        def update_preview(*args):
            period = period_var.get()
            students = filter_by_period(load_students(), period)
            preview_label.config(
                text=f"Preview: {len(students)} record(s) will be included in this report."
            )

        period_var.trace_add("write", update_preview)
        update_preview()

    # ─────────────────────────────────────────────────────────────
    #  LOGOUT
    # ─────────────────────────────────────────────────────────────

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.root.destroy()
            open_login()


# ─────────────────────────────────────────────────────────────────
#  ENTRY POINT — called by login.py after successful login
# ─────────────────────────────────────────────────────────────────

def open_login():
    """Re-opens the login window (used by Logout)."""
    import login
    # Re-run login as a fresh Tk instance
    login_win = tk.Tk()
    login_win.withdraw()
    login_win.destroy()
    os.execv(__import__("sys").executable,
             [__import__("sys").executable, "login.py"])


def launch_dashboard():
    root = tk.Tk()
    app  = SRMSApp(root)
    root.mainloop()


if __name__ == "__main__":
    launch_dashboard()
