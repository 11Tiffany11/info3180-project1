"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""


from app import app
from flask import render_template, request, redirect, url_for


from app import app, db
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory
from werkzeug.utils import secure_filename
from app.forms import PropertiesForm
from app.models import PropertyProfile

import os


###
# Routing for your application.
###

@app.route('/properties/create', methods=['GET', 'POST'])
def addNewProperty():
    # Instantiate your form class
    form = PropertiesForm()
    # Validate file upload on submit
    if request.method == 'POST':
        if form.validate_on_submit():
            #Get Form Data
            prop_title =  form.prop_title.data
            prop_description = form.prop_description.data
            prop_rooms = form.prop_rooms.data
            prop_bathrooms = form.prop_bathrooms.data
            prop_price = form.prop_price.data
            prop_type = form.prop_type.data
            prop_location = form.prop_location.data
            
            # Get file data and save to your uploads folder
            f = form.prop_photo.data
            filename = secure_filename(f.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(file_path)
            f.save(file_path)

            #Add Data to PostgreDB
            property_profiles = PropertyProfile(prop_title = prop_title,
                prop_description = prop_description,
                prop_rooms = prop_rooms,
                prop_bathrooms = prop_bathrooms,
                prop_price = prop_price,
                prop_type = prop_type,
                prop_location = prop_location)
                
            
            db.session.add(property_profiles)
            db.session.commit()
            flash ('Successfully Added New Property!')
            return redirect(url_for('query_properties'))
        flash_errors(forms)
    return render_template('new_property.html', form=form)

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(app.config('UPLOAD_FOLDER'), filename)

@app.route('/properties')
def query_properties():
    query_properties = PropertyProfile.query.all()
    return render_template('query_properties.html', query_properties=query_properties)

@app.route('/properties/<propertyid>')
def display_properties(propertyid):
    properties = PropertyProfile.query.filter_by(id=propertyid).first()
    return render_template('display_properties.html', properties=properties)


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


def get_uploaded_images():
   rootdir = os.getcwd()
   print (rootdir)
   upload_dir_path = os.path.join(rootdir, 'uploads')
   for subdir, dirs, files in os.walk(upload_dir_path):
       for file in files:
          print (os.path.join(subdir, file))
            

###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

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
