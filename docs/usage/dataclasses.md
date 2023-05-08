如果您不想使用 _pydantic_ 的 `BaseModel`，您可以在标准 [dataclasses](https://docs.python.org/3/library/dataclasses.html) 上获得相同的数据验证（在 Python 3.7 中引入） .

{!.tmp_examples/dataclasses_main.md!}

!!! note
    请记住，`pydantic.dataclasses.dataclass` 是带验证的 `dataclasses.dataclass` 的直接替代品，**不是** `pydantic.BaseModel` 的替代品（[初始化挂钩](#initialize-hooks)的工作方式略有不同）。 在某些情况下，子类化 `pydantic.BaseModel` 是更好的选择。

    有关更多信息和讨论，请参阅 [pydantic/pydantic#710](https://github.com/pydantic/pydantic/issues/710)。

您可以使用所有标准 _pydantic_ 字段类型，生成的数据类将与标准库`dataclass`装饰器创建的数据类相同。

可以通过 `__pydantic_model__` 访问底层模型及其模式。 此外，需要 `default_factory` 的字段可以由 `pydantic.Field` 或 `dataclasses.field` 指定。

{!.tmp_examples/dataclasses_default_schema.md!}

`pydantic.dataclasses.dataclass` 的参数与标准装饰器相同，除了一个额外的关键字参数 `config` 与 [Config](model_config.md) 具有相同的含义。

!!! warning
    在 v1.2 之后，必须安装 [Mypy 插件](../mypy_plugin.md) 来类型检查 _pydantic_ 数据类。

有关将验证器与数据类组合的更多信息，请参阅 [数据类验证器](validators.md#dataclass-validators)。

## 数据类配置(Dataclass Config)

如果您想像修改 `BaseModel` 一样修改 `Config`，您有以下三种选择：

{!.tmp_examples/dataclasses_config.md!}

!!! warning
    在 v1.10 之后，_pydantic_ 数据类支持 `Config.extra` 但 标准库 数据类的一些默认行为可能会占上风。 例如，当 `print`时带有允许的额外字段的 _pydantic_ 数据类时，它仍将使用 标准库 数据类的 `__str__` 方法并仅显示必需的字段。 未来可能会进一步改进这一点。

## 嵌套数据类(Nested dataclasses)

数据类和普通模型都支持嵌套数据类。

{!.tmp_examples/dataclasses_nested.md!}

数据类属性可以由元组、字典或数据类本身的实例填充。

## 标准库数据类和_pydantic_数据类(Stdlib dataclasses and _pydantic_ dataclasses)

### 转换标准库数据类为_pydantic_数据类(Convert stdlib dataclasses into _pydantic_ dataclasses)

标准库 数据类（嵌套或非嵌套）只需用 `pydantic.dataclasses.dataclass` 装饰即可轻松转换为 _pydantic_ 数据类。
_Pydantic_ 将增强给定的 标准库 数据类，但不会改变默认行为（即未经验证）。
相反，它将围绕它创建一个包装器来触发验证，就像一个普通代理一样。
仍然可以通过 `__dataclass__` 属性访问 标准库 数据类（参见下面的示例）。

{!.tmp_examples/dataclasses_stdlib_to_pydantic.md!}

### 选择何时触发校验(Choose when to trigger validation)

一旦你的 标准库 数据类被 _pydantic_ 数据类装饰器装饰，魔法方法就被添加来验证输入数据。 如果你愿意，你仍然可以继续使用你的数据类并选择何时触发它。

{!.tmp_examples/dataclasses_stdlib_run_validation.md!}

### 从标准库数据类继承(Inherit from stdlib dataclasses)

标准库 数据类（嵌套或非嵌套）也可以被继承，_pydantic_ 将自动验证所有继承的字段。

{!.tmp_examples/dataclasses_stdlib_inheritance.md!}

### 将标准库数据类与 `BaseModel` 一起使用(Use of stdlib dataclasses with `BaseModel`)

请记住，标准库 数据类（嵌套或非嵌套）在与 `BaseModel` 混合时会**自动转换**为_pydantic_数据类！ 此外，生成的 _pydantic_ 数据类将与原始配置具有**完全相同的配置**（`order`、`frozen`、...）。

{!.tmp_examples/dataclasses_stdlib_with_basemodel.md!}

### 使用自定义类型(Use custom types)

由于 标准库 数据类会自动转换为使用自定义类型添加验证，因此可能会导致一些意外行为。 在这种情况下，您只需在配置中添加 `arbitrary_types_allowed` 即可！

{!.tmp_examples/dataclasses_arbitrary_types_allowed.md!}

## 初始化钩子(Initialize hooks)

初始化数据类时，可以在 `__post_init_post_parse__` 的帮助下在 _验证后_ 执行代码。 这与 `__post_init__` 不同，它在验证之前执行代码。

!!! tip
    如果您使用 标准库 `dataclass`，您可能只有 `__post_init__` 可用，并希望在之前完成验证。 在这种情况下，您可以设置 `Config.post_init_call = 'after_validation'`

{!.tmp_examples/dataclasses_post_init_post_parse.md!}

从版本 **v1.0** 开始，任何用 `dataclasses.InitVar` 注释的字段都会传递给 `__post_init__` _和_ `__post_init_post_parse__`。

{!.tmp_examples/dataclasses_initvars.md!}

### 与标准库数据类的区别(Difference with stdlib dataclasses)

请注意，Python 标准库中的`dataclasses.dataclass`仅实现了`__post_init__`方法，因为它不运行验证步骤。

当用 `pydantic.dataclasses.dataclass` 替换 `dataclasses.dataclass` 的用法时，建议将 `__post_init__` 方法中执行的代码移动到 `__post_init_post_parse__` 方法中，只留下需要的部分代码 在验证之前执行。

## JSON Dumping

_Pydantic_ 数据类没有 `.json()` 函数。 要将它们转储为 JSON，您需要按如下方式使用 `pydantic_encoder`：

{!.tmp_examples/dataclasses_json_dumps.md!}
