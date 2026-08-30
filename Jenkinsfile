pipeline {
    agent any

    stages {
        stage('Environment') {
            steps {
                sh '''
                    python3 --version
                    pip3 --version
                    git --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m pip install --break-system-packages -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    python3 -m pytest -v
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