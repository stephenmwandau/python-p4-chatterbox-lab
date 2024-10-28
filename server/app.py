from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    """Fetch all messages."""
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages]), 200

@app.route('/messages', methods=['POST'])
def create_message():
    """Create a new message."""
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['GET'])
def get_message_by_id(id):
    """Fetch a message by its ID."""
    message = Message.query.get(id)
    if message:
        return jsonify(message.to_dict()), 200
    return jsonify({"error": "Message not found"}), 404

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    """Update a message."""
    data = request.get_json()
    message = Message.query.get(id)
    if not message:
        return jsonify({"error": "Message not found"}), 404
    message.body = data.get('body', message.body)
    db.session.commit()
    return jsonify(message.to_dict()), 200

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    """Delete a message."""
    message = Message.query.get(id)
    if not message:
        return jsonify({"error": "Message not found"}), 404
    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": "Message deleted"}), 200

if __name__ == '__main__':
    app.run(port=5555)
