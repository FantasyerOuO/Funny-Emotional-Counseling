from flask import Flask, render_template, request
from werkzeug.utils import escape
from Flask_GPT import ChatGPT

app = Flask(__name__)

@app.route('/home')
def hello_world():
    return render_template("homepage.html")

# 聊天頁面
@app.route('/start_counseling', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        systemPrompt = request.form['systemPrompt']
        userMessage = request.form['userMessage']
        completion = ChatGPT(systemPrompt, userMessage)
        return render_template("chat.html", systemPrompt=systemPrompt, userMessage=userMessage, completion=completion)
    else:
        return render_template("chat.html")
    
# 回饋頁面
@app.route('/feedback_page')
def feedback():
    return render_template("feedback.html")

if __name__ == "__main__":
    app.run(debug=True)