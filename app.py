from flask import Flask, render_template, request, send_file
from gtts import gTTS
import io
import json

app = Flask(__name__)

with open("knowledge_base.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)


def find_answer(subject, question):

  subject_data = knowledge_base.get(subject, [])
  question_lower = question.lower()
  for entry in subject_data:
     for kw in entry["keywords"]:
        if kw.lower() in question_lower:
           return entry["answer"]
     return "මෙම ප්‍රශ්නය සඳහා මට පිළිතුරක් නැත."
  



@app.route("/")
def index():
   return render_template("index.html")



@app.route("/ask", methods=["POST"])
def ask():
   data = request.json
   subject = data.get("subject")
   question = data.get("question")

   answer_text = find_answer(subject, question)

   tts = gTTS(text=answer_text, lang='si')
   mp3_fp = io.BytesIO()
   tts.write_to_fp(mp3_fp)
   mp3_fp.seek(0)

   return send_file(mp3_fp, mimetype="audio/mpeg", as_attachment=False, download_name="answer.mp3")


if __name__ == "__main__":
   app.run(debug=True)



      