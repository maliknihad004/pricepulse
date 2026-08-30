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
                    docker-compose --version
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
                    cat > .env.test <<'EOF'
DATABASE_URL=postgresql+psycopg://pricepulse:malik@pricepulse-db:5432/pricepulse
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

        stage('Deploy') {
            steps {
                sh '''
                    echo "🚀 Tests passed. Deploying PricePulse..."

                    docker-compose -f docker-compose.yml up -d --build

                    echo "📦 Current containers:"
                    docker-compose -f docker-compose.yml ps

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