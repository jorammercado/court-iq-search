from flask import Flask, request, jsonify
import json
from fuzzywuzzy import fuzz
import os

app = Flask(__name__)

# Load data from JSON file
with open('allConvertedData.json', 'r') as file:
    data = json.load(file)

# Convert the list to a dictionary for Q&A
qa_dict = {data[i].lower(): data[i + 1] for i in range(0, len(data), 2)}

def find_closest_question(user_question, questions):
    user_question = user_question.lower()
    max_similarity = 0
    closest_question = None

    for question in questions:
        similarity = fuzz.ratio(user_question, question)
        if similarity > max_similarity:
            max_similarity = similarity
            closest_question = question

    return closest_question, max_similarity

def generate_response(user_question):
    closest_question, max_similarity = find_closest_question(user_question, qa_dict.keys())
    
    if max_similarity > 60:
        return qa_dict[closest_question]
    else:
        return "I'm not sure how to answer that. Can you please ask another question or rephrase your question?"

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    user_question = data.get('question', '')
    if not user_question:
        return jsonify({'error': 'No question provided'}), 400
    
    response = generate_response(user_question)
    return jsonify({'answer': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))  # Default to 5001 if PORT environment variable is not set
    app.run(debug=False, host='0.0.0.0', port=port)
