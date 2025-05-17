from flask import Flask, render_template, request, send_file
import pandas as pd
import joblib
import os
from metric_extractor import extract_metrics


app = Flask(__name__)
model = joblib.load('model/model.joblib')
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

REQUIRED_FEATURES = [
    'TCLOC', 'LLOC', 'TNA', 'NM', 'PUA', 'TLLOC', 'NLE',
    'TNLPM', 'TLOC', 'NLPM', 'NLM', 'TNLM', 'NOI', 'TNOS', 'NOS', 'NL'
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    uploaded_file = request.files['file']
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(file_path)
    df = pd.read_csv(file_path)

    missing_cols = [col for col in REQUIRED_FEATURES if col not in df.columns]
    if missing_cols:
        return f"Error: Missing columns: {missing_cols}", 400

    df["Predicted Number of Bugs"] = model.predict(df[REQUIRED_FEATURES])
    output_path = os.path.join(UPLOAD_FOLDER, "predicted_results.csv")
    df.to_csv(output_path, index=False)

    return render_template(
        "result.html",
        table=df.to_html(classes="min-w-full divide-y divide-gray-200 text-center", index=False, border=0, justify="center"),
        csv_download_link="/download"
    )

@app.route("/analyze", methods=["POST"])
def analyze():
    uploaded_files = request.files.getlist("files")
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))
    for file in uploaded_files:
        if file.filename:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    metrics_csv = os.path.join(UPLOAD_FOLDER, "metrics.csv")
    extract_metrics(UPLOAD_FOLDER, metrics_csv)
    df = pd.read_csv(metrics_csv)

    # Remove "File" column if present for prediction
    if 'File' in df.columns:
        df_pred = df[REQUIRED_FEATURES].copy()
    else:
        df_pred = df

    missing_cols = [col for col in REQUIRED_FEATURES if col not in df_pred.columns]
    if missing_cols:
        return f"Error: Missing columns: {missing_cols}", 400

    df["Predicted Number of Bugs"] = model.predict(df_pred[REQUIRED_FEATURES])
    output_path = os.path.join(UPLOAD_FOLDER, "predicted_results.csv")
    df.to_csv(output_path, index=False)

    return render_template(
        "result.html",
        table=df.to_html(classes="min-w-full divide-y divide-gray-200 text-center", index=False, border=0, justify="center"),
        csv_download_link="/download"
    )

@app.route("/download")
def download():
    return send_file(os.path.join(UPLOAD_FOLDER, "predicted_results.csv"), as_attachment=True)

@app.route("/generate-sample-csv")
def generate_sample_csv():
    sample_data = {
        'TCLOC': [50], 'LLOC': [40], 'TNA': [3], 'NM': [2], 'PUA': [5],
        'TLLOC': [100], 'NLE': [1], 'TNLPM': [6], 'TLOC': [90], 'NLPM': [3],
        'NLM': [1], 'TNLM': [2], 'NOI': [4], 'TNOS': [2], 'NOS': [3], 'NL': [6]
    }
    df = pd.DataFrame(sample_data)
    df.to_csv("sample_input.csv", index=False)
    return send_file("sample_input.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/webhook", methods=["POST"])
def webhook():
    # You can add security checks here (e.g., verify GitHub secret)
    event = request.headers.get('X-GitHub-Event', 'ping')
    payload = request.json

    # Trigger your automation pipeline here (e.g., call Jenkins)
    # For now, just log or print the event
    print(f"Received event: {event}")
    print(payload)
    return '', 200

