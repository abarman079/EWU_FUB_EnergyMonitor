import random
import json
from datetime import datetime
import pytz

# Load configurations
try:
    with open('room_config.json', 'r') as f:
        ROOM_CONFIG = json.load(f)
except:
    ROOM_CONFIG = {}

try:
    with open('schedules.json', 'r') as f:
        SCHEDULES = json.load(f)
except:
    SCHEDULES = {}

# Bangladesh timezone
BD_TZ = pytz.timezone('Asia/Dhaka')

# Offline room configuration (8-9 rooms offline)
OFFLINE_ROOMS = ['203', '304', '402', '507', '604', '702', '803', '905', '1002']

def get_current_time():
    """Get current time in Bangladesh timezone."""
    return datetime.now(BD_TZ)

def is_class_time(room_id, current_time=None):
    """Check if there's a class scheduled in a room at the current time."""
    if current_time is None:
        current_time = get_current_time()
    
    current_day = current_time.strftime('%A')
    current_hour = current_time.hour
    current_minute = current_time.minute
    current_time_minutes = current_hour * 60 + current_minute
    
    schedule = SCHEDULES.get(room_id, {})
    day_schedule = schedule.get('schedule', [])
    
    for slot in day_schedule:
        if slot['day'] == current_day:
            start_parts = slot['start'].split(':')
            end_parts = slot['end'].split(':')
            
            start_minutes = int(start_parts[0]) * 60 + int(start_parts[1])
            end_minutes = int(end_parts[0]) * 60 + int(end_parts[1])
            
            if start_minutes <= current_time_minutes <= end_minutes:
                return True, slot
    
    return False, None

def get_room_data(room_id, current_time=None):
    """Get real-time power consumption data for a specific room."""
    if current_time is None:
        current_time = get_current_time()
    
    room_info = ROOM_CONFIG.get(room_id, {'wattage': 3000, 'equipment': []})
    base_wattage = room_info.get('wattage', 3000)
    equipment = room_info.get('equipment', [])
    
    # Check if room is offline
    if room_id in OFFLINE_ROOMS:
        power = random.uniform(10, 30)
        current_val = power / 240.0
        return {
            'room_id': room_id,
            'power': round(power, 2),
            'current': round(current_val, 3),
            'voltage': 240.0,
            'status': 'OFFLINE',
            'is_active': False,
            'course_code': None,
            'course_name': None,
            'equipment': equipment,
            'timestamp': current_time.isoformat()
        }
    
    # Check if class is in session
    is_active, class_info = is_class_time(room_id, current_time)
    
    if is_active:
        schedule = SCHEDULES.get(room_id, {})
        course_code = schedule.get('course_code', 'N/A')
        course_name = schedule.get('course_name', 'Unknown')
        
        # Active room: full equipment running
        variation = random.uniform(0.85, 1.15)
        power = base_wattage * variation
        status = 'ONLINE'
    else:
        # No class: standby power
        power = random.uniform(50, 150)
        schedule = SCHEDULES.get(room_id, {})
        course_code = schedule.get('course_code')
        course_name = schedule.get('course_name')
        status = 'STANDBY'
    
    current_val = power / 240.0
    
    return {
        'room_id': room_id,
        'power': round(power, 2),
        'current': round(current_val, 3),
        'voltage': 240.0,
        'status': status,
        'is_active': is_active,
        'course_code': course_code,
        'course_name': course_name,
        'equipment': equipment,
        'timestamp': current_time.isoformat()
    }

def get_building_summary(current_time=None):
    """Get summary data for all 44 rooms in the building."""
    if current_time is None:
        current_time = get_current_time()
    
    rooms_data = []
    total_power = 0
    active_count = 0
    
    for room_id in ROOM_CONFIG.keys():
        room_data = get_room_data(room_id, current_time)
        rooms_data.append(room_data)
        total_power += room_data['power']
        if room_data['is_active']:
            active_count += 1
    
    return {
        'timestamp': current_time.isoformat(),
        'total_power': round(total_power, 2),
        'active_rooms': active_count,
        'total_rooms': len(ROOM_CONFIG),
        'rooms': rooms_data
    }

def calculate_daily_energy(room_id):
    """Calculate estimated daily energy consumption for a room in kWh."""
    room_info = ROOM_CONFIG.get(room_id, {'wattage': 3000})
    base_wattage = room_info.get('wattage', 3000)
    
    # Get schedule for the room
    schedule = SCHEDULES.get(room_id, {})
    day_schedules = schedule.get('schedule', [])
    
    # Calculate active hours per week
    total_hours = 0
    for slot in day_schedules:
        try:
            start_parts = slot['start'].split(':')
            end_parts = slot['end'].split(':')
            start_minutes = int(start_parts[0]) * 60 + int(start_parts[1])
            end_minutes = int(end_parts[0]) * 60 + int(end_parts[1])
            hours = (end_minutes - start_minutes) / 60.0
            total_hours += hours
        except:
            continue
    
    # Average daily hours (weekly hours / 7)
    daily_hours = total_hours / 7.0 if total_hours > 0 else 8.0
    
    # Daily energy = (base_wattage * active_hours + standby_wattage * standby_hours) / 1000
    standby_hours = 24 - daily_hours
    standby_wattage = 100
    
    daily_kwh = (base_wattage * daily_hours + standby_wattage * standby_hours) / 1000.0
    
    return round(daily_kwh, 3)

def calculate_daily_cost(room_id):
    """Calculate estimated daily cost in BDT (1 kWh = 8.5 BDT)."""
    daily_kwh = calculate_daily_energy(room_id)
    cost = daily_kwh * 8.5
    return round(cost, 2)

def calculate_co2_saved(kwh):
    """Calculate CO2 emissions in kg (1 kWh = 0.85 kg CO2)."""
    co2 = kwh * 0.85
    return round(co2, 2)

def get_room_schedule(room_id):
    """Get the weekly schedule for a room."""
    return SCHEDULES.get(room_id, {
        'course_code': None,
        'course_name': None,
        'schedule': []
    })

def get_room_config(room_id):
    """Get the equipment configuration for a room."""
    return ROOM_CONFIG.get(room_id, {})

# Update offline rooms dynamically
def update_offline_rooms():
    """Randomly update which rooms are offline (8-9 rooms)."""
    global OFFLINE_ROOMS
    if ROOM_CONFIG:
        all_rooms = list(ROOM_CONFIG.keys())
        num_offline = random.randint(8, 9)
        OFFLINE_ROOMS = random.sample(all_rooms, min(num_offline, len(all_rooms)))
        print(f"🔄 Updated offline rooms: {OFFLINE_ROOMS}")

# Initialize offline rooms on startup
if ROOM_CONFIG:
    update_offline_rooms()
