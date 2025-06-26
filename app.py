import yt_dlp
from flask import Flask, request, jsonify

# تهيئة تطبيق فلاسك
app = Flask(__name__)

# ==================== التعديل الجديد هنا ====================
# هذا بروكسي عام ومجاني مقدم من مشروع Piped (بديل آخر ليوتيوب)
# وظيفته هي تمرير الطلبات إلى يوتيوب وتجنب الحظر
PROXY_URL = "https://pipedproxy.kavin.rocks"

# إعدادات yt-dlp لاستخدام البروكسي
YDL_OPTIONS = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'quiet': True,
    'proxy': PROXY_URL,  # <-- إضافة البروكسي هنا
    'geo_bypass': False # <-- مهم لتجنب مشاكل أخرى مع البروكسي
}
# ========================================================

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
