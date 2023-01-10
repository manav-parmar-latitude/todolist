from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ma=Marshmallow(app)
db=SQLAlchemy(app)

app.app_context().push()
class TodoList(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    description=db.Column(db.String(300),nullable=False)
    task_completed=db.Column(db.Boolean,nullable=False,default=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return self.name

class TodoListSchema(ma.Schema):
    class Meta:
        fields=('name','description','task_completed','date_created')
todolist_schema=TodoListSchema(many=False)
todolists_schema=TodoListSchema(many=True)
@app.route('/add-todo/',methods = ['POST'])
def add_todolist():
    try:
        name=request.json['name']
        description=request.json['description']
        new_todo=TodoList(name=name,description=description)
        db.session.add(new_todo)
        db.session.commit()
        return todolist_schema.jsonify(new_todo)
    except Exception as e:
        return jsonify({"Error":"Invalid request"})

@app.route('/all-todolist/',methods = ['GET'])
def get_todolists():
    try:
        get_todolists=TodoList.query.all()
        return todolists_schema.jsonify(get_todolists)
    except Exception as e:
        return jsonify({"Error":"Invalid request"})        

@app.route('/todolist/<int:id>/',methods = ['GET'])
def get_todolist(id):
    try:
        get_todolist=TodoList.query.get(id)
        return todolist_schema.jsonify(get_todolist)
    except Exception as e:
        return jsonify({"Error":"Invalid request"})   

@app.route('/update-todolist/<int:id>/',methods = ['PUT'])
def update_todolist(id):
    try:
        update_todo=TodoList.query.get_or_404(int(id))
        update_todo.name=request.json['name']
        update_todo.description=request.json['description']
        update_todo.task_completed=request.json['task_completed']
        db.session.commit()
        return todolist_schema.jsonify(update_todo)
    except Exception as e:
        return jsonify({"Error":"Invalid request"}) 

@app.route('/delete-todolist/<int:id>/',methods = ['DELETE'])
def delete_todolist(id):
    try:
        delete_todolist=TodoList.query.get_or_404(int(id))
        db.session.delete(delete_todolist)
        db.session.commit()
        return jsonify({"Success":"Data has been deleted"})  
    except Exception as e:
        return jsonify({"Error":"Invalid request"})     
     

if __name__=="__main__":
    app.run(debug=True)