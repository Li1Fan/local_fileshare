import os
from datetime import datetime, date

from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads/'
app.config['CLIPBOARD_URL'] = os.environ.get('CLIPBOARD_URL', '')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.template_filter('file_icon')
def file_icon(filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    icons = {
        'pdf': '📄', 'doc': '📝', 'docx': '📝', 'xls': '📊', 'xlsx': '📊',
        'ppt': '📑', 'pptx': '📑', 'txt': '📃',
        'jpg': '🖼', 'jpeg': '🖼', 'png': '🖼', 'gif': '🖼', 'webp': '🖼', 'bmp': '🖼',
        'mp4': '🎬', 'mov': '🎬', 'avi': '🎬', 'mkv': '🎬',
        'mp3': '🎵', 'wav': '🎵', 'flac': '🎵',
        'zip': '🗜', 'rar': '🗜', 'gz': '🗜', 'tar': '🗜', '7z': '🗜',
        'py': '🐍', 'js': '📜', 'html': '🌐', 'css': '🎨',
    }
    return icons.get(ext, '📁')


@app.route('/')
def index():
    folder = app.config['UPLOAD_FOLDER']
    names = os.listdir(folder)
    today = date.today()

    def date_label(d):
        delta = (today - d).days
        if delta == 0:
            return '今天'
        elif delta == 1:
            return '昨天'
        else:
            return d.strftime('%Y年%m月%d日')

    files = sorted(
        [
            {
                'name': f,
                'mtime': datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, f))),
            }
            for f in names
        ],
        key=lambda x: x['mtime'],
        reverse=True
    )
    for f in files:
        f['time_str'] = f['mtime'].strftime('%H:%M:%S')
        f['date_label'] = date_label(f['mtime'].date())

    return render_template('index.html', files=files, clipboard_url=app.config['CLIPBOARD_URL'])


@app.route('/api/upload', methods=['POST'])
def api_upload():
    files = request.files.getlist('file')
    if not files or all(not f.filename for f in files):
        return jsonify({'ok': False, 'error': 'no file provided'}), 400
    saved = []
    for file in files:
        if file and file.filename:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            saved.append(file.filename)
    return jsonify({'ok': True, 'saved': saved})


@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('file')
    for file in files:
        if file and file.filename:
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
