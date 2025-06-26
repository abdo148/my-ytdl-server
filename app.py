import yt_dlp
from flask import Flask, request, jsonify
import os
import requests # سنحتاج هذه المكتبة لجلب البروكسيات
import random

app = Flask(__name__)

# --- الإعدادات النهائية والقوية (كوكيز + محاكاة أندرويد + تدوير بروكسي) ---
cookies_file_path = os.path.join(os.path.dirname(__file__), 'cookies.txt')

def get_free_proxies():
    """الحصول على قائمة بروكسيات مجانية ومحدثة"""
    try:
        # مصدر موثوق للبروكسيات المجانية
        url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all"
        response = requests.get(url, timeout=5)
        proxies = response.text.strip().split('\n')
        # نخلط البروكسيات لنبدأ بواحد عشوائي كل مرة
        random.shuffle(proxies)
        # نأخذ أول 10 فقط لتسريع العملية
        return [f'http://{proxy.strip()}' for proxy in proxies[:10]]
    except Exception as e:
        print(f"فشل جلب البروكسيات، سنستخدم قائمة احتياطية. الخطأ: {e}")
        # قائمة بروكسيات احتياطية في حال فشل المصدر الأساسي
        return [
            'http://154.95.2.146:8080',
            'http://190.15.253.250:9991',
            'http://103.179.186.230:8080'
        ]

@app.route('/api/info')
def get_info():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "الرجاء توفير رابط الفيديو"}), 400

    if not os.path.exists(cookies_file_path):
        return jsonify({"error": "ملف الكوكيز 'cookies.txt' غير موجود"}), 500
    
    # جلب قائمة بروكسيات جديدة لكل طلب
    proxies_to_try = get_free_proxies()
    print(f"تم جلب {len(proxies_to_try)} بروكسي للتجربة.")

    for i, proxy in enumerate(proxies_to_try):
        print(f"المحاولة رقم {i+1} باستخدام البروكسي: {proxy}")
        try:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'quiet': True,
                'no_warnings': True,
                'cookiefile': cookies_file_path,
                'nocheckcertificate': True,
                'proxy': proxy, # <-- استخدام البروكسي الحالي
                'socket_timeout': 15, # مهلة انتظار أقصر لكل بروكسي
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android'] # محاكاة أندرويد
                    }
                }
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                sanitized_info = ydl.sanitize_info(info)
                print(f"✅ نجحت المحاولة مع البروكسي: {proxy}")
                return jsonify(sanitized_info) # نرجع النتيجة فور النجاح
                
        except Exception as e:
            print(f"❌ فشلت المحاولة مع {proxy}: {str(e)}")
            continue # ننتقل إلى البروكسي التالي

    # إذا فشلت كل المحاولات
    return jsonify({"error": "فشلت جميع المحاولات مع كل البروكسيات المتاحة."}), 500

if __name__ == "__main__":
    app.run()
