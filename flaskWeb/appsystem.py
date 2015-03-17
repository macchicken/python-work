from flask import request, session, g, redirect, url_for, \
    abort, render_template, flash
import flaskr
import logging
from datetime import datetime

logger=flaskr.app.logger

USERS = {}
USERS['admin']='123'
USERS['barry']='123'
USERS['cathy']='123'
USERS['ray']='123'


@flaskr.app.route('/helloWorld')
def helloWorld():
	return 'Hello World!'

@flaskr.app.route('/showEntries')
def show_entries():
	g.db=flaskr.connect_db()
	cur = g.db.execute('select title, text from entries order by id desc')
	entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)

@flaskr.app.route('/addEntry', methods=['POST'])
def add_entry():
	if not session.get('logged_in'): abort(401)
	print request.form['title']
	print request.form['text']
	g.db=flaskr.connect_db()
	g.db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

@flaskr.app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		logger.info("login start "+str(datetime.now()))
		if request.form['username'] not in USERS: error = 'Invalid username'
		elif request.form['password'] != USERS[request.form['username']]: error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			logger.info("login end " +str(datetime.now()))
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)

@flaskr.app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@flaskr.app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = None
	if request.method == 'POST':
		if request.form['username'] is None: error = 'username must not empty'
		elif request.form['password'] is None: error = 'password must not empty'
		elif request.form['username'] in USERS: error = 'user exists'
		else:
			USERS[request.form['username']]=request.form['password']
			flash('You were sign up, '+request.form['username'])
			return redirect(url_for('login'))
	return render_template('signup.html', error=error)



if __name__ == '__main__':
	DEBUG=flaskr.app.config['DEBUG']
	flaskr.app.run(host="127.0.0.1", port=20200,debug=DEBUG)