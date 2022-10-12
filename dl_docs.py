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

k8s_versions = [
    "v1.25.2",
    "v1.25.1",
    "v1.24.1",
    "v1.24.2",
    "v1.24.3",
    "v1.24.4",
    "v1.24.5",
    "v1.24.6",
    ]
"""
[
    "v1.23.1",
    "v1.23.2",
    "v1.23.3",
    "v1.23.4",
    "v1.23.5",
    "v1.23.6",
    "v1.23.7",
    "v1.23.8",
    "v1.23.9",
    "v1.23.10",
    "v1.23.11",
    "v1.23.12",
]
"""

k8s_slsa_data = k8s_versions

containers_data= {
        "k8s.gcr.io/kube-proxy": k8s_versions,
        "k8s.gcr.io/kube-controller-manager": k8s_versions,
        "k8s.gcr.io/kube-apiserver": k8s_versions,
        "k8s.gcr.io/kube-scheduler": k8s_versions,
}

def scorecard_cmd(repo, commit, fdir):
    fpath = path.join(fdir, 'scorecard-{}-{}.json'.format(repo.split('/')[-1], commit))
    cmd = ' '.join(["scorecard", "--repo={}".format(repo), "--commit={}".format(commit), "--format=json"])
    print_msg(fpath, cmd)

    f = open(fpath, 'w')
    subprocess.call(cmd,shell=True, stdout=f)
    f.close()

def kube_slsa_cmd(version, fdir):
    fpath = path.join(fdir, 'kube-slsa-{}.json'.format(version))
    cmd = "curl -sL https://dl.k8s.io/release/{}/provenance.json | jq".format(version)
    print_msg(fpath, cmd)

    f= open(fpath, 'w')
    subprocess.call(cmd, shell=True, stdout=f)
    f.close()

def syft_spdx_cmd(container_path, tag, fdir):
    fpath = path.join(fdir, 'syft-spdx-{}:{}.json'.format(container_path.replace('/','-'), tag))
    cmd = "syft -c config/syft.yaml packages {}:{} -o spdx-json | jq".format(container_path, tag)
    print_msg(fpath, cmd)

    f= open(fpath, 'w')
    subprocess.call(cmd, shell=True, stdout=f)
    f.close()


def main():
    if not path.isdir(BASE_PATH):
        mkdir(BASE_PATH)

    do_spdx()
    do_k8s_slsa()
    do_scorecards()

def do_scorecards():
    subpath = path.join(BASE_PATH, "scorecard")
    if not path.isdir(subpath):
        mkdir(subpath)

    for repo in scorecards_data:
        for commit in scorecards_data[repo]:
            scorecard_cmd(repo,commit,subpath)

def do_k8s_slsa():
    subpath = path.join(BASE_PATH, "slsa")
    if not path.isdir(subpath):
        mkdir(subpath)

    for version in k8s_slsa_data:
        kube_slsa_cmd(version, subpath)


def do_spdx():
    subpath = path.join(BASE_PATH, "spdx")
    if not path.isdir(subpath):
        mkdir(subpath)

    for container_path in containers_data:
        for tag in containers_data[container_path]:
            syft_spdx_cmd(container_path, tag, subpath)


def print_msg(path, cmd):
    print("creating file: {}, cmd: {}".format(path, cmd))

if __name__ == "__main__":
    main()
