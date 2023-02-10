# Import Flask
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import pickle

prediction_label = {
    0:"Safe",
    1:"Unsafe"
}

# Dataset columns
db_columns = {
    "COUGH": {
        "description": "The way of responding to something irritating the throat or airways",
        "img": "COUGH.png"
    },
    "MUSCLE_ACHES": {
        "description": "The type of pain affecting a few muscles or part of body",
        "img": "MUSCLE_ACHES.png"
    },
    "TIREDNESS": {
        "description": "The state of wishing for more sleep",
        "img": "TIREDNESS.png"
    },
    "SORE_THROAT": {
        "description": "The pain, scratchiness or irritation of the throat that worsens when swallow",
        "img": "SORE_THROAT.png"
    },
    "RUNNY_NOSE": {
        "description": "The lot of mucus is coming out of the nose",
        "img": "RUNNY_NOSE.png"
    },
    "STUFFY_NOSE": {
        "description": "The sensation of something blocking the nose",
        "img": "STUFFY_NOSE.png"
    },
    "FEVER": {
        "description": "The rise in body temperature over 37.8C",
        "img": "FEVER.png"
    },
    "NAUSEA": {
        "description": "The uncomfortable, queasy feeling in the stomach that makes one vomit",
        "img": "NAUSEA.png"
    },
    "VOMITING": {
        "description": "The way for body to remove harmful substances from stomach through mouth",
        "img": "VOMITING.png"
    },
    "DIARRHEA": {
        "description": "The loose and watery bowel movement causing the poop to be watery",
        "img": "DIARRHEA.png"
    },
    "SHORTNESS_OF_BREATH": {
        "description": "The tightening of chest which feels like suffocation",
        "img": "SHORTNESS_OF_BREATH.png"
    },
    "DIFFICULTY_BREATHING": {
        "description": "The inability to inhale or exhale properly",
        "img": "DIFFICULTY_BREATHING.png"
    },
    "LOSS_OF_TASTE": {
        "description": "The inability to taste anything",
        "img": "LOSS_OF_TASTE.png"
    },
    "LOSS_OF_SMELL": {
        "description": "The inability to distinguish smells",
        "img": "LOSS_OF_SMELL.png"
    },
    "ITCHY_NOSE": {
        "description": "The nose being itchy",
        "img": "ITCHY_NOSE.png"
    },
    "ITCHY_EYES": {
        "description": "The eyes being itchy",
        "img": "ITCHY_EYES.png"
    },
    "ITCHY_MOUTH": {
        "description": "The mouth being itchy",
        "img": "ITCHY_MOUTH.png"
    },
    "ITCHY_INNER_EAR": {
        "description": "The ear being itchy",
        "img": "ITCHY_INNER_EAR.png"
    },
    "SNEEZING": {
        "description": "The way to remove irritants through nose",
        "img": "SNEEZING.png"
    },
    "PINK_EYE": {
        "description": "The swelling of the eye, making it seem pink/red",
        "img": "PINK_EYE.png"
    },
}

# instantiate SQLAlchemy to handle db process
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("config.cfg")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


# AI model file
joblib_file = "./application/static/tuned_dc.pkl"
# Load from file
with open(joblib_file, 'rb') as f:
    ai_model = pickle.load(f)
    print(ai_model)
