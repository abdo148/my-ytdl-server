import yt_dlp
from flask import Flask, request, jsonify
import os

# تهيئة تطبيق فلاسك
app = Flask(__name__)

# --- الإعدادات النهائية باستخدام الكوكيز ---
# تحديد مسار ملف الكوكيز. نفترض أنه موجود في نفس مجلد الكود.
cookies_file_path = os.path.join(os.path.dirname(__file__), 'cookies.txt')

YDL_OPTIONS = {
    'format': 'bestvideo+bestaudio/best', # صيغة مرنة
    'quiet': True,
    'no_warnings': True,
    # هذا هو الخيار الأهم: استخدام ملف الكوكيز لحل مشكلة "Sign in to confirm"
    'cookiefile': cookies_file_path,
    'nocheckcertificate': True
}
# --- نهاية الإعدادات ---

@app.route('/api/info')
def get_info():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "الرجاء توفير رابط الفيديو عبر متغير 'url'"}), 400

    # خطوة مهمة: التحقق من وجود ملف الكوكيز على الخادم قبل المتابعة
    if not os.path.exists(cookies_file_path):
        # إذا لم يكن الملف موجوداً، نعيد رسالة خطأ واضحة
        return jsonify({"error": "ملف الكوكيز 'cookies.txt' غير موجود على الخادم. يرجى رفعه."}), 500

    try:
        # استخدام yt-dlp مع خيار الكوكيز
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(video_url, download=False)
            sanitized_info = ydl.sanitize_info(info)
            return jsonify(sanitized_info)
            
    except Exception as e:
        # في حال حدوث أي خطأ آخر
        return jsonify({"error": str(e)}), 500

# لتشغيل التطبيق
if __name__ == "__main__":
    app.run()
