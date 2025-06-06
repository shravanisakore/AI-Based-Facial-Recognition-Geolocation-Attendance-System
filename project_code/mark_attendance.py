# import cv2
# import os
# import csv
# import numpy as np
# from datetime import datetime
# from geopy.geocoders import Nominatim
# from geopy.distance import geodesic

# # Constants
# COLLEGE_LOCATION = (18.6776, 73.9398)  # Replace with your actual location
# ALLOWED_DISTANCE_KM = 1.0

# def get_current_location():
#     try:
#         geolocator = Nominatim(user_agent="attendance_system")
#         location = geolocator.geocode("", timeout=10)
#         if location:
#             return (location.latitude, location.longitude)
#     except Exception as e:
#         print(f"Location error: {e}")
#     return None

# def is_within_college(current_location):
#     if not current_location:
#         return False
#     try:
#         distance = geodesic(current_location, COLLEGE_LOCATION).km
#         return distance <= ALLOWED_DISTANCE_KM
#     except Exception as e:
#         print(f"Distance error: {e}")
#         return False

# def load_registered_students():
#     students = []
#     csv_file = 'registered_students.csv'
#     if not os.path.exists(csv_file):
#         print("CSV file does not exist.")
#         return students

#     try:
#         with open(csv_file, 'r') as file:
#             reader = csv.reader(file)
#             headers = next(reader, None)
#             if headers != ['student_id', 'student_name', 'image_path']:
#                 print("CSV file has incorrect format!")
#                 return []

#             for row in reader:
#                 if len(row) == 3:
#                     students.append({
#                         'id': row[0].strip(),
#                         'name': row[1].strip(),
#                         'image_path': row[2].strip()
#                     })
#     except Exception as e:
#         print(f"Error loading students: {e}")
#     return students

# def train_recognizer():
#     recognizer = cv2.face.LBPHFaceRecognizer_create()
#     faces = []
#     labels = []
#     label_ids = {}
#     current_id = 0

#     students = load_registered_students()
#     if not students:
#         print("No valid student records found in the database")
#         return None, None

#     for student in students:
#         img_path = student['image_path']
#         if not os.path.exists(img_path):
#             continue

#         img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
#         if img is None:
#             continue
#         img = cv2.resize(img, (200, 200))

#         label = student['id']
#         if label not in label_ids:
#             label_ids[label] = current_id
#             current_id += 1

#         faces.append(img)
#         labels.append(label_ids[label])

#     if not faces:
#         print("No valid face images found for training")
#         return None, None

#     recognizer.train(faces, np.array(labels))
#     return recognizer, label_ids

# def mark_attendance():
#     recognizer, label_ids = train_recognizer()
#     if recognizer is None:
#         print("Attendance system not ready. Please register students first.")
#         return

#     students = load_registered_students()
#     id_to_student = {s['id']: s for s in students}

#     current_location = get_current_location()
#     if not is_within_college(current_location):
#         print("You are not within college premises. Attendance not allowed.")
#         return

#     cap = cv2.VideoCapture(0)
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#     print("Looking for faces... Press 'q' to quit.")

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#         for (x, y, w, h) in faces:
#             roi = gray[y:y+h, x:x+w]
#             roi = cv2.resize(roi, (200, 200))

#             try:
#                 label_id, confidence = recognizer.predict(roi)
#                 student = None
#                 for sid, lid in label_ids.items():
#                     if lid == label_id and confidence < 100:
#                         student = id_to_student.get(sid)
#                         break

#                 if student:
#                     name = student['name']
#                     student_id = student['id']
#                     date_str = datetime.now().strftime("%Y-%m-%d")
#                     time_str = datetime.now().strftime("%H:%M:%S")
#                     subject = input(f"Enter subject for {name} (ID: {student_id}): ").strip()

#                     if not subject:
#                         print("Subject cannot be empty")
#                         continue

#                     attendance_file = f'attendance_records/attendance_{date_str}_{subject}.csv'
#                     already_marked = False

#                     if os.path.exists(attendance_file):
#                         with open(attendance_file, 'r') as f:
#                             reader = csv.reader(f)
#                             for row in reader:
#                                 if row and row[0] == student_id:
#                                     already_marked = True
#                                     break

#                     if not already_marked:
#                         with open(attendance_file, 'a', newline='') as f:
#                             writer = csv.writer(f)
#                             if os.stat(attendance_file).st_size == 0:
#                                 writer.writerow(['student_id', 'student_name', 'time', 'location'])
#                             writer.writerow([student_id, name, time_str, str(current_location)])
#                         print(f"Attendance marked for {name}")
#                     else:
#                         print(f"Attendance already marked for {name} today.")

#                     color = (0, 255, 0)
#                 else:
#                     name = "Unknown"
#                     color = (0, 0, 255)

#                 cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
#                 cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
#             except Exception as e:
#                 print(f"Error during recognition: {e}")
#                 continue

#         cv2.imshow('Mark Attendance', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     os.makedirs('student_images', exist_ok=True)
#     os.makedirs('attendance_records', exist_ok=True)

#     if not os.path.exists('registered_students.csv'):
#         with open('registered_students.csv', 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['student_id', 'student_name', 'image_path'])

#     mark_attendance()




# import cv2
# import os
# import csv
# import numpy as np
# from datetime import datetime
# from geopy.distance import geodesic

# # College coordinates (Pune)
# COLLEGE_LOCATION = (12.9716, 77.5946)
# ALLOWED_DISTANCE_KM = 1.0

# # === Helper Functions ===
# def get_current_location():
#     # Hardcoded Pune location for testing
#     return (18.5206, 73.8570)

# def is_within_college(current_location):
#     if not current_location:
#         return False
#     try:
#         distance = geodesic(current_location, COLLEGE_LOCATION).km
#         print(f"Current location: {current_location} | Distance from college: {distance:.3f} km")
#         return distance <= ALLOWED_DISTANCE_KM
#     except Exception as e:
#         print(f"Distance calculation error: {e}")
#         return False

# def load_registered_students():
#     students = []
#     try:
#         with open('registered_students.csv', 'r') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 if all(key in row for key in ['student_id', 'student_name', 'image_path']):
#                     students.append(row)
#     except Exception as e:
#         print(f"Error loading students: {e}")
#     return students

# def train_recognizer():
#     recognizer = cv2.face.LBPHFaceRecognizer_create()
#     faces, labels = [], []
#     label_ids, current_id = {}, 0

#     students = load_registered_students()
#     if not students:
#         print("No valid student records found in the database")
#         return None, None

