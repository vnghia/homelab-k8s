import pulumi_kubernetes as kubernetes
from homelab_model import BaseModel
from pydantic import NonNegativeInt

from . import container


class Config(BaseModel):
    fs_group: NonNegativeInt
    fs_group_change_policy: str
    run_as_group: NonNegativeInt
    run_as_non_root: bool
    run_as_user: NonNegativeInt
    seccomp_profile: container.security_context.SeccompProfile
    supplemental_groups: list[NonNegativeInt]
    supplemental_groups_policy: str

    def to_args(self) -> kubernetes.core.v1.PodSecurityContextArgs:
        return kubernetes.core.v1.PodSecurityContextArgs(
            fs_group=self.fs_group,
            fs_group_change_policy=self.fs_group_change_policy,
            run_as_group=self.run_as_group,
            run_as_non_root=self.run_as_non_root,
            run_as_user=self.run_as_user,
            seccomp_profile=self.seccomp_profile.to_args(),
            supplemental_groups=self.supplemental_groups,
            supplemental_groups_policy=self.supplemental_groups_policy,
        )
