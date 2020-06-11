pipeline {
    agent any

    stages {
        // stage('Build') {
        //     steps {
        //         echo 'Building..'
        //         sh 'docker-compose build'
        //         sh 'docker-compose up -d'
        //     }
        // }
        stage('Test') {
            steps {
                echo 'Testing..'
                sh 'docker-compose build'
                sh 'docker-compose up -d'
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