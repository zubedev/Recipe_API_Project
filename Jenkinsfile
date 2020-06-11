pipeline {
    agent any

    options {
        ansiColor('xterm')
    }

    environment {
        GH_SCRIPT = 'repo_state_update.sh'
        GH_OWNER = 'ziibii88'
        GH_REPO = 'Recipe_API_Project'
        GH_TOKEN = credentials('GH_Repo_Status')
    }

    stages {
        stage ('Status') {
            steps {
                echo 'Updating GitHub status...'
                sh "ls -al"
                sh "chmod 775 $GH_SCRIPT"
                sh "ls -al"
                sh "./$GH_SCRIPT pending $GH_OWNER $GH_REPO $GH_TOKEN $GIT_COMMIT $BUILD_URL"
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
            sh "./$GH_SCRIPT success $GH_OWNER $GH_REPO $GH_TOKEN $GIT_COMMIT $BUILD_URL"
        }
        failure {
            sh "./$GH_SCRIPT failure $GH_OWNER $GH_REPO $GH_TOKEN $GIT_COMMIT $BUILD_URL"
        }
    }
}