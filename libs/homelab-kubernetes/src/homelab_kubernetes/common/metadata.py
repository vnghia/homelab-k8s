import pulumi_kubernetes as kubernetes
from pulumi import Output


def name(metadata: Output[kubernetes.meta.v1.outputs.ObjectMeta]) -> Output[str]:
    def name_or_error(metadata: kubernetes.meta.v1.outputs.ObjectMeta) -> str:
        if hasattr(metadata, "name") and metadata.name:
            return metadata.name
        if (name := metadata.get("name")) and isinstance(name, str):
            return name
        raise ValueError(f"Name not found in metadata: {metadata}")

    return metadata.apply(name_or_error)
