pipeline {
  agent any
  def installed = fileExists 'bin/activate'
  stages {
	if (!installed) {
		stage("Install Python Virtual Enviroment") {
			sh 'virtualenv --no-site-packages .'
		}
	}   
    stage('Build') {
      steps {
        echo 'This is the Build Stage'
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