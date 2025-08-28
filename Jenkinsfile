pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/RahulPashikanti22/trosky-development.git'
            }
        }
        stage('Build Images') {
            steps {
                script {
                    sh 'docker-compose build'
                }
            }
        }
        stage('Start Services') {
            steps {
                script {
                    sh 'docker-compose up -d'
                }
            }
        }
    }
}
