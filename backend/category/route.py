from app import app, api, jsonify, db, request, get_jwt_identity, jwt_required
from backend.models.models import Category, User


@app.route(f"{api}/category/<int:category_id>", methods=['GET'])
@jwt_required()
def category(category_id):
    category_ = Category.query.filter(Category.id == category_id).first()
    return jsonify({
        'category': category_.convert_json()
    })


@app.route(f"{api}/categories", methods=['GET'])
@jwt_required()
def categories():
    categories_ = Category.query.order_by(Category.id).all()
    list = []
    for category_ in categories_:
        list.append(category_.convert_json())
    return jsonify({
        'categories': list
    })


@app.route(f"{api}/user_category", methods=['POST'])
@jwt_required()
def user_category():
    data = request.get_json()
    identity = get_jwt_identity()
    user = User.query.filter(User.username == identity).first()
    print(data)
    category_ids = data.get('category_ids')
    categories = Category.query.filter(Category.id.in_(category_ids)).all()
    user.categories = categories
    db.session.commit()
    return jsonify({
        'user': user.convert_json(),
        'status': True
    })


@app.route(f"{api}/category", methods=['POST'])
@jwt_required()
def create_category():
    data = request.get_json()
    print(data)
    new_category = Category(
        name=data.get('name'),
        price=data.get('price'),
        sms_number=data.get('sms_number'),
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify({
        'category': new_category.convert_json(),
        'status': True
    })
