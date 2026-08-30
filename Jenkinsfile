
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

        stage('Setup Test Environment') {
            steps {
                sh '''
                    cat > .env.test <<EOF
DATABASE_URL=postgresql+psycopg://pricepulse:malik@pricepulse-db:5432/pricepulse
CHECK_INTERVAL=30
EOF
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

