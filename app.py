from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['task_tracker']
tasks_collection = db['tasks']

@app.route('/')
def index():
    tasks = list(tasks_collection.find({}))
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
    task = {'title': title, 'description': description, 'due_date': due_date}
    tasks_collection.insert_one(task)
    return redirect(url_for('index'))

@app.route('/complete_task/<task_id>')
def complete_task(task_id):
    tasks_collection.update_one({'_id': ObjectId(task_id)}, {'$set': {'completed': True}})
    return redirect(url_for('index'))

@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    tasks_collection.delete_one({'_id': ObjectId(task_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
