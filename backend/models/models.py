from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import String, Integer, Boolean, Float, Column, ForeignKey, DateTime, or_, and_, desc, func, ARRAY, \
    JSON, \
    extract, Date, BigInteger, Table
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm import relationship

db = SQLAlchemy()


def db_setup(app):
    app.config.from_object('backend.models.config')
    db.app = app
    db.init_app(app)
    Migrate(app, db)
    return db


from backend.sim.models import *
from backend.category.models import *
from backend.api.models import *


class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    username = Column(String)
    phone = Column(String)
    status = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    balance = Column(BigInteger, default=0)
    categories = db.relationship(
        "Category",
        secondary="user_category",
        back_populates="users"
    )
    api_list = relationship('Api', backref="user", order_by="Api.id")
    sms_models = relationship('SmsModel', backref="user", order_by="SmsModel.id")
    filters = relationship('Filter', backref="user", order_by="Filter.id")
    sms_templates = relationship('SmsTemplate', backref="user", order_by="SmsTemplate.id")
    sms_list = relationship('Sms', backref="user", order_by="Sms.id")

    def convert_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "phone": self.phone,
            "balance": self.balance,
            "categories": [cat.convert_json_for_user() for cat in self.categories]
        }

    def convert_json_for_categories(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "phone": self.phone,
            "balance": self.balance,
        }
