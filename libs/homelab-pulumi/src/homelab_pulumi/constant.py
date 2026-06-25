import pulumi

STACK = stack if (stack := pulumi.get_stack()) != "prod" else None
