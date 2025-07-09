from backend.models.models import Column, Integer, String, db, ForeignKey


class Api(db.Model):
    __tablename__ = "api"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    token = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

    def convert_json(self):
        return {
            "id": self.id,
            "url": self.url,
            "token": self.token,
        }
