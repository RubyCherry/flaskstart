import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp_auth = Blueprint('auth', __name__, url_prefix='/auth',template_folder="templates")

@bp_auth.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Пользователь {username} уже зарегистрирован."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
    return render_template('/auth/register.html')

@bp_auth.route('/login', methods=('GET', 'POST'))
def login():
    return render_template('/auth/login.html')