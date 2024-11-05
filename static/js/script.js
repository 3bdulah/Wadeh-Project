document.addEventListener('DOMContentLoaded', function () {
    // Elements from HTML
    const form = document.getElementById('analysis-form');
    const resultDiv = document.getElementById('result');
    const loadRandomBtn = document.getElementById('load-random-sentence');
    const quizContainer = document.getElementById('quiz-container');
    const quizInstructionElem = document.getElementById('quiz-instruction');
    const quizQuestionElem = document.getElementById('quiz-question');
    const quizOptionsElem = document.getElementById('quiz-options');
    const quizFeedbackElem = document.getElementById('quiz-feedback');
    const startMicrophoneBtn = document.getElementById('start-microphone');
    const transcriptElem = document.getElementById('transcript');
    const startQuizBtn = document.getElementById('start-quiz');
    const closeQuizBtn = document.getElementById('close-quiz');
    const nextQuestionBtn = document.getElementById('next-question');
    const progressBar = document.createElement('div');
    const historyBtn = document.getElementById('history-btn'); // Updated
    const helpBtn = document.getElementById('help-btn'); // Updated
    const historyContainer = document.getElementById('history-container');
    const helpContainer = document.getElementById('help-container');
    const historyList = document.getElementById('history-list');

    let quizVisible = false;
    let quizProgress = 0;

    progressBar.className = 'progress-bar';
    document.body.appendChild(progressBar);

    // Sounds for correct/wrong answers and results
    const correctSound = new Audio('/static/sounds/correct.mp3');
    const wrongSound = new Audio('/static/sounds/wrong.mp3');
    const resultSound = new Audio('/static/sounds/correct.mp3');

    // Loading spinner element
    const loadingSpinner = document.createElement('div');
    loadingSpinner.className = 'spinner';
    document.body.appendChild(loadingSpinner);

    let history = [];

    // Sentence analysis form submission
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const sentence = document.getElementById('sentence').value;
        resultDiv.style.display = 'none';
        loadingSpinner.style.display = 'block';

        // Send sentence for analysis
        fetch('/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json',},
            body: JSON.stringify({ sentence: sentence }),
        })
        .then(response => response.json())
        .then(data => {
            loadingSpinner.style.display = 'none';
            resultDiv.style.display = 'block';
            if (data.error) {
                resultDiv.className = 'error';
                resultDiv.innerHTML = 'الحقييقققهه، الجملة قصيرة بزيادة أو فيها رموز غير مفهومة.';
                wrongSound.play();
            } else {
                resultDiv.className = 'success';
                resultDiv.innerHTML = `<strong>النتيجة:</strong><br>${data.result}`;
                resultSound.play();
                updateHistory(sentence, data.result);
            }
        })
        .catch(error => {
            loadingSpinner.style.display = 'none';
            resultDiv.className = 'error';
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = 'فيه مشكلة حصلت، حاول ثاني.';
            console.error('Error:', error);
        });
    });

    // Load random sentence
    loadRandomBtn.addEventListener('click', function () {
        fetch('/random-sentence')
            .then(response => response.json())
            .then(data => {
                document.getElementById('sentence').value = data.sentence;
                transcriptElem.textContent = 'خذ جملة تسرح فيها!';
            });
    });

    // Toggle quiz visibility
    startQuizBtn.addEventListener('click', function () {
        quizVisible = true;
        startQuizBtn.style.display = 'none';
        closeQuizBtn.style.display = 'inline-block';
        quizContainer.style.display = 'block';
        loadNextQuestion();
    });

    // Close quiz button action
    closeQuizBtn.addEventListener('click', function () {
        quizVisible = false;
        startQuizBtn.style.display = 'inline-block';
        closeQuizBtn.style.display = 'none';
        quizContainer.style.display = 'none';
        quizProgress = 0;
        progressBar.style.width = '0%';
    });

    // Load next quiz question
    function loadNextQuestion() {
        fetch('/get-quiz-question')
            .then(response => response.json())
            .then(data => {
                quizInstructionElem.textContent = data.instruction;
                quizQuestionElem.textContent = data.question;
                quizOptionsElem.innerHTML = '';
                quizFeedbackElem.textContent = '';
                nextQuestionBtn.style.display = 'none';

                data.options.forEach(option => {
                    let li = document.createElement('li');
                    li.textContent = option;
                    li.addEventListener('click', function () {
                        if (option === data.correct) {
                            li.classList.add('correct-answer');
                            correctSound.play();
                            quizFeedbackElem.textContent = 'إجابتك ترفع الراس!';
                        } else {
                            li.classList.add('wrong-answer');
                            wrongSound.play();
                            quizFeedbackElem.textContent = 'واك واك، حاول مرة ثانيه.';
                        }
                        nextQuestionBtn.style.display = 'block';
                    });
                    quizOptionsElem.appendChild(li);
                });

                // Update quiz progress
                quizProgress += 1;
                progressBar.style.width = `${quizProgress}%`;
            });
    }

    // Next question button action
    nextQuestionBtn.addEventListener('click', function () {
        loadNextQuestion();
    });

    // Microphone button feedback
    startMicrophoneBtn.addEventListener('click', function () {
        transcriptElem.textContent = 'وش ذا الصوت الزين؟';
    });

    // Web Speech API setup for voice recognition
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'ar-SA';

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('sentence').value = transcript;
            transcriptElem.textContent = 'ما شاء الله، نطقك زي العسل!';
        };

        recognition.onerror = function (event) {
            transcriptElem.textContent = `خطأ في التعرف على الصوت: ${event.error}`;
        };

        startMicrophoneBtn.addEventListener('click', function () {
            recognition.start();
        });
    } else {
        startMicrophoneBtn.textContent = 'المتصفح لا يدعم التعرف على الصوت';
    }

    // Update history with new analysis results
    function updateHistory(sentence, result) {
        const historyItem = {
            sentence: sentence,
            result: result,
            date: new Date().toLocaleString()
        };
        history.push(historyItem);
        renderHistory();
    }

    // Render history items
    function renderHistory() {
        historyList.innerHTML = '';
        history.forEach(item => {
            const li = document.createElement('li');
            li.textContent = `${item.date}: ${item.sentence} - ${item.result}`;
            historyList.appendChild(li);
        });
    }

    // Toggle history section visibility
    historyBtn.addEventListener('click', function () {
        historyContainer.style.display = historyContainer.style.display === 'none' ? 'block' : 'none';
    });

    // Toggle help section visibility
    helpBtn.addEventListener('click', function () {
        helpContainer.style.display = helpContainer.style.display === 'none' ? 'block' : 'none';
    });
});