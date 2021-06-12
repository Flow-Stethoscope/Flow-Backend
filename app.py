import json

import pymongo
from flask import Flask, request, redirect
import bcrypt

from schemas import User
from schemas import Recording

client = pymongo.MongoClient("mongodb+srv://admin:mAsSeYhAcKeZ2096@flow-db.wcavd.mongodb.net/test")
db = client["flow"]

# files = request.files


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3'}
app = Flask(__name__)
app.run()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return {"Health": "Good"}


@app.route('/test', methods=['GET'])
def test():
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


@app.route('/register_user', methods=['POST'])
def register_user():
    db_user = request.form.to_dict()
    if User.user.is_valid(db_user):
        if (db["users"].find_one({'username': db_user["username"]})) is not None:
            return "This username already exists"
        db_user["password"] = bcrypt.hashpw(db_user["password"].encode('utf-8'), bcrypt.gensalt())
        db_user["recordings"] = []
        if db_user["user_type"] == "Patient":
            db_user["doctors"] = []
            db["patients"].insert_one(db_user)
        else:
            db_user["patients"] = []
            db["doctors"].insert_one(db_user)
        db["users"].insert_one(db_user)
        return "Success"
    return "Form data incorrectly formatted"


@app.route('/login/<username>', methods=['POST'])
def login(username):
    return str(bcrypt.checkpw(request.form.to_dict()["password"].encode('utf-8'),
                              db["users"].find_one({"username": username})["password"]))


@app.route('/users/<username>', methods=['GET'])
def user(username):
    user_info = (db["users"].find_one({"username": username}))
    user_info["_id"] = None
    user_info["password"] = None
    print(user_info)
    return json.loads(json.dumps(user_info))


@app.route('/send_recording', methods=['POST'])
def send_recording():
    recording = request.form.to_dict()
    # if Recording.recording.is_valid(recording):
    if True:
        rec_id = db["recordings"].insert_one(recording).inserted_id
        db.patients.update(
            {
                "username": recording["username"]
            },
            {
                "$push": {
                    "recordings":
                        db["recordings"].find_one(
                            {"_id": rec_id}
                        )["_id"]
                }
            }
        )
        # db["patients"].update(
        #     {"username": recording["username"]},
        #     {"$push": recording}
        # )
    return "True"

# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('download_file', name=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''