from flask import render_template, url_for, request, redirect, session
from app import app
import os

@app.route('/')
@app.route('/index')
def index():

	#print all session variables:
	for key in session.keys():
		print(key, session[key])

	from datetime import datetime
	the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

	return render_template(
		"index.html",
		title="home",
		time=the_time,
	)

@app.route('/analyze')
def analyze():

	import spotipy
	import spotipy.util as util

	scope = 'user-top-read'

	print("Analyzing spotify data for " + session['current_user']['username'])

	sp = spotipy.Spotify(auth=session['current_user']['token'])

	#get top 10 artists short, medium, and long term
	top_artists = {" ".join(term.split("_")): [item['name'] for item in sp.current_user_top_artists(limit=10, offset=0, time_range=term)['items']] for term in ["short_term", "medium_term", "long_term"]}

	return render_template(
		"analyze.html",
		title="analyze",
		username=session['current_user']['username'],
		top_artists=top_artists
	)

@app.route('/login')
def login():

	return render_template(
		"login.html",
		title="login"
	)
	


@app.route('/login', methods=['POST']) 
def login_post():

	import spotipy
	import spotipy.util as util

	#clear session
	session.clear() 

	scope = 'user-top-read'

	username = request.form['text']

	token = util.prompt_for_user_token(username,scope)
	print("logged in!")
	#sp = spotipy.Spotify(auth=token)

	#create a user:
	user = {
		"username": username,
		"token": token
	}

	#store token as session variable:
	print("users:", session.get('users'))

	#check if there are not any users:
	if session.get('users') is not None:
		session['users'][username] = token
		print("There are users")
	else:
		session['users'] = {}
		session['users'][username] = token

	#set current user:
	session['current_user'] = user

	print("users:", session.get('users'))

	return redirect(url_for('index'))


#Need the following two functions to properly update CSS
@app.context_processor
def override_url_for():
	return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
	if endpoint == 'static':
		filename = values.get('filename', None)
		if filename:
			file_path = os.path.join(app.root_path,
									 endpoint, filename)
			values['q'] = int(os.stat(file_path).st_mtime)
	return url_for(endpoint, **values)
