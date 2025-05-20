pipeline {
    agent any

    environment {
        IMAGE_NAME = 'mairajakhtar/bug-detection-app'
        CONTAINER_NAME = 'bug-detection-app'
        PORT = '5000'
        DOCKERHUB_CREDENTIALS = 'dockerhub' // Jenkins credentials ID
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/MairajAkhtar/bug-detection-app.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                bat "docker build -t %IMAGE_NAME%:latest ."
            }
        }
        stage('Stop Previous Container') {
            steps {
                bat "docker rm -f %CONTAINER_NAME% || exit 0"
            }
        }
        stage('Run Docker Container') {
            steps {
                bat "docker run -d --name %CONTAINER_NAME% -p %PORT%:5000 %IMAGE_NAME%:latest"
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat '''
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                        docker push %IMAGE_NAME%:latest
                    '''
                }
            }
        }
    }
}
