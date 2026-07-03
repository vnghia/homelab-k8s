import pulumi_kubernetes as kubernetes
from homelab_model import BaseModel
from pydantic import NonNegativeInt


class Capabilities(BaseModel):
    add: list[str]
    drop: list[str]

    def to_args(self) -> kubernetes.core.v1.CapabilitiesArgs:
        return kubernetes.core.v1.CapabilitiesArgs(add=self.add, drop=self.drop)


class SeccompProfile(BaseModel):
    type: str

    def to_args(self) -> kubernetes.core.v1.SeccompProfileArgs:
        return kubernetes.core.v1.SeccompProfileArgs(type=self.type)


class Config(BaseModel):
    allow_privilege_escalation: bool
    capabilities: Capabilities
    privileged: bool
    read_only_root_filesystem: bool
    run_as_group: NonNegativeInt
    run_as_non_root: bool
    run_as_user: NonNegativeInt
    seccomp_profile: SeccompProfile

    def to_args(self) -> kubernetes.core.v1.SecurityContextArgs:
        return kubernetes.core.v1.SecurityContextArgs(
            allow_privilege_escalation=self.allow_privilege_escalation,
            capabilities=self.capabilities.to_args(),
            privileged=self.privileged,
            read_only_root_filesystem=self.read_only_root_filesystem,
            run_as_group=self.run_as_group,
            run_as_non_root=self.run_as_non_root,
            run_as_user=self.run_as_user,
            seccomp_profile=self.seccomp_profile.to_args(),
        )
