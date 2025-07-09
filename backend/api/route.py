from app import app, api, jsonify, db, request, get_jwt_identity, jwt_required
from backend.models.models import Api, User, Category


@app.route(f"{api}/api/<int:api_id>", methods=['GET'])
@jwt_required()
def api_def(api_id):
    api_ = Api.query.filter(Api.id == api_id).first()
    return jsonify({
        'api': api_.convert_json()
    })


@app.route(f"{api}/api_list", methods=['GET'])
@jwt_required()
def api_list():
    identity = get_jwt_identity()
    user = User.query.filter(User.username == identity).first()
    api_list_ = Api.query.filter(Api.user_id == user.id).order_by(Api.id).all()
    list = []
    for api_list_ in api_list_:
        list.append(api_list_.convert_json())
    return jsonify({
        'api_list': list
    })


@app.route(f"{api}/create_api")
@jwt_required()
def create_api():
    identity = get_jwt_identity()
    user = User.query.filter(User.username == identity).first()
    url = ''
    token = ''
    new_api = Api(
        url=url,
        token=token,
        user_id=user.id,
    )
    db.session.add(new_api)
    db.session.commit()
    return jsonify({
        'api': new_api.convert_json(),
        'status': True
    })
