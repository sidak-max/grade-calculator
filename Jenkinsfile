pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/sidak-max/grade-calculator.git'
            }
        }

        stage('Test') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                    pytest -v
                '''
            }
        }

        stage('Build Docker image') {
            steps {
                sh 'docker build -t sidaksingh1/grade-calculator:${GIT_COMMIT} .'
            }
        }

        stage('Push Docker image') {
            steps {
                sh '''
                    echo $DOCKERHUB_TOKEN | docker login -u $DOCKERHUB_USERNAME --password-stdin
                    docker push sidaksingh1/grade-calculator:${GIT_COMMIT}
                '''
            }
        }
    }
}