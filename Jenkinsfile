pipeline {
    agent any

    tools {
        python 'Python 3.11'  // Use the name from Global Tool Configuration
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/MairajAkhtar/bug-detection-app.git'
            }
        }

        stage('Set Up Python') {
            steps {
                bat '''
                    python -m venv venv
                    venv\\Scripts\\activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Download Model') {
            steps {
                bat '''
                    venv\\Scripts\\activate
                    python -c "
import os
import gdown

model_dir = 'model'
model_path = os.path.join(model_dir, 'model.joblib')
model_url = 'https://drive.google.com/uc?export=download&id=1Ezi8WW3XarglXXz7PDqZalw4ps8IioAX'

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
                    venv\\Scripts\\activate
                    mkdir uploads
                    python -c "from app import model; import pandas as pd; df = pd.read_csv('uploads/metrics_from_jenkins.csv'); df['Predicted Bugs'] = model.predict(df); df.to_csv('uploads/predicted_from_jenkins.csv', index=False)"
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
