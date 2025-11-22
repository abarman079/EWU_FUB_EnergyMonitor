from flask import Flask, render_template, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
from datetime import datetime, timedelta
import pytz
import json
import simulate_data
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fub_bems_secret_key_2024'

# Bangladesh timezone
BD_TZ = pytz.timezone('Asia/Dhaka')

# Database initialization
def init_db():
    """Initialize SQLite database for energy data storage."""
    conn = sqlite3.connect('energy_bems.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS energy_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            power REAL NOT NULL,
            current REAL NOT NULL,
            voltage REAL NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS room_monitoring (
            room_id TEXT PRIMARY KEY,
            monitoring_enabled INTEGER DEFAULT 1
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Database initialized")

# Initialize monitoring state for all rooms
def init_monitoring_state():
    """Initialize monitoring state for all 44 rooms."""
    conn = sqlite3.connect('energy_bems.db')
    cursor = conn.cursor()
    
    # Get all room IDs from config
    with open('room_config.json', 'r') as f:
        rooms = json.load(f)
    
    for room_id in rooms.keys():
        cursor.execute('''
            INSERT OR IGNORE INTO room_monitoring (room_id, monitoring_enabled)
            VALUES (?, 1)
        ''', (room_id,))
    
    conn.commit()
    conn.close()
    
    total_rooms = len(rooms)
    print(f"✓ Initialized monitoring for {total_rooms} rooms (all ON)")

# Global monitoring state
monitoring_enabled = True

# Background data collection
def collect_energy_data():
    """Background task to collect and store energy data every 60 seconds."""
    try:
        current_time = datetime.now(BD_TZ)
        building_data = simulate_data.get_building_summary(current_time)
        
        conn = sqlite3.connect('energy_bems.db')
        cursor = conn.cursor()
        
        for room in building_data['rooms']:
            # Check if monitoring is enabled for this room
            cursor.execute('SELECT monitoring_enabled FROM room_monitoring WHERE room_id = ?', (room['room_id'],))
            result = cursor.fetchone()
            monitoring_on = result[0] if result else 1
            
            if monitoring_on:
                cursor.execute('''
                    INSERT INTO energy_data (room_id, timestamp, power, current, voltage, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    room['room_id'],
                    room['timestamp'],
                    room['power'],
                    room['current'],
                    room['voltage'],
                    room['status']
                ))
        
        conn.commit()
        conn.close()
        
        timestamp = current_time.strftime('%H:%M:%S')
        total_power = int(building_data['total_power'])
        print(f"✓ [{timestamp}] Recorded {len(building_data['rooms'])} rooms | Building: {total_power}W")
    
    except Exception as e:
        print(f"❌ Error collecting data: {e}")

# Routes
@app.route('/')
def dashboard():
    """Main dashboard page."""
    return render_template('building_dashboard_black.html')

@app.route('/room/<room_id>')
def room_detail(room_id):
    """Room detail page."""
    return render_template('room_detail_black.html', room_id=room_id)

# API Endpoints
@app.route('/api/building/status')
def building_status():
    """Get current status of all rooms in the building."""
    try:
        current_time = datetime.now(BD_TZ)
        building_data = simulate_data.get_building_summary(current_time)
        
        # Load room config to get equipment
        with open('room_config.json', 'r') as f:
            room_config = json.load(f)
        
        # Add monitoring state and equipment to each room
        conn = sqlite3.connect('energy_bems.db')
        cursor = conn.cursor()
        
        online_count = 0
        
        for room in building_data['rooms']:
            # Add monitoring state
            cursor.execute('SELECT monitoring_enabled FROM room_monitoring WHERE room_id = ?', (room['room_id'],))
            result = cursor.fetchone()
            monitoring_enabled = result[0] if result else 1
            room['monitoring_enabled'] = monitoring_enabled
            
            # Include equipment from config
            config = room_config.get(room['room_id'], {})
            room['equipment'] = config.get('equipment', [])
            
            # Count online rooms (only if monitoring is enabled)
            if monitoring_enabled and room['is_active']:
                online_count += 1
        
        conn.close()
        
        # Calculate daily energy and cost
        total_daily_kwh = 0
        for room in building_data['rooms']:
            daily_kwh = simulate_data.calculate_daily_energy(room['room_id'])
            total_daily_kwh += daily_kwh
        
        total_daily_cost = total_daily_kwh * 8.5
        co2_saved = simulate_data.calculate_co2_saved(total_daily_kwh)
        
        response = {
            'success': True,
            'timestamp': building_data['timestamp'],
            'total_power': building_data['total_power'],
            'active_rooms': online_count,
            'total_rooms': building_data['total_rooms'],
            'daily_energy': round(total_daily_kwh, 2),
            'daily_cost': round(total_daily_cost, 2),
            'co2_saved': co2_saved,
            'rooms': building_data['rooms']
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"❌ Error in building_status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/room/<room_id>/status')
def room_status(room_id):
    """Get current status of a specific room."""
    try:
        current_time = datetime.now(BD_TZ)
        room_data = simulate_data.get_room_data(room_id, current_time)
        
        if not room_data:
            return jsonify({'success': False, 'error': 'Room not found'}), 404
        
        # Calculate daily metrics
        daily_kwh = simulate_data.calculate_daily_energy(room_id)
        daily_cost = simulate_data.calculate_daily_cost(room_id)
        
        # Get schedule info
        schedule_info = simulate_data.get_room_schedule(room_id)
        
        response = {
            'success': True,
            'room_id': room_id,
            'power': room_data['power'],
            'current': room_data['current'],
            'voltage': room_data['voltage'],
            'status': room_data['status'],
            'is_active': room_data['is_active'],
            'course_code': schedule_info.get('course_code'),
            'course_name': schedule_info.get('course_name'),
            'equipment': room_data.get('equipment', []),
            'daily_energy': daily_kwh,
            'daily_cost': daily_cost,
            'timestamp': room_data['timestamp']
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"❌ Error in room_status for {room_id}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/room/<room_id>/history')
def room_history(room_id):
    """Get historical data for a room."""
    try:
        hours = int(request.args.get('hours', 24))
        
        conn = sqlite3.connect('energy_bems.db')
        cursor = conn.cursor()
        
        cutoff_time = datetime.now(BD_TZ) - timedelta(hours=hours)
        
        cursor.execute('''
            SELECT timestamp, power, current, voltage, status
            FROM energy_data
            WHERE room_id = ? AND timestamp >= ?
            ORDER BY timestamp DESC
            LIMIT 200
        ''', (room_id, cutoff_time.isoformat()))
        
        rows = cursor.fetchall()
        conn.close()
        
        data = []
        for row in rows:
            data.append({
                'timestamp': row[0],
                'power': row[1],
                'current': row[2],
                'voltage': row[3],
                'status': row[4]
            })
        
        return jsonify({'success': True, 'data': data})
    
    except Exception as e:
        print(f"❌ Error in room_history: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/monitoring/toggle', methods=['POST'])
def toggle_monitoring():
    """Toggle global monitoring on/off."""
    global monitoring_enabled
    monitoring_enabled = not monitoring_enabled
    
    return jsonify({
        'success': True,
        'monitoring_enabled': monitoring_enabled
    })

@app.route('/api/room/<room_id>/monitoring/toggle', methods=['POST'])
def toggle_room_monitoring(room_id):
    """Toggle monitoring for a specific room."""
    try:
        conn = sqlite3.connect('energy_bems.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT monitoring_enabled FROM room_monitoring WHERE room_id = ?', (room_id,))
        result = cursor.fetchone()
        
        if result:
            new_state = 0 if result[0] == 1 else 1
            cursor.execute('UPDATE room_monitoring SET monitoring_enabled = ? WHERE room_id = ?', (new_state, room_id))
        else:
            new_state = 0
            cursor.execute('INSERT INTO room_monitoring (room_id, monitoring_enabled) VALUES (?, ?)', (room_id, new_state))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'room_id': room_id,
            'monitoring_enabled': new_state == 1
        })
    
    except Exception as e:
        print(f"❌ Error toggling monitoring: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Startup
if __name__ == '__main__':
    print("=" * 60)
    print("🏢 FUB Building Energy Management System (BEMS)")
    print("=" * 60)
    
    # Initialize database
    init_db()
    init_monitoring_state()
    
    # Count rooms
    with open('room_config.json', 'r') as f:
        rooms = json.load(f)
    with open('schedules.json', 'r') as f:
        schedules = json.load(f)
    
    print(f"📊 Monitoring: {len(rooms)} classrooms")
    print(f"📅 Schedules loaded for: {len(schedules)} active classes")
    print(f"🔄 Background data collection: Every 60 seconds")
    print(f"🎛️  Individual room control: ON/OFF switches available")
    print(f"🎨 Theme: Black Terminal Professional")
    print(f"⚙️  Equipment display: Enabled")
    print("=" * 60)
    
    # Start background scheduler
    scheduler = BackgroundScheduler(timezone=BD_TZ)
    scheduler.add_job(collect_energy_data, 'interval', seconds=60)
    scheduler.start()
    
    # Collect initial data
    collect_energy_data()
    
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
