from flask import Flask, request, jsonify, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
DB_FILE = 'users.txt'

# Load users from the text file
def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

# Save users to the text file
def save_users(users):
    with open(DB_FILE, 'w') as f:
        json.dump(users, f)

# User Registration
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    email = data.get('email')
    age = data.get('age')

    if not email or not age:
        return jsonify({"error": "Email and age are required"}), 400

    users = load_users()
    if email in users:
        return jsonify({"error": "User already exists"}), 400

    users[email] = {'age': int(age)}
    save_users(users)
    return jsonify({"message": "User added successfully"}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    users = load_users()
    if email not in users:
        return jsonify({"error": "User not found. Please register first."}), 404

    session['user_email'] = email
    return jsonify({"message": f"Logged in as {email}"}), 200

# Retrieve User Profile
@app.route('/user', methods=['GET'])
def get_user():
    email = session.get('user_email')
    if not email:
        return jsonify({"error": "User unauthorized"}), 401

    users = load_users()
    user_data = users.get(email)
    if not user_data:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(user_data), 200

# Update User Profile
@app.route('/user', methods=['PUT'])
def update_user():
    email = session.get('user_email')
    
    # Check if the user is authenticated
    if not email:
        return jsonify({"error": "User unauthorized"}), 401

    data = request.json
    age = data.get('age')

    users = load_users()
    if email not in users:
        return jsonify({"error": "User not found"}), 404

    if age is not None:
        users[email]['age'] = int(age)
    save_users(users)
    return jsonify({"message": "User updated successfully"}), 200

# Delete User Profile
@app.route('/user', methods=['DELETE'])
def delete_user():
    email = session.get('user_email')
    
    # Check if the user is authenticated
    if not email:
        return jsonify({"error": "User Denied"}), 401

    users = load_users()
    if email not in users:
        return jsonify({"error": "User not found"}), 404

    del users[email]
    save_users(users)
    session.pop('user_email', None)  # Log out the user
    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
