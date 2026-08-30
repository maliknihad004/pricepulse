pipeline {
    agent {
        docker {
            image 'python:3.14-slim'
        }
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    python --version
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    pytest -v
                '''
            }
        }
    }

    post {
        success {
            echo '✅ PricePulse CI passed successfully!'
        }

        failure {
            echo '❌ PricePulse CI failed. Deployment is blocked.'
        }

        always {
            echo 'Pipeline finished.'
        }
    }
}