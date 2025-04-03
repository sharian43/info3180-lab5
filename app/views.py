"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
from . import db
from .models import Movie
from .forms import MovieForm
from flask_wtf.csrf import generate_csrf 


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/csrf-token', methods=['GET']) 
def get_csrf(): 
    return jsonify({'csrf_token': generate_csrf()}) 
###
# The functions below should be applicable to all Flask apps.
###
@app.route('/api/v1/movies', methods=['POST'])
def movies():
    form = MovieForm()
    if form.validate_on_submit():
        title = request.form['title']
        description = request.form['description']
        photo_file = request.files['poster']

        filename = secure_filename(photo_file.filename)
        photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        movie = Movie(title=title, description=description, poster=filename)

        db.session.add(movie)
        db.session.commit()   
        response = {
            "message": "Movie successfully added",
            "title": movie.title,
            "poster": movie.poster,
            "description": movie.description,
        }
        return jsonify(response), 200
    else:
        errors = form_errors(form)
        response = {"errors": errors}
        return jsonify(response), 400

@app.route('/api/v1/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    movie_list = []
    for movie in movies:
        movie_data = {
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'poster': url_for('get_poster', filename=movie.poster)
        }
        movie_list.append(movie_data)
    return jsonify({'movies': movie_list})

@app.route('/api/v1/posters/<filename>', methods=['GET'])
def get_poster(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)


# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404