pipeline {
    agent any

    options {
        ansiColor('xterm')
    }

    environment {
        GH_REPO_TOKEN = credentials('GH_Repo_Status')
        GH_REPO = 'Recipe_API_Project'
        GH_USERNAME = 'ziibii88'
    }

    stages {
        stage ('Status') {
            steps {
                sh '''
                   curl "https://api.github.com/repos/$GH_USERNAME/$GH_REPO/statuses/$GIT_COMMIT?access_token=$GH_REPO_TOKEN" \
                       -H "Content-Type: application/json" -X POST \
                       -d "{\"state\": \"pending\",\"context\": \"continuous-integration/jenkins\", \"description\": \"pending\", \"target_url\": \"$BUILD_URL\"}"
                '''
            }
        }
        stage('Build') {
            steps {
                echo 'Building..'
                sh 'docker-compose build'
                sh 'docker-compose up -d'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
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
            sh '''
               curl "https://api.github.com/repos/$GH_USERNAME/$GH_REPO/statuses/$GIT_COMMIT?access_token=$GH_REPO_TOKEN" \
                   -H "Content-Type: application/json" -X POST \
                   -d "{\"state\": \"success\",\"context\": \"continuous-integration/jenkins\", \"description\": \"success\", \"target_url\": \"$BUILD_URL\"}"
            '''
        }
        failure {
            sh '''
               curl "https://api.github.com/repos/$GH_USERNAME/$GH_REPO/statuses/$GIT_COMMIT?access_token=$GH_REPO_TOKEN" \
                   -H "Content-Type: application/json" -X POST \
                   -d "{\"state\": \"failure\",\"context\": \"continuous-integration/jenkins\", \"description\": \"failed\", \"target_url\": \"$BUILD_URL\"}"
            '''
        }
    }
}