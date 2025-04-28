from datetime import datetime, timedelta
import pytz  # Ensure you have this package installed


# Define your time slots
time_slots = {
    'default': [
        ("10:00 AM", "11:30 AM"),
        ("11:30 AM", "1:00 PM"),
        ("1:00 PM", "2:30 PM"),
        ("2:30 PM", "4:00 PM"),
        ("4:00 PM", "5:30 PM"),
        ("5:30 PM", "7:00 PM"),
        ("7:00 PM", "8:30 PM"),
        ("8:30 PM", "10:00 PM"),
        ("11:00 PM", "1:00 AM"),
    ],
    'friday': [
        ("10:00 AM", "11:30 AM"),
        ("12:00 PM", "1:00 PM"),
        ("4:00 PM", "5:30 PM"),
        ("5:30 PM", "7:00 PM"),
        ("7:00 PM", "8:30 PM"),
        ("8:30 PM", "10:00 PM"),
    ],
}

# Set Qatar timezone
qatar_tz = pytz.timezone("Asia/Qatar")

def get_today_time_slots():
    today = datetime.now(qatar_tz)  # Use Qatar timezone
    day_name = today.strftime('%A').lower()
    time_slots_for_today = time_slots['friday'] if day_name == 'friday' else time_slots['default']
    
    current_time = today.time()  # Current time as a time object
    
    future_slots_today = []
    for start, end in time_slots_for_today:
        # Convert start time to a time object for comparison
        start_time_obj = datetime.strptime(start, "%I:%M %p").time()
        
        if start_time_obj >= current_time:
            future_slots_today.append(f"{start} - {end}")
     

    return future_slots_today, today.strftime("%Y-%m-%d")

def get_tomorrow_time_slots():
    tomorrow = datetime.now(qatar_tz) + timedelta(days=1)
    day_name = tomorrow.strftime('%A').lower()
    time_slots_for_tomorrow = time_slots['friday'] if day_name == 'friday' else time_slots['default']

    data  = datetime.now(qatar_tz) + timedelta(days=1)
    return [f"{start} - {end}" for start, end in time_slots_for_tomorrow],data.strftime("%Y-%m-%d")