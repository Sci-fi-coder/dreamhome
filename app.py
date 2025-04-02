from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Function to establish database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "iiitdwd"),
        database=os.environ.get("DB_NAME", "DreamHome")
    )

# -----------------------------------
# CRUD Operations for Property Table
# -----------------------------------

# 1. GET all properties
@app.route('/properties', methods=['GET'])
def get_properties():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Property")
    properties = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(properties), 200

# 2. GET a specific property by ID
@app.route('/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Property WHERE property_id = %s", (property_id,))
    property_data = cursor.fetchone()
    cursor.close()
    db.close()
    if property_data:
        return jsonify(property_data), 200
    return jsonify({"error": "Property not found"}), 404

# 3. CREATE a new property
@app.route('/properties', methods=['POST'])
def create_property():
    db = get_db_connection()
    cursor = db.cursor()
    data = request.json
    cursor.execute(
        "INSERT INTO Property (address, type, rooms, rent, branch_id) VALUES (%s, %s, %s, %s, %s)",
        (data['address'], data['type'], data['rooms'], data['rent'], data['branch_id'])
    )
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Property added successfully"}), 201

# 4. UPDATE a property
@app.route('/properties/<int:property_id>', methods=['PUT'])
def update_property(property_id):
    db = get_db_connection()
    cursor = db.cursor()
    data = request.json
    cursor.execute(
        "UPDATE Property SET address = %s, type = %s, rooms = %s, rent = %s, branch_id = %s WHERE property_id = %s",
        (data['address'], data['type'], data['rooms'], data['rent'], data['branch_id'], property_id)
    )
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Property updated successfully"}), 200

# 5. DELETE a property
@app.route('/properties/<int:property_id>', methods=['DELETE'])
def delete_property(property_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Property WHERE property_id = %s", (property_id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Property deleted successfully"}), 200

# -----------------------------------
# Running the Flask app
# -----------------------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