#     for student in students:
#         img_path = student['image_path']
#         if not os.path.exists(img_path):
#             continue

#         img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
#         if img is None:
#             continue

#         img = cv2.resize(img, (200, 200))
#         label = student['student_id']
#         if label not in label_ids:
#             label_ids[label] = current_id
#             current_id += 1

#         faces.append(img)
#         labels.append(label_ids[label])

#     if not faces:
#         print("No face data for training")
#         return None, None

#     recognizer.train(faces, np.array(labels))
#     print("Training complete.")
#     return recognizer, label_ids

# def mark_attendance():
#     recognizer, label_ids = train_recognizer()
#     if recognizer is None:
#         print("Attendance system not ready. Please register students first.")
#         return

#     students = load_registered_students()
#     id_to_student = {s['student_id']: s for s in students}

#     current_location = get_current_location()
#     if not is_within_college(current_location):
#         print("You are not within college premises. Attendance not allowed.")
#         return

#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("Camera could not be opened.")
#         return

#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#     os.makedirs('attendance_records', exist_ok=True)
#     print("Looking for faces... Press 'q' to quit")

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, 1.1, 5)

#         for (x, y, w, h) in faces:
#             roi_gray = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
#             label_id, confidence = recognizer.predict(roi_gray)

#             student = None
#             for sid, lid in label_ids.items():
#                 if lid == label_id and confidence < 100:
#                     student = id_to_student.get(sid)
#                     break

#             if student:
#                 name, sid = student['student_name'], student['student_id']
#                 date_str = datetime.now().strftime('%Y-%m-%d')
#                 time_str = datetime.now().strftime('%H:%M:%S')
#                 subject = input(f"Enter subject for {name} (ID: {sid}): ").strip()
#                 if not subject:
#                     continue

#                 filename = f"attendance_records/attendance_{date_str}_{subject}.csv"
#                 already_marked = False
#                 if os.path.exists(filename):
#                     with open(filename, 'r') as file:
#                         if sid in [row[0] for row in csv.reader(file)]:
#                             already_marked = True

#                 if not already_marked:
#                     with open(filename, 'a', newline='') as file:
#                         writer = csv.writer(file)
#                         if os.stat(filename).st_size == 0:
#                             writer.writerow(['student_id', 'student_name', 'time', 'location'])
#                         writer.writerow([sid, name, time_str, str(current_location)])
#                     print(f"Attendance marked for {name} at {time_str}")
#                 else:
#                     print(f"Attendance already marked for {name}")

#                 color = (0, 255, 0)
#                 label = name
#             else:
#                 color = (0, 0, 255)
#                 label = "Unknown"

#             cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
#             cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

#         cv2.imshow("Attendance", frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     os.makedirs('student_images', exist_ok=True)
#     os.makedirs('attendance_records', exist_ok=True)
#     if not os.path.exists('registered_students.csv'):
#         with open('registered_students.csv', 'w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(['student_id', 'student_name', 'image_path'])

#     mark_attendance()

# import cv2
# import os
# import csv
# import json
# import numpy as np
# from datetime import datetime
# from geopy.geocoders import Nominatim
# from geopy.distance import geodesic
# import requests


# # Load coordinates from JSON file
# def load_college_location(json_path='coordinates.json'):
#     try:
#         with open(json_path, 'r') as file:
#             data = json.load(file)
#             dd = data.get('DD', {})
#             if 'lat' in dd and 'lng' in dd:
#                 return (dd['lat'], dd['lng'])
#     except Exception as e:
#         print(f"Error loading coordinates: {e}")
#     return None

# # Load college coordinates dynamically
# COLLEGE_LOCATION = load_college_location()
# if COLLEGE_LOCATION is None:
#     print("Error: Could not load college coordinates from coordinates.json.")
#     exit()

# ALLOWED_DISTANCE_KM = 10.0  # 500 meters radius


# def get_current_location():
#     print("Fetching your current location automatically via IP...")
#     try:
#         response = requests.get("https://ipinfo.io/json")
#         data = response.json()
#         loc = data.get("loc")  # format: "lat,lng"
#         if loc:
#             lat, lng = loc.split(",")
#             print(f"Your location is approx: Latitude={lat}, Longitude={lng}")
#             return (float(lat), float(lng))
#     except Exception as e:
#         print(f"Failed to get location: {e}")
#     return None


# def is_within_college(current_location):
#     """Check if current location is within college premises"""
#     if not current_location:
#         return False
#     try:
#         distance = geodesic(current_location, COLLEGE_LOCATION).km
#         return distance <= ALLOWED_DISTANCE_KM
#     except Exception as e:
#         print(f"Distance calculation error: {e}")
#         return False

# def load_registered_students():
#     """Load registered students from CSV file"""
#     students = []
#     if not os.path.exists('registered_students.csv'):
#         print("registered_students.csv file not found.")
#         return students

#     try:
#         with open('registered_students.csv', 'r') as file:
#             reader = csv.reader(file)
#             headers = next(reader)
#             if headers != ['student_id', 'student_name', 'image_path']:
#                 print("CSV file has incorrect format!")
#                 return []
#             for row in reader:
#                 if len(row) >= 3:
#                     students.append({
#                         'id': row[0],
#                         'name': row[1],
#                         'image_path': row[2]
#                     })
#     except Exception as e:
#         print(f"Error loading students: {e}")
#     return students

# def train_recognizer():
#     recognizer = cv2.face.LBPHFaceRecognizer_create()
#     faces = []
#     labels = []
#     label_ids = {}
#     current_id = 0

#     students = load_registered_students()
#     if not students:
#         print("No valid student records found in the database")
#         return None, None

#     print(f"Training recognizer with {len(students)} students...")

#     for student in students:
#         img_path = student['image_path']
#         if not os.path.exists(img_path):
#             print(f"Image not found: {img_path}")
#             continue

#         try:
#             img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
#             if img is None:
#                 print(f"Failed to load image: {img_path}")
#                 continue

#             img = cv2.resize(img, (200, 200))

#             label = student['id']
#             if label not in label_ids:
#                 label_ids[label] = current_id
#                 current_id += 1

#             faces.append(img)
#             labels.append(label_ids[label])
#         except Exception as e:
#             print(f"Error processing {img_path}: {e}")

#     if not faces:
#         print("No valid face images found for training")
#         return None, None

#     try:
#         recognizer.train(faces, np.array(labels))
#         print("Training complete.")
#         return recognizer, label_ids
#     except Exception as e:
#         print(f"Training failed: {e}")
#         return None, None

