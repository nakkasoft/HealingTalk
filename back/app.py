from flask import Flask, jsonify, make_response, request
import openai
import os

app = Flask(__name__)

topic_data = {"topic_job":["원하는 기업에 지원할 자격이 부족하다고 느껴지는 열등감.",
"면접에서의 긴장과 실수로 인해 자신감을 잃는 상황.",
"특정 분야에 대한 경험 부족으로 도전을 망설이는 마음.",
"취업 시장에서의 경쟁 과열로 느껴지는 좌절감.",
"반복적인 탈락 경험으로 인한 자존감 하락.",
"취업 준비 기간이 길어지며 느껴지는 부모님이나 주변의 압박.",
"나이에 따른 경력 부족이나 높은 연봉 기대치의 괴리감.",
"지원한 직무와 자신의 적성 간의 불일치에서 오는 혼란.",
"장기적인 직업 전망을 고려하지 못해 느끼는 불안.",
"취업 준비와 동시에 생활비를 벌어야 하는 이중 부담."],
"topic_stress":["일상 속에서 느껴지는 책임감과 의무감의 과중.",
"학업 성적이나 직장 성과에 대한 끊임없는 압박.",
"충분히 쉬지 못해 몸과 마음이 지치는 상황.",
"주변 사람들에게 자신의 감정을 표현하지 못해 생기는 답답함.",
"스트레스 해소 방법을 찾지 못하고 감정을 억누르는 경우.",
"체력 저하와 함께 찾아오는 정신적 피로.",
"내가 잘하고 있는 걸까?라는 의심으로 인한 불안감.",
"작은 실수에도 자책하며 스스로를 몰아세우는 태도.",
"스트레스를 받는 상황에서 회피하기만 해 생기는 문제 악화.",
"스트레스가 쌓여 신체적 증상(두통, 소화불량 등)이 나타나는 문제."],
"topic_move":["현재 직장의 안정성을 버리고 새로운 도전을 해야 한다는 부담감.",
"이직 후에도 비슷한 문제를 겪을까 봐 느끼는 두려움.",
"경력 단절로 인해 커리어가 퇴보하지 않을까 하는 걱정.",
"새로운 직장에서 동료들과 잘 어울리지 못할까 봐 느끼는 불안.",
"이전 직장 상사나 동료들과 관계를 정리하는 데서 오는 스트레스.",
"이직 과정에서 필요한 스킬이나 자격을 준비할 시간 부족.",
"이직 후 업무 강도나 연봉이 기대에 미치지 못할까 하는 고민.",
"가족이나 주변 사람들이 이직 결정을 이해하지 못할까 하는 걱정.",
"이직 후에도 행복하지 않다면 다시 무엇을 해야 할지 모르는 혼란.",
"이직 준비 과정에서 기존 업무와 병행하며 느끼는 체력적 부담."],
"topic_burnout":["끝없이 반복되는 업무로 인해 삶의 의미를 잃어가는 느낌.",
"쉬고 싶어도 일에 대한 압박으로 인해 휴식을 미루는 경우.",
"주변 동료와 비교하며 느끼는 자신에 대한 무기력감.",
"성과를 내기 위해 노력했지만 인정받지 못한다고 느끼는 좌절감.",
"일상에서 아무것도 하고 싶지 않은 상태로 이어지는 의욕 상실.",
"가족이나 친구와의 관계에서도 감정 소진을 느끼는 상황.",
"신체적 피로와 함께 집중력 저하로 이어지는 문제.",
"내가 이 일을 계속할 수 있을까?라는 미래에 대한 걱정.",
"번아웃을 극복하기 위한 방법을 찾지 못하고 방치하는 상태.",
"번아웃 상태를 주변에 털어놓기 어려워 혼자 끙끙 앓는 경우."],
"topic_depress":["특정한 이유 없이도 지속되는 무거운 감정.",
"좋아하던 일에도 흥미를 느끼지 못하고 무기력해지는 상태.",
"실패 경험으로 인해 나는 쓸모없는 사람 이라고 느끼는 자책감.",
"삶에 대한 의욕이 떨어지고 모든 것이 무의미하게 느껴지는 상황.",
"주변 사람들에게 자신의 상태를 숨기며 혼자 고립되는 경우.",
"우울한 감정을 풀 방법을 찾지 못하고 더 깊어지는 좌절감.",
"이 상태가 계속된다면 어떻게 될까? 라는 두려움.",
"작은 문제에도 과도하게 반응하며 감정 기복이 심해지는 상황.",
"수면 부족 또는 과다 수면으로 인해 일상에 지장이 생기는 경우.",
"우울함이 점차 몸의 건강에도 영향을 미치는 문제(소화불량, 두통 등)."],
"topic_anxious":["미래를 계획하는 과정에서 드는 막연한 두려움.",
"스스로에 대한 신뢰가 부족해 선택이 어려운 상황.",
"불확실한 상황에서 최악의 결과를 상상하며 느끼는 공포.",
"중요한 결정을 앞두고 내가 잘할 수 있을까? 하는 고민.",
"사회적 평가나 타인의 시선을 지나치게 의식하는 경우.",
"실패를 경험한 이후 다시 시도하기 어려워지는 심리적 장벽.",
"작은 실수에도 모든 것이 끝났다는 생각에 빠지는 극단적 사고.",
"미래의 경제적 상황이나 직업 안정성에 대한 걱정.",
"반복되는 불안으로 인해 집중력이 떨어지고 일상이 무너지는 상태.",
"불안감을 털어놓을 상대가 없어 홀로 감당하려는 부담감."],
"topic_love":["인간관계가 얕거나 단절된 상태에서 느껴지는 고립감.",
"친구나 가족에게 의지하고 싶지만 부담을 줄까 봐 망설이는 마음.",
"소셜 미디어 속 행복해 보이는 타인과 비교하며 느끼는 공허함.",
"바쁜 일상 속에서 관계를 유지할 여유를 찾지 못하는 문제.",
"혼자 있는 시간이 많아지며 점점 우울해지는 상태.",
"주변에 대화할 사람이 없다고 느껴지는 고독감.",
"타인에게 거절당하거나 소외될까 봐 먼저 다가가지 못하는 경우.",
"깊은 관계를 만들기 어렵다고 느끼며 생기는 불안감.",
"외로움을 해소하기 위해 무리하게 인간관계를 유지하려는 부담.",
"외로움이 지속되어 자신감과 자존감이 떨어지는 상태."],
"topic_lonely":["상대방과의 의견 차이에서 오는 갈등과 조율의 어려움.",
"상대방이 나를 정말로 사랑하는지에 대한 불확실성.",
"연애 중에도 외로움을 느끼는 경우.",
"경제적 문제(데이트 비용, 선물 등)로 인한 부담.",
"결혼에 대한 시각 차이와 그로 인한 불화.",
"상대방과 시간을 함께 보내지 못할 때 느끼는 서운함.",
"연애 경험 부족으로 인한 자신감 저하와 불안.",
"상대방의 과거 연애 경험이나 관계에 대한 질투심.",
"연애와 직장/학업 간의 균형을 맞추기 어려운 경우.",
"연애가 끝날 경우에 대한 두려움으로 깊은 관계를 맺기 어려운 상태."]}

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")  # 환경변수에서 가져오기

@app.route('/')
def home():
    return "Hello, 청년!"

@app.route('/getdetailedquestion', methods=['GET'])
def getquestionmock():
    type = request.args.get('type')
    print(type)
    print(topic_data[type])

    response = make_response(jsonify({"option":topic_data[type]}))

    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response

@app.route('/getcheercomment', methods=['GET'])
def getcheercomment():
    type = request.args.get('type', 'general')
    print(f"Requested type: {type}")

    # OpenAI API 호출
    prompt = f"'{type}'와 관련하여 힘이 되는 응원의 말을 해줘."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "너는 따뜻하고 희망적인 응원의 메시지를 주는 조언자야."},
                      {"role": "user", "content": prompt}],
            max_tokens=550
        )
        cheer_message = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        error_message = f"OpenAI API 호출 중 오류 발생: {str(e)}"
        print(error_message)
        cheer_message = "Cheer UP!!! (Error 발생)"
        return make_response(jsonify({"comment": cheer_message, "error": error_message}), 500)


    response = make_response(jsonify({"comment": cheer_message}))
    #response = make_response(jsonify({"comment":"Cheer UP!!!"}))

    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response

if __name__ == '__main__':  
   app.run('0.0.0.0', port=5677, debug=True)

