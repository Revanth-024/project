from flask import Blueprint, render_template
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)


@views.route('/music')
@login_required
def music():
    return render_template("music.html")
    
@views.route('/chatbot')
@login_required
def chatbot():
    return render_template("chatbot.html")
    
@views.route('/tools')
@login_required
def tools():
    return render_template("tools.html")

@views.route('/todolist', methods=['GET', 'POST'])
@login_required
def todolist():
    if request.method == 'POST':
        data = request.form.get('data')
        if data:
            new_note = Note(data=data, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('views.todolist'))

    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("todolist.html", notes=notes)

@views.route('/delete_note/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    return redirect(url_for('views.todolist'))

@views.route('/calculator')
@login_required
def calculator():
    return render_template("calculator.html")

@views.route('/pomodoro')
@login_required
def pomodoro():
    return render_template("pomodoro.html")

@views.route('/code-editor')
@login_required
def code_editor():
    return render_template("code_editor.html")

import requests

@views.route('/dictionary', methods=['GET', 'POST'])
@login_required
def dictionary():
    definition = None
    word = None

    if request.method == 'POST':
        word = request.form.get('word')
        api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            definition = data[0]['meanings'][0]['definitions'][0]['definition']
        else:
            definition = "Sorry, no definition found."

    return render_template("dictionary.html", word=word, definition=definition)
@views.route('/tictactoe')
@login_required
def tictactoe():
    return render_template("tictactoe.html")
