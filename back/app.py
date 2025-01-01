from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/getquestionmock')
def mypage():
   return 'This is My Page!'


@app.route('/getquestion')
def mypage():
   return 'This is My Page!'

if __name__ == '__main__':  
   app.run('0.0.0.0', port=5677, debug=True)

