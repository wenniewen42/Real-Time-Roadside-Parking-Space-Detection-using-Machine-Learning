from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime

from models import db, User, ParkingStatus

from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['SECRET_KEY'] = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': 'Username or email already exists'}), 400

    new_user = User(
        username=username,
        email=email
    )
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/check_login', methods=['GET'])
def check_login():
    print('Checking login status')  
    if current_user.is_authenticated:
        print(f'User is authenticated: {current_user.username}')  
        return jsonify({
            'logged_in': True,
            'username': current_user.username
        })
    print('User is not authenticated')
    return jsonify({'logged_in': False})

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.get_json()
    spot = ParkingStatus.query.filter_by(id=data['id']).first()
    if spot:
        spot.available_spots = data['available_spots']
        spot.last_updated = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'Status updated successfully'}), 200
    else:
        new_spot = ParkingStatus(
            id=data['id'],
            road_name=data['road_name'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            available_spots=data['available_spots']
        )
        db.session.add(new_spot)
        db.session.commit()
        return jsonify({'message': 'New spot added successfully'}), 201

@app.route('/get_status', methods=['GET'])
def get_status():
    spots = ParkingStatus.query.all()
    return jsonify([{
        'id': spot.id,
        'road_name': spot.road_name,
        'latitude': spot.latitude,
        'longitude': spot.longitude,
        'available_spots': spot.available_spots,
        'last_updated': spot.last_updated.strftime('%Y-%m-%d %H:%M:%S')
    } for spot in spots])

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('templates', filename)

@app.route('/')
def home():
    return send_from_directory('templates', 'login.html')



#增加
# 使用字典來保存不同點位的車位狀態
parking_status = {}

@app.route('/update_parking_status', methods=['POST'])
def update_parking_status():
    data = request.json
    point_id = data.get("point_id")
    empty_spaces = data.get("empty_spaces")
    
    if point_id is None or empty_spaces is None:
        return jsonify({"error": "Invalid data"}), 400
    
    # 根據點位ID更新對應的車位數量
    parking_status[point_id] = empty_spaces
    
    return jsonify({"message": "Status updated", "data": parking_status}), 200

# 提供車位狀態查詢給前端
@app.route('/get_parking_status/<int:point_id>', methods=['GET'])
def get_parking_status(point_id):
    # 根據 point_id 查詢對應的車位狀態
    status = parking_status.get(point_id)
    if status is not None:
        return jsonify({"point_id": point_id, "available_spots": status}), 200
    else:
        return jsonify({"error": "Point ID not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
