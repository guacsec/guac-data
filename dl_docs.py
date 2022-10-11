import subprocess
from os import path, mkdir

BASE_PATH="docs/"

scorecards_data= {
    "github.com/kubernetes/kubernetes": 
        [
            "5835544ca568b757a8ecae5c153f317e5736700e",
            "b39bf148cd654599a52e867485c02c4f9d28b312",
            "c6939792865ef0f70f92006081690d77411c8ed5",
            "1d79bc3bcccfba7466c44cc2055d6e7442e140ea",
            "e4d4e1ab7cf1bf15273ef97303551b279f0920a9",
            "e979822c185a14537054f15808a118d7fcce1d6e",
            "dc2898b20c6bd9602ae1c3b51333e2e4640ed249",
            "bccf857df03c5a99a35e34020b3b63055f0c12ec",
            "a866cbe2e5bbaa01cfd5e969aa3e033f3282a8a2",
            "95ee5ab382d64cfe6c28967f36b53970b8374491",
            "7e54d50d3012cf3389e43b096ba35300f36e0817",
        ]
}

def scorecard_cmd(repo, commit, fdir):
    cmd = ' '.join(["scorecard", "--repo={}".format(repo), "--commit={}".format(commit), "--format=json"])
    fpath = path.join(fdir, 'scorecard-{}-{}.json'.format(repo.split('/')[-1], commit))
    f = open(fpath, 'w')
    subprocess.call(cmd,shell=True, stdout=f)
    f.close()


if not path.isdir(BASE_PATH):
    mkdir(BASE_PATH)


scorecard_path = path.join(BASE_PATH, "scorecard")
if not path.isdir(scorecard_path):
    mkdir(scorecard_path)

for repo in scorecards_data:
    for commit in scorecards_data[repo]:
        scorecard_cmd(repo,commit,scorecard_path)