# def mark_attendance():
#     recognizer, label_ids = train_recognizer()
#     if recognizer is None:
#         print("Attendance system not ready. Please register students first.")
#         return

#     students = load_registered_students()
#     id_to_student = {s['id']: s for s in students}

#     current_location = get_current_location()
#     if not is_within_college(current_location):
#         print("You are not within college premises. Attendance not allowed.")
#         return

#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("Error: Could not open camera")
#         return

#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     if face_cascade.empty():
#         print("Error: Could not load face detector")
#         cap.release()
#         return

#     os.makedirs('attendance_records', exist_ok=True)

#     print("Looking for faces... Press 'q' to quit.")

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Failed to capture frame")
#             break

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, 1.1, 5)

#         for (x, y, w, h) in faces:
#             roi_gray = gray[y:y+h, x:x+w]
#             roi_gray = cv2.resize(roi_gray, (200, 200))

#             try:
#                 label_id, confidence = recognizer.predict(roi_gray)
#                 student = None

#                 for s_id, s_label_id in label_ids.items():
#                     if s_label_id == label_id and confidence < 100:
#                         student = id_to_student.get(s_id)
#                         break

#                 name = student['name'] if student else "Unknown"
#                 student_id = student['id'] if student else "N/A"

#                 color = (0, 255, 0) if student else (0, 0, 255)
#                 cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
#                 cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

#                 if student:
#                     date_str = datetime.now().strftime("%Y-%m-%d")
#                     time_str = datetime.now().strftime("%H:%M:%S")
#                     subject = input(f"Enter subject for {name} (ID: {student_id}): ").strip()

#                     if not subject:
#                         print("Subject is required.")
#                         continue

#                     attendance_file = f"attendance_records/attendance_{date_str}_{subject}.csv"

#                     already_marked = False
#                     if os.path.exists(attendance_file):
#                         with open(attendance_file, 'r') as file:
#                             reader = csv.reader(file)
#                             for row in reader:
#                                 if row and row[0] == student_id:
#                                     already_marked = True
#                                     break

#                     if not already_marked:
#                         with open(attendance_file, 'a', newline='') as file:
#                             writer = csv.writer(file)
#                             if os.stat(attendance_file).st_size == 0:
#                                 writer.writerow(['student_id', 'student_name', 'time', 'location'])
#                             writer.writerow([student_id, name, time_str, str(current_location)])
#                         print(f"Attendance marked for {name} at {time_str}")
#                     else:
#                         print(f"Attendance already marked for {name}")
#             except Exception as e:
#                 print(f"Recognition error: {e}")

#         cv2.imshow('Mark Attendance', frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     os.makedirs('student_images', exist_ok=True)
#     os.makedirs('attendance_records', exist_ok=True)

#     if not os.path.exists('registered_students.csv'):
#         with open('registered_students.csv', 'w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(['student_id', 'student_name', 'image_path'])

#     mark_attendance()


# import cv2
# import os
# import csv
# import numpy as np
# from datetime import datetime
# from geopy.geocoders import Nominatim
# from geopy.distance import geodesic
# import requests

# # College coordinates for Alandi, Pune
# COLLEGE_LOCATION = (18.6229, 73.807)  # Latitude, Longitude of your college
# ALLOWED_DISTANCE_KM = 10.0  # 10 km radius allowed

# def get_current_location():
#     """Fetch current location approx by public IP using ipinfo.io"""
#     print("Fetching your current location automatically via IP...")
#     try:
#         response = requests.get("https://ipinfo.io/json")
#         data = response.json()
#         loc = data.get("loc")  # format: "lat,lng"
#         if loc:
#             lat, lng = loc.split(",")
#             print(f"Your location is approx: Latitude={lat}, Longitude={lng}")
#             return (float(lat), float(lng))
#     except Exception as e:
#         print(f"Failed to get location: {e}")
#     return None

# def is_within_college(current_location):
#     """Check if current location is within allowed distance from college"""
#     if not current_location:
#         return False
#     try:
#         distance = geodesic(current_location, COLLEGE_LOCATION).km
#         print(f"Distance from college: {distance:.2f} km")
#         return distance <= ALLOWED_DISTANCE_KM
#     except Exception as e:
#         print(f"Distance calculation error: {e}")
#         return False

# def load_registered_students():
#     """Load registered students from CSV file"""
#     students = []
#     if not os.path.exists('registered_students.csv'):
#         print("CSV file not found.")
#         return students
        
#     try:
#         with open('registered_students.csv', 'r') as file:
#             reader = csv.reader(file)
#             header = next(reader, None)
#             # Check header format
#             if not header or len(header) < 3 or header[0].lower() != 'student_id':
#                 print("CSV file has incorrect format!")
#                 return []
#             for row in reader:
#                 if len(row) >= 3:  # Ensure row has all required fields
#                     students.append({
#                         'id': row[0],
#                         'name': row[1],
#                         'image_path': row[2]
#                     })
#     except Exception as e:
#         print(f"Error loading students: {e}")
#     return students

# def train_recognizer():
#     """Train the face recognizer with registered student images"""
#     recognizer = cv2.face.LBPHFaceRecognizer_create()
#     faces = []
#     labels = []
#     label_ids = {}
#     current_id = 0
    
#     students = load_registered_students()
#     if not students:
#         print("No valid student records found in the database")
#         return None, None
    
#     print(f"Training recognizer with {len(students)} students...")
    
#     for student in students:
#         img_path = student['image_path']
#         if not os.path.exists(img_path):
#             print(f"Image not found: {img_path}")
#             continue
        
#         try:
#             img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
#             if img is None:
#                 print(f"Failed to load image: {img_path}")
#                 continue
                
#             # Resize image to standard size for better recognition
#             img = cv2.resize(img, (200, 200))
            
#             label = student['id']
#             if label not in label_ids:
#                 label_ids[label] = current_id
#                 current_id += 1
            
#             faces.append(img)
#             labels.append(label_ids[label])
#             print(f"Added training sample for {student['name']}")
            
#         except Exception as e:
#             print(f"Error processing {img_path}: {e}")
#             continue
    
#     if not faces:
#         print("No valid face images found for training")
#         return None, None
    
#     try:
#         recognizer.train(faces, np.array(labels))
#         print("Training complete.")
#         return recognizer, label_ids
#     except Exception as e:
#         print(f"Training failed: {e}")
#         return None, None

