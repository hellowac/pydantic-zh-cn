_pydantic_ 的行为可以通过模型上的 `Config` 类或 _pydantic_ 数据类来控制。

{!.tmp_examples/model_config_main.md!}

此外，您可以将配置选项指定为模型类 kwargs：

{!.tmp_examples/model_config_class_kwargs.md!}

同样，如果使用`@dataclass`装饰器：

{!.tmp_examples/model_config_dataclass.md!}

## 可选项(Options)

**`title`**
: 生成的 JSON 模式的标题

**`anystr_strip_whitespace`**
: 是否去除 str & byte 类型的前导和尾随空格（默认值：`False`）

**`anystr_upper`**
: 是否将 str 和 byte 类型的所有字符都设为大写（默认值：`False`）

**`anystr_lower`**
: 是否将 str 和 byte 类型的所有字符都设为小写（默认值：`False`）

**`min_anystr_length`**
: str 和 byte 类型的最小长度（默认值：`0`）

**`max_anystr_length`**
: str & byte 类型的最大长度（默认值：`None`）

**`validate_all`**
: 是否验证字段默认值（默认值：`False`）

**`extra`**
: 在模型初始化期间是否忽略、允许或禁止额外的属性。 接受`“ignore”`、`“allow”`或`“forbid”`的字符串值，或`“Extra”`枚举的值（默认值：`“Extra.ignore”`）。 如果包含额外的属性，`'forbid'` 将导致验证失败，`'ignore'` 将默默地忽略任何额外的属性，`'allow'` 将属性分配给模型。

**`allow_mutation`**
: 模型是否是伪不可变的，即是否允许 `__setattr__`（默认值：`True`）

**`frozen`**

!!! warning
    此参数处于测试阶段

: 设置 `frozen=True` 会执行 `allow_mutation=False` 所做的一切，还会为模型生成 `__hash__()` 方法。 如果所有属性都是可散列的，这使得模型的实例可能是可散列的。 （默认值：`False`）

**`use_enum_values`**
: 是否使用枚举的`value`属性而不是原始枚举来填充模型。 如果您想稍后序列化 `model.dict()`（默认值：`False`），这可能很有用

**`fields`**
: 包含每个字段的架构信息的`dict`； 这等同于使用 [`Field` 类](schema.md)，除非已经通过注释或 Field 类定义了一个字段，在这种情况下只有 `alias`、`include`、`exclude`、`min_length`, `max_length`, `regex`, `gt`, `lt`, `gt`, `le`, `multiple_of`, `max_digits`, `decimal_places`, `min_items`, `max_items`, `unique_items` 和 `allow_mutation` 可以设置（例如你不能设置 `default_factory` 的默认值）（默认值：`None`）

**`validate_assignment`**
: 是否对属性的`_assignment_`执行验证（默认值：`False`）

**`allow_population_by_field_name`**
: 别名字段是否可以由模型属性给出的名称以及别名（默认值：`False`）填充

!!! note
    此配置设置的名称在 **v1.0** 中从`allow_population_by_alias`更改为`allow_population_by_field_name`。

**`error_msg_templates`**
: 用于覆盖默认错误消息模板的 `dict`。 传入一个字典，其中的键与您要覆盖的错误消息匹配（默认值：`{}`）

