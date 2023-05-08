[Hypothesis](https://hypothesis.readthedocs.io/) 是用于[基于属性的测试](https://increment.com/testing/in-praise-of-property-based-testing/) 的 Python 库。 Hypothesis 可以从 [`typing`](https://docs.python.org/3/library/typing.html) 中推断出如何构造带类型注释的类，并支持内置类型、许多标准库类型和泛型类型 和 [`typing_extensions`](https://pypi.org/project/typing-extensions/) 默认模块。

从 Pydantic v1.8 和 [Hypothesis v5.29.0](https://hypothesis.readthedocs.io/en/latest/changes.html#v5-29-0)，Hypothesis 将自动加载对[自定义类型](usage/types.md) 像 `PaymentCardNumber` 和 `PositiveFloat`，这样 [`st.builds()`](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.builds ) 和 [`st.from_type()`](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.from_type) 策略无需任何用户配置即可支持它们。

!!! warning
    请注意，虽然插件支持这些类型，但假设将（当前）为受约束的函数类型生成给定参数之外的值。

### 示例测试 Example tests

{!.tmp_examples/hypothesis_property_based_test.md!}

### 与 JSON 模式一起使用 Use with JSON Schemas

要测试客户端代码，您可以将 [`Model.schema()`](usage/models.md) 与 [`hypothesis-jsonschema` 包](https://pypi.org/project/hypothesis-jsonschema /) 生成与模式匹配的任意 JSON 实例。 对于 Web API 测试，[Schemathesis](https://schemathesis.readthedocs.io) 提供了更高级别的包装器，可以检测错误和安全漏洞。
