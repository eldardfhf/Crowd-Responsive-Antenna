import time
import os
import csv

def log_rotation(angle, direction):
    """Log rotation events"""
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    log_file = os.path.join(logs_dir, "rotation_log.csv")
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_data = {
        "timestamp": timestamp,
        "angle": angle,
        "direction": direction
    }
    
    file_exists = os.path.isfile(log_file)
    with open(log_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=log_data.keys())
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(log_data)
    
    print(f"Logged rotation to {log_file}")