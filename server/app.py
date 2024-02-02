import os
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.configp['SQLALCHEMY_DATABASE_URI']= os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#postgres://flask_app_bgg0_user:1N1uqyqSwUrS9DkKxJ0kc2ef2qVOMnIx@dpg-cmu8m4uv3ddc738fpfl0-a.ohio-postgres.render.com/flask_app_bgg0
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    response_body= '''
    <h1>Chatterbox</h1>
    '''
    response= make_response(response_body, 200)
    return response

@app.route('/messages', method= ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        message_list= []
        messages= Message.query.all()
        if not messages:
            response= make_response("Message not found", 404)
            return response
        else:
            for m in messages:
                message_dict= m.to_dict()
                message_list.append(message_dict)
            response= make_response(message_list, 200)
            return response
    elif request.method== 'POST':
        new_message= Message(
            body=request.form['body'],
            username=request.form['username']
        )
        db.session.add(new_message)
        db.session.commit()

        review_dict= new_message.to_dict()
        response= make_response(review_dict, 201)
        return response



@app.route('/messages/<int:id>', method= ['PATCH', 'DELETE'])
def messages_by_id(id):
    message= Message.query.filter_by(id=id).first()
    if not message:
        response= make_response('Message does not exist', 404)
        return response
    if request.method =='PATCH':
        # update the existing message with new data
        for attr in request.form:
            setattr(message,attr, request.form.get(attr))
        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()
        response= make_response(message_dict ,200)
        return response
    
    elif request.method=='DELETE':
        db.session.delete(message)
        db.session.commit()
        response= make_response("Successfully deleted", 204)
        return response

if __name__ == '__main__':
    app.run(port=5555)
