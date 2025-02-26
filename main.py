from flask import Flask, request, jsonify, render_template
import csv
import os
import datetime

app = Flask(__name__)

DAILY_FEEDBACK_DIR = "feedback_logs"
NEW_50_FEEDBACK_FILE = "new50feedback.csv"
MAX_FEEDBACKS = 50  # 限制最新回饋筆數

# 確保存放回饋的資料夾存在
if not os.path.exists(DAILY_FEEDBACK_DIR):
    os.makedirs(DAILY_FEEDBACK_DIR)

# 取得當日回饋檔案名稱
def get_daily_feedback_file():
    today = datetime.date.today().strftime("%Y-%m-%d")
    return os.path.join(DAILY_FEEDBACK_DIR, f"{today}_feedback.csv")

# 1️⃣ **提交回饋並儲存到 CSV**
@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "回饋內容不可為空"}), 400
    
    timestamp = data.get("time", "")
    new_feedback = [timestamp, text]
    daily_feedback_file = get_daily_feedback_file()
    
    # 儲存到每日回饋檔案
    with open(daily_feedback_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(new_feedback)
    
    # 更新 `new50feedback.csv`
    feedbacks = []
    if os.path.exists(NEW_50_FEEDBACK_FILE):
        with open(NEW_50_FEEDBACK_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            feedbacks = list(reader)
    
    feedbacks.insert(0, new_feedback)  # 插入新回饋
    feedbacks = feedbacks[:MAX_FEEDBACKS]  # 保留最新 50 筆
    
    with open(NEW_50_FEEDBACK_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(feedbacks)
    
    return jsonify({"message": "回饋已提交"}), 200

# 2️⃣ **獲取所有回饋 (供首頁使用)**
@app.route("/get_feedbacks")
def get_feedbacks():
    feedbacks = []
    if os.path.exists(NEW_50_FEEDBACK_FILE):
        with open(NEW_50_FEEDBACK_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            feedbacks = [{"time": row[0], "text": row[1]} for row in reader]
    return jsonify(feedbacks)

# 3️⃣ **回饋頁面**
@app.route("/feedback_page")
def feedback_page():
    return render_template("feedback.html")

# 4️⃣ **首頁**
@app.route("/")
def homepage():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)
