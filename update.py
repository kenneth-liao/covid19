import pandas as pd
import git


def run_update():
    pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv').to_csv('data/owid-covid-data.csv')

    repo = git.Repo("C:\\Users\Kenny\projects\plotly-dash-covid19\.git")

    with repo.config_writer() as git_config:
        git_config.set_value('user', 'email', 'kennyliao22@gmail.com')
        git_config.set_value('user', 'name', 'Kenneth Liao')

    repo.index.add(['data/owid-covid-data.csv'])

    repo.index.commit('updated data')

    try:
        repo.remotes.origin.push()
    except:
        print('Error in trying to push to repo!')


if __name__ == '__main__':
    run_update()
    print('All done!')
