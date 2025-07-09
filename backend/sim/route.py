import json

from app import app, api, jsonify, db, request, sock, connections, get_jwt_identity, jwt_required
from backend.models.models import Filter, Sms, SmsUser, SmsTemplate, SmsModel, User
from datetime import datetime
from backend.functions.utils import sms_model_status


@app.route(f"{api}/sms/<int:sms_id>", methods=['GET'])
@jwt_required()
def sms(sms_id):
    sms_ = Sms.query.filter(Sms.id == sms_id).first()
    return jsonify({
        'sms': sms_.convert_json()
    })


@app.route(f"{api}/sms_list", methods=['GET'])
@jwt_required()
def sms_list():
    identity = get_jwt_identity()
    user = User.query.filter(User.username == identity).first()
    sms_list_ = Sms.query.filter(Sms.user_id == user.id).order_by(Sms.id).all()
    list = []
    for sms_ in sms_list_:
        list.append(sms_.convert_json())
    return jsonify({
        'sms_list': list
    })


@app.route(f"{api}/sms", methods=['POST'])
@jwt_required()
def create_sms():
    identity = get_jwt_identity()
    user = User.query.filter(User.username == identity).first()
    data = request.get_json()
    sms_user_ids = data.get('sms_user_ids')
    sms_model_id = data.get('sms_model_id')
    model = SmsModel.query.filter(SmsModel.id == sms_model_id).first()
    phones = []
    message = data.get('message')
    for sms_user_id in sms_user_ids:
        sms_user_ = SmsUser.query.filter(SmsUser.id == sms_user_id).first()
        phones.append(sms_user_.phone)
        to_date = datetime.now()
        new_sms = Sms(
            message=message,
            phone=sms_user_.phone,
            user_id=user.id,
            sms_user_id=sms_user_.id,
            date=to_date
        )
        db.session.add(new_sms)
        db.session.commit()
    for connection in connections:
        try:
            connection.send(json.dumps({
                "phones": phones,
                "message": message,
                "code": model.code,
            }))
        except Exception as e:
            print(f"Ulanish xatosi: {e}")
    return jsonify({
        'status': True
    })


@sock.route('/echo')
def echo(sock):
    connections.append(sock)
    try:
        while True:
            data = sock.receive()
            print(f"Kelgan xabar: {data}")
            code = data
            model = SmsModel.query.filter(SmsModel.code == code).first()
            if model:
                to_date = datetime.now()
                model.status = True
                model.status_time = to_date
                db.session.commit()
    except Exception as e:
        print(f"WebSocket yopildi: {e}")
        print(sock)
        model = SmsModel.query.filter(SmsModel.sock == sock).first()
        model.status = False
        db.session.commit()


@app.route(f"{api}/sms_model/<int:sms_model_id>", methods=['GET'])
@jwt_required()
def sms_model(sms_model_id):
    sms_model_status()
    sms_model_ = SmsModel.query.filter(SmsModel.id == sms_model_id).first()
    return jsonify({
        'sms_model': sms_model_.convert_json()
    })


@app.route(f"{api}/sms_models", methods=['GET'])
@jwt_required()
def sms_models():
    sms_model_status()
    identity = get_jwt_identity()
    user = User.query.filter(User.username == identity).first()
    sms_models_ = SmsModel.query.filter(SmsModel.user_id == user.id).order_by(SmsModel.id).all()
    list = []
    for sms_model_ in sms_models_:
        list.append(sms_model_.convert_json())
    return jsonify({
        'sms_models_': list
    })


@app.route(f"{api}/sms_model/<int:sms_model_id>", methods=['PUT'])
@jwt_required()
def change_sms_model(sms_model_id):
    data = request.get_json()
    model = SmsModel.query.get(sms_model_id)

    if not model:
        return jsonify({"message": "Project not found"}), 404

    model.wifi = data.get('wifi', model.wifi)
    model.password = data.get('password', model.password)

    db.session.commit()
    for connection in connections:
        try:
            connection.send(json.dumps({
                "code": model.code,
                "wifi": model.wifi,
                "password": model.password,
            }))
        except Exception as e:
            print(f"Ulanish xatosi: {e}")

    return jsonify({
        'status': True
    })


