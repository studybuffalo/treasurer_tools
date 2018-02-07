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
			/usr/local/bin/virtualenvwrapper.sh
			mkvirtualenv treasurer_tools
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