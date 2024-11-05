import os  # Importing os to access environment variables
import re
from flask import Flask, render_template, request, jsonify, session
import requests
import random
import json
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Secret key for session management

# Configuration variables sourced from environment
MODEL_ID = os.getenv("MODEL_ID")  # Model ID for the Arabic grammar model
API_URL = os.getenv("API_URL")  # API endpoint for text generation
IAM_TOKEN_URL = os.getenv("IAM_TOKEN_URL")  # URL to obtain an access token
API_KEY = os.getenv("API_KEY")  # IBM API key for authorization
PROJECT_ID = os.getenv("PROJECT_ID")  # Project ID for IBM Watsonx usage

# Function to retrieve an access token from IBM
def get_access_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }

    try:
        response = requests.post(IAM_TOKEN_URL, headers=headers, data=data)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"Error getting access token: {e}")
        return None

# Function to check if the text is mostly in Arabic
def is_mostly_arabic(text):
    arabic_chars = re.findall(r'[\u0600-\u06FF]', text)
    return len(arabic_chars) > len(text) * 0.5

# Function to add the analyzed sentence and result to session history
def add_to_history(sentence, result):
    if 'history' not in session:
        session['history'] = []
    session['history'].append({'sentence': sentence, 'result': result})

# Route to retrieve session history
@app.route('/history', methods=['GET'])
def get_history():
    history = session.get('history', [])
    return jsonify(history)

# Function to validate and analyze a sentence's structure
def validate_and_analyze_sentence(sentence):
    # Check if the sentence contains enough Arabic text
    if not is_mostly_arabic(sentence):
        return {"error": "الجملة تحتوي على أحرف غير عربية أو غير مفهومة. 🙃"}

    access_token = get_access_token()
    if not access_token:
        return {"error": "Failed to obtain access token. Please check the API key and network connection."}

    # Prompt to validate the sentence
    validation_prompt = (
        "رجاءً قم بتحليل الجملة التالية دون أي تفكير إضافي.ولا تقدم أي معلومات إضافية "
        "لا تهتم بالمنطق أو المعنى، فقط قم بالتحليل النحوي كما هو:\n\n"
        "مثال 1: ذهب أحمد إلى المدرسة.\n"
        "الإعراب: ذهب: فعل ماضٍ مبني على الفتح، أحمد: فاعل مرفوع وعلامة رفعه الضمة الظاهرة على آخره، "
        "إلى: حرف جر، المدرسة: اسم مجرور وعلامة جره الكسرة الظاهرة على آخره.\n\n"
        "مثال 2: السماء صافية اليوم.\n"
        "الإعراب: السماء: مبتدأ مرفوع وعلامة رفعه الضمة الظاهرة على آخره، صافية: خبر مرفوع وعلامة رفعه الضمة الظاهرة على آخره، "
        "اليوم: ظرف زمان منصوب وعلامة نصبه الفتحة الظاهرة على آخره.\n\n"
        "مثال 3: الطالب يذاكر دروسه بجدية.\n"
        "الإعراب: الطالب: مبتدأ مرفوع وعلامة رفعه الضمة الظاهرة على آخره، يذاكر: فعل مضارع مرفوع وعلامة رفعه الضمة الظاهرة على آخره، "
        "دروسه: مفعول به منصوب وعلامة نصبه الفتحة الظاهرة على آخره، والهاء: ضمير متصل في محل جر بالإضافة، بجدية: جار ومجرور.\n\n"
        "مثال 4: القمر يضيء السماء ليلاً.\n"
        "الإعراب: القمر: مبتدأ مرفوع وعلامة رفعه الضمة الظاهرة على آخره، يضيء: فعل مضارع مرفوع وعلامة رفعه الضمة الظاهرة على آخره، "
        "السماء: مفعول به منصوب وعلامة نصبه الفتحة الظاهرة على آخره، ليلاً: ظرف زمان منصوب وعلامة نصبه الفتحة الظاهرة على آخره.\n\n"
        f"الجملة: {sentence}"
    )

    body = {
        "input": validation_prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 50,
            "repetition_penalty": 1.1
        },
        "model_id": MODEL_ID,
        "project_id": PROJECT_ID
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(API_URL, headers=headers, json=body)

    if response.status_code != 200:
        return {"error": f"في مشكلة: {response.text}"}

    validation_result = response.json().get('results', [{}])[0].get('generated_text', '')

    if "غير مكتملة" in validation_result or "غير مفهومة" in validation_result:
        return {"error": "الحقييقققهه، الجملة قصيرة بزيادة أو فيها رموز غير مفهومة. 🙃"}

    return analyze_sentence_with_allam(sentence)

