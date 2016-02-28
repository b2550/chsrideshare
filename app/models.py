from app import db

grouprel = db.Table('grouprel',
                    db.Column('user', db.Integer, db.ForeignKey('users.id')),
                    db.Column('group', db.Integer, db.ForeignKey('groups.id'))
                    )


class Users(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(120), unique=True, index=True)
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.Text)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    type = db.Column(db.String(10))
    active = db.Column(db.Boolean)
    address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    uid = db.Column(db.Text(64), unique=True)
    requests = db.relationship('Requests', backref='receiver', foreign_keys='Requests.user_destination')
    sentrequests = db.relationship('Requests', backref='sender', foreign_keys='Requests.user_origin')
    notifications = db.relationship('Notifications', backref='user')
    groups = db.relationship('Groups', secondary=grouprel, lazy='dynamic', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, email, password, firstname, lastname, utype, uid, active=True):
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.type = utype
        self.active = active
        self.uid = uid

    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Users %r>' % self.email


class Requests(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    user_origin = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_destination = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Unicode)
    accepted = db.Column(db.Integer)

    def __init__(self, user_origin, user_destination, message, accepted=0):
        self.user_origin = user_origin
        self.user_destination = user_destination
        self.message = message
        self.accepted = accepted

    def __repr__(self):
        return '<Requests %r>' % self.id


class Groups(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    join_id = db.Column(db.Text, unique=True)

    def __init__(self, name, join_id):
        self.name = name
        self.join_id = join_id

    # routes = db.relationship('Routes', backref='getroutes')

    def __repr__(self):
        return '<Groups %r>' % self.id


class Routes(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.Text)

    # group = db.Column(db.Integer, db.ForeignKey('groups.id'))

    def __repr__(self):
        return '<Routes %r>' % self.id


class Notifications(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Text)

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message

    def __repr__(self):
        return '<Notifications %r>' % self.id
