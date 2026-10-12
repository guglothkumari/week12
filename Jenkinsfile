pipeline {
    agent any
    stages
    {
        stage('Run Selenium Tests') {
            steps {
                echo "Running Selenium Tests"
                bat "pip install -r requirements.txt"
                bat 'start /B python app.py'
                bat 'ping 127.0.0.1 -n 5 > nul'
                bat "python -m pytest -v test/test_register.py"
            }
        }
        stage('Build Docker Image') {
            steps {
                echo "Build Docker Image"
                bat "docker build -t seldemoapp:v1 ."
            }
        }
        stage('Docker Login') {
            steps {
                  bat 'docker login -u guglothkumari -p Kuma@2005'
                }
            }
        stage('push Docker Image to Docker Hub') {
            steps {
                echo "push Docker Image to Docker Hub"
                bat "docker tag seldemoapp:v1 guglothkumari/week12:seldemoimage1"               
                    
                bat "docker push guglothkumari/week12:seldemoimage1"
                
            }
        }
        stage('Deploy to Kubernetes') { 
            steps { 
                    // apply deployment & service 
                    bat 'kubectl apply -f deployment.yaml --validate=false' 
                    bat 'kubectl apply -f service.yaml' 
            } 
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