# Function to analyze a sentence using the IBM model
def analyze_sentence_with_allam(sentence):
    access_token = get_access_token()
    if not access_token:
        return {"error": "Failed to obtain access token. Please check the API key and network connection."}

    body = {
        "input": (
            "رجاءً قم بإعراب كامل للجملة التالية فقط ولا تقدم أي معلومات إضافية:\n\n"
            "مثال 1: ذهب أحمد إلى المدرسة.\n"
            "الإعراب: ذهب: فعل ماضٍ مبني على الفتح، أحمد: فاعل مرفوع وعلامة رفعه الضمة الظاهرة على آخره، "
            "إلى: حرف جر، المدرسة: اسم مجرور وعلامة جره الكسرة الظاهرة على آخره.\n\n"
            "مثال 2: السماء صافية اليوم.\n"
            "الإعراب: السماء: مبتدأ مرفوع وعلامة رفعه الضمة الظاهرة على آخره، صافية: خبر مرفوع وعلامة رفعه الضمة الظاهرة على آخره، "
            "اليوم: ظرف زمان منصوب وعلامة نصبه الفتحة الظاهرة على آخره.\n\n"
            "مثال 3: الطالب يذاكر دروسه بجدية.\n"
            "الإعراب: الطالب: مبتدأ مرفوع وعلامة رفعه الضمة الظاهرة على آخره، يذاكر: فعل مضارع مرفوع وعلامة رفعه الضمة الظاهرة على آخره، "
            "دروسه: مفعول به منصوب وعلامة نصبه الفتحة الظاهرة على آخره، والهاء: ضمير متصل في محل جر بالإضافة، بجدية: جار ومجرور.\n\n"
            "مثال 4: القمر يضيء السماء ليلاً.\n"
            "الإعراب: القمر: مبتدأ مرفوع وعلامة رفعه الضمة الظاهرة على آخره، يضيء: فعل مضارع مرفوع وعلامة رفعه الضمة الظاهرة على آخره، "
            "السماء: مفعول به منصوب وعلامة نصبه الفتحة الظاهرة على آخره، ليلاً: ظرف زمان منصوب وعلامة نصبه الفتحة الظاهرة على آخره.\n\n"
            f"الجملة: {sentence}\nالإعراب:"
        ),
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 300,
            "repetition_penalty": 1.2
        },
        "model_id": MODEL_ID,
        "project_id": PROJECT_ID
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(API_URL, headers=headers, json=body)

    if response.status_code != 200:
        return {"error": f"في مشكلة: {response.text}"}

    result = response.json().get('results', [{}])[0].get('generated_text', '').strip()

    if not result:
        result = "الجملة غير صحيحة أو لا يمكن تحليلها. جرب جملة ثانية! 😊"

    return {"result": result}

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to analyze a sentence submitted by the user
@app.route('/analyze', methods=['POST'])
def analyze_sentence():
    sentence = request.json.get('sentence')

    if not sentence or len(sentence.strip()) < 2:
        return jsonify({'error': 'الجملة قصيرة جدًا. 🙃'}), 400

    analysis = validate_and_analyze_sentence(sentence)

    if 'error' in analysis:
        return jsonify({'error': analysis['error']}), 400

    add_to_history(sentence, analysis['result'])
    return jsonify(analysis)

# Random sentences for testing analysis
RANDOM_SENTENCES = [
    "ذهب أحمد إلى المدرسة.",
    "السيارة سريعة جداً.",
    "الطفل يلعب بالكرة.",
    "السماء صافية اليوم.",
    "القطط تلعب في الحديقة.",
    "المعلم يشرح الدرس بوضوح.",
    "أكلتُ تفاحة لذيذة.",
    "الزهور جميلة في الربيع.",
    "نجحتُ في الامتحان بفضل الله.",
    "أحب القراءة في الصباح.",
    "الجندي يحمي الوطن.",
    "الشمس مشرقة في السماء.",
    "اشتريتُ كتابًا جديدًا من المكتبة.",
    "المهندس يبني المباني العالية.",
    "الأم تهتم بأطفالها.",
    "الطبيب يعالج المرضى.",
    "التاجر يبيع البضائع في السوق.",
    "الرياضي يجري بسرعة.",
    "العصفور يغرد على الشجرة."
]

