import os
from datetime import datetime
from flask import flash, Flask, redirect, render_template, request, send_from_directory, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from forms import PredictionsForm,SentimentsForm

app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

# WEBSITE_HOSTNAME exists only in production environment
if 'WEBSITE_HOSTNAME' not in os.environ:
    # local development, where we'll use environment variables
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('azureproject.development')
else:
    # production
    print("Loading config.production.")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Initialize the database connection
db = SQLAlchemy(app)

# Enable Flask-Migrate commands "flask db init/migrate/upgrade" to work
migrate = Migrate(app, db)

# The import must be done after db initialization due to circular import issue
from models import Restaurant, Review, Predictions, Labels, Sentiment_Label, Sentiments

@app.route('/', methods=['GET'])
def index():
    print('Request for index page received')
    predictions = Predictions.query.all()
    table_pred = Labels(predictions)
    table_pred.border = True
    sentiments = Sentiments.query.all()
    table_sent = Sentiment_Label(sentiments)
    table_sent.border = True
    return render_template('index_predictions.html', table_pred = table_pred, table_sent = table_sent)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

def save_changes(sent, form, new=False,option = 'intent'):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    if option == 'intent':
        sent.intent = form.intent.data
    else:
        sent.sentiment = form.sentiment.data
    db.session.commit()

@app.route('/label', methods=['GET', 'POST'])
@csrf.exempt
def edit_label():
    transcript_id  = request.args.get('transcript_id', None)
    sent_id  = request.args.get('sent_id', None)
    qry = db.session.query(Predictions).filter(
                Predictions.transcript_id==transcript_id and Predictions.sent_id==sent_id)
    sent = qry.first()
    if sent:
        form = PredictionsForm(formdata=request.form, obj=sent)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(sent, form)
            #flash('Intent label updated successfully!')
            return redirect('/')
        return render_template('edit_label.html',form=form)
    else:
        return 'Error loading #{id}'.format(id=id)

@app.route('/sentiment', methods=['GET', 'POST'])
@csrf.exempt
def edit_sentiment_label():
    transcript_id  = request.args.get('transcript_id', None)
    sent_id  = request.args.get('sent_id', None)
    qry = db.session.query(Sentiments).filter(
                Sentiments.transcript_id==transcript_id and Sentiments.sent_id==sent_id)
    sent = qry.first()
    if sent:
        form = SentimentsForm(formdata=request.form, obj=sent)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(sent, form, option = 'sentiment')
            #flash('Intent label updated successfully!')
            return redirect('/')
        return render_template('edit_sentiment_label.html',form=form)
    else:

        return 'Error loading #{id}'.format(id=id)

if __name__ == '__main__':
    app.run()
