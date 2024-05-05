pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/jainvaibhav2000/flask_project.git']])
            }
        }
        stage('Build and Run (deploy) on Docker Compose') {
            steps {
                sh 'docker-compose up -d --build'
            }
        }
        
    }
}
