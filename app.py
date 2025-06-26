import yt_dlp
from flask import Flask, request, jsonify

# تهيئة تطبيق فلاسك
app = Flask(__name__)

# هذا هو الخيار الأفضل للأداء على الخوادم
YDL_OPTIONS = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'quiet': True,
}

@app.route('/api/info')
def get_info():
    # الحصول على رابط يوتيوب من الطلب
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "الرجاء توفير رابط الفيديو عبر متغير 'url'"}), 400

    try:
        # استخدام yt-dlp لاستخلاص المعلومات
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(video_url, download=False)
            # تنظيف الرد لإعادته كـ JSON
            sanitized_info = ydl.sanitize_info(info)
            return jsonify(sanitized_info)

    except Exception as e:
        # في حال حدوث أي خطأ
        return jsonify({"error": str(e)}), 500

# هذا السطر ضروري لتشغيل التطبيق على Render
if __name__ == "__main__":
    app.run()
