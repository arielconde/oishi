from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import oishi

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['wav'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'fileWav' not in request.files:
            return "No file part"
        file = request.files['fileWav']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            print("Okay")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            oishi.diarize()
            return "File Uploaded"
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


"""
This route accepts a post request that contains a .WAV file
for speaker diarization, named fileWav
"""
@app.route('/diarize', methods=['POST', 'GET'])
def diarize_api():
    if 'audio' not in request.files:
        return jsonify({'message': 'No file upload.'})
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'message': 'No selected file.'})
    elif file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'result': oishi.diarize(filename)})
    else:
        return jsonify({'message': 'An error occured'})


@app.route('/stubapi')
def stubapi():
    filename = '1.wav'
    return jsonify({'result': oishi.diarize(filename)})


if __name__ == "__main__":
    app.run(debug=True)
