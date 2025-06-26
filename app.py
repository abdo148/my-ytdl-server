import yt_dlp
from flask import Flask, request, jsonify
import random
import time

# تهيئة تطبيق فلاسك
app = Flask(__name__)

# قائمة User-Agents متنوعة لمحاكاة متصفحات مختلفة
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15'
]

@app.route('/api/info')
def get_info():
    # الحصول على رابط يوتيوب من الطلب
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "الرجاء توفير رابط الفيديو عبر متغير 'url'"}), 400

    # اختيار User-Agent عشوائي لكل طلب
    user_agent = random.choice(USER_AGENTS)
    
    # --- إعدادات متقدمة مستوحاة من المساعد الذكي ---
    YDL_OPTIONS = {
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True, # لتجنب مشاكل شهادات SSL
        'geo_bypass': False,
        'http_headers': {
            'User-Agent': user_agent,
            'Accept-Language': 'en-US,en;q=0.5'
        },
        # تأخير بسيط قبل الطلب لمحاكاة سلوك الإنسان
        'sleep_interval_requests': random.uniform(0.5, 1.5)
    }
    
    try:
        # إضافة تأخير إضافي قبل بدء العملية
        time.sleep(random.uniform(0.3, 1.0))
        
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(video_url, download=False)
            sanitized_info = ydl.sanitize_info(info)
            return jsonify(sanitized_info)
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
