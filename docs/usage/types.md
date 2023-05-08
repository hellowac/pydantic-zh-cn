在可能的情况下 *pydantic* 使用 [标准库类型](#standard-library-types) 来定义字段，从而平滑学习曲线。 然而，对于许多有用的应用程序，不存在标准库类型，因此 *pydantic* 实现 [许多常用类型](#pydantic-types)。

如果没有适合您目的的现有类型，您还可以使用自定义属性和验证来实现您的[自己的 pydantic 兼容类型](#custom-data-types)。

## 标准库类型(Standard Library Types)

*pydantic* 支持 Python 标准库中的许多常见类型。 如果您需要更严格的处理，请参阅 [严格类型](#strict-types)； 如果您需要限制允许的值（例如需要一个正整数），请参阅 [Constrained Types](#constrained-types)。

`None`、`type(None)` 或 `Literal[None]`（等同于 [PEP 484](https://www.python.org/dev/peps/pep-0484/#using-none)） : 只允许 `None` 值

`bool`
: 请参阅下面的 [Booleans](#booleans)，了解有关如何验证布尔值以及允许使用哪些值的详细信息

`int`
: *pydantic* 使用 `int(v)` 将类型强制转换为 `int`； 请参阅 [this](models.md#data-conversion) 关于数据转换期间信息丢失的警告

`float`
: 类似地，`float(v)` 用于将值强制转换为浮点数

`str`
: 字符串按原样接受，`int` `float` 和 `Decimal` 使用 `str(v)` 强制转换，`bytes` 和 `bytearray` 使用 `v.decode()` 转换，枚举继承自 `str` 使用 `v.value` 进行转换，所有其他类型都会导致错误

`bytes`
: `bytes` 按原样接受，`bytearray` 使用 `bytes(v)` 转换，`str` 使用 `v.encode()` 转换，`int`、`float` 和 `Decimal` 是 使用 `str(v).encode()` 强制

`list`
: 允许 `list`、`tuple`、`set`、`frozenset`、`deque` 或生成器和转换为列表； 有关子类型约束，请参见下面的`typing.List`

`tuple`
: 允许 `list`、`tuple`、`set`、`frozenset`、`deque` 或生成器和转换为元组； 有关子类型约束，请参见下面的`typing.Tuple`

`dict`
: `dict(v)` 用于尝试转换字典； 请参阅下面的 `typing.Dict` 了解子类型约束

`set`
: 允许将 `list`、`tuple`、`set`、`frozenset`、`deque` 或生成器和强制转换为一个集合； 有关子类型约束，请参见下面的`typing.Set`

`frozenset`
: 允许 `list`、`tuple`、`set`、`frozenset`、`deque` 或生成器和强制转换为冻结集； 有关子类型约束，请参阅下面的`typing.FrozenSet`

`deque`
: 允许 `list`、`tuple`、`set`、`frozenset`、`deque` 或生成器和转换为双端队列； 有关子类型约束，请参见下面的`typing.Deque`

`datetime.date`
: 有关解析和验证的更多详细信息，请参阅下面的 [Datetime Types](#datetime-types)

`datetime.time`
: 有关解析和验证的更多详细信息，请参阅下面的 [Datetime Types](#datetime-types)

`datetime.datetime`
: 有关解析和验证的更多详细信息，请参阅下面的 [Datetime Types](#datetime-types)

`datetime.timedelta`
: 有关解析和验证的更多详细信息，请参阅下面的 [Datetime Types](#datetime-types)

`typing.Any`
: 允许任何值，包括`None`，因此`Any`字段是可选的

`typing.Annotated`
: 根据 [PEP-593](https://www.python.org/dev/peps/pep-0593/)，允许使用任意元数据包装另一种类型。 `Annotated` 提示可能包含对 [`Field` 函数](schema.md#typingannotated-fields) 的单个调用，但其他元数据将被忽略并使用根类型。

`typing.TypeVar`
: 根据 `constraints` 或 `bound` 限制允许的值，参见 [TypeVar](#typevar)

`typing.Union`
: 有关解析和验证的更多详细信息，请参阅下面的 [Union](#unions)

`typing.Optional`
: `Optional[x]` 只是 `Union[x, None]` 的简写； 有关解析和验证的更多详细信息，请参阅下面的 [Union](#unions)，有关可以接收`None`作为值的必填字段的详细信息，请参阅 [Required Fields](models.md#required-fields)。

`typing.List`
: 有关解析和验证的更多详细信息，请参阅下面的 [Typing Iterables](#typing-iterables)

`typing.Tuple`
: 有关解析和验证的更多详细信息，请参阅下面的 [Typing Iterables](#typing-iterables)

`subclass of typing.NamedTuple`
: 与 `tuple` 相同，但使用给定的 `namedtuple` 实例化并验证字段，因为它们是带注释的。 有关解析和验证的更多详细信息，请参阅下面的 [注释类型](#annotated-types)

`subclass of collections.namedtuple`
: 与 `subclass of typing.NamedTuple` 相同，但所有字段都将具有 `Any` 类型，因为它们没有注释

`typing.Dict`
: 有关解析和验证的更多详细信息，请参阅下面的 [Typing Iterables](#typing-iterables)

`subclass of typing.TypedDict`
: 与 `dict` 相同，但 *pydantic* 将验证字典，因为键被注释了。 有关解析和验证的更多详细信息，请参阅下面的 [注释类型](#annotated-types)

`typing.Set`
: 有关解析和验证的更多详细信息，请参阅下面的 [Typing Iterables](#typing-iterables)

`typing.FrozenSet`
: 有关解析和验证的更多详细信息，请参阅下面的 [Typing Iterables](#typing-iterables)

`typing.Deque`
: 有关解析和验证的更多详细信息，请参阅下面的 [Typing Iterables](#typing-iterables)

`typing.Sequence`
: 有关解析和验证的更多详细信息，请参阅下面的 [Typing Iterables](#typing-iterables)

`typing.Iterable`
: 这是为不应使用的迭代器保留的。 有关解析和验证的更多详细信息，请参阅下面的 [Infinite Generators](#infinite-generators)

`typing.Type`
: 有关解析和验证的更多详细信息，请参阅下面的 [Type](#type)

`typing.Callable`
: 有关解析和验证的更多详细信息，请参阅下面的 [Callable](#callable)

`typing.Pattern`
: 将导致输入值被传递给 `re.compile(v)` 以创建正则表达式模式

`ipaddress.IPv4Address`
: 通过将值传递给 `IPv4Address(v)` 来简单地使用类型本身进行验证； 有关其他自定义 IP 地址类型，请参阅 [Pydantic Types](#pydantic-types)

`ipaddress.IPv4Interface`
: 通过将值传递给 `IPv4Address(v)` 来简单地使用类型本身进行验证； 有关其他自定义 IP 地址类型，请参阅 [Pydantic Types](#pydantic-types)

`ipaddress.IPv4Network`
: 通过将值传递给 `IPv4Network(v)` 来简单地使用类型本身进行验证； 有关其他自定义 IP 地址类型，请参阅 [Pydantic Types](#pydantic-types)

`ipaddress.IPv6Address`
: 通过将值传递给 `IPv6Address(v)` 来简单地使用类型本身进行验证； 有关其他自定义 IP 地址类型，请参阅 [Pydantic Types](#pydantic-types)

`ipaddress.IPv6Interface`
: 通过将值传递给 `IPv6Interface(v)` 来简单地使用类型本身进行验证； 有关其他自定义 IP 地址类型，请参阅 [Pydantic Types](#pydantic-types)

`ipaddress.IPv6Network`
: 通过将值传递给 `IPv6Network(v)` 来简单地使用类型本身进行验证； 有关其他自定义 IP 地址类型，请参阅 [Pydantic Types](#pydantic-types)

`enum.Enum`
: 检查该值是否为有效的 Enum 实例

`subclass of enum.Enum`
: 检查该值是否是枚举的有效成员； 有关详细信息，请参阅 [枚举和选择](#enums-and-choices)

`enum.IntEnum`
: 检查该值是否为有效的 IntEnum 实例

`subclass of enum.IntEnum`
: 检查该值是否是整数枚举的有效成员； 有关详细信息，请参阅 [枚举和选择](#enums-and-choices)

`decimal.Decimal`
: *pydantic* 尝试将值转换为字符串，然后将字符串传递给“Decimal(v)”

`pathlib.Path`
: 通过将值传递给 `Path(v)` 来简单地使用类型本身进行验证； 有关其他更严格的路径类型，请参阅 [Pydantic Types](#pydantic-types)

`uuid.UUID`
: 字符串和字节（转换为字符串）被传递给 `UUID(v)`，对于 `bytes` 和 `bytearray` 回退到 `UUID(bytes=v)`； 有关其他更严格的 UUID 类型，请参阅 [Pydantic Types](#pydantic-types)

`ByteSize`
: 将带单位的字节字符串转换为字节

### 可迭代类型(Typing Iterables)

*pydantic* 使用 PEP 484 中定义的标准库“键入”类型来定义复杂对象。

{!.tmp_examples/types_iterables.md!}

### 无限生成器(Infinite Generators)

如果你有一个生成器，你可以使用上面描述的`Sequence`。 在这种情况下，生成器将被使用并作为列表存储在模型中，其值将使用`Sequence`的子类型（例如`Sequence[int]`中的`int`）进行验证。

但是如果你有一个你不想被消耗的生成器，例如 无限生成器或远程数据加载器，您可以使用 `Iterable` 定义其类型：

{!.tmp_examples/types_infinite_generator.md!}

!!! warning
    `Iterable` 字段只执行一个简单的检查，以确保参数是可迭代的并且不会被消耗。

    不会对它们的值进行验证，因为如果不使用可迭代对象就无法完成验证。

!!! tip
    如果您想验证无限生成器的值，您可以创建一个单独的模型并在使用生成器时使用它，并根据需要报告验证错误。

    pydantic 无法自动为您验证这些值，因为它需要使用无限生成器。

#### 验证第一个值(Validating the first value)

您可以创建一个 [validator](validators.md) 来验证无限生成器中的第一个值，但仍然不会完全消耗它。

{!.tmp_examples/types_infinite_generator_validate_first.md!}

### 联合(Unions)

`Union` 类型允许模型属性接受不同的类型，例如：

!!! info
    使用 `Union` 可能会得到意想不到的强制转换； 见下文。

    不过您还可以通过使用 [智能联合](model_config.md#smart-union) 使检查更慢但更严格

{!.tmp_examples/types_union_incorrect.md!}

但是，如上所示，*pydantic* 将尝试`match`在 `Union` 下定义的任何类型，并将使用第一个匹配的类型。 在上面的示例中，`user_03`的`id`被定义为`uuid.UUID`类（在属性的 `Union` 注释下定义），但`uuid.UUID`可以编组为`int` 它选择匹配`int`类型并忽略其他类型。

!!! warning
    `typing.Union` 在 [定义](https://docs.python.org/3/library/typing.html#typing.Union) 时也会忽略顺序，所以 `Union[int, float] == Union[float, int]` 当与基于其他类型定义中的 `Union` 类型顺序的匹配相结合时，例如 `List` 和 `Dict` 类型（因为 Python 将这些定义视为单例）。

     例如，`Dict[str, Union[int, float]] == Dict[str, Union[float, int]]` 的顺序基于第一次定义。
    
     请注意，这也可能 [受第三方库影响](https://github.com/pydantic/pydantic/issues/2835) 及其内部类型定义和导入顺序。

因此，建议在定义 `Union` 注解时，首先包含最具体的类型，然后是不太具体的类型。

在上面的示例中，`UUID` 类应该在 `int` 和 `str` 类之前，以排除这样的意外表示：

{!.tmp_examples/types_union_correct.md!}

!!! tip
    `Optional[x]` 类型是 `Union[x, None]` 的简写。

     `Optional[x]` 也可用于指定一个必填字段，该字段可以将 `None` 作为值。

     在[必填字段](models.md#required-fields) 中查看更多详细信息。

#### 区别联合【Discriminated Unions (a.k.a. Tagged Unions)】

当 `Union` 与多个子模型一起使用时，您有时会确切地知道需要检查和验证哪个子模型并希望强制执行此操作。

为此，您可以在每个具有判别值的子模型中设置相同的字段 - 让我们称之为 `my_discriminator`，这是一个（或多个）`Literal`值。

对于您的 `Union`，您可以在其值中设置鉴别器：`Field(discriminator='my_discriminator')`。

建立受歧视的工会有很多好处：

- 验证速度更快，因为它只针对一个模型进行尝试
- 失败时仅引发一个显式错误
- 生成的 JSON 模式实现了[相关的 OpenAPI 规范](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#discriminatorObject)

{!.tmp_examples/types_union_discriminated.md!}

!!! note
    使用 [Annotated Fields syntax](../schema/#typingannotated-fields) 可以方便地重新组合 `Union` 和 `discriminator` 信息。 请参阅下面的示例！

!!! warning
    区别联合不能仅与单个变体一起使用，例如 `Union[Cat]`。

    Python 在解释时将 `Union[T]` 更改为 `T`，因此 `pydantic` 无法区分 `Union[T]` 和 `T` 的字段。

#### 嵌套的区别联合(Nested Discriminated Unions)

一个字段只能设置一个鉴别器(discriminator)，但有时你想组合多个鉴别器(discriminator)。

在这种情况下，您始终可以使用 `__root__` 创建“中间(intermediate)”模型并添加鉴别器。

{!.tmp_examples/types_union_discriminated_nested.md!}

### 枚举和选择(Enums and Choices)

*pydantic* 使用 Python 的标准`enum`类来定义选择。

{!.tmp_examples/types_choices.md!}

### 日期时间类型(Datetime Types)

*Pydantic* 支持以下 [datetime](https://docs.python.org/library/datetime.html#available-types) 类型：

- `datetime` 字段可以是:

  - `datetime`，现有的 `datetime` 对象
  - `int` 或 `float`，假定为 Unix 时间，即自 1970 年 1 月 1 日以来的秒数（如果 >= `-2e10` 或 <= `2e10`）或毫秒（如果 < `-2e10` 或 > `2e10`）
  - `str`, 以下格式有效：

    - `YYYY-MM-DD[T]HH:MM[:SS[.ffffff]][Z or [±]HH[:]MM]`
    - `int` 或 `float` 作为字符串（假定为 Unix 时间）

- `date` 字段可以是:

  - `date`, 现有的 `date` 对象
  - `int` 或 `float`, 见 `datetime`
  - `str`, 以下格式有效：

    - `YYYY-MM-DD`
    - `int` 或 `float`, 见 `datetime`

- `time` 字段可以是:

  - `time`, 现有的 `time` 对象
  - `str`, 以下格式有效：

    - `HH:MM[:SS[.ffffff]][Z or [±]HH[:]MM]`

- `timedelta` 字段可以是:

  - `timedelta`, 现有的 `timedelta` 对象
  - `int` 或 `float`, 假定为秒
  - `str`, 以下格式有效：

    - `[-][DD ][HH:MM]SS[.ffffff]`
    - `[±]P[DD]DT[HH]H[MM]M[SS]S` ([ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) timedelta 的格式)

{!.tmp_examples/types_dt.md!}

### 布尔类型(Booleans)

!!! warning
    从 __v1.0__ 版本开始，解析 `bool` 字段的逻辑发生了变化。

    在 **v1.0** 之前，`bool` 解析从未失败，导致一些意外结果。
    
    新逻辑如下所述。

如果值不是以下之一，标准的 `bool` 字段将引发 `ValidationError`：

- 一个有效的布尔值（即`True`或`False`），
- 整数`0`或`1`，
- 一个 `str` ，当转换为小写时，它是其中之一
  `'0', 'off', 'f', 'false', 'n', 'no', '1', 'on', 't', 'true', 'y', 'yes'`
- 解码为 `str` 时有效（根据前面的规则）的 `bytes`

!!! note
    如果你想要更严格的布尔逻辑（例如，一个只允许 `True` 和 `False` 的字段）你可以使用 [`StrictBool`](#strict-types)。

这是一个演示其中一些行为的脚本：

{!.tmp_examples/types_boolean.md!}

### 可调用类型(Callable)

字段也可以是 `Callable` 类型：

{!.tmp_examples/types_callable.md!}

!!! warning
    可调用字段仅执行简单检查参数是否可调用； 不执行参数、它们的类型或返回类型的验证。

### 类型(Type)

*pydantic* 支持使用 `Type[T]` 来指定字段只能接受作为 `T` 子类的类（而不是实例）。

{!.tmp_examples/types_type.md!}

您还可以使用 `Type` 来指定允许使用任何类。

{!.tmp_examples/types_bare_type.md!}

### 类型声明(TypeVar)

`TypeVar` 支持不受约束、受约束或有界限。

{!.tmp_examples/types_typevar.md!}

## 文字类型(Literal Type)

!!! note
    这是从 Python 3.8 开始的 Python 标准库的一个新特性； 在 Python 3.8 之前，它需要 [typing-extensions](https://pypi.org/project/typing-extensions/) 包。

*pydantic* 支持使用 `typing.Literal`（或 Python 3.8 之前的 `typing_extensions.Literal`）作为一种轻量级的方式来指定一个字段只能接受特定的文字值：

{!.tmp_examples/types_literal1.md!}

这种字段类型的一个好处是它可以用来检查一个或多个特定值是否相等，而无需声明自定义验证器：

{!.tmp_examples/types_literal2.md!}

通过在带注释的 `Union` 中正确排序，您可以使用它来解析递减特异性的类型：

{!.tmp_examples/types_literal3.md!}

## 已注解类型(Annotated Types)

### 命名元组(NamedTuple)

{!.tmp_examples/annotated_types_named_tuple.md!}

### 标记类型字典(TypedDict)

!!! note
    这是从 Python 3.8 开始的 Python 标准库的一个新特性。 在 Python 3.8 之前，它需要 [typing-extensions](https://pypi.org/project/typing-extensions/) 包。

     但仅自 Python 3.9 起才正确区分必填字段和可选字段。

     因此，我们建议在 Python 3.8 中也使用 [typing-extensions](https://pypi.org/project/typing-extensions/)。

{!.tmp_examples/annotated_types_typed_dict.md!}

## Pydantic特有类型(Pydantic Types)

*pydantic* 还提供了多种其他有用的类型：

`FilePath`
: 类似 `Path`, 但路径必须存在并且是一个文件

`DirectoryPath`
: 类似 `Path`, 但路径必须存在并且是一个目录

`PastDate`
: 类似 `date`, 但日期应该是过去的

`FutureDate`
: 类似 `date`, 但日期应该在未来

`EmailStr`
: 需要安装 [email-validator](https://github.com/JoshData/python-email-validator)；
  输入字符串必须是一个有效的电子邮件地址，输出是一个简单的字符串

`NameEmail`
: 需要安装 [email-validator](https://github.com/JoshData/python-email-validator)；
  
  输入字符串必须是有效的电子邮件地址或格式为`Fred Bloggs <fred.bloggs@example.com>`，输出是一个 `NameEmail` 对象，它具有两个属性：`name` 和 `email`。
  
   对于 `Fred Bloggs <fred.bloggs@example.com>`，名称将是 `Fred Bloggs`；
  
   对于 `fred.bloggs@example.com`，它将是 `fred.bloggs`。

`PyObject`
: 需要一个字符串并加载在该下划线路径中可导入的 Python 对象；
  例如 如果提供了 `math.cos`，则结果字段值将是函数 `cos`

`Color`
: 用于解析 HTML 和 CSS 颜色； 参见[颜色类型](#color-type)

`Json`
: 在解析之前加载 JSON 的特殊类型包装器； 参见 [JSON 类型](#json-type)

`PaymentCardNumber`
: 用于解析和验证支付卡； 参见[支付卡](#payment-card-numbers)

`AnyUrl`
: 任何网址； 参见 [URL](#urls)

`AnyHttpUrl`
: 一个 HTTP 网址； 参见 [URL](#urls)

`HttpUrl`
: 更严格的 HTTP URL； 参见 [URL](#urls)

`FileUrl`
: 文件路径 URL； 参见 [URL](#urls)

`PostgresDsn`
: 文件路径 URL； 参见 [URL](#urls)

`CockroachDsn`
: cockroachdb DSN 样式的 URL； 参见 [URL](#urls)

`AmqpDsn`
: RabbitMQ、StormMQ、ActiveMQ 等使用的 `AMQP` DSN 样式 URL； 参见 [URL](#urls)

`RedisDsn`
: 一个 redis DSN 样式的 URL； 参见 [URL](#urls)

`MongoDsn`
: 一个 MongoDB DSN 样式的 URL； 参见 [URL](#urls)

`KafkaDsn`
: kafka DSN 样式的 URL； 参见 [URL](#urls)

`stricturl`
: 任意 URL 约束的类型方法； 参见 [URL](#urls)

`UUID1`
: 需要类型 1 的有效 UUID; 参见 `UUID` [above](#standard-library-types)

`UUID3`
: 需要类型 3 的有效 UUID; 参见 `UUID` [above](#standard-library-types)

`UUID4`
: 需要类型 4 的有效 UUID; 参见 `UUID` [above](#standard-library-types)

`UUID5`
: 需要类型 5 的有效 UUID; 参见 `UUID` [above](#standard-library-types)

`SecretBytes`
: 值部分保密的字节; 参见 [Secrets](#secret-types)

`SecretStr`
: 值部分保密的字符串; 参见 [Secrets](#secret-types)

`IPvAnyAddress`
: 允许 `IPv4Address` 或 `IPv6Address`

`IPvAnyInterface`
: 允许 `IPv4Interface` 或 `IPv6Interface`

`IPvAnyNetwork`
: 允许 `IPv4Network` 或 `IPv6Network`

`NegativeFloat`
: 允许一个负数的浮点数； 使用标准的 `float` 解析然后检查值是否小于 0；
  参见 [约束类型](#constrained-types)

`NegativeInt`
: 允许一个负数的整数； 使用标准的 `int` 解析然后检查值是否小于 0；
  参见 [约束类型](#constrained-types)

`PositiveFloat`
: 允许一个正的浮点数； 使用标准的 `float` 解析然后检查值是否大于 0；
  参见 [约束类型](#constrained-types)

`PositiveInt`
: 允许一个正整数； 使用标准的 `int` 解析然后检查值是否大于 0；
  参见 [约束类型](#constrained-types)

`conbytes`
: 用于约束字节的类型方法；
  参见 [约束类型](#constrained-types)

`condecimal`
: 用于约束 Decimals 的类型方法；
  参见 [约束类型](#constrained-types)

`confloat`
: 用于约束浮点数的类型方法；
  参见 [约束类型](#constrained-types)

`conint`
: 用于约束整数的类型方法；
  参见 [约束类型](#constrained-types)

`condate`
: 限制日期的类型方法；
  参见 [约束类型](#constrained-types)

`conlist`
: 用于约束列表的类型方法；
  参见 [约束类型](#constrained-types)

`conset`
: 约束集的类型方法；
  参见 [约束类型](#constrained-types)

`confrozenset`
: 用于约束冻结集的类型方法；
  参见 [约束类型](#constrained-types)

`constr`
: 用于约束 字符串 的类型方法；
  参见 [约束类型](#constrained-types)

### 链接类型(URLs)

对于 URI/URL 验证，可以使用以下类型：

- `AnyUrl`: 允许任何方案，不需要 TLD，需要主机地址
- `AnyHttpUrl`: 方案 `http` 或 `https`，不需要 TLD，需要主机地址
- `HttpUrl`: 方案 `http` 或 `https`，需要 TLD，需要主机地址，最大长度 2083
- `FileUrl`: 匹配 `file`, 不需要主机地址
- `PostgresDsn`: 需要用户信息，不需要 TLD，需要主机地址，从 V.10 开始，`PostgresDsn` 支持多个主机。 以下方案是被支持的:
  - `postgres`
  - `postgresql`
  - `postgresql+asyncpg`
  - `postgresql+pg8000`
  - `postgresql+psycopg`
  - `postgresql+psycopg2`
  - `postgresql+psycopg2cffi`
  - `postgresql+py-postgresql`
  - `postgresql+pygresql`
- `CockroachDsn`: 方案 `cockroachdb`，需要用户信息，不需要 TLD，需要主机地址。 此外，它支持的 DBAPI 方言：
  - `cockroachdb+asyncpg`
  - `cockroachdb+psycopg2`
- `AmqpDsn`: 模式 `amqp` 或 `amqps`，不需要用户信息，不需要 TLD，不需要主机地址
- `RedisDsn`: 匹配 `redis` 或 `rediss`，不需要用户信息，不需要 tld，不需要主机地址（已更改：用户信息）（例如，`rediss://:pass@localhost`）
- `MongoDsn` : 匹配 `mongodb`, 不需要用户信息，不需要数据库名称，从 __v1.6__ 开始不需要端口），用户信息可以在没有用户部分的情况下传递（例如，`mongodb://mongodb0.example.com:27017`）
- `stricturl`: 具有以下关键字参数的方法：
  - `strip_whitespace: bool = True`
  - `min_length: int = 1`
  - `max_length: int = 2 ** 16`
  - `tld_required: bool = True`
  - `host_required: bool = True`
  - `allowed_schemes: Optional[Set[str]] = None`

!!! warning
    在 V1.10.0 和 v1.10.1 中，`stricturl` 还采用可选的 `quote_plus` 参数，并且 URL 组件在某些情况下采用百分比编码。 此功能已在 v1.10.2 中删除，请参阅 [#4470](https://github.com/pydantic/pydantic/pull/4470) 了解说明和更多详细信息。

当提供无效 URL 时，上述类型（全部继承自 `AnyUrl`）将尝试给出描述性错误：

{!.tmp_examples/types_urls.md!}

如果您需要自定义 URI/URL 类型，可以使用与上面定义的类型类似的方式创建它。

#### 网址属性(URL Properties)

假设输入 URL 为`http://samuel:pass@example.com:8000/the/path/?query=here#fragment=is;this=bit`，上述类型导出以下属性：

- `scheme`: 始终设置 - url 方案（上面的 `http`）
- `host`: 始终设置 - 网址主机（上面的“example.com”）
- `host_type`: 始终设置 - 描述主机类型，或者：

  - `domain`: 例如 `example.com`,
  - `int_domain`: 国际域名，见[下文](#international-domains)，例如 `exampl£e.org`,
  - `ipv4`: IP V4 地址，例如 `127.0.0.1`，或
  - `ipv6`: IP V6 地址，例如 `2001:db8:ff00:42`

- `user`: 可选 - 用户名（如果包含）（上面的 `samuel`）
- `password`: 可选 - 如果包含密码（上面的 `pass`）
- `tld`: 可选 - 顶级域（上面的“com”）， __注意：这对于任何二级域都是错误的，例如 “co.uk”.__ 如果您需要完整的 TLD 验证，您需要实施自己的 TLD 列表
- `port`: 可选 - 端口（上面的“8000”）
- `path`: 可选 - 路径（上面的`/the/path/`）
- `query`: 可选 - URL 查询（又名 GET 参数或“搜索字符串”）（上面的 `query=here`）
- `fragment`: 可选 - 片段（上面的`fragment=is;this=bit`）

如果需要进一步验证，验证器可以使用这些属性来强制执行特定行为：

{!.tmp_examples/types_url_properties.md!}

#### 国际域名(International Domains)

“国际域”（例如，主机或 TLD 包含非 ascii 字符的 URL）将通过 [punycode](https://en.wikipedia.org/wiki/Punycode) 进行编码（参见 [本文](https: //www.xudongz.com/blog/2017/idn-phishing/) 很好地说明了为什么这很重要）：

{!.tmp_examples/types_url_punycode.md!}

!!! warning
    #### 主机名中的下划线

    在 *pydantic* 中，域的所有部分都允许使用下划线，除了 tld。从技术上讲，这可能是错误的——理论上主机名不能有下划线，但子域可以。

    解释这一点； 考虑以下两种情况：

    - `exam_ple.co.uk`: 主机名是 `exam_ple`，这是不允许的，因为它包含下划线
    - `foo_bar.example.com` 主机名是 `example`，应该允许，因为下划线在子域中

    如果没有详尽的 TLD 列表，就不可能区分这两者。 因此允许使用下划线，但如果需要，您始终可以在验证器中进行进一步验证。

    此外，Chrome、Firefox 和 Safari 目前都接受 `http://exam_ple.com` 作为 URL，所以我们的关系很好（或者至少是大）。

### 颜色类型(Color Type)

您可以根据 [CSS3 规范](http://www.w3.org/TR/css3-color/#svg-color) 使用 `Color` 数据类型来存储颜色。 颜色可以通过以下方式定义：

- [name](http://www.w3.org/TR/SVG11/types.html#ColorKeywords) (例如 `"Black"`, `"azure"`)
- [hexadecimal value](https://en.wikipedia.org/wiki/Web_colors#Hex_triplet)
  (例如 `"0x000"`, `"#FFFFFF"`, `"7fffd4"`)
- RGB/RGBA 元组 (例如 `(255, 255, 255)`, `(255, 255, 255, 0.5)`)
- [RGB/RGBA 字符串](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value#RGB_colors)
  (例如 `"rgb(255, 255, 255)"`, `"rgba(255, 255, 255, 0.5)"`)
- [HSL 字符串](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value#HSL_colors)
  (例如 `"hsl(270, 60%, 70%)"`, `"hsl(270, 60%, 70%, .5)"`)

{!.tmp_examples/types_color.md!}

`Color` 拥有下列方法:

**`original`**
: 传递给 `Color` 的原始字符串或元组

**`as_named`**
: 返回命名的 CSS3 颜色； 如果设置了 alpha 通道或不存在这样的颜色，则失败，除非提供了 `fallback=True`，在这种情况下它会回退到 `as_hex`

**`as_hex`**
: 返回格式为 `#fff` 或 `#ffffff` 的字符串； 如果设置了 alpha 通道，将包含 4（或 8）个十六进制值， 例如 `#7f33cc26`

**`as_rgb`**
: 如果设置了 alpha 通道，则返回格式为 `rgb(<red>, <green>, <blue>)` 或 `rgba(<red>, <green>, <blue>, <alpha>)` 的字符串

**`as_rgb_tuple`**
: 返回 RGB(a) 格式的 3 元组或 4 元组。 `alpha` 关键字参数可用于定义是否应包含 alpha 通道； 选项：`True` - 始终包括，`False` - 从不包括，`None`（默认）- 如果设置则包括

**`as_hsl`**
: 格式为`hsl(<hue deg>, <saturation %>, <lightness %>)`或`hsl(<hue deg>, <saturation %>, <lightness %>, <alpha>)`的字符串，如果 alpha 通道已设置

**`as_hsl_tuple`**
: 返回 HSL(a) 格式的 3 元组或 4 元组。 `alpha` 关键字参数可用于定义是否应包含 alpha 通道； 选项：`True` - 始终包括，`False` - 从不包括，`None`（默认值）- 如果设置则包括

`Color` 的`__str__` 方法返回`self.as_named(fallback=True)`。

!!! note
    `as_hsl*` 指的是 html 和世界上大多数地方使用的色调、饱和度、亮度`HSL`，__not__ Python 的`colorsys`中使用的`HLS`。

### 保密类型(Secret Types)

您可以使用 `SecretStr` 和 `SecretBytes` 数据类型来存储您不希望在日志记录或回溯中可见的敏感信息。 `SecretStr` 和 `SecretBytes` 可以幂等地初始化，也可以分别使用 `str` 或 `bytes` 进行初始化。 `SecretStr` 和 `SecretBytes` 在转换为 json 时将被格式化为 `'**********'` 或 `''`。

{!.tmp_examples/types_secret_types.md!}

### Json类型(Json Type)

您可以使用 `Json` 数据类型让 *pydantic* 首先加载原始 JSON 字符串。 它还可以选择用于将加载的对象解析为另一种类型，基于参数化的`Json`类型：

{!.tmp_examples/types_json_type.md!}

### 支付卡号码(Payment Card Numbers)

`PaymentCardNumber` 类型验证[支付卡](https://en.wikipedia.org/wiki/Payment_card)（例如借记卡或信用卡）。

{!.tmp_examples/types_payment_card_number.md!}

`PaymentCardBrand` 可以是基于 BIN 的以下之一：

- `PaymentCardBrand.amex`
- `PaymentCardBrand.mastercard`
- `PaymentCardBrand.visa`
- `PaymentCardBrand.other`

实际验证验证卡号是：

- 只有数字的`str`
- [luhn](https://en.wikipedia.org/wiki/Luhn_algorithm) 有效的
- 基于 BIN 的正确长度，如果是美国运通卡、万事达卡或维萨卡，以及所有其他品牌的 12 到 19 位数字

## 约束类型(Constrained Types)

可以使用 `con*` 类型函数来限制许多常见类型的值：

{!.tmp_examples/types_constrained.md!}

其中 `Field` 指的是 [字段函数](schema.md#field-customization)。

### `conlist` 的参数

使用 `conlist` 类型函数时可以使用以下参数

- `item_type: Type[T]`: 列表项的类型
- `min_items: int = None`: 列表中的最小项目数
- `max_items: int = None`: 列表中的最大项目数
- `unique_items: bool = None`: 强制列表元素是唯一的

### `conset` 的参数

使用 `conset` 类型函数时可以使用以下参数

- `item_type: Type[T]`: 设置项目的类型
- `min_items: int = None`: 集合中的最小项目数
- `max_items: int = None`: 集合中的最大项目数

### `confrozenset` 的参数

使用 `confrozenset` 类型函数时可以使用以下参数

- `item_type: Type[T]`: frozenset 项目的类型
- `min_items: int = None`: frozenset 中的最小项目数
- `max_items: int = None`: frozenset 中的最大项目数

### `conint` 的参数

使用 `conint` 类型函数时可以使用以下参数

- `strict: bool = False`: 控制类型强制
- `gt: int = None`: 强制整数大于设定值
- `ge: int = None`: 强制整数大于或等于设定值
- `lt: int = None`: 强制整数小于设定值
- `le: int = None`: 强制整数小于或等于设定值
- `multiple_of: int = None`: 强制整数为设定值的倍数

### `confloat` 的参数

使用 `confloat` 类型函数时可以使用以下参数

- `strict: bool = False`: 控制类型强制
- `gt: float = None`: 强制浮动大于设定值
- `ge: float = None`: 强制float大于等于设定值
- `lt: float = None`: 强制 float 小于设定值
- `le: float = None`: 强制 float 小于或等于设置值
- `multiple_of: float = None`: 强制 float 是设置值的倍数
- `allow_inf_nan: bool = True`: 是否允许无穷大（`+inf` 和 `-inf`）和 NaN 值，默认为 `True`，设置为 `False` 以与 `JSON` 兼容，
  见 [#3994](https://github.com/pydantic/pydantic/pull/3994) 获取更多详情, 在 __V1.10__ 版本中添加

### `condecimal` 的参数

使用 `condecimal` 类型函数时可以使用以下参数

- `gt: Decimal = None`: 强制小数大于设定值
- `ge: Decimal = None`: 强制小数大于或等于设定值
- `lt: Decimal = None`: 强制小数小于设定值
- `le: Decimal = None`: 强制小数小于或等于设定值
- `max_digits: int = None`: 小数点内的最大位数。 它不包括小数点前的零或尾随的小数零
- `decimal_places: int = None`: 允许的最大小数位数。 它不包括尾随的小数零
- `multiple_of: Decimal = None`: 强制小数为设定值的倍数

### `constr` 的参数

使用 `constr` 类型函数时可以使用以下参数

- `strip_whitespace: bool = False`: 删除前导和尾随空格
- `to_upper: bool = False`: 将所有字符转为大写
- `to_lower: bool = False`: 将所有字符变为小写
- `strict: bool = False`: 控制类型强制
- `min_length: int = None`: 字符串的最小长度
- `max_length: int = None`: 字符串的最大长度
- `curtail_length: int = None`: 当字符串长度超过设定值时，将字符串长度收缩到设定值
- `regex: str = None`: 用于验证字符串的正则表达式

### `conbytes` 的参数

使用 `conbytes` 类型函数时可以使用以下参数

- `strip_whitespace: bool = False`: 删除前导和尾随空格
- `to_upper: bool = False`: 将所有字符转为大写
- `to_lower: bool = False`: 将所有字符变为小写
- `min_length: int = None`: 字节串的最小长度
- `max_length: int = None`: 字节串的最大长度
- `strict: bool = False`: 控制类型强制

### `condate` 的参数

使用 `condate` 类型函数时可以使用以下参数

- `gt: date = None`: 强制日期大于设定值
- `ge: date = None`: 强制日期大于或等于设定值
- `lt: date = None`: 强制日期小于设定值
- `le: date = None`: 强制日期小于或等于设定值

## 严格类型(Strict Types)

您可以使用`StrictStr`、`StrictBytes`、`StrictInt`、`StrictFloat`和`StrictBool`类型来防止来自兼容类型的强制转换。

只有当验证值属于相应类型或该类型的子类型时，这些类型才会通过验证。

此行为也通过`ConstrainedStr`、`ConstrainedBytes`、`ConstrainedFloat`和`ConstrainedInt`类的`strict`字段公开，并且可以与大量复杂的验证规则结合使用。

以下注意事项适用：

- `StrictBytes`（以及 `ConstrainedBytes` 的 `strict` 选项）将接受 `bytes` 和 `bytearray` 类型。
- `StrictInt`（以及 `ConstrainedInt` 的 `strict` 选项）将不接受 `bool` 类型，即使 `bool` 是 Python 中 `int` 的子类。 其他子类将起作用。
- `StrictFloat`（以及 `ConstrainedFloat` 的 `strict` 选项）将不接受 `int`。

{!.tmp_examples/types_strict.md!}

## 字节大小类型(ByteSize)

您可以使用`ByteSize`数据类型将字节字符串表示形式转换为原始字节，并打印出人类可读的字节版本。

!!! info
    请注意，`1b` 将被解析为`1 byte`而不是`1 bit`。

{!.tmp_examples/types_bytesize.md!}

## 自定义数据类型(Custom Data Types)

您还可以定义自己的自定义数据类型。 有几种方法可以实现它。

### 带有 `__get_validators__` 的类 (Classes with `__get_validators__`)

您使用带有类方法 `__get_validators__` 的自定义类。 它将被调用以获取验证器来解析和验证输入数据。

!!! tip
    这些验证器具有与 [Validators](validators.md) 中相同的语义，您可以声明参数 `config`、`field` 等。

{!.tmp_examples/types_custom_type.md!}

类似的验证可以使用 [`constr(regex=...)`](#constrained-types) 来实现，除了值不会用空格格式化，模式将只包含完整模式，返回值将是 香草字符串。

有关如何生成模型架构的更多详细信息，请参阅 [schema](schema.md)。

### 允许任意类型(Arbitrary Types Allowed)

您可以使用 [模型配置](model_config.md) 中的 `arbitrary_types_allowed` 配置允许任意类型。

{!.tmp_examples/types_arbitrary_allowed.md!}

### 作为类型的通用类(Generic Classes as Types)

!!! warning
    这是一种您一开始可能不需要的高级技术。 在大多数情况下，您可能会使用标准的 *pydantic* 模型。

您可以使用 [Generic Classes](https://docs.python.org/3/library/typing.html#typing.Generic) 作为字段类型，并根据“类型参数(type parameters)”（或子类型）执行自定义验证 与 `__get_validators__` 。

如果您用作子类型的通用类具有类方法`__get_validators__`，则无需使用`arbitrary_types_allowed`即可工作。

因为您可以声明接收当前 `field` 的验证器，所以您可以提取 `sub_field` （从通用类类型参数）并使用它们验证数据。

{!.tmp_examples/types_generics.md!}
