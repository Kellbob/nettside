from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request
from app.forms import RegistrationForm, LoginForm, DeleteForm, ChangeRoleForm, MakePostForm
from werkzeug.urls import url_parse
from app.models import User, Post
from app import app, db

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/')
@app.route('/index')
@login_required
def index():
    if current_user.role != "Member":
        return render_template('index.html', om_admin='ja', title='Home', Post=Post())
    else:
        return render_template('index.html', title='Home', Post=Post())

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role="Member")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin_settings')
@login_required
def admin_settings():
    users = User.query.all()
    if current_user.role != "Member":
        return render_template('admin_settings.html', title='Admin settings', om_admin='ja', users=users)
    return redirect(url_for('index'))

@app.route('/slutt')
@login_required
def slutt():
    if current_user.role != "Member":
        shutdown_server()
        return render_template('slutt.html', om_admin='ja')
    return redirect(url_for('index'))

@app.route('/user/<username>', methods=['GET','POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.role != "Member":
        form = DeleteForm()
        form2 = ChangeRoleForm()
        form3 = MakePostForm()
        if form.submit.data and form.validate():
            if form.confirm.data == "Confirm":
                db.session.delete(user)
                db.session.commit()
        if form2.submit2.data and form2.validate():
            if form2.confirm2_1.data == "Confirm":
                print(form2.radio_buttons.data)
                user.role = form2.radio_buttons.data
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('admin_settings'))
        if form3.submit3.data and form3.validate():
            p = Post(body = form3.body.data, author=user)
            db.session.add(p)
            db.session.commit()
        return render_template('user.html', title=user.username, user=user, om_admin='ja', form=form, form2=form2, form3=form3)
    return redirect(url_for('admin_settings'))
