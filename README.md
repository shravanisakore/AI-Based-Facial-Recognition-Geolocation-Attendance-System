# 📸 AI-Based Facial Recognition & Geolocation Attendance System

An intelligent attendance system that combines **facial recognition** and **IP-based geolocation tracking** to ensure secure and verified attendance marking. Built using **Streamlit** for a user-friendly web interface, **OpenCV** for facial detection, and **IPinfo API** for geolocation.

---

## 🔧 Tech Stack

| Requirement           | Solution                              | Advantage                            |
|-----------------------|-------------------------------------|------------------------------------|
| Real-Time Face Detection | OpenCV + Haar Cascade                | Fast & lightweight                 |
| Face Recognition      | LBPH (Local Binary Pattern Histogram) | Works offline, no cloud dependency  |
| Location Tracking     | IPinfo API + Haversine Formula       | No GPS needed, works on any device |
| User Interface        | Streamlit                           | Rapid development, clean UI        |
| Data Storage          | CSV files                         | Simple, no complex DB setup         |
| Scalability (Future)  | SQLite / MySQL                    | Handles large student databases     |
| Deployment (Future)   | PyInstaller                      | Easy cross-device distribution      |

---

## 🎯 Features

- 📷 **Face Registration:** Users can register their faces via image upload.
- 🧠 **Model Training:** Face data is trained using the Haar Cascade + LBPH algorithm.
- 🔐 **Secure Attendance:** Attendance is marked only if the face is recognized and location is verified.
- 🌐 **IP-Based Location:** Location fetched using IPinfo API and verified via the Haversine formula.
- 📊 **Data Storage:** All data is stored in simple CSV files for easy access and portability.

---
