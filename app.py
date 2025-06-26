import yt_dlp
from flask import Flask, request, jsonify

# تهيئة تطبيق فلاسك
app = Flask(__name__)

# --- الإعدادات النهائية والقوية (بروكسي + هيدرز) ---

# هذا بروكسي عام ومجاني ومخصص لتجنب حظر يوتيوب
PROXY_URL = "https://pipedproxy.kavin.rocks"

YDL_OPTIONS = {
    'format': 'bestvideo+bestaudio/best', # صيغة مرنة
    'quiet': True,
    'no_warnings': True,
    'proxy': PROXY_URL,  # <-- استخدام البروكسي لتجاوز الحظر
    'geo_bypass': False, # <-- مهم ليعمل البروكسي بشكل صحيح
    # إضافة Headers كإجراء احترازي إضافي
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }
}
# --- نهاية الإعدادات ---

@app.route('/api/info')
def get_info():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "الرجاء توفير رابط الفيديو عبر متغير 'url'"}), 400

    try:
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(video_url, download=False)
            sanitized_info = ydl.sanitize_info(info)
            return jsonify(sanitized_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
