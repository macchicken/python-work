import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
import flaskr



@flaskr.app.route('/helloWorld')
def helloWorld():
	print g.db
	return 'Hello World!'

@flaskr.app.route('/showEntries')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@flaskr.app.route('/addEntry', methods=['POST'])
def add_entry():
	if not session.get('logged_in'): abort(401)
	print request.form['title']
	print request.form['text']
	g.db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

@flaskr.app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != flaskr.app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != flaskr.app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@flaskr.app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))



if __name__ == '__main__':
	flaskr.app.run(host="127.0.0.1", port=20000,debug=flaskr.DEBUG)