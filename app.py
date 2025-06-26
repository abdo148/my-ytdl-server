import yt_dlp
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# --- الإعدادات النهائية والقوية (كوكيز + محاكاة أندرويد) ---
cookies_file_path = os.path.join(os.path.dirname(__file__), 'cookies.txt')

YDL_OPTIONS = {
    'format': 'bestvideo+bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'cookiefile': cookies_file_path,
    'nocheckcertificate': True,
    
    # --- هذا هو التعديل الأهم المستوحى من المساعد ---
    # نجعل yt-dlp يتصرف كتطبيق أندرويد
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'web_embedded'] 
        }
    }
    # --- نهاية التعديل ---
}

@app.route('/api/info')
def get_info():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "الرجاء توفير رابط الفيديو"}), 400

    if not os.path.exists(cookies_file_path):
        return jsonify({"error": "ملف الكوكيز 'cookies.txt' غير موجود"}), 500

    try:
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(video_url, download=False)
            sanitized_info = ydl.sanitize_info(info)
            return jsonify(sanitized_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
