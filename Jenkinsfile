pipeline {
    agent any

    environment {
        IMAGE_NAME = 'bug-detection-tool'
        CONTAINER_NAME = 'bug-detection-app'
        PORT = '5000'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/MairajAkhtar/bug-detection-app.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                bat "docker build -t %IMAGE_NAME% ."
            }
        }
        stage('Stop Previous Container') {
            steps {
                bat "docker rm -f %CONTAINER_NAME% || exit 0"
            }
        }
        stage('Run Docker Container') {
            steps {
                bat "docker run -d --name %CONTAINER_NAME% -p %PORT%:5000 %IMAGE_NAME%"
            }
        }
    }
}
