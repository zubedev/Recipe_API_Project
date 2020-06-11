pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                echo $PWD
                ls -al
                docker-compose build
                docker-compose up -d
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                echo $PWD
                ls -al
                docker-compose run -rm app sh -c "python manage.py test && flake8"
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
            docker-compose down
        }
    }
}