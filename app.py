import os
from flask import Flask, render_template_string, request, send_file
import yt_dlp

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>YouTube Downloader</title></head>
<body>
    <h2>YouTube Video Downloader</h2>
    <form method="POST" action="/download">
        <input type="text" name="url" placeholder="Paste YouTube URL here" style="width: 300px;" required>
        <button type="submit">Download</button>
    </form>
    {% if error %}<p style="color: red;">{{ error }}</p>{% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'format': 'best',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
