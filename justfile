default:
    just --list

[arg("image")]
[group("host")]
image-download image:
    curl -L -O --output-dir $PWD/ "$(pulumi stack output cluster.image.{{ image }}.url)"

[group("config")]
config-dump-talos:
    pulumi stack output --show-secrets cluster.talosconfig > ".config/talosconfig/$(pulumi stack --show-name).yaml"

[group("config")]
config-dump-kube:
    pulumi stack output --show-secrets cluster.kubeconfig > ".config/kubeconfig/$(pulumi stack --show-name).yaml"

[group("kustomize")]
kustomize-build-cilium:
    kustomize build --enable-helm ./config/cluster/kubernetes/networking/cilium | \
    nickel export --stdin-format yaml --format json | \
    jq '{"cluster": {"kubernetes": {"networking": {"cilium": {"manifests": . } } } } }' | \
    nickel convert --stdin-format json | \
    sed -e 's/"__CILIUM_NAMESPACE__"/cluster.kubernetes.networking.cilium.namespace/g' > ./config/cluster/kubernetes/networking/cilium/manifests.ncl
