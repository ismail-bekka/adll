from flask import Flask, render_template, request, jsonify
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# تحميل معلومات عدل 3 من ملف JSON
with open("adll3_data.json", "r", encoding="utf-8") as f:
    adll3_info = json.load(f)

# تجهيز الأسئلة والإجابات لاستخدامها في التدريب
questions = list(adll3_info.keys())
answers = list(adll3_info.values())

# تنظيف النصوص وإعداد النموذج
def preprocess_text(text):
    text = text.lower()  # تحويل النص إلى حروف صغيرة
    text = re.sub(r'[^\w\s]', '', text)  # إزالة الرموز والعلامات
    return text.strip()

# تطبيق التنظيف على جميع الأسئلة
cleaned_questions = [preprocess_text(q) for q in questions]

# تحويل الأسئلة إلى مصفوفات عددية باستخدام TF-IDF
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(cleaned_questions)

def get_adll3_info(user_input):
    user_input = preprocess_text(user_input)
    user_vector = vectorizer.transform([user_input])
    
    # حساب التشابه بين السؤال المدخل وجميع الأسئلة المتاحة
    similarities = cosine_similarity(user_vector, question_vectors)
    best_match_index = similarities.argmax()  # العثور على أقرب تطابق

    if similarities[0, best_match_index] > 0.3:  # إذا كان التشابه عاليًا بما يكفي
        return answers[best_match_index]
    else:
        return "عذرًا، لم أفهم سؤالك. حاول إعادة صياغته أو اسألني عن شيء آخر."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "").strip()
    response = get_adll3_info(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
