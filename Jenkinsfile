pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr: '10'))
  }
  stages {
    stage('Build') {
      steps {
        echo 'Setup virtual environment'
        script {
          sh 'pipenv install --dev'
        }
        echo 'Migrate database'
        script {
          sh 'pipenv run python manage.py migrate --noinput'
        }
        echo 'Collect static'
        script {
          sh 'pipenv run python manage.py collectstatic --noinput'
        }
      }
    }
  }
}
