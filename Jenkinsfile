pipeline {
    agent any

    stages {

        stage('Environment') {
            steps {
                sh '''
                    echo "🔍 Checking environment..."

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
                    echo "📦 Installing dependencies..."

                    python3 -m pip install --break-system-packages -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    echo "🧪 Running tests..."

                    python3 -m pytest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "🐳 Building Docker image..."

                    docker compose build
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    echo "🚀 Deploying PricePulse..."

                    docker compose down || true
                    docker compose up -d

                    echo "📦 Running containers:"
                    docker compose ps
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    echo "🔍 Verifying deployment..."

                    docker compose ps

                    if [ "$(docker compose ps -q)" = "" ]; then
                        echo "❌ No containers are running."
                        exit 1
                    fi

                    echo "✅ Deployment verification completed."
                '''
            }
        }
    }

    post {

        success {
            echo '✅ PricePulse CI/CD pipeline completed successfully!'
        }

        failure {
            echo '❌ Pipeline failed. Deployment was blocked or unsuccessful.'
        }

        always {
            echo '🏁 Pipeline finished.'
        }
    }
}