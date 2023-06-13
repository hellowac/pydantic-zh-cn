!!! note

    译者注: **JSON Schema** 就是一种描述JSON数据长什么样子的规范和格式，详情参考[JSON Schema 规范（中文版）](https://json-schema.apifox.cn/){target="_blank"}

    对于将 JSON-schema 转化为 md 文档，参考: [jsonschema2md2](https://pypi.org/project/jsonschema2md2/){target="_blank"}

    对于 在mkdocs 中展示 JSON-schema, 参考: [mkdocs-schema-reader](https://pypi.org/project/mkdocs-schema-reader/){target="_blank"}

    对于 直接根据 JSON-schema 生成 HTML文档, 参考: [json-schema-for-humans](https://pypi.org/project/json-schema-for-humans/){target="_blank"}

*Pydantic* 允许从模型自动创建 JSON 模式(Schema)：

{!.tmp_examples/schema_main.md!}

生成的模式符合规范：
[JSON Schema Core](https://json-schema.org/latest/json-schema-core.html),
[JSON Schema Validation](https://json-schema.org/latest/json-schema-validation.html) 和
[OpenAPI](https://github.com/OAI/OpenAPI-Specification).

`BaseModel.schema` 将返回模式的字典，而 `BaseModel.schema_json` 将返回该字典的 JSON 字符串表示。

根据规范，使用的子模型被添加到 `definitions` JSON 属性中并被引用。

所有子模型（及其子模型）模式都直接放在顶级“定义”JSON 键中，以便于重用和参考。

带有自定义标题、描述或默认值等修改（通过 `Field` 类）的“子模型”被递归包含，而不是被引用。

模型的 `description` 取自类的文档字符串或`Field`类的参数 `description` 。

默认情况下，模式是使用别名作为键生成的，但可以使用模型属性名称通过调用 `MainModel.schema/schema_json(by_alias=False)` 来生成。

`$ref` 的格式（上面的`"#/definitions/FooBar"`）可以通过使用 `ref_template` 关键字参数调用 `schema()` 或 `schema_json()` 来改变，
例如 `ApplePie.schema(ref_template='/schemas/{model}.json#/')`，这里的 `{model}` 将替换为使用 `str.format()` 的模型命名。

## 获取指定类型的schema Getting schema of a specified type

*Pydantic* 包括两个独立的实用程序函数 `schema_of` 和 `schema_json_of`，可用于以更特殊的方式应用用于 *pydantic* 模型的模式生成逻辑。
这些函数的行为类似于 `BaseModel.schema` 和 `BaseModel.schema_json`，但适用于任意与 pydantic 兼容的类型。

{!.tmp_examples/schema_ad_hoc.md!}

## Field定制 Field customization

可选地，`Field`函数可用于提供有关字段和验证的额外信息。

它有以下参数：

* `default`: （位置参数）字段的默认值。
    由于 `Field` 替换了字段的默认值，因此第一个参数可用于设置默认值。
    使用省略号 (`...`) 表示该字段是必填项。
* `default_factory`: 当此字段需要默认值时将调用的零参数可调用对象。
    除其他用途外，这可用于设置动态默认值。
    禁止同时设置 `default` 和 `default_factory`。
* `alias`: 字段的公开名称
* `title`: 如果省略，则使用 `field_name.title()`
* `description`: 如果省略并且注解是子模型，则将使用子模型的文档字符串
* `exclude`: 转储（`.dict` 和 `.json`）实例时排除此字段。 [导出模型部分](exporting_models.md#advanced-include-and-exclude) 中详细描述了确切的语法和配置选项。
* `include`: 转储（`.dict` 和 `.json`）实例时（仅）包含此字段。 [导出模型部分](exporting_models.md#advanced-include-and-exclude) 中详细描述了确切的语法和配置选项。
* `const`: 如果存在，此参数*必须*与字段的默认值相同。
* `gt`: 对于数值（``int``、`float`、`Decimal`），向 JSON Schema 添加“大于”验证和 `exclusiveMinimum` 注释
* `ge`: 对于数值，这会向 JSON 模式添加“大于或等于”验证和`最小值(minimum)`注释
* `lt`: 对于数值，这会向 JSON 模式添加“小于”验证和`exclusiveMinimum`注释
* `le`: 对于数值，这会向 JSON 模式添加“小于或等于”验证和`最大值(maximum)`注释
* `multiple_of`: 对于数值，这会向 JSON 模式添加“倍数”的验证和`multipleOf`的注释
* `max_digits`: 对于 `Decimal` 值，这会添加验证以在小数点内具有最大位数。 它不包括小数点前的零或尾随的小数零。
* `decimal_places`: 对于 `Decimal`值，这会添加一个验证，以允许最多有多个小数位。 它不包括尾随的小数零。
* `min_items`: 对于列表值，这会向 JSON 模式添加相应的验证和 `minItems` 的注释
* `max_items`: 对于列表值，这会向 JSON 模式添加相应的验证和 `maxItems` 的注释
* `unique_items`: 对于列表值，这会向 JSON 模式添加相应的验证和 `uniqueItems` 的注释
* `min_length`: 对于字符串值，这会向 JSON 模式添加相应的验证和 `minLength` 注释
* `max_length`: 对于字符串值，这会向 JSON 模式添加相应的验证和 `maxLength` 注释
* `allow_mutation`: 一个默认为 `True` 的布尔值。 为 False 时，如果字段是在实例上分配的，则该字段会引发 `TypeError`。 模型配置必须将`validate_assignment`设置为`True`才能执行此检查。
* `regex`: 对于字符串值，这会向 JSON 模式添加从传递的字符串生成的正则表达式验证和 `pattern` 注释

  !!! note
      *pydantic* 使用 `re.match` 验证字符串，它将正则表达式视为隐式锚定在开头。 相反，JSON Schema 验证器将 `pattern` 关键字视为隐式未锚定的，更像是 `re.search` 所做的。

      对于互操作性，根据您想要的行为，要么显式地使用 `^` 锚定您的正则表达式（例如 `^foo` 以匹配任何以 `foo` 开头的字符串），或者显式地允许带有 `.*?` 的任意前缀（例如 `.*?foo` 匹配任何包含子字符串 `foo` 的字符串）。

      请参阅 [#1631](https://github.com/pydantic/pydantic/issues/1631)，了解 **v2** 中对 *pydantic* 行为的可能更改的讨论。

* `repr`: 一个默认为`True`的布尔值。 当为 False 时，该字段应从对象表示中隐藏。
* `**` 任何其他关键字参数（例如 `examples`）将被逐字添加到字段的模式中

除了使用`Field`，[Config 类](model_config.md) 的`fields`属性可用于设置除`default`之外的所有上述参数。

### 非强制字段约束 Unenforced Field constraints

如果 *pydantic* 发现未强制执行的约束，则会引发错误。 如果你想强制约束出现在模式中，即使它在解析时没有被检查，你可以使用带有原始模式属性名称的 `Field()` 的可变参数：

{!.tmp_examples/schema_unenforced_constraints.md!}

### typing.Annotated 字段 Fields

与其分配`Field`值，不如在类型提示中使用`typing.Annotated`指定：

{!.tmp_examples/schema_annotated.md!}

`Field` 每个字段只能提供一次 - 如果在 `Annotated` 中使用并作为赋值，将引发错误。

默认值可以在 `Annotated` 之外设置为指定值，也可以在 `Annotated` 内使用 `Field.default_factory` 设置 - `Field.default` 参数在 `Annotated` 中不受支持。

对于 3.9 之前的 Python 版本，可以使用 `typing_extensions.Annotated`。

## 修改自定义字段的schema Modifying schema in custom fields

自定义字段类型可以使用 `__modify_schema__` 类方法自定义为它们生成的模式； 有关详细信息，请参阅 [自定义数据类型](types.md#custom-data-types)。

`__modify_schema__` 也可以采用类型为 `Optional[ModelField]` 的 `field` 参数。 *pydantic* 将检查 `__modify_schema__` 的签名以确定是否应包含 `field` 参数。

{!.tmp_examples/schema_with_field.md!}

## JSON Schema 类型(Types)

类型、自定义字段类型和约束（如`max_length`）按以下优先顺序映射到相应的规范格式（当有等效项可用时）：

1. [JSON Schema Core](http://json-schema.org/latest/json-schema-core.html#rfc.section.4.3.1)
2. [JSON Schema Validation](http://json-schema.org/latest/json-schema-validation.html)
3. [OpenAPI Data Types](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#data-types)
4. 标准的 `format` JSON 字段用于为更复杂的 `string` 子类型定义 *pydantic* 扩展。

从 Python / *pydantic* 到 JSON Schema 的字段模式映射完成如下：

{!.tmp_schema_mappings.html!}

## 顶层Schema生成 Top-level schema generation

您还可以生成一个顶级 JSON 架构，该架构仅在其`definitions`中包含模型列表和相关子模型：

{!.tmp_examples/schema_top_level.md!}

## schema定制 Schema customization

您可以自定义生成的 `$ref` JSON 位置：定义始终存储在键 `definitions` 下，但可以为引用使用指定的前缀。

如果您需要扩展或修改 JSON Schema 默认定义位置，这将很有用。 例如: 使用 OpenAPI：

{!.tmp_examples/schema_custom.md!}

也可以扩展/覆盖模型中生成的 JSON 模式。

为此，请使用`Config`子类属性`schema_extra`。

例如，您可以将 `examples` 添加到 JSON Schema：

{!.tmp_examples/schema_with_example.md!}

对于更细粒度的控制，您可以选择将 `schema_extra` 设置为可调用的，并对生成的模式进行后处理。
可调用对象可以有一个或两个位置参数。
第一个是模式字典。
第二个，如果被接受，将是模型类。
可调用对象预计会*就地*改变模式字典； 不使用返回值。

例如，可以从模型的“属性”中删除“标题”键：

{!.tmp_examples/schema_extra_callable.md!}
