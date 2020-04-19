from flask_login import current_user
from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    if current_user.is_authenticated:
        if current_user.username != "Member":
            return render_template('404.html', om_admin="ja"), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if current_user.is_authenticated:
        if current_user.username != "Member":
            return render_template('500.html', om_admin="ja"), 500
    return render_template('500.html'), 500
