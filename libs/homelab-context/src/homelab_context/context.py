from typing import Any

import pulumi

from .resolve import ResolveSource, ResolveType, resolve


class Context:
    def __init__(self) -> None:
        self.pulumi = pulumi.Config()
        self.pulumi_secrets = self.pulumi.require_secret_object("secrets")

    def resolve(self, data: Any) -> Any:
        if isinstance(data, str) and data.startswith("#ref:"):
            ref = data[5:].split(":", maxsplit=2)

            source = ResolveSource(ref[0])
            type = ResolveType(ref[1])
            key = ref[2]

            match source:
                case ResolveSource.PULUMI_SECRETS:
                    return self.pulumi_secrets.apply(
                        lambda secrets: resolve(secrets, key, type)
                    )
        elif isinstance(data, list):
            return [self.resolve(item) for item in data]
        elif isinstance(data, dict):
            return {key: self.resolve(value) for key, value in data.items()}
        return data
