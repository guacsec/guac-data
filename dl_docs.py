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

latest_tag = ["latest"]

spdx_containers_data= {
        # kubernetes images
        "k8s.gcr.io/kube-proxy": k8s_versions,
        "k8s.gcr.io/kube-controller-manager": k8s_versions,
        "k8s.gcr.io/kube-apiserver": k8s_versions,
        "k8s.gcr.io/kube-scheduler": k8s_versions,
}

cyclonedx_containers_data= {
        "docker.io/library/alpine": latest_tag,
        "docker.io/library/bash": latest_tag,
        "docker.io/library/busybox": latest_tag,
        "docker.io/library/caddy": latest_tag,
        "docker.io/library/composer": latest_tag,
        "docker.io/library/consul": latest_tag,
        "docker.io/library/debian": latest_tag,
        "docker.io/library/docker": latest_tag,
        "docker.io/library/haproxy": latest_tag,
        "docker.io/library/httpd": latest_tag,
        "docker.io/library/memcached": latest_tag,
        "docker.io/library/nginx": latest_tag,
        "docker.io/library/postgres": latest_tag,
        "docker.io/library/python": latest_tag,
        "docker.io/library/rabbitmq": latest_tag,
        "docker.io/library/redis": latest_tag,
        "docker.io/library/ubuntu": latest_tag,
        "docker.io/library/vault": latest_tag,
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

def syft_cyclonedx_cmd(container_path, tag, fdir):
    fpath = path.join(fdir, 'syft-cyclonedx-{}:{}.json'.format(container_path.replace('/','-'), tag))
    cmd = "syft -c config/syft.yaml packages {}:{} -o cyclonedx-json | jq".format(container_path, tag)
    print_msg(fpath, cmd)

    f= open(fpath, 'w')
    subprocess.call(cmd, shell=True, stdout=f)
    f.close()



def main():
    if not path.isdir(BASE_PATH):
        mkdir(BASE_PATH)

    do_cyclonedx()
    do_k8s_slsa()
    do_spdx()
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

    for container_path in spdx_containers_data:
        for tag in spdx_containers_data[container_path]:
            syft_spdx_cmd(container_path, tag, subpath)

def do_cyclonedx():
    subpath = path.join(BASE_PATH, "cyclonedx")
    if not path.isdir(subpath):
        mkdir(subpath)

    for container_path in cyclonedx_containers_data:
        for tag in cyclonedx_containers_data[container_path]:
            syft_spdx_cmd(container_path, tag, subpath)



def print_msg(path, cmd):
    print("creating file: {}, cmd: {}".format(path, cmd))

if __name__ == "__main__":
    main()
