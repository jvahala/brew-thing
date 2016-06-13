from flask import render_template
from app import app


@app.route('/')
@app.route('/mainpage')
def slpage():
    return render_template('mainpage.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
