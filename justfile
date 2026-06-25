default:
    just --list

[arg("image")]
[group("host")]
image-download image:
    curl -L -O --output-dir $PWD/ "$(pulumi stack output cluster.image.{{ image }}.url)"

[group("config")]
config-dump-talos:
    pulumi stack output --show-secrets cluster.talosconfig > ".config/talosconfig/$(pulumi stack --show-name).yaml"
