from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def extract_direct_link(url):
    # Look for m3u8 or mp4 anywhere inside the URL string
    # Use regex to find a substring ending with .m3u8 or .mp4
    m3u8_match = re.search(r'(https?://[^\s"\']+\.m3u8)', url)
    mp4_match = re.search(r'(https?://[^\s"\']+\.mp4)', url)

    if m3u8_match:
        return m3u8_match.group(1)
    elif mp4_match:
        return mp4_match.group(1)
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    data = request.get_json()
    url = data.get('url', '').strip()
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    direct_link = extract_direct_link(url)

    if direct_link:
        return jsonify({'direct_link': direct_link})
    else:
        return jsonify({'error': 'No direct .m3u8 or .mp4 link found in the input'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
