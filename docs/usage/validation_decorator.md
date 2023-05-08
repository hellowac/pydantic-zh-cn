`validate_arguments` 装饰器允许传递给函数的参数在调用函数之前使用函数的注释进行解析和验证。 在引擎盖下，它使用相同的模型创建和初始化方法； 它提供了一种极其简单的方法，可以使用最少的样板文件将验证应用于您的代码。

!!! info "测试版"
    `validate_arguments` 装饰器在 **beta** 中，它已在**临时基础**上添加到 **v1.5** 中的 *pydantic*。 它可能会在未来的版本中发生重大变化，其界面将在 **v2** 之前具体化。 来自社区的反馈在它仍然是临时的时候将非常有用； 评论 [#1205](https://github.com/pydantic/pydantic/issues/1205) 或创建一个新问题。

使用示例：

{!.tmp_examples/validation_decorator_main.md!}

## 参数类型(Argument Types)

参数类型是从函数的类型注释中推断出来的，没有类型装饰器的参数被认为是`Any`。 由于 `validate_arguments` 在内部使用标准的 `BaseModel`，因此可以验证 [types](types.md) 中列出的所有类型，包括 *pydantic* 模型和 [自定义类型](types.md#custom-data-types)。 与 *pydantic* 的其余部分一样，类型可以在传递给实际函数之前由装饰器强制转换：

{!.tmp_examples/validation_decorator_types.md!}

一些注意事项：

- 尽管它们作为字符串传递，但装饰器将 `path` 和 `regex` 分别转换为 `Path` 对象和 `regex`
- `max` 没有类型注释，因此将被装饰器视为 `Any`

像这样的类型强制可能非常有用，但也会造成混淆或不受欢迎，请参阅[下文](#coercion-and-strictness)，了解 `validate_arguments` 在这方面的局限性。

## 函数签名(Function Signatures)

装饰器旨在使用所有可能的参数配置及其所有可能的组合来处理函数：

- 带或不带默认值的位置或关键字参数
- 通过 `*` 定义的变量位置参数（通常是 `*args`）
- 通过 `**` 定义的变量关键字参数（通常是 `**kwargs`）
- 仅关键字参数 - `*,` 之后的参数
- 仅位置参数 - `, /` 之前的参数（Python 3.8 中的新功能）

演示以上所有参数类型：

{!.tmp_examples/validation_decorator_parameter_types.md!}

## 使用Field描述函数参数(Using Field to describe function arguments)

[Field](schema.md#field-customization) 也可以与`validate_arguments`一起使用，以提供有关字段和验证的额外信息。 一般来说，它应该在带有 [Annotated](schema.md#typingannotated-fields) 的类型提示中使用，除非指定了 `default_factory`，在这种情况下，它应该用作字段的默认值：

{!.tmp_examples/validation_decorator_field.md!}

[别名](model_config.md#alias-precedence) 可以像往常一样与装饰器一起使用。

{!.tmp_examples/validation_decorator_field_alias.md!}

## 和mypy一起使用(Usage with mypy)

`validate_arguments` 装饰器应该与 [mypy](http://mypy-lang.org/) 一起“开箱即用”，因为它被定义为返回一个与它装饰的函数具有相同签名的函数。 唯一的限制是因为我们欺骗 `mypy` 认为装饰器返回的函数与被装饰的函数相同； 访问 [raw function](#raw-function) 或其他属性将需要设置 `type: ignore`。

## 无需调用函数的校验(Validate without calling the function)

默认情况下，参数验证是通过直接调用带有参数的装饰函数来完成的。 但是，如果您想在不 *实际* 调用函数的情况下验证它们怎么办？ 为此，您可以调用绑定到装饰函数的 `validate` 方法。

{!.tmp_examples/validation_decorator_validate.md!}

## 原始函数(Raw function)

被装饰的原始函数是可访问的，如果在某些情况下您信任您的输入参数并希望以最高性能的方式调用该函数，这将很有用（请参阅下面的[性能说明](#performance)）：

{!.tmp_examples/validation_decorator_raw_function.md!}

## 异步函数(Async Functions)

`validate_arguments` 也可以用于异步函数：

{!.tmp_examples/validation_decorator_async.md!}

## 自定义配置(Custom Config)

`validate_arguments` 背后的模型可以使用配置设置进行自定义，这相当于在普通模型中设置 `Config` 子类。

!!! warning
    `@validate_arguments` 尚不支持允许配置别名的 `Config` 的 `fields` 和 `alias_generator` 属性，使用它们会引发错误。

配置是使用装饰器的 `config` 关键字参数设置的，它可以是配置类或稍后转换为类的属性字典。

{!.tmp_examples/validation_decorator_config.md!}

## 限制(Limitations)

`validate_arguments` 已在临时基础上发布，没有所有花里胡哨的东西，可能会在以后添加，请参阅 [#1205](https://github.com/pydantic/pydantic/issues/1205) 以获得更多关于这方面的信息。

尤其：

### 校验异常(Validation Exception)

目前在验证失败时，会引发标准的 *pydantic* `ValidationError`，请参阅[模型错误处理](models.md#error-handling)。

这很有用，因为它的 `str()` 方法提供了所发生错误的有用详细信息，而 `.errors()` 和 `.json()` 等方法在向最终用户公开错误时很有用，但是 `ValidationError` 继承自 `ValueError` **不是** `TypeError` 这可能是意外的，因为 Python 会在无效或缺少参数时引发 `TypeError`。 将来可以通过允许自定义错误或默认引发不同的异常或两者同时解决。

### 强制和严格(Coercion and Strictness)

*pydantic* 目前倾向于尝试强制类型而不是在类型错误时引发错误，请参阅 [模型数据转换](models.md#data-conversion) 和 `validate_arguments` 也不例外。

请参阅 [#1098](https://github.com/pydantic/pydantic/issues/1098) 和其他带有“严格”标签的问题，以了解对此的讨论。 如果 *pydantic* 将来获得“严格”模式，`validate_arguments` 将可以选择使用它，它甚至可能成为装饰器的默认模式。

### 性能(Performance)

我们付出了巨大的努力使 *pydantic* 尽可能高效，并且参数检查和模型创建仅在定义函数时执行一次，但是与调用原始函数相比，使用 `validate_arguments` 装饰器仍然会对性能产生影响。

在许多情况下，这几乎没有或根本没有明显的影响，但是请注意，`validate_arguments` 不是强类型语言中函数定义的等效项或替代项； 永远不会。

### 返回值(Return Value)

函数的返回值未根据其返回类型注释进行验证，这可能会在将来添加为一个选项。

### 配置和校验(Config and Validators)

不支持自定义 [`Config`](model_config.md) 上的 `fields` 和 `alias_generator`，请参见 [above](#custom-config)。

[验证器](validators.md) 也不是。

### 模型字段和保留参数(Model fields and reserved arguments)

以下名称可能不会被参数使用，因为它们可以在内部用于存储有关函数签名的信息：

- `v__args`
- `v__kwargs`
- `v__positional_only`

这些名称（与`“args”`和`“kwargs”`一起）可能会或可能不会（取决于函数的签名）显示为内部*pydantic*模型上的字段，可通过`.model`访问，因此该模型不是 目前特别有用（例如用于生成模式）。

随着错误产生方式的改变，这在未来应该是可以修复的。
