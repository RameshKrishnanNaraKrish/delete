pipeline {
    agent any

  parameters {
        string(name: 'PR_URL', defaultValue: 'https://github.com/RameshKrishnanNaraKrish/react-project-webapp/pull/7', description: 'URL of the Pull Request (e.g., https://github.com/owner/repo/pull/123)')
    }

    environment {
        GITHUB_API_URL = 'https://api.github.com/repos'
        GITHUB_TOKEN = credentials('github')  // Use Jenkins credentials for GitHub token
    }

    stages {
      stage('Validate and Extract PR Details') {
            steps {
                script {
                    if (!params.PR_URL) {
                        error "PR_URL parameter is required!"
                    }

                    def matcher = params.PR_URL =~ /https:\/\/github\.com\/([^\/]+)\/([^\/]+)\/pull\/(\d+)/
                    if (!matcher.matches()) {
                        error "Invalid PR URL format. Expected format: https://github.com/owner/repo/pull/123"
                    }

                    env.OWNER = matcher[0][1]
                    env.REPO = matcher[0][2]
                    env.PR_ID = matcher[0][3]

                    echo "Extracted Owner: ${env.OWNER}"
                    echo "Extracted Repo: ${env.REPO}"
                    echo "Extracted PR ID: ${env.PR_ID}"
                }
            }
        }

        stage('Checkout Repository') {
            steps {
                git branch: 'main', url: "https://github.com/${env.OWNER}/${env.REPO}.git"
            }
        }

        stage('Revert PR') {
            steps {
                script {
                    // Checkout the repository
                    checkout scm

                    script {
                    // Set up Python environment (assuming Python and pip are available)
                    sh 'python3 -m venv venv'
                    sh '. venv/bin/activate && pip install requests'

                    // Run the Python script to revert the PR
                    withEnv(["GITHUB_OWNER=${env.OWNER}", "GITHUB_REPO=${env.REPO}", "PR_ID=${env.PR_ID}", "GITHUB_TOKEN=${env.GITHUB_TOKEN}"]) {
                        sh 'git checkout -b revert-pr-$PR_ID'
                        sh '. venv/bin/activate && python3 revert_pr.py'

                                            // Add and commit the changes
                            sh 'git add .'
                            sh 'git commit -m "Revert PR $PR_ID"'
        
                            // Push the new branch
                            sh 'git push origin revert-pr-$PR_ID'

                        
                        }
                    }
                }
            }
        }

        stage('Create Pull Request') {
            steps {
                script {
                    // Create a pull request for the revert branch
                    sh """
                    curl -X POST -H "Authorization: token ${env.GITHUB_TOKEN}" \
                    -d '{ "title": "Revert PR ${env.PR_ID}", "head": "revert-pr-${env.PR_ID}", "base": "main" }' \
                    ${env.GITHUB_API_URL}/${env.OWNER}/${env.REPO}/pulls
                    """
                }
            }
        }
    }
}
