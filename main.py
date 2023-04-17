from compress_images import images_to_pdf
import os
import shutil
from flask import Flask, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
import threading

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Check if file has allowed extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Call example function with uploads directory path
def example(uploads_dir):
    print("Example function called with path:", uploads_dir)


# Route for home page
@app.route('/')
def index():
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        shutil.rmtree(os.path.abspath(app.config['UPLOAD_FOLDER']))
    return render_template('index.html')

# Route for download page
@app.route('/download_pdf')
def download_pdf():
    return render_template('download_pdf.html')

@app.route('/get_pdf')
def get_pdf():
    # Replace 'example.pdf' with the name of your PDF file
    filename = 'compressed/compressed.pdf'
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)
    #shutil.rmtree(os.path.abspath(app.config['UPLOAD_FOLDER']))


# Route for file upload
@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('file')
    filenames = []
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.mkdir(os.path.abspath(app.config['UPLOAD_FOLDER']))
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            t = threading.Thread(target=example, args=(os.path.join(app.config['UPLOAD_FOLDER'], filename),))
            t.start()
            t.join()
            filenames.append(filename)
    # Call example function with uploads directory path
    images_to_pdf(os.path.abspath(app.config['UPLOAD_FOLDER']))
    
    return render_template('download_pdf.html')


if __name__ == '__main__':
    app.run(debug=False, port=os.getenv("PORT", default=5000))
