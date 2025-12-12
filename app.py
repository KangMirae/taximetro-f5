"""
Flask application entry point.

Provides:
- Web UI routes
- REST API endpoints for taximeter control
"""

from flask import Flask, render_template, jsonify, request
from src.config import setup_logging, load_rates
from src.taximeter import Taximeter
from src.storage import HistoryManager

setup_logging()
rates = load_rates()

app = Flask(__name__)

# Application-wide instances
taxi = Taximeter(rates)
history_mgr = HistoryManager()
current_customer = "Guest"

@app.route('/')
def index():
    return render_template('index.html')

# --- API endpoints ---

@app.route('/api/start', methods=['POST'])
def start():
    """trip start"""
    global current_customer
    data = request.json
    current_customer = data.get('name', 'Guest')
    level = data.get('level', 1)
    
    taxi.start_journey(level=level)
    return jsonify({"status": "started"})

@app.route('/api/toggle_state', methods=['POST'])
def toggle_state():
    """when click STOP/MOVE button"""
    taxi.change_state()
    return jsonify({"status": "ok", "new_state": taxi.current_state})

@app.route('/api/toggle_option', methods=['POST'])
def toggle_option():
    """when click surcharge option"""
    data = request.json
    option = data.get('option') # 'out-of-city' or 'night'
    is_active = data.get('active')
    
    taxi.toggle_option(option, is_active)
    return jsonify({"status": "ok"})

@app.route('/api/update')
def update():
    """0.1초마다 호출됨: 화면 데이터 갱신"""
    return jsonify(taxi.get_live_data())

@app.route('/api/stop', methods=['POST'])
def stop():
    """도착(여정 종료)"""
    final_fare = taxi.stop_journey()
    
    # save trip history (trip_history.json)
    history_mgr.save_trip(current_customer, final_fare)
    
    return jsonify({"fare": final_fare})

@app.route('/api/history')
def history():
    """get history list"""
    data = history_mgr.get_all_trips()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)