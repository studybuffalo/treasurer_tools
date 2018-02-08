pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'Setup virtual environment and install requirements.txt'
        script {
          sh """
          PATH=$WORKSPACE/venv/bin:/usr/local/bin:$PATH
          if [ ! -d "venv" ]; then
          virtualenv venv
          fi
          . venv/bin/activate
          pip install -r requirements.txt --download-cache=/tmp/$JOB_NAME
          """
        }
        
        echo 'Collect static'
        sh '''""" sh
. venv/bin/activate
python test_app.py
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