# def mark_attendance():
#     """Main function to mark attendance using face recognition"""
#     recognizer, label_ids = train_recognizer()
#     if recognizer is None:
#         print("Attendance system not ready. Please register students first.")
#         return
    
#     students = load_registered_students()
#     id_to_student = {s['id']: s for s in students}
    
#     current_location = get_current_location()
#     within_college = is_within_college(current_location)
    
#     if not within_college:
#         print("You are not within college premises. Attendance not allowed.")
#         return
    
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("Error: Could not open camera")
#         return
    
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     if face_cascade.empty():
#         print("Error: Could not load face detector")
#         cap.release()
#         return
    
#     print("Looking for recognized faces... Press 'q' to quit")
#     os.makedirs('attendance_records', exist_ok=True)
    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Failed to capture frame")
#             break
            
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
#         for (x, y, w, h) in faces:
#             roi_gray = gray[y:y+h, x:x+w]
#             roi_gray = cv2.resize(roi_gray, (200, 200))
            
#             try:
#                 label_id, confidence = recognizer.predict(roi_gray)
#                 student = None
#                 for s_id, s_label_id in label_ids.items():
#                     if s_label_id == label_id and confidence < 100:
#                         student = id_to_student.get(s_id)
#                         break
                
#                 if student:
#                     name = student['name']
#                     student_id = student['id']
#                     date_str = datetime.now().strftime("%Y-%m-%d")
#                     time_str = datetime.now().strftime("%H:%M:%S")
                    
#                     subject = input(f"Enter subject for {name} (ID: {student_id}): ").strip()
#                     if not subject:
#                         print("Subject cannot be empty")
#                         continue
                    
#                     attendance_file = f"attendance_records/attendance_{date_str}_{subject}.csv"
                    
#                     already_marked = False
#                     if os.path.exists(attendance_file):
#                         with open(attendance_file, 'r') as file:
#                             reader = csv.reader(file)
#                             for row in reader:
#                                 if row and row[0] == student_id:
#                                     already_marked = True
#                                     break
                    
#                     if not already_marked:
#                         with open(attendance_file, 'a', newline='') as file:
#                             writer = csv.writer(file)
#                             if os.stat(attendance_file).st_size == 0:
#                                 writer.writerow(['student_id', 'student_name', 'time', 'location'])
#                             writer.writerow([student_id, name, time_str, str(current_location)])
#                         print(f"Attendance marked for {name} in {subject} at {time_str}")
#                     else:
#                         print(f"Attendance already marked for {name} today in {subject}")
#                 else:
#                     name = "Unknown"
                
#                 color = (0, 255, 0) if student else (0, 0, 255)
#                 cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
#                 cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
#                 if student:
#                     cv2.putText(frame, f"Confidence: {confidence:.2f}", (x, y+h+20), 
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
#             except Exception as e:
#                 print(f"Recognition error: {e}")
#                 continue
        
#         cv2.imshow('Mark Attendance', frame)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
    
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     os.makedirs('student_images', exist_ok=True)
#     os.makedirs('attendance_records', exist_ok=True)
    
#     if not os.path.exists('registered_students.csv'):
#         with open('registered_students.csv', 'w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(['student_id', 'student_name', 'image_path'])
    
#     mark_attendance()


# # mark_attendance_gui.py
# import cv2
# import os
# import csv
# import numpy as np
# from datetime import datetime
# import tkinter as tk
# from tkinter import messagebox, ttk
# from PIL import Image, ImageTk
# import requests
# from geopy.distance import geodesic

# class MarkAttendanceGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Mark Attendance")
#         self.root.geometry("1000x700")
        
#         # College location (Alandi, Pune)
#         self.COLLEGE_LOCATION = (18.6229, 73.807)
#         self.ALLOWED_DISTANCE_KM = 10.0
        
#         # Variables
#         self.current_location = None
#         self.recognizer = None
#         self.label_ids = None
#         self.students = []
#         self.id_to_student = {}
#         self.subject = tk.StringVar()
#         self.status_var = tk.StringVar()
#         self.status_var.set("Initializing...")
        
#         # Setup GUI
#         self.setup_gui()
        
#         # Initialize system
#         self.initialize_system()
        
#         # Initialize camera
#         self.cap = cv2.VideoCapture(0)
#         self.update_camera()
    
#     def setup_gui(self):
#         # Main frame
#         main_frame = tk.Frame(self.root)
#         main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
#         # Left panel (controls)
#         left_panel = tk.Frame(main_frame, width=300)
#         left_panel.pack(side=tk.LEFT, fill=tk.Y)
        
#         tk.Label(left_panel, text="Subject:", font=('Helvetica', 12)).pack(anchor='w', pady=5)
#         tk.Entry(left_panel, textvariable=self.subject, font=('Helvetica', 12)).pack(fill=tk.X, pady=5)
        
#         tk.Button(left_panel, text="Check Location", command=self.check_location, 
#                  font=('Helvetica', 12), bg='#4CAF50', fg='white').pack(pady=10, fill=tk.X)
        
#         self.location_label = tk.Label(left_panel, text="Location: Not checked", font=('Helvetica', 10), wraplength=250)
#         self.location_label.pack(pady=10)
        
#         self.distance_label = tk.Label(left_panel, text="Distance: -", font=('Helvetica', 10))
#         self.distance_label.pack(pady=5)
        
#         tk.Button(left_panel, text="Refresh Recognition", command=self.initialize_system, 
#                  font=('Helvetica', 12), bg='#2196F3', fg='white').pack(pady=10, fill=tk.X)
        
#         tk.Button(left_panel, text="Close", command=self.close_window, 
#                  font=('Helvetica', 12), bg='#F44336', fg='white').pack(pady=10, fill=tk.X)
        
#         # Right panel (camera and info)
#         right_panel = tk.Frame(main_frame)
#         right_panel.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
#         # Camera display
#         self.camera_label = tk.Label(right_panel, bg='black')
#         self.camera_label.pack(expand=True, fill=tk.BOTH)
        
#         # Recognized student info
#         self.student_info = tk.Label(right_panel, text="No student recognized", 
#                                    font=('Helvetica', 14), pady=10)
#         self.student_info.pack(fill=tk.X)
        
#         # Status bar
#         tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X)
    
#     def initialize_system(self):
#         self.status_var.set("Loading student database...")
#         self.root.update()
        
#         # Load registered students
#         self.students = self.load_registered_students()
#         if not self.students:
#             messagebox.showerror("Error", "No students found in database. Please register students first.")
#             self.status_var.set("No students in database")
#             return
        
