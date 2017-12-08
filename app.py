from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

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
        print("Okay 1")
        if file and allowed_file(file.filename):
            print("Okay")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "File Uploaded"
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
