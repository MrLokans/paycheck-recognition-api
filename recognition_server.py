import os

from flask import (
    Flask,
    jsonify,
    request
)
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '{}/uploads/'.format(os.getcwd())
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/recognize/', methods=('POST', 'GET'))
def recognize():
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        file = request.files.get('picture')
        if file is None:
            return jsonify({'error': 'No selected file'})
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({"status": "file {} successfully uploaded".format(file.filename)})
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=picture>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
