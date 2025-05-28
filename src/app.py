import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# IMPORTANT: The route for POST was '/member', but the tests are calling '/members'.
# Let's change the route to '/members' to match the test suite.
@app.route('/members', methods=['POST']) # Changed from '/member' to '/members'
def add_member():
    member_data = request.get_json()
    if not member_data:
        return jsonify({"error": "Bad request, request body must be JSON"}), 400
    
    # Asegurarse de que los campos requeridos estén presentes
    required_fields = ["first_name", "age", "lucky_numbers"]
    if not all(field in member_data for field in required_fields):
        return jsonify({"error": "Missing required fields. Required: first_name, age, lucky_numbers"}), 400
    
    # Asegurarse de que 'lucky_numbers' sea una lista
    if not isinstance(member_data["lucky_numbers"], list):
        return jsonify({"error": "lucky_numbers must be a list"}), 400

    new_member = jackson_family.add_member(member_data)
    # Devuelve el miembro añadido con su ID y otros datos
    return jsonify(new_member), 200

# IMPORTANT: The routes for GET and DELETE by ID were '/member/<int:member_id>',
# but the tests are calling '/members/<int:id>'.
# Let's change these routes to '/members/<int:member_id>' to match the test suite.
@app.route('/members/<int:member_id>', methods=['GET']) # Changed from '/member' to '/members'
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404

@app.route('/members/<int:member_id>', methods=['DELETE']) # Changed from '/member' to '/members'
def delete_member(member_id):
    result = jackson_family.delete_member(member_id)
    if result["done"]:
        return jsonify(result), 200
    return jsonify({"error": "Member not found"}), 404

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)