# Route to get a random sentence
@app.route('/random-sentence', methods=['GET'])
def random_sentence():
    sentence = random.choice(RANDOM_SENTENCES)
    return jsonify({'sentence': sentence})

# Quiz questions for grammar practice
QUIZ_QUESTIONS = [
    {
        'question': "الطلاب يدرسون بجدية.",
        'options': ["مبتدأ", "خبر", "فاعل"],
        'correct': "مبتدأ",
        'instruction': "ما هو إعراب 'الطلاب' في هذه الجملة؟"
    },
    {
        'question': "قرأتُ كتبًا كثيرة.",
        'options': ["مفعول به", "فاعل", "حال"],
        'correct': "مفعول به",
        'instruction': "ما هو إعراب 'كتبًا' في هذه الجملة؟"
    },
    {
        'question': "البنات نشيطات.",
        'options': ["مبتدأ", "خبر", "جمع مؤنث سالم"],
        'correct': "جمع مؤنث سالم",
        'instruction': "ما هو إعراب 'البنات' في هذه الجملة؟"
    },
    {
        'question': "المعلمات ماهرات في التدريس.",
        'options': ["مبتدأ", "خبر", "جمع مؤنث سالم"],
        'correct': "جمع مؤنث سالم",
        'instruction': "ما هو إعراب 'المعلمات' في هذه الجملة؟"
    },
    {
        'question': "الفاعل في الجملة يرفع بالـ...",
        'options': ["الضمة", "الفتحة", "الكسرة"],
        'correct': "الضمة",
        'instruction': "ما هي علامة رفع الفاعل؟"
    },
    {
        'question': "المفعول به في الجملة ينصب بالـ...",
        'options': ["الفتحة", "الضمة", "الكسرة"],
        'correct': "الفتحة",
        'instruction': "ما هي علامة نصب المفعول به؟"
    },
    {
        'question': "المضاف إليه يجر بالـ...",
        'options': ["الكسرة", "الضمة", "الفتحة"],
        'correct': "الكسرة",
        'instruction': "ما هي علامة جر المضاف إليه؟"
    },
    {
        'question': "اجتهدتُ في دراستي. ما هو إعراب 'اجتهدتُ'؟",
        'options': ["فعل ماضٍ", "فعل مضارع", "اسم"],
        'correct': "فعل ماضٍ",
        'instruction': "ما هو نوع الفعل 'اجتهدتُ' في هذه الجملة؟"
    },
    {
        'question': "الصيف حار في الرياض. ما هو إعراب 'حار'؟",
        'options': ["مبتدأ", "خبر", "صفة"],
        'correct': "خبر",
        'instruction': "ما هو إعراب 'حار' في هذه الجملة؟"
    },
    {
        'question': "يُكرم الرجل ضيفه. ما هو إعراب 'الرجل'؟",
        'options': ["مبتدأ", "فاعل", "مفعول به"],
        'correct': "فاعل",
        'instruction': "ما هو إعراب 'الرجل' في هذه الجملة؟"
    },
    {
        'question': "الطالب المجتهد مميز. ما هو إعراب 'المجتهد'؟",
        'options': ["نعت", "مبتدأ", "خبر"],
        'correct': "نعت",
        'instruction': "ما هو إعراب 'المجتهد' في هذه الجملة؟"
    },
    {
        'question': "الممرضات مجتهدات في العمل.",
        'options': ["مبتدأ", "خبر", "جمع مؤنث سالم"],
        'correct': "جمع مؤنث سالم",
        'instruction': "ما هو إعراب 'الممرضات' في هذه الجملة؟"
    },
    {
        'question': "الطالبات يحضرن الدروس بانتظام.",
        'options': ["مبتدأ", "جمع مؤنث سالم", "مفعول به"],
        'correct': "جمع مؤنث سالم",
        'instruction': "ما هو إعراب 'الطالبات' في هذه الجملة؟"
    },
    {
        'question': "المدرسة الكبيرة جميلة.",
        'options': ["مبتدأ", "صفة", "مفعول به"],
        'correct': "مبتدأ",
        'instruction': "ما هو إعراب 'المدرسة' في هذه الجملة؟"
    },
    {
        'question': "الطائرة سريعة جدًا.",
        'options': ["مبتدأ", "خبر", "فاعل"],
        'correct': "مبتدأ",
        'instruction': "ما هو إعراب 'الطائرة' في هذه الجملة؟"
    },
    {
        'question': "الطالب المبدع ينجح دائمًا.",
        'options': ["مبتدأ", "نعت", "مفعول به"],
        'correct': "مبتدأ",
        'instruction': "ما هو إعراب 'الطالب' في هذه الجملة؟"
    },
    {
        'question': "رأيتُ المعلمة في الفصل.",
        'options': ["فاعل", "مضاف", "مفعول به"],
        'correct': "مفعول به",
        'instruction': "ما هو إعراب 'المعلمة' في هذه الجملة؟"
    },
    {
        'question': "جاءت النساء إلى الاجتماع.",
        'options': ["مبتدأ", "جمع مؤنث سالم", "خبر"],
        'correct': "جمع مؤنث سالم",
        'instruction': "ما هو إعراب 'النساء' في هذه الجملة؟"
    },
    {
        'question': "المثنى في الجملة يُرفع بالـ...",
        'options': ["الألف", "الضمة", "الفتحة"],
        'correct': "الألف",
        'instruction': "ما هي علامة رفع المثنى؟"
    },
    {
        'question': "البنات مجتهدات. ما هو إعراب 'مجتهدات'؟",
        'options': ["نعت", "جمع مؤنث سالم", "حال"],
        'correct': "جمع مؤنث سالم",
        'instruction': "ما هو إعراب 'مجتهدات' في هذه الجملة؟"
    },
    {
        'question': "اشتريتُ عشر كتب. ما هو إعراب 'كتب'؟",
        'options': ["مضاف", "تمييز", "مفعول به"],
        'correct': "تمييز",
        'instruction': "ما هو إعراب 'كتب' في هذه الجملة؟"
    },
    {
        'question': "التلميذان مجتهدان. ما هو إعراب 'التلميذان'؟",
        'options': ["مبتدأ", "مثنى", "مضاف"],
        'correct': "مثنى",
        'instruction': "ما هو إعراب 'التلميذان' في هذه الجملة؟"
    },
    {
        'question': "قابلتُ مريمَ في السوق.",
        'options': ["ممنوع من الصرف", "مفعول به", "حال"],
        'correct': "ممنوع من الصرف",
        'instruction': "ما هو إعراب 'مريم' في هذه الجملة؟"
    },
    {
        'question': "ضربتُ ضربًا شديدًا. ما هو إعراب 'ضربًا'؟",
        'options': ["مفعول مطلق", "مفعول به", "حال"],
        'correct': "مفعول مطلق",
        'instruction': "ما هو إعراب 'ضربًا' في هذه الجملة؟"
    },
    {
        'question': "كانت السماء صافية. ما هو إعراب 'صافية'؟",
        'options': ["خبر كان", "حال", "صفة"],
        'correct': "خبر كان",
        'instruction': "ما هو إعراب 'صافية' في هذه الجملة؟"
    },
    {
        'question': "الجملة: 'كانت الفتاة سعيدة'. ما هو إعراب 'سعيدة'؟",
        'options': ["حال", "خبر كان", "نعت"],
        'correct': "خبر كان",
        'instruction': "ما هو إعراب 'سعيدة' في هذه الجملة؟"
    }
]

# Route to get a quiz question
@app.route('/get-quiz-question', methods=['GET'])
def get_quiz_question():
    question = random.choice(QUIZ_QUESTIONS)
    return jsonify(question)

# Route to check the submitted quiz answer
@app.route('/submit-quiz-answer', methods=['POST'])
def submit_quiz_answer():
    selected_answer = request.json.get('answer')
    correct_answer = request.json.get('correct')

    if selected_answer == correct_answer:
        return jsonify({'feedback': 'إجابتك صحيحة! 🎉'})
    else:
        return jsonify({'feedback': 'إجابتك خاطئة، حاول مرة أخرى. 😅'})

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)