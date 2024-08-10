from flask import Flask, render_template, request as req
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def Index():
    return render_template("index.html")

@app.route("/Summarize", methods=["GET", "POST"])
def Summarize():
    if req.method == "POST":
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}
        data = req.form["data"]
        maxL = int(req.form["maxL"])
        minL = maxL // 4

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        output = query({
            "inputs": data,
            "parameters": {"min_length": minL, "max_length": maxL},
        })

        # Debugging: Print the output to check its structure
        print("API Response:", output)

        # Check if output is a list and has the expected structure
        if isinstance(output, list) and len(output) > 0 and "summary_text" in output[0]:
            summary_text = output[0]["summary_text"]
        else:
            summary_text = "Error: Unexpected API response format."

        return render_template("index.html", result=summary_text)
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
