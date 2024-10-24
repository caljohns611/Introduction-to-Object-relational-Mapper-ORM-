# task 1

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:your_password@127.0.0.1/gym_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    name = fields.String(required=True)
    age = fields.String(required=True)

    class Meta:
        fields = ("name", "age")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)


class WorkoutSessions(ma.Schema):
    date = fields.String(required=True)
    member_id = fields.String(required=True)
    duration_minutes = fields.String(required=True)
    calories_burned = fields.String(required=True)

    class Meta:
        fields = ("date", "member_id", "duration_minutes", "calories_burned")

workout_schema = WorkoutSessions()
workouts_schema = WorkoutSessions(many=True)


class Member(db.Model):
    __tablename__ = 'Members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.String)

class WorkoutSessions(db.Model):
    __tablename__ = 'Workout_sessions'
    id = db.Column(db.Integer, primary=True)
    date = db.Column(db.String)
    member_id = db.Column(db.String)
    duration_minutes = db.Column(db.String)
    calories_burned = db.Column(db.String)


# task 2

@app.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return members_schema.jsonify(members)


@app.route('/members', methods=['POST'])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_member = Member(name=member_data['name'], age = member_data['age'])

    db.session.add(new_member)
    db.session.commit()
    return jsonify({"message": "New customer added successfully"}), 201


@app.route('/member/<int:id', method=['PUT'])
def update_member(id):
    member = Member.query.get_or_404(id)
    try:
        member_data = member_schema.load(request.json)
    except ValueError as err:
        return jsonify(err.messages), 400

    member.name = member_data['name']
    member.age = member_data['age']
    db.session.commit()
    return jsonify({"message": "Member details updated successfully"}), 200


@app.route('/member/<int:id', method=['DELETE'])
def delete_member(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": "Member removed successfully"}), 200


# task 3


@app.route('/workout_sessions', methods=['POST'])
def add_workoutsession():
    try:
        workout_data = workout_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_workout = WorkoutSessions(date = workout_data['date'], member_id = workout_data['member_id'], duration_minutes = workout_data['duration_minutes'], calories_burned = workout_data['calories_burned'])

    db.session.add(new_workout)
    db.session.commit()
    return jsonify({"message": "New workout session added successfully"}), 201


@app.route('/workoutsessions/<int:id', method=['PUT'])
def update_workout(id):
    workout_session = WorkoutSessions.query.get_or_404(id)
    try:
        workout_data = workout_schema.load(request.json)
    except ValueError as err:
        return jsonify(err.messages), 400

    workout_session.date = workout_data['date']
    workout_session.member_id = workout_data['member_id']
    workout_session.duration_minutes = workout_data['duration_minutes']
    workout_session.calories_burned = workout_data['calories_burned']
    db.session.commit()
    return jsonify({"message": "workout session details updated successfully"}), 200


@app.route('/workoutsessions', methods=['GET'])
def get_workouts():
    workouts = WorkoutSessions.query.all()
    return workouts_schema.jsonify(workouts)




with app.app_context():
    db.create_all()

if __name__=='__main__':
    app.run(debug=True)