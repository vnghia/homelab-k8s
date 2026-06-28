import pulumi


class Context:
    def __init__(self) -> None:
        self.pulumi = pulumi.Config()
