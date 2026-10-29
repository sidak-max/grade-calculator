pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'sidaksingh1'
        IMAGE_REPO = 'sidaksingh1/grade-calculator'
    }

    stages {
        stage('Source Code') {
            steps {
                echo 'Source code is checked out from the repository.'
                git branch: 'main', url: 'https://github.com/sidak-max/grade-calculator.git'
            }
        }

        stage('Version Control') {
            steps {
                echo 'Checking version control status.'
                sh '''
                    git --version
                    git status
                    git rev-parse --short HEAD
                '''
            }
        }

        stage('Continuous Integration') {
            steps {
                echo 'Installing dependencies and running tests.'
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest -v
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'Building Docker image with commit SHA tag.'
                sh '''
                    docker build -t ${IMAGE_REPO}:${GIT_COMMIT} .
                '''
            }
        }

        stage('Deployment') {
            steps {
                echo 'Deploying the built image to Kubernetes.'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${IMAGE_REPO}:${GIT_COMMIT}
                        sed -i "s|IMAGE_PLACEHOLDER|${IMAGE_REPO}:${GIT_COMMIT}|g" k8s/deployment.yaml
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml
                        kubectl rollout status deployment/grade-calculator
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
            sh 'docker logout || true'
        }
    }
}
