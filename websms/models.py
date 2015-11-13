from websms.database import db

class AlertsSubscriberData(db.Model):
    __tablename__ = 'alerts_subscriber_data'

    subscriber_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    number = db.Column(db.String(30))
    active = db.Column(db.SmallInteger)
    alert_on_beam_down = db.Column(db.SmallInteger)
    alert_on_beam_up = db.Column(db.SmallInteger)
    alert_on_blam = db.Column(db.SmallInteger)
    alert_on_fsm = db.Column(db.SmallInteger)
    date_added = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)