import requests
import os
import json

class GithubAPI:
  """ Manage authenticated requests to the Github API """

  def __init__(self, personal_access_token):
    self.auth_fragment = 'access_token={0}'.format(personal_access_token)

  def last_commit_date(self, commits_url):
    """ Get the timestamp of the latest commit. """
    commits_endpoint  = commits_url[0:commits_url.find('{')]
    commits_endpoint_auth = '{0}?{1}'.format(
      commits_endpoint, self.auth_fragment)
    
    cur = requests.get(commits_endpoint_auth)
    if cur.status_code < 400:
      last_commit = cur.json()[0]
      return last_commit['commit']['committer']['date']

  def repository_languages(self, repository_name, languages_url):
    """ Get the languages identified in each repository. """
    languages_endpoint_auth = "{0}?{1}".format(
      languages_url, self.auth_fragment)

    r = requests.get(languages_endpoint_auth)
    if r.status_code < 400:
      languages = r.json()
      result = {
        'name': repository_name,
        'languages': languages}
      return result


  def list_of_repos_url(self, organization):
    repo_list_url = 'https://api.github.com/orgs/{0}/repos?{1}'.format(
      organization, self.auth_fragment)
    return repo_list_url
    #return requests.get(repo_list_url)

  def list_of_repos(self, next_page_url):
    return requests.get(next_page_url)


def next_page_from_header(link_header):
  """ Parse the response Link header to get the next page to retrieve """

  if "next" in link_header:
    n = [l for l in link_header.split(',') if 'next' in l][0]
    return n[n.find("<")+1:n.find(">")]


if __name__ == '__main__':
  org_name = '18F'

  personal_access_token = os.environ.get('GITHUB_TOKEN')
  github = GithubAPI(personal_access_token)

  next_page = github.list_of_repos_url(org_name)

  languages_list = []
  while next_page:
    r = github.list_of_repos(next_page)

    #for repository in r.json():
    #  name = repository['name']
    #  last_commit = github.last_commit_date(repository['commits_url'])
    #  private = repository['private']
    #  print("{0},{1},{2}".format(name, last_commit, private))
    
    # Get the languages for each repository
    for repository in r.json():
      name = repository['name']
      languages = github.repository_languages(name, repository['languages_url'])
      languages_list.append(languages)

    next_page = next_page_from_header(r.headers['Link'])

  with open('languages.json', 'w') as languages_outfile:
    json.dump(languages_list, languages_outfile)


  # Get date of latest commit

  # Languages related information
  #languages_url = single_repo['languages_url']
  #lr = requests.get(languages_url)
  #print(lr.json())
