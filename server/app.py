from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import asc

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages = Message.query.order_by(asc(Message.created_at)).all()

    if request.method == 'GET':
        response_body = [message.to_dict() for message in messages]

        response = make_response(response_body, 200)

        return response
    
    elif request.method == 'POST':
        json_data = request.get_json()

        message = Message(
            username=json_data['username'],
            body=json_data['body']
        )

        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(message_dict, 200)

        return response


@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if request.method == 'PATCH':
        json_data = request.get_json()

        for attribute in json_data:
            setattr(message, attribute, json_data[attribute])

        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(message_dict, 200)

        return response
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_success": True,
            "message": "Message deleted successfully."
        }

        response = make_response(response_body, 200)

        return response

if __name__ == '__main__':  
    app.run(port=5555)
