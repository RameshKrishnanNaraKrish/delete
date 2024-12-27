pipeline {
    agent any

  parameters {
        string(name: 'PR_URL', defaultValue: 'https://github.com/RameshKrishnanNaraKrish/react-project-webapp/pull/8', description: 'URL of the Pull Request (e.g., https://github.com/owner/repo/pull/123)')
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

        stage('Clean Workspace') {
            steps {
                script {
                    // Remove existing repository if it exists
                    sh '''
                    if [ -d "${REPO}" ]; then
                        echo "Directory ${REPO} exists. Deleting it..."
                        rm -rf "${REPO}"
                    fi
                    '''
                }
            }
        }
        stage('Clone Repository') {
            steps {
                script {
                    // Clone the repository
                    sh '''
                    echo "Cloning repository..."
                    git clone https://github.com/$OWNER/$REPO.git
                    '''
                }
            }
        }


        stage('Revert PR') {
            steps {
                script {

                    def response = sh(script: """
                        curl -s -H "Authorization: token ${env.GITHUB_TOKEN}" \
                        ${env.GITHUB_API_URL}/${env.OWNER}/${env.REPO}/pulls/${env.PR_ID} | jq -r '.merge_commit_sha'
                    """, returnStdout: true).trim()

                    env.MERGE_COMMIT_SHA = response

                    def mergeCommitSha = env.MERGE_COMMIT_SHA

                    sh '''
                        cd $REPO
                        git pull origin main
                        pwd
                        git status
                        git revert -m 1 $MERGE_COMMIT_SHA
                    '''
                }
            }
        }

        stage('Push Revert Branch') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'github', variable: 'GITHUB_TOKEN')]) {
                    // Configure Git to use the token for authentication
                        sh '''
                            git config user.name "Jenkins CI"
                            git config user.email "jenkins@example.com"

                            git remote set-url origin https://$GITHUB_TOKEN@github.com/$OWNER/$REPO.git
                            
                            git push origin main
                        '''
                    }
                }
            }
        }
    }
}
