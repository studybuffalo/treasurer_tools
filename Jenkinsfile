pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'This is the Build Stage'
        script {
          def installed = fileExists 'bin/activate'
          if (!installed) {
            echo 'Creating virtual environment'
            sh """
            set -euox pipefail
            
            # Get an unique venv folder to using *inside* workspace
            VENV=".venv-$BUILD_NUMBER"
            
            # Initialize new venv
            virtualenv "$VENV"
            """
          }
        }
        
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