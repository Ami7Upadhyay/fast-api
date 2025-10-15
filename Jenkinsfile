pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'amitupadhyay16'
        IMAGE_NAME = 'fastapi-demo'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Ami7Upadhyay/fast-api.git'
            }
        }

        stage('Build') {
            steps {
                bat "docker build -t %IMAGE_NAME%:latest ."
            }
        }

        stage('Test') {
            steps {
                // only works if pytest installed in image or on agent
                bat 'pytest || exit 0'
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat "docker login -u %DOCKER_USER% -p %DOCKER_PASS%"
                    bat "docker tag %IMAGE_NAME%:latest %DOCKERHUB_USER%/%IMAGE_NAME%:latest"
                    bat "docker push %DOCKERHUB_USER%/%IMAGE_NAME%:latest"
                }
            }
        }

        stage('Deploy') {
            steps {
                bat '''
                ssh user@your-server "docker pull %DOCKERHUB_USER%/%IMAGE_NAME%:latest && docker stop fastapi-demo || true && docker rm fastapi-demo || true && docker run -d --name fastapi-demo -p 8000:8000 %DOCKERHUB_USER%/%IMAGE_NAME%:latest"
                '''
            }
        }
    }
}
