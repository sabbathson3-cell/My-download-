from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # ब्लगस्पटसँग लिंक जोड्नका लागि

@app.route('/')
def home():
    return jsonify({"status": "Global Downloader Server is Running"})

@app.route('/get-link')
def get_link():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL required"}), 400

    # युट्युबको कडा सेक्युरिटी तोड्ने र सबैका लागि चल्ने मुख्य सेटिङ
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        # 🧠 युट्युबलाई आधिकारिक मोबाइल एपबाट रिक्वेस्ट आएको भन्दै झुक्याउने जुक्ति
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'web_embedded'],
                'skip': ['dash', 'hls']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')
            title = info.get('title', 'video')
            
            if download_url:
                return jsonify({
                    "title": title,
                    "download_url": download_url
                })
            else:
                return jsonify({"error": "Extraction failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

app = app
