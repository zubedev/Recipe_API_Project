pipeline {
    agent any

    options {
        ansiColor('xterm')
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                sh 'docker-compose build'
                sh 'docker-compose up -d'
            }
        }
        state('Migrate') {
            steps {
                echo 'Migrating..'
                sh 'docker-compose exec app python manage.py makemigrations --no-input --merge'
                sh 'docker-compose exec app python manage.py migrate --no-input'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                sh 'docker-compose exec app python manage.py test'
                sh 'docker-compose exec app flake8'
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
    }
}