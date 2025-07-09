from app import app, api, jsonify, db, request, get_jwt_identity, jwt_required
from backend.models.models import User, SmsModel, Sms, Category, Filter, SmsUser
from sqlalchemy import extract, func


@app.route(f"{api}/admin_statistics", methods=['GET'])
@jwt_required()
def admin_statistics():
    identity = get_jwt_identity()
    user = User.query.filter(User.username == identity).first()
    if not user.admin:
        return jsonify({
            'status': False
        })
    models = SmsModel.query.order_by(SmsModel.id).all()
    users = User.query.filter(User.categories == None).order_by(User.id).all()
    print(users)
    users_sms = User.query.order_by(User.id).all()
    sms_list = []
    for user in users_sms:
        sms = Sms.query.filter(Sms.user_id == user.id).order_by(Sms.id).all()
        object = {
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'sms': len(sms)
        }
        sms_list.append(object)
    categories = Category.query.order_by(Category.id).all()
    category_list = []
    for category in categories:
        object = {
            'name': category.name,
            'price': category.price,
            'users': len(category.users)
        }
        category_list.append(object)
    return jsonify({
        'balance': user.balance,
        'models': [item.convert_json_for_statistics() for item in models],
        'new_users': [item.convert_json_for_categories() for item in users],
        'sms': sms_list,
        'categories': category_list
    })


@app.route(f"{api}/user_statistics", methods=['GET'])
@jwt_required()
def user_statistics():
    identity = get_jwt_identity()
    user = User.query.filter(User.username == identity).first()
    if not user.admin:
        return jsonify({'status': False})
    monthly_stats = (
        db.session.query(
            extract('year', Sms.date).label('year'),
            extract('month', Sms.date).label('month'),
            func.count(Sms.id).label('count')
        )
        .filter(Sms.user_id == user.id)
        .group_by('year', 'month')
        .order_by('year', 'month')
        .all()
    )
    stats = []
    for stat in monthly_stats:
        stats.append({
            "year": int(stat.year),
            "month": int(stat.month),
            "count": stat.count
        })
    # for category in user.categories:
    #     print(category)
    filters = Filter.query.filter(Filter.user_id == user.id).order_by(Filter.id).all()
    return jsonify({
        "status": True,
        "sms": stats,
        "categories": [{
            'name': 'dsfdf',
            'sms': 12
        }],
        "users": [item.convert_json_for_statistics() for item in filters]
    })
