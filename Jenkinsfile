pipeline {
    agent any

    environment {
        APP_VERSION = 'v2.1'
        DOCKERHUB_USERNAME = 'simraabid'
        DOCKER_IMAGE = "${DOCKERHUB_USERNAME}/pythonapp:${APP_VERSION}"
        AKS_CLUSTER_NAME = 'pythonapp-aks-cluster-sa'
        AKS_RESOURCE_GROUP = 'A5.2-RG-Terraform'
    }

    stages {

        stage('Verify kubectl Configuration') {
            steps {
                sh '''
                    # Verify kubeconfig exists
                    if [ ! -f ~/.kube/config ]; then
                        echo "ERROR: kubeconfig not found at ~/.kube/config"
                        exit 1
                    fi
                    
                    # Verify kubectl can connect to cluster
                    kubectl cluster-info
                    kubectl get nodes
                '''
            }
        }

        stage('Checkout') {
            steps {
                git branch: 'test', url: 'https://github.com/simra333/A2.2Flask.git'
            }
        }

        stage('Build') {
            steps {
                sh '''
                    echo Building the application...
                    sudo apt-get update
                    sudo apt-get install -y python3.10-venv
                    python3 -m venv venv
                    . venv/bin/activate 
                    pip install --upgrade pip
                    pip install --upgrade setuptools>=78.1.1
                    pip install -r requirements.txt
                '''
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
                sh '''
                    echo "Building Docker image in: ${WORKSPACE}"
                    docker build --no-cache -t ${DOCKER_IMAGE} .
                '''
                }
            }
        stage('vulnerability scanning') {
            steps {
                sh '''
                    # Install and run Trivy
                    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy image --severity HIGH,CRITICAL ${DOCKER_IMAGE}
                '''
            }
        }
        stage('Docker Hub Login and Push') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh '''
                            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                            docker push ${DOCKER_IMAGE}
                        '''
                    }
                }
            }
        }
        stage('Deploy to AKS') {
            steps {
                sh '''
                    # Update the deployment with new image
                    kubectl set image deployment/pythonapp-deployment pythonapp=${DOCKER_IMAGE}
                    
                    # Trigger a rolling restart to ensure fresh pull
                    kubectl rollout restart deployment/pythonapp-deployment
                    
                    # Wait for rollout to complete
                    kubectl rollout status deployment/pythonapp-deployment --timeout=300s

                    # Wait for pods to be ready
                    kubectl wait --for=condition=ready pod -l app=pythonapp --timeout=60s
            
                    # Give terminating pods time to fully terminate
                    sleep 5
                    
                    # Verify deployment
                    kubectl get pods
                    kubectl describe pod -l app=pythonapp | grep "Image:"
                    kubectl get services
                    
                    # Verify templates in running pod
                    POD_NAME=$(kubectl get pod -l app=pythonapp -o jsonpath='{.items[0].metadata.name}')
                    kubectl exec $POD_NAME -- ls -la /app/templates/
                '''
            }
        }
    }

    post {
        always {
            sh '''
                echo "Final Pipeline Status:"
                kubectl get all
                kubectl logs -l app=pythonapp --tail=100 || true
            '''
        }
        success {
            sh 'echo Deployment successful!'
        }
        failure {
            sh '''
                echo Pipeline failed! Checking logs...
                kubectl describe pods -l app=pythonapp
                kubectl logs -l app=pythonapp --tail=200
            '''
        }
    }
}