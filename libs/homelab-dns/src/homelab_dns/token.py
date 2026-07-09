import functools
import urllib.parse
from typing import ClassVar

import homelab_common as common
import homelab_pulumi as pulumi
import orjson
import pulumi_cloudflare as cloudflare
from homelab_context import Context
from pulumi import ComponentResource, Output, ResourceOptions

from . import config, reference


class Token(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "token"

    SCOPE: ClassVar[str] = "com.cloudflare.api.account.zone"
    URL_SCOPE: ClassVar[str] = urllib.parse.quote_plus(SCOPE)

    def __init__(
        self,
        name: str,
        context: Context,
        config: config.Config,
        *,
        opts: ResourceOptions | None,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._context = context
        self._config = config

        self._api_resources = orjson.dumps(
            {f"{self.SCOPE}.{zone.id}": "*" for zone in self._config.zones.values()},
        ).decode()

        self._cert_manager = cloudflare.ApiToken(
            "cert-manager",
            opts=self._child_opts.merge(ResourceOptions(delete_before_replace=True)),
            name=common.string.add_prefix(
                pulumi.constant.STACK,
                common.string.add_suffix(self._name, "cert-manager", separator="-"),
                separator="-",
            ),
            policies=[
                cloudflare.ApiTokenPolicyArgs(
                    effect="allow",
                    permission_groups=[
                        self.zone_read_permission_group_args,
                        self.dns_write_permission_group_args,
                    ],
                    resources=self._api_resources,
                ),
            ],
        )

        self._context.set(reference.token.Reference, self)

        self.register_outputs({})

    @classmethod
    def get_permission_group_args(
        cls, name: str,
    ) -> Output[cloudflare.ApiTokenPolicyPermissionGroupArgs]:
        return cloudflare.get_api_token_permission_groups_list_output(
            name=urllib.parse.quote_plus(name), scope=cls.URL_SCOPE,
        ).apply(
            lambda result: cloudflare.ApiTokenPolicyPermissionGroupArgs(
                id=result.results[0].id,
            ),
        )

    @functools.cached_property
    def zone_read_permission_group_args(
        self,
    ) -> Output[cloudflare.ApiTokenPolicyPermissionGroupArgs]:
        return self.get_permission_group_args("Zone Read")

    @functools.cached_property
    def dns_write_permission_group_args(
        self,
    ) -> Output[cloudflare.ApiTokenPolicyPermissionGroupArgs]:
        return self.get_permission_group_args("DNS Write")

    @property
    def cert_manager(self) -> Output[str]:
        return self._cert_manager.value
