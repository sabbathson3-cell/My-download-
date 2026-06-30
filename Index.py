from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # यसले ब्लगस्पटलाई सर्भरसँग कनेक्ट हुन दिन्छ

@app.route('/')
def home():
    return "Vercel Python Downloader Server is Running!"

@app.route('/get-link', methods=['GET'])
def get_link():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL missing"}), 400

    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')
            title = info.get('title')
            thumbnail = info.get('thumbnail')

            return jsonify({
                "download_url": download_url,
                "title": title,
                "thumbnail": thumbnail
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel का लागि यो आवश्यक छ
app.debug = True
