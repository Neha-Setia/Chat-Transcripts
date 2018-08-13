from flask import Flask, render_template
import cf_deployment_tracker
import os
from DecisionTreeQuestionnaire import DecisionTreeQuestionnaire
from flask import request
from flask import send_file
from flask_cors import CORS

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)
CORS(app)

port = int(os.getenv('PORT', 8000))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rest/chat', methods=['GET','POST'])
def get_next_question():
    
    if request.method == 'POST':
        print("request.json")
        print(request.json)
        
        if request.json:
            DecisionTreeQuestionnaire.temp_qtn_ans[request.json["question"]] = request.json["answer"]
        else:
            DecisionTreeQuestionnaire.temp_qtn_ans = {}
            
        current_question = DecisionTreeQuestionnaire.question_and_answer()
        print("question")
        print(current_question)
        return current_question
    else:
        return "Only POST method is accepted"


@app.route('/rest/decision-tree', methods=['GET'])
def getDecisionTreeImage():
    return send_file('decisiontree.png', mimetype='image/png')
    
    
if __name__ == '__main__':
    print("Starting...")
    DecisionTreeQuestionnaire.train()
    #DecisionTreeQuestionnaire
    app.run(host='0.0.0.0', port=port, debug=True)
    
