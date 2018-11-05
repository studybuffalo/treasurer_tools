pipeline {
  agent { dockerfile true }
  options {
    disableConcurrentBuilds()
    buildDiscarder(logRotator(numToKeepStr: '5'))
    timeout(time: 60, unit: 'MINUTES')
  }
  stages {
    stage('Build') {
      steps {
        echo 'Setup virtual environment'
        script {
          sh 'pipenv install --dev  --ignore-pipfile'
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
    stage('Test') {
      steps {
        echo 'Running Django tests'
        script {
          sh 'pipenv run python manage.py jenkins --enable-coverage --settings=config.settings.test --noinput'
        }
      }
    }
    stage('Security') {
      steps {
        echo 'Running security checks'
        script {
          sh 'pipenv check'
        }
      }
    }
  }
  post {
    always {
      step([$class: 'CoberturaPublisher', coberturaReportFile: 'reports/coverage.xml', failUnhealthy: false, failUnstable: false, maxNumberOfBuilds: 10, onlyStable: false, sourceEncoding: 'ASCII'])
      junit 'reports/junit.xml'
    }
  }
}
