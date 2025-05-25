from flask import Flask, request, render_template, jsonify
import requests
import re
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    target_url = data.get('url')
    if not target_url:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        res = requests.get(target_url, timeout=10)
        content = res.text

        m3u8_links = list(set(re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', content)))
        mp4_links = list(set(re.findall(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*', content)))

        # Priority: if m3u8 found, show only those, else mp4, else none
        if m3u8_links:
            return jsonify({'type': 'm3u8', 'links': m3u8_links})
        elif mp4_links:
            return jsonify({'type': 'mp4', 'links': mp4_links})
        else:
            return jsonify({'type': 'none', 'message': 'No direct m3u8 or mp4 links found.'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
