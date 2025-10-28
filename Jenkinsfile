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
        stage('Docker Build') {
            steps {
                sh 'docker build -t pythonapp:latest .'
            }
        }
        stage('Docker Push') {
            steps {
                sh 'docker tag pythonapp:latest simraabid/pythonapp:latest'
                sh 'docker push simraabid/pythonapp:latest'
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f k8s-deployment.yaml
                    kubectl rollout status deployment/pythonapp-deployment
                    kubectl get pods
                    kubectl get services
                '''
            }
        }
    }

    post {
        always {
            sh '''
                echo "Final Pipeline Status:"
                kubectl get all
                kubectl -l app=pythonapp --tail=100 || true
            '''
        }
        success {
            sh 'echo Deployment successful!'
        }
        failure {
            sh '''
                echo Pipeline failed! Checking logs...
                kubectl describe pods -l app=pythonapp
                kubectl logs -l app=pythonapp --tail=200'
            '''
        }
    }
}