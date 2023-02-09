from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db, db_columns, prediction_label
# from . import  ai_model
from datetime import datetime
from sqlalchemy import desc
from flask import json, jsonify

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
@main.route('/home')
def index():
    return render_template("index.html", safe=None)

@main.route("/safe")
def safe():
    return render_template("index.html", safe=True)

@main.route("/unsafe")
def unsafe():
    return render_template("index.html", safe=False)

# @main.route('/history')
# def history():
#     return render_template('history.html', prediction_label=prediction_label)

# @main.route('/predict', methods=["GET", "POST"])
# def predict():
#     form = PredictionForm()
#     if request.method == "POST":
#         cough = form.cough.data
#         muscle_aches = form.muscle_aches.data
#         tiredness = form.tiredness.data
#         sore_throat = form.sore_throat.data
#         runny_nose = form.runny_nose.data
#         stuffy_nose = form.stuffy_nose.data
#         fever = form.fever.data
#         nausea = form.nausea.data
#         vomiting = form.vomiting.data
#         diarrhea = form.diarrhea.data
#         shortness_of_breath = form.shortness_of_breath.data
#         difficulty_breathing = form.difficulty_breathing.data
#         loss_of_taste = form.loss_of_taste.data
#         loss_of_smell = form.loss_of_smell.data
#         itchy_nose = form.itchy_nose.data
#         itchy_eyes = form.itchy_eyes.data
#         itchy_mouth = form.itchy_mouth.data
#         itchy_inner_ear = form.itchy_inner_ear.data
#         sneezing = form.sneezing.data
#         pink_eye = form.pink_eye.data
#         X_test = [[
#             cough,
#             muscle_aches,
#             tiredness,
#             sore_throat,
#             runny_nose,
#             stuffy_nose,
#             fever,
#             nausea,
#             vomiting,
#             diarrhea,
#             shortness_of_breath,
#             difficulty_breathing,
#             loss_of_taste,
#             loss_of_smell,
#             itchy_nose,
#             itchy_eyes,
#             itchy_mouth,
#             itchy_inner_ear,
#             sneezing,
#             pink_eye,
#         ]]

#         prediction = ai_model.predict(X_test)
#         new_entry = Entry(
#             user=current_user.id,
#             cough=cough,
#             muscle_aches=muscle_aches,
#             tiredness=tiredness,
#             sore_throat=sore_throat,
#             runny_nose=runny_nose,
#             stuffy_nose=stuffy_nose,
#             fever=fever,
#             nausea=nausea,
#             vomiting=vomiting,
#             diarrhea=diarrhea,
#             shortness_of_breath=shortness_of_breath,
#             difficulty_breathing=difficulty_breathing,
#             loss_of_taste=loss_of_taste,
#             loss_of_smell=loss_of_smell,
#             itchy_nose=itchy_nose,
#             itchy_eyes=itchy_eyes,
#             itchy_mouth=itchy_mouth,
#             itchy_inner_ear=itchy_inner_ear,
#             sneezing=sneezing,
#             pink_eye=pink_eye,
#             prediction=int(prediction[0]),
#             predicted_on=datetime.now())
#         add_entry(new_entry)
#         flash(f"Prediction: {prediction_label[prediction[0]]}", "success")
#         return redirect(url_for('main.history'))
#     return render_template("predict.html", db_columns=db_columns, form=form)


# def add_entry(new_entry):
#     try:
#         db.session.add(new_entry)
#         db.session.commit()
#         return new_entry.id
#     except Exception as error:
#         db.session.rollback()
#         flash(error, "danger")
#         return 0


# def get_entries(user):
#     try:
#         entries = Entry.query.filter_by(
#             user=user.id).order_by(desc(Entry.id)).all()
#         print(entries)
#         return entries
#     except Exception as error:
#         db.session.rollback()
#         flash(error, "danger")
#         return 0


# @main.route('/delete/<id>', methods=['POST'])
# def delete(id):
#     if request.method == "POST":
#         delete_entry(id)
#     return redirect(url_for('main.history'))


# def get_entry(id):
#     try:
#         result = Entry.query.get(id)
#         return result
#     except Exception as error:
#         db.session.rollback()
#         flash(error, "danger")
#         return 0


# def delete_entry(id):
#     try:
#         entry = Entry.query.get(id)
#         db.session.delete(entry)
#         db.session.commit()
#     except Exception as error:
#         db.session.rollback()
#         flash(error, "danger")
#         return 0


# # API GET
# @main.route("/api/get/<id>", methods=['GET'])
# def api_get(id):
#     entry = get_entry(int(id))
#     data = {
#         "id": entry.id,
#         "cough": entry.cough,
#         "muscle_aches": entry.muscle_aches,
#         "tiredness": entry.tiredness,
#         "sore_throat": entry.sore_throat,
#         "runny_nose": entry.runny_nose,
#         "stuffy_nose": entry.stuffy_nose,
#         "fever": entry.fever,
#         "nausea": entry.nausea,
#         "vomiting": entry.vomiting,
#         "diarrhea": entry.diarrhea,
#         "shortness_of_breath": entry.shortness_of_breath,
#         "difficulty_breathing": entry.difficulty_breathing,
#         "loss_of_taste": entry.loss_of_taste,
#         "loss_of_smell": entry.loss_of_smell,
#         "itchy_nose": entry.itchy_nose,
#         "itchy_eyes": entry.itchy_eyes,
#         "itchy_mouth": entry.itchy_mouth,
#         "itchy_inner_ear": entry.itchy_inner_ear,
#         "sneezing": entry.sneezing,
#         "pink_eye": entry.pink_eye,
#         "prediction": entry.prediction,
#     }
#     result = jsonify(data)
#     return result