#         self.id_to_student = {s['id']: s for s in self.students}
        
#         # Train recognizer
#         self.status_var.set("Training face recognizer...")
#         self.root.update()
        
#         self.recognizer, self.label_ids = self.train_recognizer()
#         if self.recognizer is None:
#             messagebox.showerror("Error", "Failed to train recognizer. Check student images.")
#             self.status_var.set("Training failed")
#             return
        
#         self.status_var.set(f"System ready - {len(self.students)} students loaded")
    
#     def load_registered_students(self):
#         students = []
#         if not os.path.exists('registered_students.csv'):
#             return students
            
#         try:
#             with open('registered_students.csv', 'r') as file:
#                 reader = csv.reader(file)
#                 header = next(reader, None)
#                 if not header or len(header) < 3 or header[0].lower() != 'student_id':
#                     return []
#                 for row in reader:
#                     if len(row) >= 3:
#                         students.append({
#                             'id': row[0],
#                             'name': row[1],
#                             'image_path': row[2]
#                         })
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to load students: {e}")
#         return students
    
#     def train_recognizer(self):
#         recognizer = cv2.face.LBPHFaceRecognizer_create()
#         faces = []
#         labels = []
#         label_ids = {}
#         current_id = 0
        
#         for student in self.students:
#             img_path = student['image_path']
#             if not os.path.exists(img_path):
#                 continue
            
#             try:
#                 img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
#                 if img is None:
#                     continue
                
#                 img = cv2.resize(img, (200, 200))
#                 label = student['id']
                
#                 if label not in label_ids:
#                     label_ids[label] = current_id
#                     current_id += 1
                
#                 faces.append(img)
#                 labels.append(label_ids[label])
#             except Exception as e:
#                 print(f"Error processing {img_path}: {e}")
#                 continue
        
#         if not faces:
#             return None, None
        
#         try:
#             recognizer.train(faces, np.array(labels))
#             return recognizer, label_ids
#         except Exception as e:
#             print(f"Training failed: {e}")
#             return None, None
    
#     def get_current_location(self):
#         """Fetch current location approx by public IP using ipinfo.io"""
#         self.status_var.set("Fetching location...")
#         self.root.update()
        
#         try:
#             response = requests.get("https://ipinfo.io/json")
#             data = response.json()
#             loc = data.get("loc")  # format: "lat,lng"
#             if loc:
#                 lat, lng = loc.split(",")
#                 return (float(lat), float(lng))
#         except Exception as e:
#             print(f"Failed to get location: {e}")
#         return None
    
#     def check_location(self):
#         self.current_location = self.get_current_location()
#         if not self.current_location:
#             self.location_label.config(text="Location: Could not determine location")
#             messagebox.showerror("Error", "Could not determine your location")
#             return
        
#         try:
#             distance = geodesic(self.current_location, self.COLLEGE_LOCATION).km
#             self.location_label.config(text=f"Location: {self.current_location}")
#             self.distance_label.config(text=f"Distance: {distance:.2f} km from college")
            
#             if distance <= self.ALLOWED_DISTANCE_KM:
#                 messagebox.showinfo("Success", "You are within college premises")
#                 self.status_var.set("Location verified - within college")
#             else:
#                 messagebox.showwarning("Warning", "You are not within college premises")
#                 self.status_var.set("Location verified - outside college")
#         except Exception as e:
#             messagebox.showerror("Error", f"Distance calculation failed: {e}")
    
#     def update_camera(self):
#         if self.recognizer is None:
#             self.root.after(100, self.update_camera)
#             return
            
#         ret, frame = self.cap.read()
#         if ret:
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#             faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
#             recognized_student = None
#             confidence = 0
            
#             for (x, y, w, h) in faces:
#                 roi_gray = gray[y:y+h, x:x+w]
#                 roi_gray = cv2.resize(roi_gray, (200, 200))
                
#                 try:
#                     label_id, conf = self.recognizer.predict(roi_gray)
#                     for s_id, s_label_id in self.label_ids.items():
#                         if s_label_id == label_id and conf < 100:  # Confidence threshold
#                             recognized_student = self.id_to_student.get(s_id)
#                             confidence = conf
#                             break
                    
#                     color = (0, 255, 0) if recognized_student else (0, 0, 255)
#                     cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    
#                     label = recognized_student['name'] if recognized_student else "Unknown"
#                     cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                    
#                     if recognized_student:
#                         cv2.putText(frame, f"Confidence: {confidence:.2f}", (x, y+h+20), 
#                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                        
#                         # Automatically mark attendance if conditions are met
#                         if (self.current_location and 
#                             geodesic(self.current_location, self.COLLEGE_LOCATION).km <= self.ALLOWED_DISTANCE_KM and
#                             self.subject.get()):
#                             self.mark_attendance(recognized_student)
                
#                 except Exception as e:
#                     print(f"Recognition error: {e}")
            
#             # Update student info display
#             if recognized_student:
#                 self.student_info.config(
#                     text=f"Recognized: {recognized_student['name']} (ID: {recognized_student['id']})\nConfidence: {confidence:.2f}",
#                     fg='green')
#             else:
#                 self.student_info.config(text="No student recognized", fg='red')
            
#             # Display camera feed
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             img = Image.fromarray(frame)
#             imgtk = ImageTk.PhotoImage(image=img)
            
#             self.camera_label.imgtk = imgtk
#             self.camera_label.configure(image=imgtk)
        
#         self.root.after(10, self.update_camera)
    
#     def mark_attendance(self, student):
#         date_str = datetime.now().strftime("%Y-%m-%d")
#         time_str = datetime.now().strftime("%H:%M:%S")
#         subject = self.subject.get()
        
#         if not subject:
#             return
            
#         attendance_file = f"attendance_records/attendance_{date_str}_{subject}.csv"
#         os.makedirs('attendance_records', exist_ok=True)
        
#         # Check if already marked
#         already_marked = False
#         if os.path.exists(attendance_file):
#             with open(attendance_file, 'r') as file:
#                 reader = csv.reader(file)
#                 for row in reader:
#                     if row and row[0] == student['id']:
#                         already_marked = True
#                         break
        
#         if not already_marked:
#             with open(attendance_file, 'a', newline='') as file:
#                 writer = csv.writer(file)
#                 if os.stat(attendance_file).st_size == 0:
#                     writer.writerow(['student_id', 'student_name', 'time', 'location'])
#                 writer.writerow([student['id'], student['name'], time_str, str(self.current_location)])
            
