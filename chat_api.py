from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

# 1️⃣ **處理 ChatGPT 回應**
@app.route("/chat_response", methods=["POST"])
def chat_response():
    data = request.get_json()
    nickname = data.get("nickname", "匿名")
    age = data.get("age", "未知")
    gender = data.get("gender", "未知")
    relationship = data.get("relationship", "未知")
    user_message = data.get("message", "")
    
    if not user_message.strip():
        return jsonify({"response": "請輸入有效的訊息"})
    
    system_prompt = (
        f"你是一名感情諮商師，請針對用戶的問題提供溫暖且有幫助的建議。\n"
        f"使用者資訊如下：\n"
        f"- 暱稱: {nickname}\n"
        f"- 年齡: {age}\n"
        f"- 性別: {gender}\n"
        f"- 感情狀態: {relationship}\n"
    )
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    
    chatgpt_response = completion.choices[0].message.content.strip()
    return jsonify({"response": chatgpt_response})

if __name__ == "__main__":
    app.run(debug=True)
