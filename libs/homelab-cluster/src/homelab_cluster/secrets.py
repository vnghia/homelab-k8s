from typing import Self

import pulumiverse_talos as talos
from homelab_types import BaseModel
from pulumi import Output, ResourceOptions
from pydantic import ConfigDict


class ClusterClientConfiguration(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    ca_certificate: Output[str]
    client_certificate: Output[str]
    client_key: Output[str]

    @classmethod
    def from_output(
        cls, output: Output[talos.machine.outputs.ClientConfiguration]
    ) -> Self:
        return cls(
            ca_certificate=output.apply(
                lambda client_configuration: client_configuration.ca_certificate
            ),
            client_certificate=output.apply(
                lambda client_configuration: client_configuration.client_certificate
            ),
            client_key=output.apply(
                lambda client_configuration: client_configuration.client_key
            ),
        )

    def to_args(self) -> talos.machine.ClientConfigurationArgs:
        return talos.machine.ClientConfigurationArgs(
            ca_certificate=self.ca_certificate,
            client_certificate=self.client_certificate,
            client_key=self.client_certificate,
        )


class ClusterCertificate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cert: Output[str]
    key: Output[str]

    @classmethod
    def from_output(
        cls, output: Output[talos.machine.outputs.CertificateResult]
    ) -> Self:
        return cls(
            cert=output.apply(lambda certificate: certificate.cert),
            key=output.apply(lambda certificate: certificate.key),
        )

    def to_args(self) -> talos.machine.CertificateArgs:
        return talos.machine.CertificateArgs(
            cert=self.cert,  # type: ignore [arg-type]
            key=self.key,  # type: ignore [arg-type]
        )


class ClusterKey(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    key: Output[str]

    @classmethod
    def from_output(cls, output: Output[talos.machine.outputs.KeyResult]) -> Self:
        return cls(key=output.apply(lambda key: key.key))

    def to_args(self) -> talos.machine.KeyArgs:
        return talos.machine.KeyArgs(
            key=self.key,  # type: ignore [arg-type]
        )


class ClusterCertificates(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    etcd: ClusterCertificate
    k8s: ClusterCertificate
    k8s_aggregator: ClusterCertificate
    k8s_serviceaccount: ClusterKey
    os: ClusterCertificate

    @classmethod
    def from_output(
        cls, output: Output[talos.machine.outputs.CertificatesResult]
    ) -> Self:
        return cls(
            etcd=ClusterCertificate.from_output(
                output.apply(lambda certificates: certificates.etcd)
            ),
            k8s=ClusterCertificate.from_output(
                output.apply(lambda certificates: certificates.k8s)
            ),
            k8s_aggregator=ClusterCertificate.from_output(
                output.apply(lambda certificates: certificates.k8s_aggregator)
            ),
            k8s_serviceaccount=ClusterKey.from_output(
                output.apply(lambda certificates: certificates.k8s_serviceaccount)
            ),
            os=ClusterCertificate.from_output(
                output.apply(lambda certificates: certificates.os)
            ),
        )

    def to_args(self) -> talos.machine.CertificatesArgs:
        return talos.machine.CertificatesArgs(
            etcd=self.etcd.to_args(),
            k8s=self.k8s.to_args(),
            k8s_aggregator=self.k8s_aggregator.to_args(),
            k8s_serviceaccount=self.k8s_serviceaccount.to_args(),
            os=self.os.to_args(),
        )


class Cluster(BaseModel):
    id: Output[str]
    secret: Output[str]

    @classmethod
    def from_output(cls, output: Output[talos.machine.outputs.ClusterResult]) -> Self:
        return cls(
            id=output.apply(lambda cluster: cluster.id),
            secret=output.apply(lambda cluster: cluster.secret),
        )

    def to_args(self) -> talos.machine.ClusterArgs:
        return talos.machine.ClusterArgs(
            id=self.id,  # type: ignore [arg-type]
            secret=self.secret,  # type: ignore [arg-type]
        )


class ClusterKubernetesSecrets(BaseModel):
    bootstrap_token: Output[str]
    secretbox_encryption_secret: Output[str]
    aescbc_encryption_secret: Output[str | None]

    @classmethod
    def from_output(
        cls, output: Output[talos.machine.outputs.KubernetesSecretsResult]
    ) -> Self:
        return cls(
            bootstrap_token=output.apply(
                lambda kubernetes_secrets: kubernetes_secrets.bootstrap_token
            ),
            secretbox_encryption_secret=output.apply(
                lambda kubernetes_secrets: (
                    kubernetes_secrets.secretbox_encryption_secret
                )
            ),
            aescbc_encryption_secret=output.apply(
                lambda kubernetes_secrets: kubernetes_secrets.aescbc_encryption_secret
            ),
        )

    def to_args(self) -> talos.machine.KubernetesSecretsArgs:
        return talos.machine.KubernetesSecretsArgs(
            bootstrap_token=self.bootstrap_token,  # type: ignore [arg-type]
            secretbox_encryption_secret=self.secretbox_encryption_secret,  # type: ignore [arg-type]
            aescbc_encryption_secret=self.aescbc_encryption_secret,  # type: ignore [arg-type]
        )


class ClusterTrustdInfo(BaseModel):
    token: Output[str]

    @classmethod
    def from_output(
        cls, output: Output[talos.machine.outputs.TrustdInfoResult]
    ) -> Self:
        return cls(token=output.apply(lambda trustd_info: trustd_info.token))

    def to_args(self) -> talos.machine.TrustdInfoArgs:
        return talos.machine.TrustdInfoArgs(
            token=self.token,  # type: ignore [arg-type]
        )


class ClusterMachineSecrets(BaseModel):
    certs: ClusterCertificates
    cluster: Cluster
    secrets: ClusterKubernetesSecrets
    trustdinfo: ClusterTrustdInfo

    @classmethod
    def from_output(
        cls, output: Output[talos.machine.outputs.MachineSecretsResult]
    ) -> Self:
        return cls(
            certs=ClusterCertificates.from_output(
                output.apply(lambda machine_secrets: machine_secrets.certs)
            ),
            cluster=Cluster.from_output(
                output.apply(lambda machine_secrets: machine_secrets.cluster)
            ),
            secrets=ClusterKubernetesSecrets.from_output(
                output.apply(lambda machine_secrets: machine_secrets.secrets)
            ),
            trustdinfo=ClusterTrustdInfo.from_output(
                output.apply(lambda machine_secrets: machine_secrets.trustdinfo)
            ),
        )

    def to_args(self) -> talos.machine.MachineSecretsArgs:
        return talos.machine.MachineSecretsArgs(
            certs=self.certs.to_args(),
            cluster=self.cluster.to_args(),
            secrets=self.secrets.to_args(),
            trustdinfo=self.trustdinfo.to_args(),
        )


class ClusterSecrets:
    def __init__(self, *, opts: ResourceOptions | None, version: str) -> None:
        self._secrets = talos.machine.Secrets(
            "secrets", opts=opts, talos_version=version
        )

        self.client_configuration = ClusterClientConfiguration.from_output(
            self._secrets.client_configuration
        )
        self.machine_secrets = ClusterMachineSecrets.from_output(
            self._secrets.machine_secrets
        )
