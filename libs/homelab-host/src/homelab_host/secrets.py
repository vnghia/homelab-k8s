from typing import Self

import pulumiverse_talos as talos
from homelab_model import BaseModel
from pulumi import Output, ResourceOptions


class ClientConfiguration(BaseModel):
    ca_certificate: Output[str]
    client_certificate: Output[str]
    client_key: Output[str]

    @classmethod
    def from_output(cls, output: Output[talos.machine.outputs.ClientConfiguration]) -> Self:
        return cls(
            ca_certificate=output.apply(lambda result: result.ca_certificate),
            client_certificate=output.apply(lambda result: result.client_certificate),
            client_key=output.apply(lambda result: result.client_key),
        )

    def to_args(self) -> talos.machine.ClientConfigurationArgs:
        return talos.machine.ClientConfigurationArgs(
            ca_certificate=self.ca_certificate, client_certificate=self.client_certificate, client_key=self.client_key
        )


class Certificate(BaseModel):
    cert: Output[str]
    key: Output[str]

    @classmethod
    def from_output(cls, output: Output[talos.machine.outputs.CertificateResult]) -> Self:
        return cls(cert=output.apply(lambda result: result.cert), key=output.apply(lambda result: result.key))

    def to_args(self) -> talos.machine.CertificateArgs:
        return talos.machine.CertificateArgs(
            cert=self.cert,  # type: ignore [arg-type]
            key=self.key,  # type: ignore [arg-type]
        )


class Key(BaseModel):
    key: Output[str]

    @classmethod
    def from_output(cls, output: Output[talos.machine.outputs.KeyResult]) -> Self:
        return cls(key=output.apply(lambda result: result.key))

    def to_args(self) -> talos.machine.KeyArgs:
        return talos.machine.KeyArgs(
            key=self.key  # type: ignore [arg-type]
        )


class Certificates(BaseModel):
    etcd: Certificate
    k8s: Certificate
    k8s_aggregator: Certificate
    k8s_serviceaccount: Key
    os: Certificate

    @classmethod
    def from_output(cls, output: Output[talos.machine.outputs.CertificatesResult]) -> Self:
        return cls(
            etcd=Certificate.from_output(output.apply(lambda result: result.etcd)),
            k8s=Certificate.from_output(output.apply(lambda result: result.k8s)),
            k8s_aggregator=Certificate.from_output(output.apply(lambda result: result.k8s_aggregator)),
            k8s_serviceaccount=Key.from_output(output.apply(lambda result: result.k8s_serviceaccount)),
            os=Certificate.from_output(output.apply(lambda result: result.os)),
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
        return cls(id=output.apply(lambda cluster: cluster.id), secret=output.apply(lambda cluster: cluster.secret))

    def to_args(self) -> talos.machine.ClusterArgs:
        return talos.machine.ClusterArgs(
            id=self.id,  # type: ignore [arg-type]
            secret=self.secret,  # type: ignore [arg-type]
        )


class KubernetesSecrets(BaseModel):
    bootstrap_token: Output[str]
    secretbox_encryption_secret: Output[str]
    aescbc_encryption_secret: Output[str | None]

    @classmethod
    def from_output(cls, output: Output[talos.machine.outputs.KubernetesSecretsResult]) -> Self:
        return cls(
            bootstrap_token=output.apply(lambda result: result.bootstrap_token),
            secretbox_encryption_secret=output.apply(lambda result: result.secretbox_encryption_secret),
            aescbc_encryption_secret=output.apply(lambda result: result.aescbc_encryption_secret),
        )

    def to_args(self) -> talos.machine.KubernetesSecretsArgs:
        return talos.machine.KubernetesSecretsArgs(
            bootstrap_token=self.bootstrap_token,  # type: ignore [arg-type]
            secretbox_encryption_secret=self.secretbox_encryption_secret,  # type: ignore [arg-type]
            aescbc_encryption_secret=self.aescbc_encryption_secret,  # type: ignore [arg-type]
        )


class TrustdInfo(BaseModel):
    token: Output[str]

    @classmethod
    def from_output(cls, output: Output[talos.machine.outputs.TrustdInfoResult]) -> Self:
        return cls(token=output.apply(lambda result: result.token))

    def to_args(self) -> talos.machine.TrustdInfoArgs:
        return talos.machine.TrustdInfoArgs(
            token=self.token  # type: ignore [arg-type]
        )


class MachineSecrets(BaseModel):
    certs: Certificates
    cluster: Cluster
    secrets: KubernetesSecrets
    trustdinfo: TrustdInfo

    @classmethod
    def from_output(cls, output: Output[talos.machine.outputs.MachineSecretsResult]) -> Self:
        return cls(
            certs=Certificates.from_output(output.apply(lambda result: result.certs)),
            cluster=Cluster.from_output(output.apply(lambda result: result.cluster)),
            secrets=KubernetesSecrets.from_output(output.apply(lambda result: result.secrets)),
            trustdinfo=TrustdInfo.from_output(output.apply(lambda result: result.trustdinfo)),
        )

    def to_args(self) -> talos.machine.MachineSecretsArgs:
        return talos.machine.MachineSecretsArgs(
            certs=self.certs.to_args(),
            cluster=self.cluster.to_args(),
            secrets=self.secrets.to_args(),
            trustdinfo=self.trustdinfo.to_args(),
        )


class Secrets:
    def __init__(self, *, opts: ResourceOptions | None, version: str) -> None:
        self._secrets = talos.machine.Secrets("secrets", opts=opts, talos_version=version)

        self.client_configuration_output = self._secrets.client_configuration
        self.client_configuration = ClientConfiguration.from_output(self.client_configuration_output)

        self.machine_secrets_output = self._secrets.machine_secrets
        self.machine_secrets = MachineSecrets.from_output(self.machine_secrets_output)
