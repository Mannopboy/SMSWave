from backend.models.models import Column, Integer, String, BigInteger, db, ForeignKey, Boolean, DateTime, relationship


class SmsModel(db.Model):
    __tablename__ = "sms_model"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    wifi = Column(String)
    password = Column(String)
    status = Column(Boolean, default=False)
    status_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))

    def convert_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "status": self.status,
            "wifi": self.wifi,
            "password": self.password,
        }

    def convert_json_for_statistics(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "status": self.status,
        }


class Filter(db.Model):
    __tablename__ = "filter"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    sms_users = relationship('SmsUser', backref="filter", order_by="SmsUser.id")

    def convert_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def convert_json_for_statistics(self):
        return {
            "id": self.id,
            "name": self.name,
            "users": len(self.sms_users)
        }


class SmsTemplate(db.Model):
    __tablename__ = "sms_template"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

    def convert_json(self):
        return {
            "id": self.id,
            "text": self.text,
        }


class SmsUser(db.Model):
    __tablename__ = "sms_user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    phone = Column(String)
    filter_id = Column(Integer, ForeignKey('filter.id'))
    sms_list = relationship('Sms', backref="sms_user", order_by="Sms.id")

    def convert_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "phone": self.phone,
        }


class Sms(db.Model):
    __tablename__ = "sms"
    id = Column(Integer, primary_key=True)
    message = Column(String)
    phone = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    sms_user_id = Column(Integer, ForeignKey('sms_user.id'))
    date = Column(DateTime)

    def convert_json(self):
        return {
            "id": self.id,
            "message": self.message,
            "phone": self.phone,
            "sms_user": self.sms_user.convert_json(),
        }