# # API DELETE


# @main.route('/api/delete/<id>', methods=['GET'])
# def api_delete(id):
#     if request.method == "GET":
#         delete_entry(id)
#     return jsonify({'result': 'ok'})

# # API ADD


# @main.route("/api/add", methods=['POST'])
# def api_add():
#     #retrieve the json file posted from client
#     data = request.get_json()
#     #retrieve each field from the data
#     user = data['user']
#     cough = data["cough"]
#     muscle_aches = data["muscle_aches"]
#     tiredness = data["tiredness"]
#     sore_throat = data["sore_throat"]
#     runny_nose = data["runny_nose"]
#     stuffy_nose = data["stuffy_nose"]
#     fever = data["fever"]
#     nausea = data["nausea"]
#     vomiting = data["vomiting"]
#     diarrhea = data["diarrhea"]
#     shortness_of_breath = data["shortness_of_breath"]
#     difficulty_breathing = data["difficulty_breathing"]
#     loss_of_taste = data["loss_of_taste"]
#     loss_of_smell = data["loss_of_smell"]
#     itchy_nose = data["itchy_nose"]
#     itchy_eyes = data["itchy_eyes"]
#     itchy_mouth = data["itchy_mouth"]
#     itchy_inner_ear = data["itchy_inner_ear"]
#     sneezing = data["sneezing"]
#     pink_eye = data["pink_eye"]
#     prediction = data['prediction']

#     #create an Entry object store all data for db action
#     new_entry = Entry(
#         user=user,
#         cough=cough,
#         muscle_aches=muscle_aches,
#         tiredness=tiredness,
#         sore_throat=sore_throat,
#         runny_nose=runny_nose,
#         stuffy_nose=stuffy_nose,
#         fever=fever,
#         nausea=nausea,
#         vomiting=vomiting,
#         diarrhea=diarrhea,
#         shortness_of_breath=shortness_of_breath,
#         difficulty_breathing=difficulty_breathing,
#         loss_of_taste=loss_of_taste,
#         loss_of_smell=loss_of_smell,
#         itchy_nose=itchy_nose,
#         itchy_eyes=itchy_eyes,
#         itchy_mouth=itchy_mouth,
#         itchy_inner_ear=itchy_inner_ear,
#         sneezing=sneezing,
#         pink_eye=pink_eye,
#         prediction=prediction,
#         predicted_on=datetime.now())
#     #invoke the add entry function to add entry
#     result = add_entry(new_entry)
#     #return the result of the db action
#     return jsonify({'id': result})

# # API Predict Endpoint to test AI Model


# @main.route("/api/predict", methods=['POST'])
# def api_predict():
#     data = request.get_json()
#     cough = data["cough"]
#     muscle_aches = data["muscle_aches"]
#     tiredness = data["tiredness"]
#     sore_throat = data["sore_throat"]
#     runny_nose = data["runny_nose"]
#     stuffy_nose = data["stuffy_nose"]
#     fever = data["fever"]
#     nausea = data["nausea"]
#     vomiting = data["vomiting"]
#     diarrhea = data["diarrhea"]
#     shortness_of_breath = data["shortness_of_breath"]
#     difficulty_breathing = data["difficulty_breathing"]
#     loss_of_taste = data["loss_of_taste"]
#     loss_of_smell = data["loss_of_smell"]
#     itchy_nose = data["itchy_nose"]
#     itchy_eyes = data["itchy_eyes"]
#     itchy_mouth = data["itchy_mouth"]
#     itchy_inner_ear = data["itchy_inner_ear"]
#     sneezing = data["sneezing"]
#     pink_eye = data["pink_eye"]
#     X_test = [[
#         cough,
#         muscle_aches,
#         tiredness,
#         sore_throat,
#         runny_nose,
#         stuffy_nose,
#         fever,
#         nausea,
#         vomiting,
#         diarrhea,
#         shortness_of_breath,
#         difficulty_breathing,
#         loss_of_taste,
#         loss_of_smell,
#         itchy_nose,
#         itchy_eyes,
#         itchy_mouth,
#         itchy_inner_ear,
#         sneezing,
#         pink_eye,
#     ]]

#     prediction = ai_model.predict(X_test)
#     new_entry = Entry(
#         user=data["id"],
#         cough=cough,
#         muscle_aches=muscle_aches,
#         tiredness=tiredness,
#         sore_throat=sore_throat,
#         runny_nose=runny_nose,
#         stuffy_nose=stuffy_nose,
#         fever=fever,
#         nausea=nausea,
#         vomiting=vomiting,
#         diarrhea=diarrhea,
#         shortness_of_breath=shortness_of_breath,
#         difficulty_breathing=difficulty_breathing,
#         loss_of_taste=loss_of_taste,
#         loss_of_smell=loss_of_smell,
#         itchy_nose=itchy_nose,
#         itchy_eyes=itchy_eyes,
#         itchy_mouth=itchy_mouth,
#         itchy_inner_ear=itchy_inner_ear,
#         sneezing=sneezing,
#         pink_eye=pink_eye,
#         prediction=int(prediction[0]),
#         predicted_on=datetime.now())
#     result = add_entry(new_entry)
#     return jsonify({'id': result, "prediction": int(prediction[0])})
