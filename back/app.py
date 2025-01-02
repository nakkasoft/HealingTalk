from flask import Flask, jsonify, make_response

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/getquestionmock', methods=['GET'])
def getquestionmock():

    response = make_response(jsonify(
    {"option":["원하는 기업에 지원할 자격이 부족하다고 느껴지는 열등감.", 
    "면접에서의 긴장과 실수로 인해 자신감을 잃는 상황.",
    "특정 분야에 대한 경험 부족으로 도전을 망설이는 마음.",
    "취업 시장에서의 경쟁 과열로 느껴지는 좌절감.",
    "반복적인 탈락 경험으로 인한 자존감 하락.",
    "취업 준비 기간이 길어지며 느껴지는 부모님이나 주변의 압박.",
    "나이에 따른 경력 부족이나 높은 연봉 기대치의 괴리감.",
    "지원한 직무와 자신의 적성 간의 불일치에서 오는 혼란.",
    "장기적인 직업 전망을 고려하지 못해 느끼는 불안.",
    "취업 준비와 동시에 생활비를 벌어야 하는 이중 부담."]}))

    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response

@app.route('/getquestion')
def getquestion():
   return 'This is My Page!'

if __name__ == '__main__':  
   app.run('0.0.0.0', port=5677, debug=True)

