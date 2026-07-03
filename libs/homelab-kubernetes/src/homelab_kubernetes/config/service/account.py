import pulumi_kubernetes as kubernetes
from homelab_model import BaseModel


class Rule(BaseModel):
    api_groups: list[str]
    resources: list[str]
    verbs: list[str]

    def to_args(self) -> kubernetes.rbac.v1.PolicyRuleArgs:
        return kubernetes.rbac.v1.PolicyRuleArgs(
            api_groups=self.api_groups,
            resources=self.resources,
            verbs=self.verbs,
        )


class Config(BaseModel):
    cluster: bool
    rules: list[Rule]
