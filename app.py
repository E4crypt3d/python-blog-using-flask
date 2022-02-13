import params as params
from flask import Flask,render_template,request,redirect,flash
from flask_mail import Mail
from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,TextAreaField,SubmitField
from wtforms.validators import DataRequired, length, Email
import json

with open('config.json','r') as f:
    params = json.load(f)['params']
app = Flask(__name__)
app.config['SECRET_KEY'] = "5860dd16e9e934843f5453fb61f36e4b48950b90"
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params["gmail_user"],
    MAIL_PASSWORD = params["gmail_pass"]
)
mail = Mail(app)

class Contactus(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),length(max=15)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Name', validators=[DataRequired(),length(max=20)])
    message = TextAreaField('Your Message', validators=[DataRequired()])
    send_email = SubmitField('Email Us')


@app.route('/')
def homepage():
    return render_template('/index.html', params=params)

@app.route('/contactus', methods=['GET','POST'])
def contactus():
    form = Contactus()
    if form.validate_on_submit():
        flash('Your message was sent successfully.\nThanks for visiting us we will get back to you soon.\nHAPPY GAMING..! Regards DARKISTAN')
    if (request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        mail.send_message(f"This is a message from CLAN BLOG by {name}",
                          sender=email,
                          recipients=[params['gmail_user']],
                          body=email+'\n'+subject+'\n'+message)
        return redirect('/contactus')
    return render_template('/contactus.html', params=params, form=form)

@app.route('/watchus')
def watchus():
    return render_template('/watchus.html', params=params)

app.run(debug=True)