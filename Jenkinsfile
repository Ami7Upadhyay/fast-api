pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'amitupadhyay16'
        IMAGE_NAME = 'fastapi-demo'
        CONTAINER_NAME = 'fastapi-demo'
        HOST_PORT = '8090'        // Jenkins uses 8080, so deploy on 8090
        CONTAINER_PORT = '8000'   // Port your FastAPI app listens on inside container
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

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-cred',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat "echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin"
                    bat "docker tag %IMAGE_NAME%:latest %DOCKERHUB_USER%/%IMAGE_NAME%:latest"
                    bat "docker push %DOCKERHUB_USER%/%IMAGE_NAME%:latest"
                }
            }
        }

        stage('Deploy') {
            steps {
                // Stop and remove existing container if running
                bat """
                docker stop %CONTAINER_NAME% || exit 0
                docker rm %CONTAINER_NAME% || exit 0
                docker pull %DOCKERHUB_USER%/%IMAGE_NAME%:latest
                docker run -d --restart always --name %CONTAINER_NAME% -p %HOST_PORT%:%CONTAINER_PORT% %DOCKERHUB_USER%/%IMAGE_NAME%:latest
                """
            }
        }
    }
}
