# SPDX-License-Identifier: copyleft-next-0.3.1

import re
import os.path
from github import Github
from gitlab import Gitlab
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

###
#
# Things you might need to change
#
###

# Your GUAC GraphQL server
GRAPHQL_SERVER = "http://localhost:8080/query"

# File containing a PAT or classic token for GitHub authentication
# If this file does not exist, we'll use an unauthenticated session,
# which probably means you'll get rate limited.
GITHUB_TOKEN_FILE='.github_token'

# File containing a PAT for GitLab authentication
# If this file does not exist, we'll use an unauthenticated session,
# which may mean you'll get rate limited.
GITLAB_TOKEN_FILE='.gitlab_token'

###
#
# Things you probably won't need to change
#
###

def queryGithub():
    '''
    Search for GitHub repos with the "hacktoberfest" topic

    Inputs: none
    Outputs: gh_participants (list)
    '''
    gh_participants = []
    # Test for a GitHub token file and setup the GitHub session
    if os.path.exists(GITHUB_TOKEN_FILE):
        with open(GITHUB_TOKEN_FILE) as gh_token_file:
            github_token = gh_token_file.read().strip()
            gh_token_file.close()
            github_session = Github(github_token)
    else:
        github_session = Github()
        print("Using unauthenticated session for GitHub," + \
              "you may get rate limited!")

    print("Getting list of Hacktoberfest repos from GitHub (be patient!)")

    response = github_session.search_repositories(query=f'topic:hacktoberfest')
    for repo in response:
        gh_participants.append("github.com/" + repo.full_name)

    return gh_participants

def queryGitlab():
    '''
    Search for GitHub repos with the "hacktoberfest" topic

    Inputs: none
    Outputs: gl_participants (list)
    '''
    gl_participants = []

    # Test for a GitHub token file and setup the GitHub session
    if os.path.exists(GITLAB_TOKEN_FILE):
        with open(GITLAB_TOKEN_FILE) as gl_token_file:
            gitlab_token = gl_token_file.read().strip()
            gl_token_file.close()
            gitlab_session = Gitlab(private_token=gitlab_token)
    else:
        gitlab_session = Gitlab()
        print("Using unauthenticated session for GitLab," + \
              "you may get rate limited!")
    print("Getting list of Hacktoberfest repos from GitLab (be patient!)")

    response = gitlab_session.projects.list(get_all=True, topic="hacktoberfest")
    for repo in response:
        gl_participants.append("gitlab.com/" + repo.path_with_namespace)
    return gl_participants

def queryGuac():
    '''
    Search the data in GUAC and return anything with HasSrcAt

    Inputs: none
    Outputs: sources (list)
    '''
    sources = []
    print("Searching your GUAC data")
    transport = RequestsHTTPTransport(url=GRAPHQL_SERVER)
    gql_client = Client(transport=transport, fetch_schema_from_transport=True)

    with open('query.gql') as query_file:
        gql_query = gql(query_file.read())
        query_file.close()

    guac_data = gql_client.execute(gql_query)

    for source_entry in guac_data['HasSourceAt']:
        source = source_entry['source']['namespaces'][0]
        sources.append(source['namespace'] + '/' + source['names'][0]['name'])

    return sources

def findProjects(sources, participants):
    '''
    Search the participants from GitHub and GitLab in our GUAC data

    Inputs: sources (list), participants(list)
    Outputs: none
    '''
    hacktoberfest_deps = []
    for repo in sources:
        if repo.startswith('github.com') or repo.startswith('gitlab.com'):
            if repo in participants:
                hacktoberfest_deps.append(repo)

    print("Here are the Hacktoberfest projects in your GUAC data:")
    for dep in hacktoberfest_deps:
        print(dep)

sources = queryGuac()

# Search the forges for participating projects
participants = []
participants.extend(queryGithub())
participants.extend(queryGitlab())

findProjects(sources, participants)
