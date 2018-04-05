pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr: "20"))
  }
  stages {
    stage('Build') {
      steps {
        echo 'Setup virtual environment'
        script {
          sh """
          PATH=$WORKSPACE/venv/bin:/usr/local/bin:$PATH
          if [ ! -d "venv" ]; then
          virtualenv venv
          fi
          . venv/bin/activate
          pip install -r requirements.txt
          """
        }
        echo 'Install requirements.txt'
        script {
          sh """
          . venv/bin/activate
          pip install -r requirements.txt
          """
        }
        echo 'Migrate database'
        script {
          sh """
          . venv/bin/activate
          python manage.py migrate --noinput
          """
        }
        echo 'Collect static'
        script {
          sh """
          . venv/bin/activate
          python manage.py collectstatic --noinput
          """
        }
      }
    }
    stage('Test') {
      steps {
        echo 'This is the Testing Stage'
        script {
          sh """
          . venv/bin/activate
          python manage.py jenkins --enable-coverage --settings=config.settings.test
          """
        }
        script {
          sh """
          . venv/bin/activate
          /* pylint --rcfile=.pylintrc --output-format=parseable --reports=no treasurer_tools > reports/pylint.txt || echo "pylint exited with $?" */
          """
        }
      }
    }
    stage('Deploy') {
      steps {
        echo 'This is the Deploy Stage'
      }
    }
  }
}