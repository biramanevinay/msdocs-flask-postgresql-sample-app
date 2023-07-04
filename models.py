from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import validates
from app import db
from flask_table import Table, Col, LinkCol

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    street_address = Column(String(50))
    description = Column(String(250))

    def __str__(self):
        return self.name

class Review(db.Model):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    restaurant = Column(Integer, ForeignKey('restaurant.id', ondelete="CASCADE"))
    user_name = Column(String(30))
    rating = Column(Integer)
    review_text = Column(String(500))
    review_date = Column(DateTime)

    @validates('rating')
    def validate_rating(self, key, value):
        assert value is None or (1 <= value <= 5)
        return value

    def __str__(self):
        return f"{self.user_name}: {self.review_date:%x}"


class Predictions(db.Model):
    __tablename__ = 'predictions'
    transcript_id = Column(String(1000), primary_key=True)
    sent_id = Column(String(100), primary_key=True)
    sentence = Column(String(5000))
    intent = Column(String(1000))
    score = Column(db.Float)

    def __str__(self):
        return self.name
    
class Labels(Table):
    transcript_id = Col('Transcript Id')
    sent_id = Col('Sentence Id')
    sentence = Col('Sentence')
    intent = Col('Intent')
    score = Col('Score')
    edit = LinkCol('Edit', 'edit_label', url_kwargs=dict(transcript_id='transcript_id',sent_id='sent_id'))   
    
class Sentiments(db.Model):
    __tablename__ = 'sentiments'
    transcript_id = Column(String(1000), primary_key=True)
    sent_id = Column(String(100), primary_key=True)
    sentence = Column(String(5000))
    sentiment = Column(String(100))
    score = Column(db.Float)

    def __str__(self):
        return self.name
    
class Sentiment_Label(Table):
    transcript_id = Col('Transcript Id')
    sent_id = Col('Sentence Id')
    sentence = Col('Sentence')
    sentiment = Col('Sentiment')
    score = Col('Score')
    edit = LinkCol('Edit', 'edit_sentiment_label', url_kwargs=dict(transcript_id='transcript_id',sent_id='sent_id'))   