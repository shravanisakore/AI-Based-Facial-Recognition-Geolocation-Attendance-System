# import tkinter as tk
# from tkinter import messagebox, filedialog
# import subprocess
# import os

# # Create the main window
# root = tk.Tk()
# root.title("Smart Attendance System")
# root.geometry("500x400")
# root.configure(bg='#f0f4f7')

# # Set icon (optional, if you have an .ico file)
# # root.iconbitmap('icon.ico')

# def register_student():
#     subprocess.run(["python", "register_student.py"])

# def mark_attendance():
#     subprocess.run(["python", "mark_attendance.py"])

# def view_attendance():
#     filename = filedialog.askopenfilename(initialdir="attendance_records", title="Select Attendance File",
#                                           filetypes=(("CSV Files", "*.csv"),))
#     if filename:
#         os.system(f'start notepad "{filename}"')

# def show_about():
#     messagebox.showinfo("About", "Smart Attendance System\nDeveloped with Python, OpenCV, and Tkinter\nLocation-based, Face-verified Attendance")

# # Title Label
# title_label = tk.Label(root, text="Smart Attendance System", font=("Helvetica", 18, "bold"), fg="#333", bg="#f0f4f7")
# title_label.pack(pady=20)

# # Buttons
# btn_register = tk.Button(root, text="Register Student", font=("Helvetica", 14), width=25, command=register_student, bg="#4CAF50", fg="white")
# btn_register.pack(pady=10)

# btn_attendance = tk.Button(root, text="Mark Attendance", font=("Helvetica", 14), width=25, command=mark_attendance, bg="#2196F3", fg="white")
# btn_attendance.pack(pady=10)

# btn_view = tk.Button(root, text="View Attendance Records", font=("Helvetica", 14), width=25, command=view_attendance, bg="#FFC107", fg="black")
# btn_view.pack(pady=10)

# btn_about = tk.Button(root, text="About System", font=("Helvetica", 14), width=25, command=show_about, bg="#9C27B0", fg="white")
# btn_about.pack(pady=10)

# btn_exit = tk.Button(root, text="Exit", font=("Helvetica", 14), width=25, command=root.quit, bg="#F44336", fg="white")
# btn_exit.pack(pady=20)

# # Start the GUI event loop
# root.mainloop()




import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os
import csv
from PIL import Image, ImageTk
import webbrowser
import sys

class MITAttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("MIT Academy of Engineering - Smart Attendance System")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Set MIT theme colors
        self.bg_color = "#002147"  # MIT dark blue
        self.accent_color = "#A31F34"  # MIT red
        self.secondary_color = "#8C8C8C"  # Light gray
        self.text_color = "#060404"
        
        # Configure styles
        self.configure_styles()
        
        # Create main container
        self.create_main_container()
        
        # Create necessary directories
        os.makedirs('student_images', exist_ok=True)
        os.makedirs('attendance_records', exist_ok=True)
        
        # Initialize student database if it doesn't exist
        if not os.path.exists('registered_students.csv'):
            with open('registered_students.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['student_id', 'student_name', 'image_path'])
    
    def configure_styles(self):
        style = ttk.Style()
        
        # Configure main frame style
        style.configure('Main.TFrame', background=self.bg_color)
        
        # Configure header style
        style.configure('Header.TLabel', 
                      background=self.bg_color,
                      foreground=self.text_color,
                      font=('Helvetica', 24, 'bold'),
                      padding=10)
        
        # Configure button styles
        style.configure('Primary.TButton',
                       font=('Helvetica', 12, 'bold'),
                       foreground=self.text_color,
                       background=self.accent_color,
                       borderwidth=1,
                       padding=10)
        
        style.map('Primary.TButton',
                background=[('active', '#C1272D'), ('pressed', '#8A1F26')])
        
        style.configure('Secondary.TButton',
                       font=('Helvetica', 12),
                       foreground=self.text_color,
                       background=self.secondary_color,
                       borderwidth=1,
                       padding=8)
        
        style.map('Secondary.TButton',
                background=[('active', '#A6A6A6'), ('pressed', '#737373')])
        
        # Configure card style
        style.configure('Card.TFrame',
                      background='#F5F5F5',
                      relief='raised',
                      borderwidth=2)
        
        # Configure card title
        style.configure('CardTitle.TLabel',
                      background='#F5F5F5',
                      foreground=self.bg_color,
                      font=('Helvetica', 14, 'bold'),
                      padding=(10, 5))
        
        # Configure status bar
        style.configure('Status.TLabel',
                      background=self.secondary_color,
                      foreground=self.text_color,
                      font=('Helvetica', 10),
                      padding=5)
    
    def create_main_container(self):
        # Main container frame
        self.main_frame = ttk.Frame(self.root, style='Main.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header()
        
        # Content area
        self.create_content_area()
        
        # Status bar
        self.create_status_bar()
    
    def create_header(self):
        header_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        # MIT Logo (placeholder)
        logo_frame = ttk.Frame(header_frame, width=80, height=80, style='Main.TFrame')
        logo_frame.pack(side=tk.LEFT)
        
        # Try to load MIT logo
        try:
            logo_img = Image.open("mit_logo.jpg") if os.path.exists("mit_logo.jpg") else None
            if logo_img:
                logo_img = logo_img.resize((80, 80), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label = ttk.Label(logo_frame, image=self.logo_photo, background=self.bg_color)
                logo_label.pack()
        except:
            pass
        
        # Title
        title_frame = ttk.Frame(header_frame, style='Main.TFrame')
        title_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(title_frame, 
                 text="MIT Academy of Engineering", 
                 style='Header.TLabel').pack(anchor='w')
        
        ttk.Label(title_frame, 
                 text="Smart Attendance System", 
                 style='Header.TLabel',
                 font=('Helvetica', 18)).pack(anchor='w')
        
        # Navigation buttons
        nav_frame = ttk.Frame(header_frame, style='Main.TFrame')
        nav_frame.pack(side=tk.RIGHT)
        
        ttk.Button(nav_frame, 
                  text="About MIT", 
                  style='Secondary.TButton',
                  command=self.open_mit_website).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(nav_frame, 
                  text="Help", 
                  style='Secondary.TButton',
                  command=self.show_help).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(nav_frame, 
                  text="Exit", 
                  style='Secondary.TButton',
                  command=self.root.quit).pack(side=tk.LEFT, padx=5)
    
    def create_content_area(self):
        content_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Quick Actions
        left_panel = ttk.Frame(content_frame, width=300, style='Main.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        self.create_quick_actions(left_panel)
        
        # Right panel - Dashboard
        right_panel = ttk.Frame(content_frame, style='Main.TFrame')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_dashboard(right_panel)
    
    def create_quick_actions(self, parent):
        # Quick Actions card
        card = ttk.Frame(parent, style='Card.TFrame')
        card.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(card, 
                 text="Quick Actions", 
                 style='CardTitle.TLabel').pack(fill=tk.X)
        
        # Action buttons
        actions = [
            ("Register Student", self.register_student, "icons/register.png"),
            ("Mark Attendance", self.mark_attendance, "icons/attendance.png"),
            ("View Records", self.view_attendance, "icons/report.png"),
            ("Manage Database", self.manage_database, "icons/database-storage.png")
        ]
        
        for text, command, icon_path in actions:
            btn = ttk.Button(card, 
                           text=text, 
                           style='Primary.TButton',
                           command=command)
            
            # Try to add icon
            try:
                if os.path.exists(icon_path):
                    icon_img = Image.open(icon_path)
                    icon_img = icon_img.resize((24, 24), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(icon_img)
                    btn.config(image=photo, compound=tk.LEFT)
                    btn.image = photo  # Keep reference
            except:
                pass
            
            btn.pack(fill=tk.X, pady=5, padx=10)
        
        # System Info card
        info_card = ttk.Frame(parent, style='Card.TFrame')
        info_card.pack(fill=tk.X)
        
        ttk.Label(info_card, 
                 text="System Information", 
                 style='CardTitle.TLabel').pack(fill=tk.X)
        
        info_text = tk.Text(info_card, 
                          height=8, 
                          width=30,
                          bg='#F5F5F5',
                          fg=self.bg_color,
                          font=('Helvetica', 10),
                          padx=10,
                          pady=10,
                          wrap=tk.WORD,
                          relief='flat')
        info_text.pack(fill=tk.BOTH, padx=5, pady=5)
        
        info_text.insert(tk.END, "MIT Academy of Engineering\nSmart Attendance System\n\n")
        info_text.insert(tk.END, "Version: 2.0\n")
        info_text.insert(tk.END, "Developed by: MIT CS Department\n")
        info_text.insert(tk.END, "Features:\n- Face Recognition\n- Location Tracking\n- Real-time Monitoring")
        info_text.config(state=tk.DISABLED)
    
    def create_dashboard(self, parent):
        # Dashboard with tabs
        tab_control = ttk.Notebook(parent)
        tab_control.pack(fill=tk.BOTH, expand=True)
        
        # Overview Tab
        overview_tab = ttk.Frame(tab_control)
        tab_control.add(overview_tab, text="Overview")
        
        self.create_overview_tab(overview_tab)
        
        # Recent Activity Tab
        activity_tab = ttk.Frame(tab_control)
        tab_control.add(activity_tab, text="Recent Activity")
        
        self.create_activity_tab(activity_tab)
        
        # Statistics Tab
        stats_tab = ttk.Frame(tab_control)
        tab_control.add(stats_tab, text="Statistics")
        
        self.create_stats_tab(stats_tab)
    
    def create_overview_tab(self, parent):
        # Create a canvas for scrolling
        canvas = tk.Canvas(parent, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Welcome message
        welcome_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        welcome_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Label(welcome_frame, 
                 text="Welcome to Smart Attendance System", 
                 style='CardTitle.TLabel').pack(fill=tk.X)
        
        welcome_text = tk.Text(welcome_frame, 
                             height=4, 
                             width=80,
                             bg='#F5F5F5',
                             fg=self.bg_color,
                             font=('Helvetica', 12),
                             padx=10,
                             pady=10,
                             wrap=tk.WORD,
                             relief='flat')
        welcome_text.pack(fill=tk.BOTH, padx=5, pady=5)
        
        welcome_text.insert(tk.END, "Welcome to the MIT Academy of Engineering Smart Attendance System. ")
        welcome_text.insert(tk.END, "This system provides automated attendance marking using facial recognition ")
        welcome_text.insert(tk.END, "and location verification for enhanced security and accuracy.")
        welcome_text.config(state=tk.DISABLED)
        
        # Quick Stats
        stats_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        stats_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Label(stats_frame, 
                 text="Quick Statistics", 
                 style='CardTitle.TLabel').pack(fill=tk.X)
        
        stats_container = ttk.Frame(stats_frame, style='Card.TFrame')
        stats_container.pack(fill=tk.X, padx=10, pady=10)
        
        # Sample stats (would normally be dynamic)
        stats = [
            ("Registered Students", "1,245"),
            ("Today's Attendance", "87%"),
            ("Pending Verifications", "12"),
            ("System Status", "Online")
        ]
        
        for i, (title, value) in enumerate(stats):
            if i % 2 == 0:
                row_frame = ttk.Frame(stats_container, style='Card.TFrame')
                row_frame.pack(fill=tk.X)
            
            stat_frame = ttk.Frame(row_frame, style='Card.TFrame')
            stat_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
            
            ttk.Label(stat_frame, 
                     text=title,
                     background='#F5F5F5',
                     foreground=self.secondary_color,
                     font=('Helvetica', 10)).pack()
            
            ttk.Label(stat_frame, 
                     text=value,
                     background='#F5F5F5',
                     foreground=self.accent_color,
                     font=('Helvetica', 16, 'bold')).pack()
    
    def create_activity_tab(self, parent):
        # Activity log table
        container = ttk.Frame(parent, style='Card.TFrame')
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(container, 
                 text="Recent Attendance Activities", 
                 style='CardTitle.TLabel').pack(fill=tk.X)
        
        # Create treeview with scrollbars
        tree_frame = ttk.Frame(container, style='Card.TFrame')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Horizontal scrollbar
        h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal")
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Vertical scrollbar
        v_scroll = ttk.Scrollbar(tree_frame)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        tree = ttk.Treeview(tree_frame, 
                           columns=("Date", "Time", "Student ID", "Name", "Subject", "Status"),
                           show="headings",
                           yscrollcommand=v_scroll.set,
                           xscrollcommand=h_scroll.set)
        
        # Configure columns
        tree.heading("Date", text="Date")
        tree.heading("Time", text="Time")
        tree.heading("Student ID", text="Student ID")
        tree.heading("Name", text="Name")
        tree.heading("Subject", text="Subject")
        tree.heading("Status", text="Status")
        
        tree.column("Date", width=100, anchor=tk.CENTER)
        tree.column("Time", width=80, anchor=tk.CENTER)
        tree.column("Student ID", width=120, anchor=tk.CENTER)
        tree.column("Name", width=150, anchor=tk.W)
        tree.column("Subject", width=150, anchor=tk.W)
        tree.column("Status", width=100, anchor=tk.CENTER)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Configure scrollbars
        v_scroll.config(command=tree.yview)
        h_scroll.config(command=tree.xview)
        
        # Add sample data (would normally load from database)
        sample_data = [
            ("2023-06-15", "09:30:45", "MIT2023001", "Rahul Sharma", "Data Structures", "Present"),
            ("2023-06-15", "09:31:12", "MIT2023002", "Priya Patel", "Data Structures", "Present"),
            ("2023-06-15", "09:32:45", "MIT2023003", "Amit Singh", "Data Structures", "Late"),
            ("2023-06-14", "10:15:22", "MIT2023004", "Neha Gupta", "Algorithms", "Present"),
            ("2023-06-14", "10:16:05", "MIT2023005", "Vikram Joshi", "Algorithms", "Present"),
            ("2023-06-13", "11:30:18", "MIT2023006", "Sneha Reddy", "Computer Networks", "Present"),
            ("2023-06-13", "11:31:45", "MIT2023007", "Arjun Kumar", "Computer Networks", "Absent"),
        ]
        
        for item in sample_data:
            tree.insert("", tk.END, values=item)
    
    def create_stats_tab(self, parent):
        container = ttk.Frame(parent, style='Card.TFrame')
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(container, 
                 text="Attendance Statistics", 
                 style='CardTitle.TLabel').pack(fill=tk.X)
        
        # Placeholder for charts (would normally use matplotlib or other visualization)
        chart_frame = ttk.Frame(container, style='Card.TFrame')
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        chart_label = ttk.Label(chart_frame, 
                              text="Attendance Charts Would Appear Here",
                              background='#F5F5F5',
                              foreground=self.secondary_color,
                              font=('Helvetica', 12),
                              padding=50)
        chart_label.pack(fill=tk.BOTH, expand=True)
        
        # Summary statistics
        summary_frame = ttk.Frame(container, style='Card.TFrame')
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(summary_frame, 
                 text="Summary Statistics",
                 style='CardTitle.TLabel').pack(fill=tk.X)
        
        # Sample summary stats
        stats = [
            ("Overall Attendance Rate", "89%"),
            ("Best Attendance Subject", "Data Structures (94%)"),
            ("Most Punctual Student", "Priya Patel (100%)"),
            ("Subjects Today", "3"),
            ("Total Records", "1,847")
        ]
        
        for title, value in stats:
            stat_frame = ttk.Frame(summary_frame, style='Card.TFrame')
            stat_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Label(stat_frame, 
                     text=title,
                     background='#F5F5F5',
                     foreground=self.bg_color,
                     font=('Helvetica', 10)).pack(side=tk.LEFT, padx=10)
            
            ttk.Label(stat_frame, 
                     text=value,
                     background='#F5F5F5',
                     foreground=self.accent_color,
                     font=('Helvetica', 10, 'bold')).pack(side=tk.RIGHT, padx=10)
    
    def create_status_bar(self):
        status_frame = ttk.Frame(self.main_frame, style='Status.TLabel')
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        ttk.Label(status_frame, 
                 text="System Ready | MIT Academy of Engineering | CS Department",
                 style='Status.TLabel').pack(side=tk.LEFT, padx=10)
        
        ttk.Label(status_frame, 
                 text="Developed by MIT Engineering Team",
                 style='Status.TLabel').pack(side=tk.RIGHT, padx=10)
    
    def register_student(self):
        """Open the student registration module"""
        try:
            subprocess.Popen(["python", "register_student.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open registration module: {str(e)}")
    
    def mark_attendance(self):
        """Open the attendance marking module"""
        try:
            subprocess.Popen(["python", "mark_attendance.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open attendance module: {str(e)}")
    
    def view_attendance(self):
        """Open a file dialog to view attendance records"""
        filename = filedialog.askopenfilename(
            initialdir="attendance_records", 
            title="Select Attendance File",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        if filename:
            try:
                if sys.platform == "win32":
                    os.startfile(filename)
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, filename])
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")
    
    def manage_database(self):
        messagebox.showinfo("Info", "Database management feature will be implemented in the next version")
    
    def open_mit_website(self):
        webbrowser.open("https://mitaoe.ac.in/")
    
    def show_help(self):
        help_text = """
        MIT Academy of Engineering - Smart Attendance System Help
        
        1. Register Student: 
           - Add new students to the system with photo capture
           
        2. Mark Attendance:
           - Take attendance using facial recognition
           - Requires location verification
           
        3. View Records:
           - View and export attendance records
           
        4. Dashboard:
           - Overview of system status and statistics
           - Recent activity log
           
        For technical support, contact:
        Computer Science Department
        MIT Academy of Engineering
        """
        messagebox.showinfo("Help", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = MITAttendanceSystem(root)
    root.mainloop()