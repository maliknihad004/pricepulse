pipeline {
    agent any

    stages {

        stage('Environment') {
            steps {
                sh '''
                    python3 --version
                    pip3 --version
                    git --version
                    docker --version
                    docker compose version
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

        stage('Build and Deploy') {
            steps {
                sh '''
                    echo "🚀 Tests passed. Building and deploying PricePulse..."

                    docker compose down || true

                    docker compose up -d --build

                    echo "📦 Current containers:"
                    docker compose ps

                    echo "✅ PricePulse deployment completed."
                '''
            }
        }
    }

    post {

        success {
            echo '✅ PricePulse CI/CD passed successfully!'
        }

        failure {
            echo '❌ PricePulse CI/CD failed. Deployment was blocked.'
        }

        always {
            echo 'Pipeline finished.'
        }
    }
}