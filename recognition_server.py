import logging
import os

from flask import (
    Flask,
    jsonify,
    request
)
from werkzeug.utils import secure_filename

from recognition_service import RecognizerService


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('recognizer.flask')

if not os.path.exists(UPLOAD_FOLDER):
    logger.info("Upload dir ({}) does not exist, creating."
                .format(UPLOAD_FOLDER))
    os.mkdir(UPLOAD_FOLDER)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False
recognizer = RecognizerService()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/recognize/', methods=('POST', 'GET'))
def recognize():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files.get('picture')
        if file is None or file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            output_fname = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(output_fname)
            recognized_text = recognizer.recognize_image(output_fname)
            try:
                os.remove(output_fname)
            except:
                logger.exception("Error removing file ({})"
                                 .format(output_fname))
            # TODO (mrlokans) add celery/RQ task
            return jsonify({"recognized": recognized_text})
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
