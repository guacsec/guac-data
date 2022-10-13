import subprocess
from os import path, mkdir

BASE_PATH="docs/"

scorecards_data= {
    "github.com/kubernetes/kubernetes": 
        [
            "aaf024b5e8dc5e08e4414583203968ca0a5ec043",
            "3985f0a87ba4277b561e0cac9fba4f594eb8228a",
            "140c27533044e9e00f800d3ad0517540e3e4ecad",
            "252935368ab67f38cb252df0a961a6dcb81d20eb",
            "3d3ac0431b6b56adc06a948a9aeb24757f643249",
            "1ff66136acfd7717292f65447b2ebff162570f46",
            "9ea33a8d02b38a2ac996f4328e7b1449f2cbc888",
            "3c7da84d8fc03c30d3409e9c846ae4bc2de0b4d5",
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

    do_scorecards()
    do_spdx()
    do_k8s_slsa()

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
