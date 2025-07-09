from backend.models.models import Column, Integer, String, db, ForeignKey, Table,Boolean

user_category = Table(
    'user_category',
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True)
)


class Category(db.Model):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    sms_number = Column(Integer)
    api = Column(Boolean)

    users = db.relationship(
        "User",
        secondary="user_category",
        back_populates="categories"
    )

    def convert_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "sms_number": self.sms_number,
            "users": [cat.convert_json_for_categories() for cat in self.users]
        }

    def convert_json_for_user(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "sms_number": self.sms_number,
        }
