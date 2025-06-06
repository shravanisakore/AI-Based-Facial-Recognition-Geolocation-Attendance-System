# import cv2
# import os
# import csv
# import numpy as np
# from datetime import datetime

# # Create directories if they don't exist
# if not os.path.exists('student_images'):
#     os.makedirs('student_images')
# if not os.path.exists('attendance_records'):
#     os.makedirs('attendance_records')

# # Initialize face cascade
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# def register_student():
#     student_id = input("Enter Student ID: ")
#     student_name = input("Enter Student Name: ")
    
#     # Initialize webcam
#     cap = cv2.VideoCapture(0)
    
#     print("Looking for face... Press 's' to capture")
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Failed to capture image")
#             break
            
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
#         for (x, y, w, h) in faces:
#             cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
#         cv2.imshow('Register Student', frame)
        
#         key = cv2.waitKey(1)
#         if key == ord('s'):
#             if len(faces) == 1:
#                 # Save the captured image
#                 img_name = f"student_images/{student_id}.jpg"
#                 cv2.imwrite(img_name, gray[y:y+h, x:x+w])  # Save only face region
#                 print(f"Face captured and saved as {img_name}")
                
#                 # Save student details to CSV
#                 with open('registered_students.csv', 'a', newline='') as file:
#                     writer = csv.writer(file)
#                     writer.writerow([student_id, student_name, img_name])
#                 print("Student registered successfully!")
#             else:
#                 print("Please make sure only one face is visible")
#             break
#         elif key == ord('q'):
#             break
    
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     # Create CSV file with header if it doesn't exist
#     if not os.path.exists('registered_students.csv'):
#         with open('registered_students.csv', 'w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(['student_id', 'student_name', 'image_path'])
    
#     register_student()


# # register_student_gui.py
# import cv2
# import os
# import csv
# import tkinter as tk
# from tkinter import messagebox, ttk
# from PIL import Image, ImageTk

# class RegisterStudentGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Student Registration")
#         self.root.geometry("800x600")
        
#         # Variables
#         self.student_id = tk.StringVar()
#         self.student_name = tk.StringVar()
#         self.captured_image = None
        
#         # Create directories if they don't exist
#         os.makedirs('student_images', exist_ok=True)
        
#         # Initialize face cascade
#         self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
#         # Setup GUI
#         self.setup_gui()
        
#         # Initialize webcam
#         self.cap = cv2.VideoCapture(0)
#         self.update_camera()
        
#     def setup_gui(self):
#         # Main frame
#         main_frame = tk.Frame(self.root, padx=20, pady=20)
#         main_frame.pack(expand=True, fill=tk.BOTH)
        
#         # Left panel (form)
#         left_panel = tk.Frame(main_frame)
#         left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
#         tk.Label(left_panel, text="Student ID:", font=('Helvetica', 12)).pack(anchor='w', pady=5)
#         tk.Entry(left_panel, textvariable=self.student_id, font=('Helvetica', 12)).pack(fill=tk.X, pady=5)
        
#         tk.Label(left_panel, text="Student Name:", font=('Helvetica', 12)).pack(anchor='w', pady=5)
#         tk.Entry(left_panel, textvariable=self.student_name, font=('Helvetica', 12)).pack(fill=tk.X, pady=5)
        
#         tk.Button(left_panel, text="Capture Photo", command=self.capture_photo, 
#                  font=('Helvetica', 12), bg='#4CAF50', fg='white').pack(pady=20)
        
#         tk.Button(left_panel, text="Register Student", command=self.register_student, 
#                  font=('Helvetica', 12), bg='#2196F3', fg='white').pack(pady=10)
        
#         tk.Button(left_panel, text="Close", command=self.close_window, 
#                  font=('Helvetica', 12), bg='#F44336', fg='white').pack(pady=10)
        
#         # Right panel (camera)
#         right_panel = tk.Frame(main_frame)
#         right_panel.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
#         self.camera_label = tk.Label(right_panel, bg='black')
#         self.camera_label.pack(expand=True, fill=tk.BOTH)
        
#         # Status bar
#         self.status_var = tk.StringVar()
#         self.status_var.set("Ready")
#         tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X)
    
