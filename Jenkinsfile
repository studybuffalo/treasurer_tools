pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'This is the Build Stage'
         if (!fileExists 'bin/activate') {
			echo 'Test'
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