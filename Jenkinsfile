pipeline {
    agent any

    options {
        ansiColor('xterm')
    }

    environment {
        GH_OWNER = 'ziibii88'
        GH_REPO = 'Recipe_API_Project'
        GH_TOKEN = credentials('GH_Repo_Status')
    }

    stages {
        stage ('Status') {
            steps {
                echo 'Updating GitHub status...'
                sh """
                curl "https://api.github.com/repos/$GH_OWNER/$GH_REPO/statuses/$GIT_COMMIT" \
                  -H "Authorization: token $GH_TOKEN" -X POST \
                  -d "{\"state\": \"pending\", \"context\": \"continuous-integration/jenkins\", \"description\": \"pending\", \"target_url\": \"$BUILD_URL\"}"
                """
            }
        }
        stage('Build') {
            steps {
                echo 'Building Docker container...'
                sh 'docker-compose build'
                sh 'docker-compose up -d'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing application...'
                // -T flag need to disable TTY input
                sh 'docker-compose exec -T app python manage.py test'
                sh 'docker-compose exec -T app flake8'
            }
        }
        // stage('Deploy') {
        //     steps {
        //         echo 'Deploying....'
        //     }
        // }
    }

    post {
        always {
            sh 'docker-compose down'
        }
        success {
            sh """
                curl "https://api.github.com/repos/$GH_OWNER/$GH_REPO/statuses/$GIT_COMMIT" \
                  -H "Authorization: token $GH_TOKEN" -X POST \
                  -d "{\"state\": \"success\", \"context\": \"continuous-integration/jenkins\", \"description\": \"success\", \"target_url\": \"$BUILD_URL\"}"
                """
        }
        failure {
            sh """
                curl "https://api.github.com/repos/$GH_OWNER/$GH_REPO/statuses/$GIT_COMMIT" \
                  -H "Authorization: token $GH_TOKEN" -X POST \
                  -d "{\"state\": \"failure\", \"context\": \"continuous-integration/jenkins\", \"description\": \"failure\", \"target_url\": \"$BUILD_URL\"}"
                """
        }
    }
}