#             self.status_var.set(f"Attendance marked for {student['name']} in {subject}")
#         else:
#             self.status_var.set(f"Attendance already marked for {student['name']}")
    
#     def close_window(self):
#         self.cap.release()
#         self.root.destroy()








import sys
import os
import csv
import cv2
import numpy as np
from datetime import datetime
import requests
from geopy.distance import geodesic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QHBoxLayout, QWidget, 
                            QMessageBox, QComboBox, QTextEdit, QTabWidget)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal

# Configuration
COLLEGE_LOCATION = (18.5196, 73.8554)  # Alandi, Pune coordinates
ALLOWED_DISTANCE_KM = 10.0
MIN_CONFIDENCE = 70  # Minimum confidence threshold for face recognition

class AttendanceSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Attendance System")
        self.setGeometry(100, 100, 1000, 700)
        
        # Initialize variables
        self.recognizer = None
        self.label_ids = {}
        self.id_to_student = {}
        self.current_location = None
        self.within_college = False
        self.current_subject = ""
        self.cap = None
        self.timer = QTimer()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Create directories if needed
        os.makedirs('student_images', exist_ok=True)
        os.makedirs('attendance_records', exist_ok=True)
        
        # Initialize CSV file if not exists
        if not os.path.exists('registered_students.csv'):
            with open('registered_students.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['student_id', 'student_name', 'image_path'])
        
        self.initUI()
    
    def initUI(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        
        # Create tabs
        self.tabs = QTabWidget()
        self.attendance_tab = QWidget()
        self.registration_tab = QWidget()
        self.reports_tab = QWidget()
        
        self.tabs.addTab(self.attendance_tab, "Attendance")
        self.tabs.addTab(self.registration_tab, "Registration")
        self.tabs.addTab(self.reports_tab, "Reports")
        
        # Setup each tab
        self.setup_attendance_tab()
        self.setup_registration_tab()
        self.setup_reports_tab()
        
        main_layout.addWidget(self.tabs)
        main_widget.setLayout(main_layout)
        
        # Status bar
        self.statusBar().showMessage("System Ready")
        
        # Load initial data
        self.load_student_data()
        self.train_recognizer()
        self.check_location()
    
    def setup_attendance_tab(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Mark Attendance")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Location info
        self.location_label = QLabel("Location: Checking...")
        layout.addWidget(self.location_label)
        
        # Camera display
        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setMinimumSize(640, 480)
        self.camera_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        layout.addWidget(self.camera_label)
        
        # Subject selection
        subject_layout = QHBoxLayout()
        subject_label = QLabel("Subject:")
        self.subject_combo = QComboBox()
        self.subject_combo.addItems(["Math", "Science", "History", "English", "Computer Science"])
        self.subject_combo.setEditable(True)
        subject_layout.addWidget(subject_label)
        subject_layout.addWidget(self.subject_combo)
        layout.addLayout(subject_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start Camera")
        self.start_btn.setStyleSheet("padding: 8px;")
        self.start_btn.clicked.connect(self.toggle_camera)
        button_layout.addWidget(self.start_btn)
        
        self.mark_btn = QPushButton("Mark Attendance")
        self.mark_btn.setStyleSheet("padding: 8px; background-color: #4CAF50; color: white;")
        self.mark_btn.clicked.connect(self.mark_attendance)
        self.mark_btn.setEnabled(False)
        button_layout.addWidget(self.mark_btn)
        
        layout.addLayout(button_layout)
        
        # Log
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        layout.addWidget(self.log_text)
        
        self.attendance_tab.setLayout(layout)
    
    def setup_registration_tab(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Register New Student")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Student ID
        id_layout = QHBoxLayout()
        id_label = QLabel("Student ID:")
        id_label.setFixedWidth(100)
        self.reg_id_input = QLineEdit()
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.reg_id_input)
        form_layout.addLayout(id_layout)
        
        # Student Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Student Name:")
        name_label.setFixedWidth(100)
        self.reg_name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.reg_name_input)
        form_layout.addLayout(name_layout)
        
        layout.addLayout(form_layout)
        
        # Camera display
        self.reg_camera_label = QLabel()
        self.reg_camera_label.setAlignment(Qt.AlignCenter)
        self.reg_camera_label.setMinimumSize(640, 480)
        self.reg_camera_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        layout.addWidget(self.reg_camera_label)
        
        # Registration buttons
        reg_button_layout = QHBoxLayout()
        
        self.reg_start_btn = QPushButton("Start Camera")
        self.reg_start_btn.setStyleSheet("padding: 8px;")
        self.reg_start_btn.clicked.connect(self.toggle_reg_camera)
        reg_button_layout.addWidget(self.reg_start_btn)
        
        self.capture_btn = QPushButton("Capture")
        self.capture_btn.setStyleSheet("padding: 8px;")
        self.capture_btn.clicked.connect(self.capture_face)
        self.capture_btn.setEnabled(False)
        reg_button_layout.addWidget(self.capture_btn)
        
        self.register_btn = QPushButton("Register")
        self.register_btn.setStyleSheet("padding: 8px; background-color: #2196F3; color: white;")
        self.register_btn.clicked.connect(self.register_student)
        self.register_btn.setEnabled(False)
        reg_button_layout.addWidget(self.register_btn)
        
        layout.addLayout(reg_button_layout)
        
        self.registration_tab.setLayout(layout)
    
    def setup_reports_tab(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Attendance Reports")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Date and subject selection
        filter_layout = QHBoxLayout()
        
        date_label = QLabel("Date:")
        self.date_combo = QComboBox()
        self.populate_dates()
        filter_layout.addWidget(date_label)
        filter_layout.addWidget(self.date_combo)
        
        subject_label = QLabel("Subject:")
        self.report_subject_combo = QComboBox()
        self.report_subject_combo.addItems(["All", "Math", "Science", "History", "English", "Computer Science"])
        filter_layout.addWidget(subject_label)
        filter_layout.addWidget(self.report_subject_combo)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet("padding: 5px;")
        refresh_btn.clicked.connect(self.load_attendance_report)
        filter_layout.addWidget(refresh_btn)
        
        layout.addLayout(filter_layout)
        
        # Report display
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        layout.addWidget(self.report_text)
        
        # Export button
        export_btn = QPushButton("Export to CSV")
        export_btn.setStyleSheet("padding: 8px; background-color: #607D8B; color: white;")
        export_btn.clicked.connect(self.export_report)
        layout.addWidget(export_btn)
        
        self.reports_tab.setLayout(layout)
        
        # Load initial report
        self.load_attendance_report()
    
    def toggle_camera(self):
        if self.cap is None:
            self.start_camera()
        else:
            self.stop_camera()
    
    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            QMessageBox.critical(self, "Error", "Could not open video device")
            return
        
        self.start_btn.setText("Stop Camera")
        self.mark_btn.setEnabled(self.within_college)
        self.timer.timeout.connect(self.update_attendance_frame)
        self.timer.start(30)  # Update every 30ms
        self.log_message("Camera started - Ready for attendance")
    
    def stop_camera(self):
        if self.cap is not None:
            self.timer.stop()
            self.cap.release()
            self.cap = None
            self.camera_label.clear()
            self.camera_label.setText("Camera off")
            self.start_btn.setText("Start Camera")
            self.mark_btn.setEnabled(False)
            self.log_message("Camera stopped")
    
    def update_attendance_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.log_message("Failed to capture frame")
            return
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (200, 200))
            
            try:
                if self.recognizer:
                    label_id, confidence = self.recognizer.predict(roi_gray)
                    student = None
                    
                    for s_id, s_label_id in self.label_ids.items():
                        if s_label_id == label_id and confidence < MIN_CONFIDENCE:
                            student = self.id_to_student.get(s_id)
                            break
                    
                    if student:
                        name = student['name']
                        student_id = student['id']
                        color = (0, 255, 0)  # Green
                        text = f"{name} (ID: {student_id})"
                        confidence_text = f"Confidence: {confidence:.1f}%"
                    else:
                        name = "Unknown"
                        color = (0, 0, 255)  # Red
                        text = name
                        confidence_text = ""
                    
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                    if confidence_text:
                        cv2.putText(frame, confidence_text, (x, y+h+20), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            except Exception as e:
                self.log_message(f"Recognition error: {str(e)}")
                continue
        
        # Display the frame
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.camera_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
            self.camera_label.width(), self.camera_label.height(), Qt.KeepAspectRatio))
    
    def mark_attendance(self):
        if not self.within_college:
            QMessageBox.warning(self, "Warning", "You are not within college premises. Attendance not allowed.")
            return
        
        self.current_subject = self.subject_combo.currentText().strip()
        if not self.current_subject:
            QMessageBox.warning(self, "Warning", "Please select a subject")
            return
        
        ret, frame = self.cap.read()
        if not ret:
            self.log_message("Failed to capture frame for attendance")
            return
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        if len(faces) == 0:
            QMessageBox.warning(self, "Warning", "No face detected")
            return
        elif len(faces) > 1:
            QMessageBox.warning(self, "Warning", "Multiple faces detected. Please have only one student at a time.")
            return
        
        (x, y, w, h) = faces[0]
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (200, 200))
        
        try:
            if self.recognizer:
                label_id, confidence = self.recognizer.predict(roi_gray)
                student = None
                
                for s_id, s_label_id in self.label_ids.items():
                    if s_label_id == label_id and confidence < MIN_CONFIDENCE:
                        student = self.id_to_student.get(s_id)
                        break
                
                if student:
                    name = student['name']
                    student_id = student['id']
                    date_str = datetime.now().strftime("%Y-%m-%d")
                    time_str = datetime.now().strftime("%H:%M:%S")
                    
                    attendance_file = f"attendance_records/attendance_{date_str}_{self.current_subject}.csv"
                    
                    # Check if already marked
                    already_marked = False
                    if os.path.exists(attendance_file):
                        with open(attendance_file, 'r') as file:
                            reader = csv.reader(file)
                            for row in reader:
                                if row and row[0] == student_id:
                                    already_marked = True
                                    break
                    
                    if not already_marked:
                        with open(attendance_file, 'a', newline='') as file:
                            writer = csv.writer(file)
                            if os.stat(attendance_file).st_size == 0:
                                writer.writerow(['student_id', 'student_name', 'time', 'location'])
                            writer.writerow([student_id, name, time_str, str(self.current_location)])
                        
                        self.log_message(f"Attendance marked for {name} in {self.current_subject} at {time_str}")
                        QMessageBox.information(self, "Success", f"Attendance marked for {name}")
                    else:
                        self.log_message(f"Attendance already marked for {name} today in {self.current_subject}")
                        QMessageBox.information(self, "Info", f"Attendance already marked for {name}")
                else:
                    QMessageBox.warning(self, "Warning", "Student not recognized or confidence too low")
        except Exception as e:
            self.log_message(f"Error marking attendance: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to mark attendance: {str(e)}")
    
    def toggle_reg_camera(self):
        if self.reg_cap is None:
            self.start_reg_camera()
        else:
            self.stop_reg_camera()
    
    def start_reg_camera(self):
        self.reg_cap = cv2.VideoCapture(0)
        if not self.reg_cap.isOpened():
            QMessageBox.critical(self, "Error", "Could not open video device")
            return
        
        self.reg_start_btn.setText("Stop Camera")
        self.capture_btn.setEnabled(True)
        self.reg_timer = QTimer()
        self.reg_timer.timeout.connect(self.update_reg_frame)
        self.reg_timer.start(30)
    
    def stop_reg_camera(self):
        if self.reg_cap is not None:
            self.reg_timer.stop()
            self.reg_cap.release()
            self.reg_cap = None
            self.reg_camera_label.clear()
            self.reg_camera_label.setText("Camera off")
            self.reg_start_btn.setText("Start Camera")
            self.capture_btn.setEnabled(False)
    
    def update_reg_frame(self):
        ret, frame = self.reg_cap.read()
        if not ret:
            return
        
        self.current_reg_frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.reg_camera_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
            self.reg_camera_label.width(), self.reg_camera_label.height(), Qt.KeepAspectRatio))
    
    def capture_face(self):
        if not hasattr(self, 'current_reg_frame'):
            QMessageBox.warning(self, "Warning", "No frame captured")
            return
        
        gray = cv2.cvtColor(self.current_reg_frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 1:
            (x, y, w, h) = faces[0]
            self.captured_face = gray[y:y+h, x:x+w]
            
            # Show preview
            rgb_face = cv2.cvtColor(self.captured_face, cv2.COLOR_GRAY2RGB)
            h, w = rgb_face.shape[:2]
            bytes_per_line = 3 * w
            qt_image = QImage(rgb_face.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.reg_camera_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
                self.reg_camera_label.width(), self.reg_camera_label.height(), Qt.KeepAspectRatio))
            
            self.register_btn.setEnabled(True)
            QMessageBox.information(self, "Success", "Face captured successfully")
        else:
            QMessageBox.warning(self, "Warning", "Please make sure only one face is visible")
    
    def register_student(self):
        student_id = self.reg_id_input.text().strip()
        student_name = self.reg_name_input.text().strip()
        
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
            self.load_student_data()
            self.train_recognizer()
            self.reset_registration_form()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save data: {str(e)}")
    
    def reset_registration_form(self):
        self.reg_id_input.clear()
        self.reg_name_input.clear()
        self.register_btn.setEnabled(False)
        if hasattr(self, 'captured_face'):
            del self.captured_face
    
    def load_student_data(self):
        self.id_to_student = {}
        if not os.path.exists('registered_students.csv'):
            return
            
        try:
            with open('registered_students.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header
                for row in reader:
                    if len(row) >= 3:
                        self.id_to_student[row[0]] = {
                            'id': row[0],
                            'name': row[1],
                            'image_path': row[2]
                        }
        except Exception as e:
            self.log_message(f"Error loading student data: {str(e)}")
    
    def train_recognizer(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        faces = []
        labels = []
        self.label_ids = {}
        current_id = 0
        
        if not self.id_to_student:
            self.log_message("No student data available for training")
            return
        
        for student_id, student in self.id_to_student.items():
            img_path = student['image_path']
            if not os.path.exists(img_path):
                self.log_message(f"Image not found: {img_path}")
                continue
            
            try:
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    self.log_message(f"Failed to load image: {img_path}")
                    continue
                    
                img = cv2.resize(img, (200, 200))
                
                if student_id not in self.label_ids:
                    self.label_ids[student_id] = current_id
                    current_id += 1
                
                faces.append(img)
                labels.append(self.label_ids[student_id])
                self.log_message(f"Added training sample for {student['name']}")
                
            except Exception as e:
                self.log_message(f"Error processing {img_path}: {str(e)}")
                continue
        
        if faces:
            try:
                self.recognizer.train(faces, np.array(labels))
                self.log_message(f"Training complete with {len(faces)} samples")
            except Exception as e:
                self.log_message(f"Training failed: {str(e)}")
        else:
            self.log_message("No valid face images found for training")
    
    def check_location(self):
        self.location_label.setText("Location: Checking...")
        self.worker = LocationWorker()
        self.worker.location_found.connect(self.update_location_status)
        self.worker.start()
    
    def update_location_status(self, location):
        if location:
            self.current_location = location
            distance = geodesic(location, COLLEGE_LOCATION).km
            self.within_college = distance <= ALLOWED_DISTANCE_KM
            
            status = "Within college" if self.within_college else "Outside college"
            self.location_label.setText(
                f"Location: {location[0]:.4f}, {location[1]:.4f} | "
                f"Distance: {distance:.2f} km | Status: {status}"
            )
            
            if self.within_college:
                self.mark_btn.setEnabled(self.cap is not None)
            else:
                self.mark_btn.setEnabled(False)
        else:
            self.location_label.setText("Location: Unable to determine")
            self.within_college = False
            self.mark_btn.setEnabled(False)
    
    def populate_dates(self):
        self.date_combo.clear()
        dates = set()
        
        if os.path.exists('attendance_records'):
            for filename in os.listdir('attendance_records'):
                if filename.startswith('attendance_'):
                    parts = filename.split('_')
                    if len(parts) >= 3:
                        dates.add(parts[1])  # The date part
        
        self.date_combo.addItem("All")
        for date in sorted(dates, reverse=True):
            self.date_combo.addItem(date)
    
    def load_attendance_report(self):
        selected_date = self.date_combo.currentText()
        selected_subject = self.report_subject_combo.currentText()
        
        report_text = ""
        total_records = 0
        
        if os.path.exists('attendance_records'):
            for filename in os.listdir('attendance_records'):
                if filename.startswith('attendance_'):
                    parts = filename.split('_')
                    if len(parts) >= 3:
                        file_date = parts[1]
                        file_subject = parts[2].split('.')[0]
                        
                        # Check filters
                        if (selected_date == "All" or selected_date == file_date) and \
                           (selected_subject == "All" or selected_subject == file_subject):
                            with open(os.path.join('attendance_records', filename), 'r') as file:
                                reader = csv.reader(file)
                                header = next(reader, None)
                                
                                report_text += f"\n=== {file_date} - {file_subject} ===\n"
                                for row in reader:
                                    if len(row) >= 4:
                                        report_text += f"{row[1]} (ID: {row[0]}) at {row[2]}\n"
                                        total_records += 1
        
        if not report_text:
            report_text = "No attendance records found matching the criteria"
        else:
            report_text = f"Total records: {total_records}\n" + report_text
        
        self.report_text.setPlainText(report_text)
    
    def export_report(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report", "", "CSV Files (*.csv)")
        
        if file_path:
            try:
                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Date', 'Subject', 'Student ID', 'Student Name', 'Time', 'Location'])
                    
                    if os.path.exists('attendance_records'):
                        for filename in os.listdir('attendance_records'):
                            if filename.startswith('attendance_'):
                                parts = filename.split('_')
                                if len(parts) >= 3:
                                    file_date = parts[1]
                                    file_subject = parts[2].split('.')[0]
                                    
                                    with open(os.path.join('attendance_records', filename), 'r') as att_file:
                                        reader = csv.reader(att_file)
                                        next(reader, None)  # Skip header
                                        for row in reader:
                                            if len(row) >= 4:
                                                writer.writerow([file_date, file_subject, row[0], row[1], row[2], row[3]])
                
                QMessageBox.information(self, "Success", f"Report exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export report: {str(e)}")
    
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
    
    def closeEvent(self, event):
        if self.cap is not None:
            self.stop_camera()
        if hasattr(self, 'reg_cap') and self.reg_cap is not None:
            self.stop_reg_camera()
        event.accept()

class LocationWorker(QThread):
    location_found = pyqtSignal(tuple)
    
    def run(self):
        try:
            response = requests.get("https://ipinfo.io/json", timeout=5)
            data = response.json()
            loc = data.get("loc")
            if loc:
                lat, lng = loc.split(",")
                self.location_found.emit((float(lat), float(lng)))
                return
        except Exception:
            pass
        self.location_found.emit(None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application font
    font = app.font()
    font.setPointSize(10)
    app.setFont(font)
    
    window = AttendanceSystem()
    window.show()
    sys.exit(app.exec_())
