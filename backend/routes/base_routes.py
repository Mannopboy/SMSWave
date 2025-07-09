from app import app, api, db, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token, \
    unset_jwt_cookies
from backend.models.models import User
from backend.functions.utils import get_json_field


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    return app.send_static_file("index.html")


@app.route(f"{api}/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    username_sign = User.query.filter(User.username == identity).first()
    return jsonify({
        'user': username_sign.convert_json(),
        "access_token": access_token,
        'status': True,
        "refresh_token": create_refresh_token(identity=username_sign.username),
    })


@app.route(f'{api}/login', methods=['POST'])
def login():
    username = get_json_field('username')
    password = get_json_field('password')
    username_sign = User.query.filter_by(username=username).first()
    if username_sign and check_password_hash(username_sign.password, password):
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        return jsonify({
            'user': username_sign.convert_json(),
            'access_token': access_token,
            'refresh_token': refresh_token,
            'msg': 'Login',
            'status': True
        })
    else:
        return jsonify({
            "msg": "Username yoki parol noto'g'ri"
        })


@app.route(f"{api}/profile")
@jwt_required()
def profile():
    identity = get_jwt_identity()
    user = User.query.filter(User.username == identity).first()
    return jsonify({
        'user': user.convert_json()
    })


@app.route(f"{api}/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"msg": "logout successful", 'status': True})
    unset_jwt_cookies(response)
    return response


@app.route(f'{api}/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = get_json_field('username')
        username_check = User.query.filter_by(username=username).first()
        if username_check:
            return jsonify({
                "message": "Username is already exists",
                'status': False,
            })
        name = get_json_field('name')
        surname = get_json_field('surname')
        password = get_json_field('password')
        password = generate_password_hash(password)
        username = get_json_field('username')
        phone = get_json_field('phone')
        add = User(name=name, surname=surname, password=password, username=username, phone=phone)
        db.session.add(add)
        db.session.commit()
        return jsonify({
            'status': True,
            "msg": "Registration was successful"
        })
