default:
    just --list

[arg("image")]
[group("host")]
image-download image:
    curl -L -O --output-dir $PWD/ $(pulumi stack output cluster.image.{{ image }}.url)
