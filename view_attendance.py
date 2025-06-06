import os
import csv
from datetime import datetime

def view_attendance():
    print("Available attendance records:")
    records = [f for f in os.listdir('attendance_records') if f.startswith('attendance_')]
    
    if not records:
        print("No attendance records found!")
        return
    
    for i, record in enumerate(records, 1):
        print(f"{i}. {record}")
    
    try:
        choice = int(input("Select record to view (number): "))
        selected_record = records[choice-1]
    except (ValueError, IndexError):
        print("Invalid selection!")
        return
    
    with open(f'attendance_records/{selected_record}', 'r') as file:
        reader = csv.reader(file)
        print("\nAttendance Record:")
        print("="*50)
        for row in reader:
            if row:  # Skip empty rows
                print(f"ID: {row[0]}, Name: {row[1]}, Time: {row[2]}, Location: {row[3]}")
        print("="*50)

if __name__ == "__main__":
    view_attendance()