@app.route(f"{api}/sms_model", methods=['POST'])
@jwt_required()
def create_sms_model():
    identity = get_jwt_identity()
    user = User.query.filter(User.username == identity).first()
    data = request.get_json()
    print(data)
    new_sms_model = SmsModel(
        name=data.get('name'),
        code=data.get('code'),
        wifi=data.get('wifi'),
        password=data.get('password'),
        user_id=user.id,
    )
    db.session.add(new_sms_model)
    db.session.commit()
    return jsonify({
        'sms_model': new_sms_model.convert_json(),
        'status': True
    })


@app.route(f"{api}/sms_user/<int:sms_user_id>", methods=['GET'])
@jwt_required()
def sms_user(sms_user_id):
    sms_user_ = SmsUser.query.filter(SmsUser.id == sms_user_id).first()
    return jsonify({
        'sms_user': sms_user_.convert_json()
    })


@app.route(f"{api}/sms_users", methods=['GET'])
@jwt_required()
def sms_users():
    identity = get_jwt_identity()
    user = User.query.filter(User.username == identity).first()
    filters = Filter.query.filter(Filter.user_id == user.id).order_by(Filter.id).all()
    list1 = []
    for filter in filters:
        ssms_users_ = SmsUser.query.filter(SmsUser.filter_id == filter.id).order_by(SmsUser.id).all()
        for sms_user_ in ssms_users_:
            list1.append(sms_user_)
    list = []
    for sms_user_ in list1:
        list.append(sms_user_.convert_json())
    return jsonify({
        'sms_users': list
    })


@app.route(f"{api}/sms_user", methods=['POST'])
@jwt_required()
def create_sms_user():
    data = request.get_json()
    print(data)
    new_sms_user = SmsUser(
        name=data.get('name'),
        surname=data.get('surname'),
        phone=data.get('phone'),
        filter_id=data.get('filter_id'),
    )
    db.session.add(new_sms_user)
    db.session.commit()
    return jsonify({
        'sms_user': new_sms_user.convert_json(),
        'status': True
    })


@app.route(f"{api}/sms_template/<int:sms_template_id>", methods=['GET'])
@jwt_required()
def sms_template(sms_template_id):
    sms_template_ = SmsTemplate.query.filter(SmsTemplate.id == sms_template_id).first()
    return jsonify({
        'sms_template': sms_template_.convert_json()
    })


@app.route(f"{api}/sms_templates", methods=['GET'])
@jwt_required()
def sms_templates():
    identity = get_jwt_identity()
    user = User.query.filter(User.username == identity).first()
    sms_templates_ = SmsTemplate.query.filter(SmsTemplate.user_id == user.id).order_by(SmsTemplate.id).all()
    list = []
    for sms_template_ in sms_templates_:
        list.append(sms_template_.convert_json())
    return jsonify({
        'sms_templates': list
    })


@app.route(f"{api}/sms_template", methods=['POST'])
@jwt_required()
def create_sms_template():
    identity = get_jwt_identity()
    user = User.query.filter(User.username == identity).first()
    data = request.get_json()
    print(data)
    new_sms_template = SmsTemplate(
        text=data.get('text'),
        user_id=user.id,
    )
    db.session.add(new_sms_template)
    db.session.commit()
    return jsonify({
        'sms_template': new_sms_template.convert_json(),
        'status': True
    })


@app.route(f"{api}/filter/<int:filter_id>", methods=['GET'])
@jwt_required()
def filter(filter_id):
    filter_ = Filter.query.filter(Filter.id == filter_id).first()
    return jsonify({
        'filter': filter_.convert_json()
    })


