import os

from flask import Flask, render_template, request, redirect, url_for, send_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads/'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect(url_for('index'))


@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)


@app.route('/delete/<filename>')
def delete_file(filename):
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('index'))


@app.route('/delete_all')
def delete_all():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    for file in files:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
