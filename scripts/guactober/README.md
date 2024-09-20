# guactober

A script to search your [GUAC](https://guac.sh) data for projects partcipating in [Hacktoberfest](https://hacktoberfest.com).

## Requirements

* Python modules
    * json
    * re
    * PyGithub
    * python-gitlab
* (optional) A GitHub token (either a PAT or classic token) in `../.github_token`
* (optional) A GitLab token in `../.gitlab_token`

**Note:** If you don't use the token files, you run the risk of getting rate-limited in your queries of GitHub and GitLab.

## Usage

After installing any missing requirements, run `python3 ./guactober.py`

The script assumes your query is in `./query.gql` and that your GraphQL query endpoint is `http://localhost:8080/query`.

The table below describes setting you may want to change.
All the settings described appear near the top of the script.

| Setting | Description
| ------- | -----------
| GITHUB_TOKEN_FILE | The path on disk to a file containing your GitHub token (and only your GitHub token)
| GITLAB_TOKEN_FILE | The path on disk to a file containing your GitLab token (and only your GitLab token)
| GRAPHQL_SERVER | The full URL to your GUAC GraphQL server's query endpoint

The script will print a list of repositories that are listed as participating in Hacktoberfest.