@app.route(f"{api}/filters", methods=['GET'])
@jwt_required()
def filters():
    identity = get_jwt_identity()
    user = User.query.filter(User.username == identity).first()
    filters_ = Filter.query.filter(Filter.user_id == user.id).order_by(Filter.id).all()
    list = []
    for filter_ in filters_:
        list.append(filter_.convert_json())
    return jsonify({
        'filters': list
    })


@app.route(f"{api}/filter", methods=['POST'])
@jwt_required()
def create_filter():
    identity = get_jwt_identity()
    user = User.query.filter(User.username == identity).first()
    data = request.get_json()
    print(data)
    new_filter = Filter(
        name=data.get('name'),
        user_id=user.id,
    )
    db.session.add(new_filter)
    db.session.commit()
    return jsonify({
        'filter': new_filter.convert_json(),
        'status': True
    })

# @sock.route('/echo')
# def echo(sock):
#     connections.append(sock)
#     try:
#         while True:
#             data = sock.receive()
#             print(data)
#             print(f"Arduino'dan olingan xabar: {data}")
#             for connection in connections:
#                 if connection != sock:
#                     try:
#                         payload = json.loads(data)
#                         phone = payload.get("phone", [])
#                         message = payload.get("message", "")
#                         connection.send(json.dumps({
#                             "phone": phone,
#                             "message": message,
#                             'status': True
#                         }))
#                     except Exception as e:
#                         print(f"Ulanish xatosi: {e}")
#                         connections.remove(connection)
#     except Exception as e:
#         print(f"WebSocket yopildi: {e}")
#         connections.remove(sock)


# @sock.route('/echo1')
# def echo1(sock):
#     connections.append(sock)
#     try:
#         while True:
#             data = sock.receive()
#             print(f"Kelgan xabar: {data}")
#
#             # Data formatini parse qilish (JSON bo‘ladi)
#             try:
#                 payload = json.loads(data)
#                 phones = payload.get("phones", [])
#                 message = payload.get("message", "")
#
#                 # Har bir raqam uchun xabarni clientlarga yuborish
#                 for connection in connections:
#                     try:
#                         connection.send(json.dumps({
#                             "phones": phones,
#                             "message": message,
#                             'status': False
#                         }))
#                     except Exception as e:
#                         print(f"Ulanish xatosi: {e}")
#                         connections.remove(connection)
#             except Exception as e:
#                 print(f"Xatolik: {e}")
#     except Exception as e:
#         print(f"WebSocket yopildi: {e}")
#         connections.remove(sock)

# latest_event = {}
#
#
# @app.route('/face-event', methods=['POST'])
# def face_event():
#     event_log_raw = request.form.get('event_log')
#
#     if not event_log_raw:
#         return "Bo'sh so‘rov", 400
#
#     try:
#         event = json.loads(event_log_raw)
#         access_event = event.get("AccessControllerEvent", {})
#
#         user_name = access_event.get("name", "").strip()
#         verify_mode = access_event.get("currentVerifyMode", "")
#         timestamp = event.get("dateTime", "")
#
#         # 1. Foydalanuvchi yo‘q yoki verify_mode noto‘g‘ri bo‘lsa — umuman ishlamaysiz
#         if not user_name or verify_mode not in ("face", "cardOrFace"):
#             return "Noto‘g‘ri yoki foydalanuvchisiz hodisa", 204
#         print(" Yuz aniqlash hodisasi:")
#         print(" Foydalanuvchi:", user_name)
#         print(" ID:", access_event.get("employeeNoString", ""))
#         print(" Vaqt:", timestamp)
#         print(" Verify Mode:", verify_mode)
#         print(" IP:", event.get("ipAddress"))
#
#     except Exception as e:
#         print(" JSON parsing xato:", e)
#         return "Xatolik", 500
#
#     return "OK"
