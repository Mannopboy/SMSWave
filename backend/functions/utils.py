from app import request, db, SmsModel
from datetime import datetime, timedelta


def get_json_field(field_name):
    return request.get_json().get(field_name)


def get_form_field(field_name, type_form=None):
    if type_form == "file":
        return request.files.get(field_name)
    elif type_form == "file_list":
        return request.files.getlist(field_name)
    else:
        return request.form.get(field_name)


def sms_model_status():
    models = SmsModel.query.order_by(SmsModel.id).all()
    if models:
        for model in models:
            current_time = datetime.now()
            if model.status_time:
                time_difference = current_time - model.status_time
                if time_difference > timedelta(seconds=10) and model.status:
                    model.status = False
                    db.session.commit()
            else:
                model.status = False
                db.session.commit()
    return None
