# واضح (Wadeh) - Arabic Grammar Analysis Tool

**Wadeh** is an AI-driven web application that automates Arabic grammar analysis using the ALLaM model, hosted on IBM Watsonx. The tool assists Arabic language learners, educators, and enthusiasts by providing accurate and accessible grammatical analysis in Arabic.

## Project Overview
Wadeh was developed as part of the **Allam Challenge 2024** hackathon, chosen from over 200 ideas for its unique contribution to Arabic language education. Using advanced prompt engineering with IBM Watsonx, Wadeh can analyze complex grammatical structures and assist users in understanding Arabic syntax.

### Key Features
- **Automated Grammar Analysis**: Provides i'rab (إعراب) analysis for Arabic sentences.
- **Random Sentence Generator**: Practice with randomly generated sentences.
- **Grammar Quiz**: Interactive quizzes to test users' knowledge of Arabic grammar.
- **User History and Help Sections**: Access analysis history and FAQs for a better user experience.

## Installation
To set up Wadeh locally, follow these steps:

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/wadeh.git
   cd wadeh
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Setup
Create a `.env` file in the root directory of the project to store environment variables. Use the following format for the file:

```plaintext
MODEL_ID=sdaia/allam-1-13b-instruct
API_URL=https://eu-de.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29
IAM_TOKEN_URL=https://iam.cloud.ibm.com/identity/token
API_KEY=your_ibm_api_key
PROJECT_ID=your_project_id
SECRET_KEY=your_flask_secret_key
```

**Note**: Make sure to replace `your_ibm_api_key`, `your_project_id`, and `your_flask_secret_key` with your actual values. Keep this `.env` file private and do not share it.

### Usage
Start the Flask server:
```bash
flask run
```
Open a web browser and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to use Wadeh.

## Project Structure
```plaintext
wadeh/
├── main.py                # Main application file
├── .env                   # Environment variables
├── templates/
│   └── index.html         # HTML template
├── static/
│   ├── css/
│   │   └── styles.css     # CSS file for styling
│   │   └── SF.Arabic.ttf  # Font
│   ├── js/
│   │   └── script.js      # JavaScript file for functionality
│   ├── sounds/            # Sound effects for correct/incorrect answers
│   │   ├── correct.mp3    # Correct answer sound effect
│   │   └── wrong.mp3      # Incorrect answer sound effect
│   └── favicon.ico        # Favicon for the application
├── requirements.txt       # Python dependencies
├── LICENSE.txt            # License file
└── README.md              # Project documentation
```


## Features
- **Sentence Analysis**: Enter an Arabic sentence, and Wadeh will analyze its grammar structure, providing detailed i'rab.
- **Grammar Quiz**: Test your knowledge with an interactive grammar quiz featuring various questions and instant feedback.
- **Random Sentence Generator**: Generate a random Arabic sentence to practice analysis or test your understanding.
- **User History & Help Section**: Access your analysis history and view FAQs for guidance.

## Technologies Used
- **Python**: Backend logic and API handling
- **Flask**: Web framework to handle requests and render pages
- **HTML, CSS, JavaScript**: Frontend for user interface
- **IBM Watsonx**: Model hosting and prompt engineering for Arabic grammar analysis

## Acknowledgments
This project was developed as part of the Allam Challenge 2024, focusing on Large Language Models (LLMs) for the Arabic language.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any inquiries or contributions, please reach out to **Abdullah Hani Abdellatif Al-Shobaki** at ***abdullah.hani2004@icloud.com***.
