from wtforms import Form, StringField, SelectField, validators

class PredictionsForm(Form):
    intent_types = [('Money Transfer', 'Money Transfer'),
                   ('Account Block', 'Account Block'),
                   ('Logging in Issue', 'Logging in Issue')
                   ]
    transcript_id = StringField('Transcript Id')
    sent_id = StringField('Sentence Id')
    sentence = StringField('Sentence')
    score = StringField('Score')
    intent = SelectField('Intent', choices=intent_types)


class SentimentsForm(Form):
    sentiment_types = [('Positive', 'Positive'),
                   ('Negative', 'Negative'),
                   ('Neutral', 'Neutral')
                   ]
    transcript_id = StringField('Transcript Id')
    sent_id = StringField('Sentence Id')
    sentence = StringField('Sentence')
    score = StringField('Score')
    sentiment = SelectField('Sentiment', choices=sentiment_types)