from flask import Blueprint, render_template, request, redirect, url_for, session, json
from .models import Todo
import pandas as pd

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        task_content=request.form['content']
        new_task=Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Votre graphe ne fonctionne pas'    

    else:
        tasks= Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)
        
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Problème rencontré lors de la suppression de votre graphe'

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method=='POST':
        task.content=request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Problème rencontré lors de la mise à jour du graphe.'    
    else:
        return render_template('update.html',task=task)