#     def update_camera(self):
#         ret, frame = self.cap.read()
#         if ret:
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
#             for (x, y, w, h) in faces:
#                 cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             img = Image.fromarray(frame)
#             imgtk = ImageTk.PhotoImage(image=img)
            
#             self.camera_label.imgtk = imgtk
#             self.camera_label.configure(image=imgtk)
        
#         self.root.after(10, self.update_camera)
    
#     def capture_photo(self):
#         if not self.student_id.get() or not self.student_name.get():
#             messagebox.showerror("Error", "Please enter student ID and name first")
#             return
            
#         ret, frame = self.cap.read()
#         if ret:
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
#             if len(faces) == 1:
#                 (x, y, w, h) = faces[0]
#                 self.captured_image = gray[y:y+h, x:x+w]
                
#                 # Show preview
#                 preview = cv2.cvtColor(cv2.rectangle(frame.copy(), (x, y), (x+w, y+h), (0, 255, 0), 2), cv2.COLOR_BGR2RGB)
#                 preview_img = Image.fromarray(preview)
#                 preview_imgtk = ImageTk.PhotoImage(image=preview_img)
                
#                 # Create preview window
#                 preview_window = tk.Toplevel(self.root)
#                 preview_window.title("Captured Photo Preview")
                
#                 label = tk.Label(preview_window, image=preview_imgtk)
#                 label.image = preview_imgtk
#                 label.pack()
                
#                 tk.Label(preview_window, text="Is this photo acceptable?", font=('Helvetica', 12)).pack(pady=10)
                
#                 btn_frame = tk.Frame(preview_window)
#                 btn_frame.pack(pady=10)
                
#                 tk.Button(btn_frame, text="Yes", command=lambda: self.save_photo(preview_window), 
#                          font=('Helvetica', 12), bg='#4CAF50', fg='white').pack(side=tk.LEFT, padx=10)
#                 tk.Button(btn_frame, text="No", command=preview_window.destroy, 
#                          font=('Helvetica', 12), bg='#F44336', fg='white').pack(side=tk.LEFT, padx=10)
                
#                 self.status_var.set("Photo captured - please confirm")
#             else:
#                 messagebox.showerror("Error", "Please make sure only one face is visible")
    
#     def save_photo(self, preview_window):
#         img_name = f"student_images/{self.student_id.get()}.jpg"
#         cv2.imwrite(img_name, self.captured_image)
#         self.status_var.set(f"Photo saved as {img_name}")
#         preview_window.destroy()
    
#     def register_student(self):
#         if not self.student_id.get() or not self.student_name.get():
#             messagebox.showerror("Error", "Please enter student ID and name")
#             return
            
#         if self.captured_image is None:
#             messagebox.showerror("Error", "Please capture a photo first")
#             return
            
#         img_name = f"student_images/{self.student_id.get()}.jpg"
        
#         # Save to CSV
#         csv_exists = os.path.exists('registered_students.csv')
#         with open('registered_students.csv', 'a', newline='') as file:
#             writer = csv.writer(file)
#             if not csv_exists:
#                 writer.writerow(['student_id', 'student_name', 'image_path'])
#             writer.writerow([self.student_id.get(), self.student_name.get(), img_name])
        
#         messagebox.showinfo("Success", "Student registered successfully!")
#         self.status_var.set("Student registered successfully")
        
#         # Reset form
#         self.student_id.set("")
#         self.student_name.set("")
#         self.captured_image = None
    
#     def close_window(self):
#         self.cap.release()
#         self.root.destroy()










import sys
import os
import csv
import cv2
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QHBoxLayout, QWidget, 
                            QMessageBox, QFileDialog)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer

# Create directories if they don't exist
os.makedirs('student_images', exist_ok=True)
os.makedirs('attendance_records', exist_ok=True)

class FaceRegistrationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Face Registration System")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize face cascade
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        if self.face_cascade.empty():
            QMessageBox.critical(self, "Error", "Failed to load face detection model")
            sys.exit(1)
        
        # Create CSV file with header if it doesn't exist
        if not os.path.exists('registered_students.csv'):
            with open('registered_students.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['student_id', 'student_name', 'image_path'])
        
        self.initUI()
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        
    def initUI(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Student Face Registration")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Image display
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(640, 480)
        self.image_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        layout.addWidget(self.image_label)
        
        # Form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Student ID
        id_layout = QHBoxLayout()
        id_label = QLabel("Student ID:")
        id_label.setFixedWidth(100)
        self.id_input = QLineEdit()
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.id_input)
        form_layout.addLayout(id_layout)
        
        # Student Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Student Name:")
        name_label.setFixedWidth(100)
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        form_layout.addLayout(name_layout)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start Camera")
        self.start_btn.setStyleSheet("padding: 8px;")
        self.start_btn.clicked.connect(self.start_camera)
        button_layout.addWidget(self.start_btn)
        
        self.capture_btn = QPushButton("Capture")
        self.capture_btn.setStyleSheet("padding: 8px;")
        self.capture_btn.clicked.connect(self.capture_face)
        self.capture_btn.setEnabled(False)
        button_layout.addWidget(self.capture_btn)
        
        self.register_btn = QPushButton("Register")
        self.register_btn.setStyleSheet("padding: 8px; background-color: #4CAF50; color: white;")
        self.register_btn.clicked.connect(self.register_student)
        self.register_btn.setEnabled(False)
        button_layout.addWidget(self.register_btn)
        
        layout.addLayout(button_layout)
        
        main_widget.setLayout(layout)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
    def start_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                QMessageBox.critical(self, "Error", "Could not open video device")
                return
            
            self.start_btn.setText("Stop Camera")
            self.capture_btn.setEnabled(True)
            self.timer.start(30)  # Update every 30ms
            self.statusBar().showMessage("Camera started - Look at the camera and press Capture when ready")
        else:
            self.timer.stop()
            self.cap.release()
            self.cap = None
            self.image_label.clear()
            self.image_label.setText("Camera off")
            self.start_btn.setText("Start Camera")
            self.capture_btn.setEnabled(False)
            self.statusBar().showMessage("Camera stopped")
    
    def update_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame.copy()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                # Convert to QImage and display
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.image_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
                    self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio))
    
    def capture_face(self):
        if hasattr(self, 'current_frame'):
            gray = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) == 1:
                (x, y, w, h) = faces[0]
                self.captured_face = gray[y:y+h, x:x+w]
                
                # Show preview
                rgb_face = cv2.cvtColor(self.captured_face, cv2.COLOR_GRAY2RGB)
                h, w = rgb_face.shape[:2]
                bytes_per_line = 3 * w
                qt_image = QImage(rgb_face.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.image_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
                    self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio))
                
                self.register_btn.setEnabled(True)
                self.statusBar().showMessage("Face captured - Fill details and click Register")
            else:
                QMessageBox.warning(self, "Warning", "Please make sure only one face is visible")
    
    def register_student(self):
        student_id = self.id_input.text().strip()
        student_name = self.name_input.text().strip()
        
        if not student_id or not student_name:
            QMessageBox.warning(self, "Warning", "Please enter both Student ID and Name")
            return
        
        if not hasattr(self, 'captured_face'):
            QMessageBox.warning(self, "Warning", "No face captured")
            return
        
        # Save the captured image
        img_name = f"student_images/{student_id}.jpg"
        cv2.imwrite(img_name, self.captured_face)
        
        # Save student details to CSV
        try:
            with open('registered_students.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([student_id, student_name, img_name])
            
            QMessageBox.information(self, "Success", "Student registered successfully!")
            self.reset_form()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save data: {str(e)}")
    
    def reset_form(self):
        self.id_input.clear()
        self.name_input.clear()
        self.register_btn.setEnabled(False)
        if self.cap is not None:
            self.statusBar().showMessage("Ready for next registration")
        else:
            self.statusBar().showMessage("Camera off - Start camera to register another student")
    
    def closeEvent(self, event):
        if self.cap is not None:
            self.timer.stop()
            self.cap.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern style
    
    # Set application font
    font = app.font()
    font.setPointSize(10)
    app.setFont(font)
    
    window = FaceRegistrationApp()
    window.show()
    sys.exit(app.exec_())