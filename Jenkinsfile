pipeline {
  agent any
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
          """
        }
        
        echo 'Install requirements.txt'
        sh '''""" sh
    . venv/bin/activate
    pip install -r requirements.txt
"""'''
        echo 'Collect static files'
        sh '''sh """
    . venv/bin/activate
    python3.6 manage.py collectstatic --noinput
"""'''
      }
    }
    stage('Test') {
      steps {
        echo 'This is the Testing Stage'
      }
    }
    stage('Deploy') {
      steps {
        echo 'This is the Deploy Stage'
      }
    }
  }
}