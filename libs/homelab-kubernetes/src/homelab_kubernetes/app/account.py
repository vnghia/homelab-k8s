from typing import ClassVar

import homelab_common
import pulumi_kubernetes as kubernetes
from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from .. import common, config, namespace


class Account(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "account"

    def __init__(
        self,
        context: Context,
        name: str,
        config: config.app.account.Config,
        *,
        opts: ResourceOptions,
        app: str,
        namespace: namespace.Namespace,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._context = context
        self._config = config
        self._app = app
        self._namespace = namespace

        self._account = kubernetes.core.v1.ServiceAccount(
            self._name,
            opts=self._child_opts,
            metadata=kubernetes.meta.v1.ObjectMetaArgs(namespace=self._namespace.name),
        )
        self.name = common.metadata.name(self._account.metadata)

        if self._config.cluster:
            name = homelab_common.string.add_prefix(
                self._app, self._name, separator=":"
            )
            self._role = kubernetes.rbac.v1.ClusterRole(
                name,
                opts=self._child_opts,
                rules=[rule.to_args() for rule in self._config.rules],
            )
            self._binding = kubernetes.rbac.v1.ClusterRoleBinding(
                name,
                opts=self._child_opts,
                subjects=[
                    kubernetes.rbac.v1.SubjectArgs(
                        kind="ServiceAccount",
                        name=common.metadata.name(self._account.metadata),
                        namespace=self._namespace.name,
                    )
                ],
                role_ref=kubernetes.rbac.v1.RoleRefArgs(
                    api_group="rbac.authorization.k8s.io",
                    kind="ClusterRole",
                    name=common.metadata.name(self._role.metadata),
                ),
            )

        self.register_outputs({})
