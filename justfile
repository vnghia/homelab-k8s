default:
    just --list

[arg("host")]
[group("host")]
host-download-image host:
    curl -L -o $PWD/dev/vms/{{ host }}/metal-amd64.iso $(pulumi stack output host.{{ host }}.image.url)
