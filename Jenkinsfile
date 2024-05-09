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
        stage('SonarQube analysis') {
            steps {
                withSonarQubeEnv('sonar-server') {
                    sh 'docker run --rm -e SONAR_HOST_URL="http://public_ip:9000" -e SONAR_LOGIN="sqp_ba2334be835d028b2aed8efcf830bfe5b9d84392" -v "$(pwd):/usr/src" sonarsource/sonar-scanner-cli -Dsonar.projectKey=flask_project -Dsonar.sources=. -Dsonar.language=py'
                }
            }
        }
                
    }
}
