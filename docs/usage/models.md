在pydantic中定义对象的主要方法是通过模型（模型只是继承自的类`BaseModel`）。

您可以将模型视为类似于严格类型化语言中的类型，或者视为 API 中单个端点的要求。

不受信任的数据可以传递给模型，在解析和验证之后，`pydantic`保证生成的模型实例的字段将符合模型上定义的字段类型。

!!! 笔记

    *pydantic*主要是一个解析库，**而不是一个验证库**。

    验证是达到目的的一种手段：建立一个符合所提供的类型和约束的模型。

    换句话说，*pydantic*保证输出模型的类型和约束，而不是输入数据。
    
    这听起来像是一个深奥的区别，但事实并非如此。如果您不确定这意味着什么或它如何影响您的使用，您应该阅读下面有关[数据转换](#数据转换)的部分。
    
    虽然验证不是*pydantic*的主要目的，但您**可以**使用此库进行自定义[验证](validators.md)。

## 基本模型使用(Basic model usage)

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name = 'Jane Doe'
```

这儿的 `User`是一个有两个字段的模型，`id`一个是整数，是必需的，另一个`name`是字符串，不是必需的（它有一个默认值）。`name`的类型是从默认值推断出来的，因此不需要类型注释（但是当某些字段没有类型注释时请注意有关[字段顺序](#field-ordering)的警告）。

```py
user = User(id='123')
user_x = User(id='123.45')
```

这儿的 `user` 是 `User` 的实例，**对象的初始化将执行所有的解析和验证**。如果没有引发`ValidationError`，则生成的模型实例是有效的。

```py
assert user.id == 123
assert user_x.id == 123
assert isinstance(user_x.id, int)  # Note that 123.45 was casted to an int and its value is 123
```

有关`user_x`形式的数据转换的更多详细信息，请参阅[数据转换](#data-conversion)。
模型的字段可以作为用户对象的普通属性来访问。 根据字段类型，字符串“123”已转换为 int

```py
assert user.name == 'Jane Doe'
```

`name` 在用户初始化时没有设置，所以它有默认值

```py
assert user.__fields_set__ == {'id'}
```

初始化用户时提供的字段。

```py
assert user.dict() == dict(user) == {'id': 123, 'name': 'Jane Doe'}
```

`.dict()` 或 `dict(user)` 将提供字段的字典，但 `.dict()` 可以接受许多其他参数。

```py
user.id = 321
assert user.id == 321
```

该模型是可变的，因此可以更改字段值。

### 模型属性(Model properties)

上面的例子只展示了模型可以做什么的冰山一角。模型具有以下方法和属性：

`dict()`
: 返回模型字段和值的字典形式;
  参考 [导出模型](exporting_models.md#modeldict)

`json()`
: 返回一个 JSON 字符串表示 `dict()`；
  参考 [导出模型](exporting_models.md#modeljson)

`copy()`
: 返回模型的副本（默认情况下为浅副本）; 参考 [导出模型](exporting_models.md#modelcopy)

`parse_obj()`
: 如果对象不是字典，则用于将任何对象加载到模型中并进行错误处理的实用程序；
  参考 [辅助函数](#helper-functions)

`parse_raw()`
: 用于加载多种格式的字符串的辅助函数; 参考 [辅助函数] (#helper-functions)

`parse_file()`
: 类似于 `parse_raw()` 但用于文件路径； 参考 [辅助函数] (#helper-functions)

`from_orm()`
: 将数据从任意类加载到模型中； 参考 [ORM模式](#orm-mode-aka-arbitrary-class-instances)

`schema()`
: 返回将模型表示为 JSON Schema 的字典； 参考 [图式](schema.md)

`schema_json()`
: 返回 `schema()` 的 JSON 字符串表示； 参考 [图式](schema.md)

`construct()`
: 一种无需运行验证即可创建模型的类方法；
  参考 [创建无需校验的模型](#creating-models-without-validation)

`__fields_set__`
: 初始化模型实例时设置的字段名称集

`__fields__`
: 模型字段的字典

`__config__`
: 模型的配置类, 参考 [模型配置](model_config.md)

## 嵌套模型(Recursive Models)

可以使用模型本身作为注释中的类型来定义更复杂的分层数据结构。

{!.tmp_examples/models_recursive.md!}

对于自引用模型， 见 [延时注解](postponed_annotations.md#self-referencing-models).

## ORM 模式【又名任意类实例】 (aka Arbitrary Class Instances)

可以从任意类实例创建 Pydantic 模型以支持映射到 ORM 对象的模型。

去做这个：

1. [Config](model_config.md) 的属性 `orm_mode` 必须设置为 `True`.
2. 必须使用特殊构造函数 `from_orm` 来创建模型实例。

此处的示例使用 SQLAlchemy，但同样的方法适用于任何 ORM。

{!.tmp_examples/models_orm_mode.md!}

### 保留名称(Reserved names)

您可能希望在保留的 SQLAlchemy 字段之后重新命名。 在这种情况下，**Field** 别名会很方便：

{!.tmp_examples/models_orm_mode_reserved_name.md!}

!!! note

    上面的示例之所以有效，是因为别名优先于字段填充的字段名称。 访问 `SQLModel`的 `metadata` 属性会导致`ValidationError`。

### 嵌套ORM模型(Recursive ORM models)

ORM 实例将使用 `from_orm` 递归地以及在顶层进行解析。

这里使用普通类来演示原理，但也可以使用任何 ORM 类。

{!.tmp_examples/models_orm_mode_recursive.md!}

### 数据绑定(Data binding)

*pydantic* 使用 `GetterDict` 类处理任意类（参见 [utils.py](https://github.com/pydantic/pydantic/blob/1.10.X-fixes/pydantic/utils.py)）， 它试图为任何类提供类似字典的接口。 您可以通过将您自己的 `GetterDict` 子类设置为 `Config.getter_dict` 的值来自定义其工作方式（参见 [config](model_config.md)）。

您还可以使用带有 `pre=True` 的 [root_validators](validators.md#root-validators) 自定义类验证。
在这种情况下，您的验证器函数将被传递给您可以复制和修改的 `GetterDict` 实例。

将为每个字段调用 `GetterDict` 实例，并将标记（如果未设置其他默认值）。 返回此标记意味着该字段丢失。 任何其他值都将被解释为该字段的值。

{!.tmp_examples/models_orm_mode_data_binding.md!}

## 错误处理(Error Handling)

*pydantic* 会在发现正在验证的数据中存在错误时引发 `ValidationError`。

!!! note

    验证代码不应引发 `ValidationError` 本身，而是引发 `ValueError`、`TypeError` 或 `AssertionError`（或 `ValueError` 或 `TypeError` 的子类），它们将被捕获并用于填充 `ValidationError`。

无论发现多少错误，都会引发一个异常，即 `ValidationError` 将包含有关所有错误及其发生方式的信息。

您可以通过多种方式访问这些错误：

`e.errors()`
: 方法将返回在输入数据中发现的错误列表。

`e.json()`
: 方法将返回 `errors` 的 JSON 表示。

`str(e)`
: 方法将返回错误的人类可读表示。

每个错误对象包含：

`loc`
: 错误的位置作为列表。 列表中的第一项将是发生错误的字段，如果该字段是 [子模块](models.md#recursive-models)，则将出现后续项以指示错误的嵌套位置。

`type`
: 错误类型的计算机可读标识符。

`msg`
:错误类型的计算机可读标识符。

`ctx`
: 一个可选对象，其中包含呈现错误消息所需的值。

作为示范：

{!.tmp_examples/models_errors1.md!}

### 自定义错误(Custom Errors)

在您的自定义数据类型或验证器中，您应该使用 `ValueError`、`TypeError` 或 `AssertionError` 来引发错误。

有关使用 `@validator` 装饰器的更多详细信息，请参阅 [校验器](validators.md)。

{!.tmp_examples/models_errors2.md!}

您还可以定义自己的错误类，它可以自定义错误代码、消息模板和上下文：

{!.tmp_examples/models_errors3.md!}

## 辅助函数(Helper Functions)

*Pydantic* 在模型上提供了三个 `classmethod` 辅助函数来解析数据：

* **`parse_obj`**: 这与模型的 `__init__` 方法非常相似，除了它采用字典而不是关键字参数。 如果传递的对象不是字典，则会引发`ValidationError`。
* **`parse_raw`**: 这需要 *str* 或 *bytes* 并将其解析为 *json*，然后将结果传递给 `parse_obj`。通过适当设置 `content_type` 参数也支持解析 *pickle* 数据。
* **`parse_file`**: 这需要一个文件路径，读取文件并将内容传递给`parse_raw`。 如果省略了 `content_type`，则从文件的扩展名中推断出来。

{!.tmp_examples/models_parse.md!}

!!! warning
    引用 [官方 `pickle` 文档](https://docs.python.org/3/library/pickle.html)，“pickle 模块对于错误或恶意构造的数据不安全。切勿取消接收来自不受信任或未经身份验证的来源。”

!!! info
    因为它会导致任意代码执行，作为安全措施，您需要显式地将 `allow_pickle` 传递给解析函数，以便加载 `pickle` 数据。

### 创建无需校验的模型(Creating models without validation)

*pydantic* 还提供了 `construct()` 方法，该方法允许创建模型**无需验证**当数据已经过验证或来自受信任的来源并且您希望尽可能高效地创建模型时，这可能很有用 可能（`construct()` 通常比创建具有完整验证的模型快 30 倍左右）。

!!! warning
    `construct()` 不做任何验证，这意味着它可以创建无效的模型。 **您应该只对已经过验证或您信任的数据使用 `construct()` 方法。**

{!.tmp_examples/models_construct.md!}

`construct()` 的 `_fields_set` 关键字参数是可选的，但可以让您更准确地了解哪些字段是最初设置的，哪些不是。 如果它被省略，`__fields_set__` 将只是所提供数据的键。

例如，在上面的示例中，如果未提供 `_fields_set`，则`new_user.fields_set`将为`{'id', 'age', 'name'}`。

## 通用模型(Generic Models)

Pydantic 支持创建通用模型，以便更轻松地重用通用模型结构。

为了声明通用模型，执行以下步骤：

* 声明一个或多个 `typing.TypeVar` 实例以用于参数化您的模型。
* 声明一个继承自 `pydantic.generics.GenericModel` 和 `typing.Generic` 的 pydantic 模型，在其中将 `TypeVar` 实例作为参数传递给 `typing.Generic`。
* 使用 `TypeVar` 实例作为注解，您可以在其中将它们替换为其他类型或 pydantic 模型。

下面是一个使用 `GenericModel` 创建易于重用的 HTTP 响应负载包装器的示例：

{!.tmp_examples/models_generics.md!}

如果您在通用模型定义中设置 `Config` 或使用 `validator`，它将以与从 `BaseModel` 继承时相同的方式应用于具体子类。 在泛型类上定义的任何方法也将被继承。

Pydantic 的泛型也与 mypy 正确集成，因此如果您要在不使用 `GenericModel` 的情况下声明类型，您将获得您希望 mypy 提供的所有类型检查。

!!! note
    在内部，pydantic 使用 `create_model`在运行时生成（缓存的）具体 `BaseModel`，因此使用 `GenericModel` 引入的开销基本上为零。

要从 `GenericModel` 继承而不替换 `TypeVar` 实例，类还必须从 `typing.Generic` 继承：

{!.tmp_examples/models_generics_inheritance.md!}

您还可以创建 `GenericModel` 的通用子类，部分或完全替换超类中的类型参数。

{!.tmp_examples/models_generics_inheritance_extend.md!}

如果具体子类的名称很重要，您还可以覆盖默认行为：

{!.tmp_examples/models_generics_naming.md!}

在嵌套模型中使用相同的 `TypeVar` 允许您在模型的不同点强制执行类型关系：

{!.tmp_examples/models_generics_nested.md!}

Pydantic 还像处理 `List` 和 `Dict` 等内置泛型类型一样处理 `GenericModel`，以使其保持未参数化或使用有界 `TypeVar` 实例：

* 如果您在实例化通用模型之前没有指定参数，它们将被视为`Any`
* 您可以使用一个或多个*bounded(有界)*参数对模型进行参数化以添加子类检查

此外，与 `List` 和 `Dict` 一样，使用 `TypeVar` 指定的任何参数稍后都可以替换为具体类型。

{!.tmp_examples/models_generics_typevars.md!}

## 动态模型的创建(Dynamic model creation)

在某些情况下，直到运行时才知道模型的形态(shape)。 为此 *pydantic* 提供了 `create_model` 方法来允许动态创建模型。

{!.tmp_examples/models_dynamic_creation.md!}

这里的 `StaticFoobarModel` 和 `DynamicFoobarModel` 是相同的。

!!! warning
    请参阅 [必须的可选参数](#required-optional-fields) 中的注释，以了解省略号作为字段默认值和仅注释字段之间的区别。
    参见 [pydantic/pydantic#1047](https://github.com/pydantic/pydantic/issues/1047) 获取更多详细信息。

字段由 `(<type>, <default value>)` 形式的元组或仅由默认值定义。 特殊关键字参数 `__config__` 和 `__base__` 可用于自定义新模型。 这包括使用额外字段扩展基本模型。

{!.tmp_examples/models_dynamic_inheritance.md!}

您还可以通过将字典传递给 `__validators__` 参数来添加验证器。

{!.tmp_examples/models_dynamic_validators.md!}

## 从`NamedTuple`或`TypedDict`创建模型(Model creation from `NamedTuple` or `TypedDict`)

有时，您已经在应用程序中使用了继承自 `NamedTuple` 或 `TypedDict` 的类，并且您不想复制所有信息以拥有 `BaseModel`。 为此*pydantic* 提供了`create_model_from_namedtuple` 和`create_model_from_typeddict` 方法。 这些方法具有与 `create_model` 完全相同的关键字参数。

{!.tmp_examples/models_from_typeddict.md!}

## 自定义根类型(Custom Root Types)

Pydantic 模型可以通过声明 `__root__` 字段来定义自定义根类型。

根类型可以是 pydantic 支持的任何类型，并由 `__root__` 字段上的类型提示指定。 根值可以通过 `__root__` 关键字参数传递给模型 `__init__` ，或者作为 `parse_obj` 的第一个也是唯一一个参数。

{!.tmp_examples/models_custom_root_field.md!}

如果您为具有自定义根类型的模型调用 `parse_obj` 方法，并将 *dict* 作为第一个参数，则使用以下逻辑：

* 如果自定义根类型是映射类型（例如，`Dict` 或 `Mapping`），参数本身总是根据自定义根类型进行验证。
* 对于其他自定义根类型，如果字典恰好有一个值为 `__root__` 的键，则将根据自定义根类型验证相应的值。
* 否则，将根据自定义根类型验证字典本身。

这在以下示例中得到了证明：

{!.tmp_examples/models_custom_root_field_parse_obj.md!}

!!! warning
    为了向后兼容，目前支持使用单键 `"__root__"` 在 dict 上调用 `parse_obj` 方法以实现向后兼容性，但不推荐并且可能在未来版本中删除。

如果您想直接访问 `__root__` 字段中的项目或迭代这些项目，您可以实现自定义 `__iter__` 和 `__getitem__` 函数，如以下示例所示。

{!.tmp_examples/models_custom_root_access.md!}

## 伪不变性(Faux Immutability)

可以通过 `allow_mutation = False` 将模型配置为不可变的。 设置后，尝试更改实例属性的值将引发错误。 有关 `Config` 的更多详细信息，请参阅 [模型配置](model_config.md)。

!!! warning
    Python 中的不变性从来都不是严格的。 如果开发人员有决心/愚蠢，他们总是可以修改所谓的“不可变”对象。

{!.tmp_examples/models_mutation.md!}

尝试更改 `a` 导致错误，而 `a` 保持不变。 然而，dict `b` 是可变的，而 `foobar` 的不变性并不能阻止 `b` 被改变。

## 抽象基类(Abstract Base Classes)

Pydantic 模型可以与 Python 的[抽象基类](https://docs.python.org/3/library/abc.html) (ABC) 一起使用。

{!.tmp_examples/models_abc.md!}

## 字段顺序(Field Ordering)

字段顺序在模型中很重要，原因如下：

* 在定义的订单字段中执行验证； [fields validators](validators.md) 可以访问前面字段的值，但不能访问后面的字段
* 字段顺序保留在模型 [schema](schema.md) 中
* 字段顺序保留在 [validation errors](#error-handling)
* 字段顺序由 [`.dict()` 和 `.json()`](exporting_models.md#modeldict)等保存

从 **v1.0** 开始，所有带有注解的字段（无论是仅注解还是带有默认值）都将位于所有没有注解的字段之前。 在各自的组中，字段保持其定义的顺序。

{!.tmp_examples/models_field_order.md!}

!!! warning
    如上面的示例所示，在同一模型中结合使用带注释和非带注释的字段可能会导致令人惊讶的字段排序。 （这是由于 Python 的限制）

    因此，**我们建议向所有字段添加类型注释**，即使默认值会自行确定类型以保证保留字段顺序。

## 必须字段(Required fields)

要根据需要声明一个字段，您可以仅使用注解来声明它，或者您可以使用省略号（`...`）作为值：

{!.tmp_examples/models_required_fields.md!}

其中 `Field` 指的是 [字段函数](schema.md#field-customization)。

这里 `a`、`b` 和 `c` 都是必需的。 但是，在 `b` 中使用省略号不适用于 [mypy](mypy.md)，从 **v1.0** 开始，在大多数情况下应避免使用。

### 必须但可选字段(Required Optional fields)

!!! warning
    由于版本 **v1.2** 注解仅可为空（`Optional[...]`、`Union[None, ...]` 和`Any`）字段和带有省略号（`...`）的可为空字段）作为默认值，不再意味着同一件事。

    在某些情况下，这可能会导致 **v1.2** 无法完全向后兼容早期的 **v1.*** 版本。

如果你想指定一个字段，该字段在仍然需要时可以采用“无”值，则可以将“可选”与“...”一起使用：

{!.tmp_examples/models_required_field_optional.md!}

在这个模型中，`a`、`b` 和 `c` 可以取 `None` 作为值。 但是 `a` 是可选的，而 `b` 和 `c` 是必需的。 `b` 和 `c` 需要一个值，即使该值为 `None`。

## 具有动态默认值的字段(Field with dynamic default value)

当用默认值声明一个字段时，您可能希望它是动态的（即每个模型不同）。 为此，您可能需要使用`default_factory`。

!!! info "测试版"
    `default_factory` 参数在 **beta** 中，它已在 **临时基础** 中添加到 **v1.5** 中的 *pydantic*。 它可能会在未来的版本中发生重大变化，并且其签名或行为在 **v2** 之前不会具体。 来自社区的反馈在它仍然是临时的时候将非常有用； 评论 [#866](https://github.com/pydantic/pydantic/issues/866) 或创建一个新问题。

使用示例：

{!.tmp_examples/models_default_factory.md!}

其中 `Field` 指的是 [字段函数](schema.md#field-customization)。

!!! warning
    `default_factory` 需要设置字段类型。

## 自动排除的属性(Automatically excluded attributes)

以下划线开头的类变量和用 `typing.ClassVar` 注释的属性将自动从模型中排除。

## 私有模型属性(Private model attributes)

如果您需要改变或操作模型实例的内部属性，您可以使用 `PrivateAttr` 声明它们：

{!.tmp_examples/private_attributes.md!}

私有属性名称必须以下划线开头，以防止与模型字段冲突：支持 `_attr` 和 `__attr__` 。

如果 `Config.underscore_attrs_are_private` 为 `True`，任何非 ClassVar 下划线属性都将被视为私有：

{!.tmp_examples/private_attributes_underscore_attrs_are_private.md!}

在创建类时，pydantic 构造了填充私有属性的 `__slots__` 。

## 将数据解析为指定类型(Parsing data into a specified type)

Pydantic 包括一个独立的实用函数 `parse_obj_as` ，可用于应用用于以更特殊的方式填充 pydantic 模型的解析逻辑。 此函数的行为类似于 `BaseModel.parse_obj` ，但适用于任意与 pydantic 兼容的类型。

当您想要将结果解析为不是 `BaseModel` 的直接子类的类型时，这尤其有用。

例如：

{!.tmp_examples/parse_obj_as.md!}

此函数能够将数据解析为 pydantic 可以作为 `BaseModel` 字段处理的任何类型。

Pydantic 还包括两个类似的独立函数，称为 `parse_file_as` 和 `parse_raw_as`，它们类似于 `BaseModel.parse_file` 和`BaseModel.parse_raw`。

## 数据转换(Data Conversion)

*pydantic* 可能会转换输入数据以强制其符合模型字段类型，在某些情况下这可能会导致信息丢失。

例如：

{!.tmp_examples/models_data_conversion.md!}

这是 *pydantic* 深思熟虑的决定，通常这是最有用的方法。 请参阅[此处](https://github.com/pydantic/pydantic/issues/578)，了解有关该主题的更长时间讨论。

尽管如此，部分支持[严格类型检查](types.md#strict-types)。

## 模型签名(Model signature)

所有 *pydantic* 模型都将根据其字段生成签名：

{!.tmp_examples/models_signature.md!}

准确的签名对于内省目的和库（如`FastAPI`或 `hypothesis` ）很有用。

生成的签名也将遵循自定义的 `__init__` 函数：

{!.tmp_examples/models_signature_custom_init.md!}

要包含在签名中，字段的别名或名称必须是有效的 Python 标识符。 *pydantic* 更喜欢别名而不是名称，但如果别名不是有效的 Python 标识符，则可以使用字段名称。

如果一个字段的别名和名称都是无效的标识符，则会添加一个 `**data` 参数。

此外，如果 `Config.extra` 为 `Extra.allow`，`**data` 参数将始终出现在签名中。

!!! note
    模型签名中的类型与模型注释中声明的类型相同，不一定是实际可以提供给该字段的所有类型。

    一旦 [#1055](https://github.com/pydantic/pydantic/issues/1055) 得到解决，这可能会在某一天得到解决。

## 结构模式匹配(Structural pattern matching)

*pydantic* 支持模型的结构模式匹配，如 Python 3.10 中的 [PEP 636](https://peps.python.org/pep-0636/) 所介绍的那样。

{!.tmp_examples/models_structural_pattern_matching.md!}

!!! note
    match-case 语句看起来好像创建了一个新模型，但不要被愚弄了；

    它只是获取属性并比较它或声明和初始化它的语法糖。
