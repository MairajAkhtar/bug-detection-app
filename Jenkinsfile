pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/MairajAkhtar/bug-detection-app.git'
            }
        }

        stage('Set Up Python') {
            steps {
                bat '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Download Model') {
            steps {
                bat '''
                    source venv/bin/activate
                    python3 -c "
import os
import gdown

model_dir = 'model'
model_path = os.path.join(model_dir, 'model.joblib')
model_url = 'YOUR_GOOGLE_DRIVE_MODEL_LINK'  # Replace with the actual link

if not os.path.exists(model_dir):
    os.makedirs(model_dir)

if not os.path.exists(model_path):
    gdown.download(model_url, model_path, quiet=False)
"
                '''
            }
        }

        stage('Run Jenkins Prediction') {
            steps {
                bat '''
                    source venv/bin/activate
                    mkdir -p uploads
                    python3 -c "from app import model; import pandas as pd; df = pd.read_csv('uploads/metrics_from_jenkins.csv'); df['Predicted Bugs'] = model.predict(df); df.to_csv('uploads/predicted_from_jenkins.csv', index=False)"
                '''
            }
        }

        stage('Archive Output') {
            steps {
                archiveArtifacts artifacts: 'uploads/predicted_from_jenkins.csv', fingerprint: true
            }
        }
    }
}
