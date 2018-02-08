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
          pip install -r requirements.txt
          """
        }
        
        echo 'Collect static'
        sh '''""" sh
. venv/bin/activate
python test_app.py
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