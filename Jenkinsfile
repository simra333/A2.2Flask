pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'jenkins-setup', url: 'https://github.com/simra333/A2.2Flask.git'
            }
        }

        stage('Build') {
            steps {
                sh 'echo Building the application...'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && python3 -m pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh '. venv/bin/activate && python -m logger.test_flow_logger'
                sh 'echo Test completed successfully!'
            }
        }
    }
}