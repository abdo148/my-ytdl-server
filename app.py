import yt_dlp
from flask import Flask, request, jsonify

# تهيئة تطبيق فلاسك
app = Flask(__name__)

# --- الإعدادات النهائية والمحسنة ---
# نستخدم User-Agent لمتصفح حقيقي لتجنب مشاكل الحظر
# هذا هو الحل الأكثر شيوعاً لمشكلة "Failed to extract player response"
YDL_OPTIONS = {
    'format': 'bestvideo+bestaudio/best',
    'quiet': True,
    'no_warnings': True, # لتجنب طباعة تحذيرات غير ضرورية في السجل
    'extract_flat': 'in_playlist', # لتحسين أداء قوائم التشغيل إذا تم استخدامها
    # إضافة Headers تحاكي متصفح حقيقي
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }
}
# --- نهاية الإعدادات ---

@app.route('/api/info')
def get_info():
    # الحصول على رابط يوتيوب من الطلب
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "الرجاء توفير رابط الفيديو عبر متغير 'url'"}), 400

    try:
        # استخدام yt-dlp لاستخلاص المعلومات مع الإعدادات المحدثة
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            # استخلاص المعلومات
            info = ydl.extract_info(video_url, download=False)
            # تنظيف الرد لإعادته كـ JSON (ضروري)
            sanitized_info = ydl.sanitize_info(info)
            return jsonify(sanitized_info)

    except Exception as e:
        # في حال حدوث أي خطأ، نعيده للمستخدم
        return jsonify({"error": str(e)}), 500

# هذا السطر ضروري لتشغيل التطبيق على Render باستخدام gunicorn
# وعند تشغيله محلياً باستخدام "flask run"
if __name__ == "__main__":
    app.run()
