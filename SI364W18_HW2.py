## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
	album_name = StringField(label='Enter the name of an album: ', validators=[Required()])
	album_rating = RadioField(label='How much do you like this album? (1 = low, 3= high)', choices=[('1', 1),('2',2),('3',3)], validators=[Required()])
	submit = SubmitField(label='Submit')

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def artist_form():
	if request.method=='GET':
		artist=request.args.get('artist')
		return render_template('artistform.html',artist=artist)

@app.route('/artistinfo',methods=['GET'])
def artist_info():
	if request.method=='GET':
		artist=request.args.get('artist')
		lst_songs = []
		base_url = 'https://itunes.apple.com/search'
		params_diction = {}
		params_diction['term'] = artist
		resp = requests.get(base_url, params=params_diction)
		text=resp.text
		python_obj = json.loads(text)
		for item in python_obj['results']:
			lst_songs.append(item)
		return render_template('artist_info.html', objects=lst_songs)

@app.route('/artistlinks',methods=['GET'])
def artist_links():
		return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def specific_artist_name(artist_name):
	if request.method=='GET':
		base_url = 'https://itunes.apple.com/search'
		params_diction = {}
		params_diction['term'] = artist_name
		resp = requests.get(base_url, params=params_diction)
		text=resp.text
		python_obj = json.loads(text)
		results = python_obj['results']
		return render_template('specific_artist.html',results=results)

@app.route('/album_entry')
def showform():
	form_var = AlbumEntryForm()
	return render_template('album_entry.html',form=form_var)

@app.route('/album_result',methods = ['POST'])
def album_results():
	form = AlbumEntryForm()
	if form.validate_on_submit(): 
		album_name1 = form.album_name.data
		album_rating1 = form.album_rating.data
		return render_template('album_data.html', album_name=album_name1, album_rating=album_rating1)
	return "Sorry, no data available."

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
