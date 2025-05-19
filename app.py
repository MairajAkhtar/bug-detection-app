from flask import Flask, render_template, request, send_file
import pandas as pd
import joblib
import os
import gdown
from metric_extractor import extract_metrics


def download_model():
    model_dir = 'model'
    model_path = os.path.join(model_dir, 'model.joblib')
    model_url = 'https://drive.google.com/uc?export=download&id=1Ezi8WW3XarglXXz7PDqZalw4ps8IioAX'

    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    if not os.path.exists(model_path):
        print("Downloading model.joblib from Google Drive...")
        gdown.download(model_url, model_path, quiet=False)
        print("Download complete.")
    else:
        print("Model already exists. Skipping download.")
    return model_path


app = Flask(__name__)
model_path = download_model()
model = joblib.load(model_path)
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
    app.run(host="0.0.0.0", port=5000, debug=True)


from flask import Flask, request

app = Flask(__name__)

@app.route('/github-webhook/', methods=['POST'])
def github_webhook():
    if request.method == 'POST':
        print("GitHub webhook received!")
        print(request.json)  # Print the payload
        return "OK", 200
    else:
        return "Method Not Allowed", 405