**`arbitrary_types_allowed`**
: 是否允许字段的任意用户类型（通过检查值是否是该类型的实例来验证它们）。 如果为`False`，将在模型声明时引发`RuntimeError`（默认值：`False`）。 请参阅 [Field Types](types.md#arbitrary-types-allowed) 中的示例。

**`orm_mode`**
: 是否允许使用 [ORM 模式](models.md#orm-mode-aka-arbitrary-class-instances)

**`getter_dict`**
: 在分解任意类进行验证时使用的自定义类（应继承自 `GetterDict`），与 `orm_mode` 一起使用； 参见 [数据绑定](models.md#data-binding)。

**`alias_generator`**
: 一个可调用的，它接受一个字段名并为其返回一个别名； 参见 [专用部分](#alias-generator)

**`keep_untouched`**
: 模型默认值的类型元组（例如描述符），在模型创建期间不应更改并且不会包含在模型模式中。 **注意**：这意味着模型上具有 _这种类型的默认值_ 而不是 _这种类型的注释_ 的属性将被单独保留。

**`schema_extra`**
: 用于扩展/更新生成的 JSON Schema 的 `dict`，或用于对其进行后处理的可调用对象； 参见 [schema 自定义](schema.md#schema-customization)

**`json_loads`**
: 用于解码 JSON 的自定义函数； 参见 [自定义 JSON（反）序列化](exporting_models.md#custom-json-deserialisation)

**`json_dumps`**
: 用于编码 JSON 的自定义函数； 参见 [自定义 JSON（反）序列化](exporting_models.md#custom-json-deserialisation)

**`json_encoders`**
: 用于自定义类型编码为 JSON 的方式的 `dict`； 参见 [JSON 序列化](exporting_models.md#modeljson)

**`underscore_attrs_are_private`**
: 是否将任何下划线非类属性视为私有，或保持原样； 参见 [私有模型属性](models.md#private-model-attributes)

**`copy_on_model_validation`**
: 字符串文字来控制模型实例在验证过程中的处理方式，使用以下方法（有关此字段更改的完整讨论，请参阅 [#4093](https://github.com/pydantic/pydantic/pull/4093) :

* `'none'` - 模型不会在验证时被复制，它们只是保持“不变(untouched)”
* `'shallow'` - 模型是浅拷贝的，这是默认的
* `'deep'` - 模型被深度复制

**`smart_union`**
: _pydantic_ 是否应该尝试检查 `Union` 中的所有类型以防止不希望的强制转换； 请参阅 [专用部分](#smart-union)

**`post_init_call`**
: stdlib 数据类 `__post_init__` 是否应该在解析和验证之前（默认行为值为 `'before_validation'`）或之后（值为 `'after_validation'`）运行[转换](dataclasses.md#stdlib-dataclasses-and -_pydantic_-数据类)。

**`allow_inf_nan`**
: 是否允许无穷大（`+inf` 和 `-inf`）和 NaN 值浮动字段，默认为 `True`，设置为 `False` 以兼容 `JSON`，参见[#3994](https:// github.com/pydantic/pydantic/pull/3994）了解更多详情，添加于**V1.10**

## 全局改变行为(Change behaviour globally)

如果您希望全局更改 _pydantic_ 的行为，您可以使用自定义 `Config` 创建自己的自定义 `BaseModel`，因为配置是继承的

{!.tmp_examples/model_config_change_globally_custom.md!}

## 别名生成器(Alias Generator)

如果数据源字段名称与您的代码风格不匹配（例如 CamelCase 字段），您可以使用 `alias_generator` 自动生成别名：

{!.tmp_examples/model_config_alias_generator.md!}

这里的驼峰案例指的是 [“大驼峰案例”](https://en.wikipedia.org/wiki/Camel_case) 又名帕斯卡案例，例如 `驼峰式`。 如果您想改用小驼峰式，例如 `camelCase`，而是使用 `to_lower_camel` 函数。

## 别名优先(Alias Precedence)

!!! warning
    别名优先级逻辑在 **v1.4** 中发生了变化，以解决以前版本中的错误和意外行为。
    在某些情况下，这可能代表一个**重大变化**，请参阅 [#1178](https://github.com/pydantic/pydantic/issues/1178) 和下面的优先顺序了解详细信息。

在一个字段的别名可能定义在多个地方的情况下，选择的值确定如下（按优先级降序排列）：

1. 通过 `Field(..., alias=<alias>)` 直接在模型上设置
2. 在 `Config.fields` 中定义，直接在模型上
3. 在父模型上通过 `Field(..., alias=<alias>)` 设置
4. 在父模型的`Config.fields`中定义
5. 由 `alias_generator` 生成，无论它是在模型上还是在父级上

!!! note
    这意味着在子模型上定义的 `alias_generator` **不会** 优先于在父模型中的字段上定义的别名。

例如：

{!.tmp_examples/model_config_alias_precedence.md!}

## 智能联合(Smart Union)

默认情况下，如 [此处](types.md#unions) 所述，_pydantic_ 尝试按照 `Union` 的顺序验证（并强制执行）。 所以有时候你可能会有意想不到的强制数据。

{!.tmp_examples/model_config_smart_union_off.md!}

为防止这种情况，您可以启用 `Config.smart_union`。 _Pydantic_ 然后会在尝试强制之前检查所有允许的类型。 要知道这当然会更慢，尤其是当你的 `Union` 很大的时候。

{!.tmp_examples/model_config_smart_union_on.md!}

!!! warning
    请注意，此选项**尚不支持复合类型**（例如，区分 `List[int]` 和 `List[str]`）。
    一旦在 _pydantic_ 中添加严格模式，此选项将得到进一步改进，并且可能成为 v2 中的默认行为！

{!.tmp_examples/model_config_smart_union_on_edge_case.md!}
