from __future__ import annotations

from functools import lru_cache

from aws_cdk.aws_lambda import Code, SingletonFunction, Runtime
from aws_cdk.core import Stack, Duration
from b_twilio_sdk_layer.layer import Layer as TwilioLayer


class TwilioWorkflowSingletonFunction(SingletonFunction):
    """
    Custom workflow resource Singleton Lambda function.

    Creates a workflow on stack creation.
    Updates the workflow on workflow name change.
    Deletes the workflow on stack deletion.
    """

    def __init__(
            self,
            scope: Stack,
            name: str
    ) -> None:
        self.__name = name

        super().__init__(
            scope=scope,
            id=name,
            uuid=f'454c0197-1ebc-4988-ad2a-c567eea6143a',
            function_name=name,
            code=self.__code(),
            layers=[TwilioLayer(scope, f'TwilioLayerFor{name}')],
            timeout=Duration.minutes(1),
            handler='main.index.handler',
            runtime=Runtime.PYTHON_3_8
        )

    @lru_cache
    def __code(self) -> Code:
        from .source import root
        return Code.from_asset(root)

    @property
    def function_name(self):
        return self.__name
