除了通过名称直接访问模型属性（例如 `model.foobar`）之外，还可以通过多种方式转换和导出模型：

## `model.dict(...)`

这是将模型转换为字典的主要方式。 子模型将递归地转换为字典。

参数:

* `include`: 要包含在返回字典中的字段； 见 [下文](#advanced-include-and-exclude)
* `exclude`: 从返回的字典中排除的字段； 见 [下文](#advanced-include-and-exclude)
* `by_alias`: 字段别名是否应该用作返回字典中的键； 默认`false`
* `exclude_unset`: 是否应从返回的字典中排除在创建模型时未明确设置的字段； 默认`false`。
    在 **v1.0** 之前，`exclude_unset` 被称为 `skip_defaults`； `skip_defaults` 的使用现已弃用
* `exclude_defaults`: 是否应从返回的字典中排除等于其默认值（无论是否设置）的字段； 默认“假”
* `exclude_none`: 是否应从返回的字典中排除等于`None`的字段； 默认`false`。

例子:

{!.tmp_examples/exporting_models_dict.md!}

## `dict(model)` 和迭代(`dict(model)` and iteration)

*pydantic* 模型也可以使用 `dict(model)` 转换为字典，您还可以使用 `for field_name, value in model:` 迭代模型的字段。 使用这种方法返回原始字段值，因此子模型不会转换为字典。

例子:

{!.tmp_examples/exporting_models_iterate.md!}

## `model.copy(...)`

`copy()` 允许复制模型，这对于不可变模型特别有用。

参数:

* `include`: 要包含在返回字典中的字段； 见 [下文](#advanced-include-and-exclude)
* `exclude`: 从返回的字典中排除的字段； 见 [下文](#advanced-include-and-exclude)
* `update`: 创建复制模型时要更改的值字典
* `deep`: 是否对新模型进行深拷贝； 默认`false`。

例子:

{!.tmp_examples/exporting_models_copy.md!}

## `model.json(...)`

The `.json()` method will serialise a model to JSON. (For models with a [custom root type](models.md#custom-root-types),
only the value for the `__root__` key is serialised)

参数:

* `include`: 要包含在返回字典中的字段； 见 [下文](#advanced-include-and-exclude)
* `exclude`: 从返回的字典中排除的字段； 见 [下文](#advanced-include-and-exclude)
* `by_alias`: 字段别名是否应该用作返回字典中的键； 默认`false`。
* `exclude_unset`: 是否应从返回的字典中排除在创建模型时未设置且具有默认值的字段； 默认`false`。
  在 **v1.0** 之前，`exclude_unset` 被称为 `skip_defaults`； `skip_defaults` 的使用现已弃用
* `exclude_defaults`: 是否应从返回的字典中排除等于其默认值（无论是否设置）的字段； 默认`false`。
* `exclude_none`: 是否应从返回的字典中排除等于`None`的字段； 默认`false`。
* `encoder`: 传递给 `json.dumps()` 的 `default` 参数的自定义编码器函数； 默认为自定义编码器，旨在处理所有常见类型。
* `**dumps_kwargs`: 任何其他关键字参数都传递给 `json.dumps()` ，例如 `indent`。

*pydantic* 可以将许多常用类型序列化为 JSON（例如`datetime`、`date`或`UUID`），这通常会因简单的`json.dumps(foobar)`而失败。

{!.tmp_examples/exporting_models_json.md!}

### `json_encoders`

可以使用 `json_encoders` 配置属性在模型上自定义序列化； 键应该是类型（或前向引用的类型名称），值应该是序列化该类型的函数（参见下面的示例）：

{!.tmp_examples/exporting_models_json_encoders.md!}

默认情况下，`timedelta`被编码为总秒数的简单浮点数。 `timedelta_isoformat` 作为一个可选的替代方案提供，它实现了 [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) 时间差异编码。

`json_encoders` 也在模型继承期间合并，子编码器优先于父编码器。

{!.tmp_examples/exporting_models_json_encoders_merge.md!}

### 序列化自引用或其他模型(Serialising self-reference or other models)

默认情况下，模型被序列化为字典。

如果你想以不同的方式序列化它们，你可以在调用 `json()` 方法时添加 `models_as_dict=False` 并在 `json_encoders` 中添加模型的类。

在前向引用的情况下，您可以使用带有类名的字符串而不是类本身

{!.tmp_examples/exporting_models_json_forward_ref.md!}

### 序列化子类(Serialising subclasses)

!!! note
    版本 **v1.5** 中的新功能。

    在 **v1.5** 之前，普通类型的子类不会自动序列化为 JSON。

公共类型的子类像它们的超类一样自动编码：

{!.tmp_examples/exporting_models_json_subclass.md!}

### 自定义 JSON（反）序列化(Custom JSON (de)serialisation)

为了提高编码和解码 JSON 的性能，可以通过 `Config` 的 `json_loads` 和 `json_dumps` 属性使用替代 JSON 实现（例如 [ujson](https://pypi.python.org/pypi/ujson)） `。

{!.tmp_examples/exporting_models_ujson.md!}

`ujson` 通常不能用于转储 JSON，因为它不支持日期时间等对象的编码，并且不接受 `default` 回退函数参数。 为此，您可以使用另一个库，例如 [orjson](https://github.com/ijl/orjson)。

{!.tmp_examples/exporting_models_orjson.md!}

请注意，`orjson` 本身负责处理 `datetime` 编码，使其比 `json.dumps` 更快，但这意味着您不能总是使用 `Config.json_encoders` 自定义编码。

## `pickle.dumps(model)`

使用与 `copy()` 相同的方案，*pydantic* 模型支持高效的 pickling 和 unpickling。

{!.tmp_examples/exporting_models_pickle.md!}

## 高级包含和排除(Advanced include and exclude)

`dict`、`json` 和 `copy` 方法支持 `include` 和 `exclude` 参数，它们可以是集合或字典。 这允许嵌套选择要导出的字段：

{!.tmp_examples/exporting_models_exclude1.md!}

`True` 表示我们想要排除或包含整个键，就好像我们将它包含在一个集合中一样。 当然，可以在任何深度级别进行相同的操作。

在从子模型或字典的列表或元组中包含或排除字段时必须特别小心。 在这种情况下，`dict` 和相关方法需要整数键来按元素包含或排除。 要从列表或元组的**每个**成员中排除一个字段，可以使用字典键`__all__`，如下所示：

{!.tmp_examples/exporting_models_exclude2.md!}

`json` 和 `copy` 方法也是如此。

### 模型和字段级别包含和排除(Model and field level include and exclude)

除了传递给 `dict`、`json` 和 `copy` 方法的显式参数 `exclude` 和 `include` 之外，我们还可以将 `include`/`exclude` 参数直接传递给 `Field` 构造函数或 模型`Config`类中的等效`Field`实例：

{!.tmp_examples/exporting_models_exclude3.md!}

在使用多种策略的情况下，`exclude`/`include`字段按照以下规则进行合并：

* 首先，模型配置级别设置（通过`Field`实例）按字段与字段构造器设置（即`Field(..., exclude=True)`）合并，字段构造器优先。
* 结果设置按类与 `dict`、`json`、`copy` 调用的显式设置合并，显式设置优先。

请注意，在合并设置时，`exclude` 通过计算键的`union`合并，而`include` 通过计算键的`交集(intersection)`合并。

生成的合并排除设置：

{!.tmp_examples/exporting_models_exclude4.md!}

与使用合并包含设置相同，如下所示：

{!.tmp_examples/exporting_models_exclude5.md!}
