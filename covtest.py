from flask import Flask, got_request_exception, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import json

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)




class CovUserModel(db.Model):
    __tablename__ = 'usert'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pinCode = db.Column(db.String(6), nullable=False)
    phoneNumber = db.Column(db.String(13), nullable=False)
    result = db.Column(db.String(10), nullable=False)
    covu = relationship("AssessModel", back_populates="users")
    def __repr__(self):
        return f"Uzers(id = {id})"

class AssessModel(db.Model):
    __tablename__ = 'assesst'
    id = db.Column(db.Integer, primary_key=True)
    assessid = Column(Integer, ForeignKey('usert.id'))
    symptoms = db.Column(db.String(100), nullable=False)
    travelHistory = db.Column(db.String(5), nullable=False)
    contactWithCovidPatient = db.Column(db.String(5), nullable=False) 
    users = relationship("CovUserModel", back_populates="covu")
class AdminModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pinCode = db.Column(db.String(6), nullable=False)
    phoneNumber = db.Column(db.String(13), nullable=False)
    role = db.Column(db.String(13), nullable=False)
    def __repr__(self):
        return f"Admins(id = {id})"
    # name = db.Column(db.String(100), nullable=False)
    # options = db.Column(db.String(200), nullable=False)
    # correct_option = db.Column(db.Integer, nullable=False)
    # quiz = Column(Integer, ForeignKey('quizt.id'))
    # points = db.Column(db.Integer, nullable=False)
    # quizs = relationship("QuizModel", back_populates="question")

    # def __repr__(self):
        # return f"Question(name = {name}, options = {options}, correct_option = {correct_option}, \
            # quiz = {quiz}, points = {points})"

db.create_all()

user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, help="Missing 'name'", required=True)
user_args.add_argument("pinCode", type=str, help="Missing 'pinCode'", required=True)
user_args.add_argument("result", type=str, help="Missing 'result'", required=False)
user_args.add_argument("phoneNumber", type=str, help="Missing 'phoneNumber'", required=True)

admin_args = reqparse.RequestParser()
admin_args.add_argument("name", type=str, help="Missing 'name'", required=True)
admin_args.add_argument("pinCode", type=str, help="Missing 'pinCode'", required=True)
admin_args.add_argument("phoneNumber", type=str, help="Missing 'phoneNumber'", required=True)

assess_args = reqparse.RequestParser()
assess_args.add_argument("symptoms", type=str, help="Missing 'symptoms'", required=True)
assess_args.add_argument("travelHistory", type=str, help="Missing 'travelHistory'", required=True)
assess_args.add_argument("contactWithCovidPatient", type=str, help="Missing 'contactWithCovidPatient'", required=True)

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'pinCode': fields.String,
    'result': fields.String,
    'phoneNumber': fields.String
}
    
admin_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'pinCode': fields.String,
    'role': fields.String,
    'phoneNumber': fields.String
}
    
assess_fields = {
    'assessid': fields.Integer,
    'symptoms': fields.String,
    'travelHistory': fields.String,
    'contactWithCovidPatient':fields.String
}

# @marshal_with(quiz_fields)
# def return_quiz(result):
    # return result
class Uzers(Resource):
    def post(self):
        args_tup = ("name", "pinCode", "phoneNumber")
        data = request.json
        for arg in args_tup:
            if arg not in data:
                return {"status": "failure","reason": "missing args"},400
        args = user_args.parse_args()
        result = CovUserModel.query.all()
        user_id = len(result)+1
        ruser = CovUserModel(id=user_id, name=args['name'], phoneNumber=args['phoneNumber'], pinCode=args['pinCode'], result="negative")
        db.session.add(ruser)
        db.session.commit()
        return {"userId":str(user_id)}, 201









api.add_resource(Uzers, "/api/covuser")
# api.add_resource(CovAssess, "/api/covassess")
# api.add_resource(CovAdmin, "/api/covadmin/<int:admin_id>", "/api/questions/")
# api.add_resource(GetAllQ, "/api/quiz-questions/<int:quiz_id>")
# api.add_resource(Homes, "/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)