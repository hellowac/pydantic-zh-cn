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

### Reserved names

您可能希望在保留的 SQLAlchemy 字段之后重新命名。 在这种情况下，**Field** 别名会很方便：

{!.tmp_examples/models_orm_mode_reserved_name.md!}

!!! note

    上面的示例之所以有效，是因为别名优先于字段填充的字段名称。 访问 `SQLModel`的 `metadata` 属性会导致`ValidationError`。

### 嵌套ORM模型(Recursive ORM models)

ORM 实例将使用 `from_orm` 递归地以及在顶层进行解析。

这里使用普通类来演示原理，但也可以使用任何 ORM 类。

{!.tmp_examples/models_orm_mode_recursive.md!}

### 数据绑定(Data binding)

Arbitrary classes are processed by *pydantic* using the `GetterDict` class (see
[utils.py](https://github.com/pydantic/pydantic/blob/1.10.X-fixes/pydantic/utils.py)), which attempts to
provide a dictionary-like interface to any class. You can customise how this works by setting your own
sub-class of `GetterDict` as the value of `Config.getter_dict` (see [config](model_config.md)).

You can also customise class validation using [root_validators](validators.md#root-validators) with `pre=True`.
In this case your validator function will be passed a `GetterDict` instance which you may copy and modify.

The `GetterDict` instance will be called for each field with a sentinel as a fallback (if no other default
value is set). Returning this sentinel means that the field is missing. Any other value will
be interpreted as the value of the field.

{!.tmp_examples/models_orm_mode_data_binding.md!}

## 错误处理(Error Handling)

*pydantic* will raise `ValidationError` whenever it finds an error in the data it's validating.

!!! note
    Validation code should not raise `ValidationError` itself, but rather raise `ValueError`, `TypeError` or
    `AssertionError` (or subclasses of `ValueError` or `TypeError`) which will be caught and used to populate
    `ValidationError`.

One exception will be raised regardless of the number of errors found, that `ValidationError` will
contain information about all the errors and how they happened.

You can access these errors in several ways:

`e.errors()`
: method will return list of errors found in the input data.

`e.json()`
: method will return a JSON representation of `errors`.

`str(e)`
: method will return a human readable representation of the errors.

Each error object contains:

`loc`
: the error's location as a list. The first item in the list will be the field where the error occurred,
  and if the field is a [sub-model](models.md#recursive-models), subsequent items will be present to indicate
  the nested location of the error.

`type`
: a computer-readable identifier of the error type.

`msg`
: a human readable explanation of the error.

`ctx`
: an optional object which contains values required to render the error message.

As a demonstration:

{!.tmp_examples/models_errors1.md!}

### 自定义错误(Custom Errors)

In your custom data types or validators you should use `ValueError`, `TypeError` or `AssertionError` to raise errors.

See [validators](validators.md) for more details on use of the `@validator` decorator.

{!.tmp_examples/models_errors2.md!}

You can also define your own error classes, which can specify a custom error code, message template, and context:

{!.tmp_examples/models_errors3.md!}

## 辅助函数(Helper Functions)

*Pydantic* provides three `classmethod` helper functions on models for parsing data:

* **`parse_obj`**: this is very similar to the `__init__` method of the model, except it takes a dict
  rather than keyword arguments. If the object passed is not a dict a `ValidationError` will be raised.
* **`parse_raw`**: this takes a *str* or *bytes* and parses it as *json*, then passes the result to `parse_obj`.
  Parsing *pickle* data is also supported by setting the `content_type` argument appropriately.
* **`parse_file`**: this takes in a file path, reads the file and passes the contents to `parse_raw`. If `content_type` is omitted,
  it is inferred from the file's extension.

{!.tmp_examples/models_parse.md!}

!!! warning
    To quote the [official `pickle` docs](https://docs.python.org/3/library/pickle.html),
    "The pickle module is not secure against erroneous or maliciously constructed data.
    Never unpickle data received from an untrusted or unauthenticated source."

!!! info
    Because it can result in arbitrary code execution, as a security measure, you need
    to explicitly pass `allow_pickle` to the parsing function in order to load `pickle` data.

### 创建无需校验的模型(Creating models without validation)

*pydantic* also provides the `construct()` method which allows models to be created **without validation** this
can be useful when data has already been validated or comes from a trusted source and you want to create a model
as efficiently as possible (`construct()` is generally around 30x faster than creating a model with full validation).

!!! warning
    `construct()` does not do any validation, meaning it can create models which are invalid. **You should only
    ever use the `construct()` method with data which has already been validated, or you trust.**

{!.tmp_examples/models_construct.md!}

The `_fields_set` keyword argument to `construct()` is optional, but allows you to be more precise about
which fields were originally set and which weren't. If it's omitted `__fields_set__` will just be the keys
of the data provided.

For example, in the example above, if `_fields_set` was not provided,
`new_user.__fields_set__` would be `{'id', 'age', 'name'}`.

## 通用模型(Generic Models)

Pydantic supports the creation of generic models to make it easier to reuse a common model structure.

In order to declare a generic model, you perform the following steps:

* Declare one or more `typing.TypeVar` instances to use to parameterize your model.
* Declare a pydantic model that inherits from `pydantic.generics.GenericModel` and `typing.Generic`,
  where you pass the `TypeVar` instances as parameters to `typing.Generic`.
* Use the `TypeVar` instances as annotations where you will want to replace them with other types or
  pydantic models.

Here is an example using `GenericModel` to create an easily-reused HTTP response payload wrapper:

{!.tmp_examples/models_generics.md!}

If you set `Config` or make use of `validator` in your generic model definition, it is applied
to concrete subclasses in the same way as when inheriting from `BaseModel`. Any methods defined on
your generic class will also be inherited.

Pydantic's generics also integrate properly with mypy, so you get all the type checking
you would expect mypy to provide if you were to declare the type without using `GenericModel`.

!!! note
    Internally, pydantic uses `create_model` to generate a (cached) concrete `BaseModel` at runtime,
    so there is essentially zero overhead introduced by making use of `GenericModel`.

To inherit from a GenericModel without replacing the `TypeVar` instance, a class must also inherit from
`typing.Generic`:

{!.tmp_examples/models_generics_inheritance.md!}

You can also create a generic subclass of a `GenericModel` that partially or fully replaces the type
parameters in the superclass.

{!.tmp_examples/models_generics_inheritance_extend.md!}

If the name of the concrete subclasses is important, you can also override the default behavior:

{!.tmp_examples/models_generics_naming.md!}

Using the same TypeVar in nested models allows you to enforce typing relationships at different points in your model:

{!.tmp_examples/models_generics_nested.md!}

Pydantic also treats `GenericModel` similarly to how it treats built-in generic types like `List` and `Dict` when it
comes to leaving them unparameterized, or using bounded `TypeVar` instances:

* If you don't specify parameters before instantiating the generic model, they will be treated as `Any`
* You can parametrize models with one or more *bounded* parameters to add subclass checks

Also, like `List` and `Dict`, any parameters specified using a `TypeVar` can later be substituted with concrete types.

{!.tmp_examples/models_generics_typevars.md!}

## 动态模型的创建(Dynamic model creation)

There are some occasions where the shape of a model is not known until runtime. For this *pydantic* provides
the `create_model` method to allow models to be created on the fly.

{!.tmp_examples/models_dynamic_creation.md!}

Here `StaticFoobarModel` and `DynamicFoobarModel` are identical.

!!! warning
    See the note in [Required Optional Fields](#required-optional-fields) for the distinction between an ellipsis as a
    field default and annotation-only fields.
    See [pydantic/pydantic#1047](https://github.com/pydantic/pydantic/issues/1047) for more details.

Fields are defined by either a tuple of the form `(<type>, <default value>)` or just a default value. The
special key word arguments `__config__` and `__base__` can be used to customise the new model. This includes
extending a base model with extra fields.

{!.tmp_examples/models_dynamic_inheritance.md!}

You can also add validators by passing a dict to the `__validators__` argument.

{!.tmp_examples/models_dynamic_validators.md!}

## 从`NamedTuple`或`TypedDict`创建模型(Model creation from `NamedTuple` or `TypedDict`)

Sometimes you already use in your application classes that inherit from `NamedTuple` or `TypedDict`
and you don't want to duplicate all your information to have a `BaseModel`.
For this *pydantic* provides `create_model_from_namedtuple` and `create_model_from_typeddict` methods.
Those methods have the exact same keyword arguments as `create_model`.

{!.tmp_examples/models_from_typeddict.md!}

## 自定义根类型(Custom Root Types)

Pydantic models can be defined with a custom root type by declaring the `__root__` field.

The root type can be any type supported by pydantic, and is specified by the type hint on the `__root__` field.
The root value can be passed to the model `__init__` via the `__root__` keyword argument, or as
the first and only argument to `parse_obj`.

{!.tmp_examples/models_custom_root_field.md!}

If you call the `parse_obj` method for a model with a custom root type with a *dict* as the first argument,
the following logic is used:

* If the custom root type is a mapping type (eg., `Dict` or `Mapping`),
  the argument itself is always validated against the custom root type.
* For other custom root types, if the dict has precisely one key with the value `__root__`,
  the corresponding value will be validated against the custom root type.
* Otherwise, the dict itself is validated against the custom root type.

This is demonstrated in the following example:

{!.tmp_examples/models_custom_root_field_parse_obj.md!}

!!! warning
    Calling the `parse_obj` method on a dict with the single key `"__root__"` for non-mapping custom root types
    is currently supported for backwards compatibility, but is not recommended and may be dropped in a future version.

If you want to access items in the `__root__` field directly or to iterate over the items, you can implement custom `__iter__` and `__getitem__` functions, as shown in the following example.

{!.tmp_examples/models_custom_root_access.md!}

## 伪不变性(Faux Immutability)

Models can be configured to be immutable via `allow_mutation = False`. When this is set, attempting to change the
values of instance attributes will raise errors. See [model config](model_config.md) for more details on `Config`.

!!! warning
    Immutability in Python is never strict. If developers are determined/stupid they can always
    modify a so-called "immutable" object.

{!.tmp_examples/models_mutation.md!}

Trying to change `a` caused an error, and `a` remains unchanged. However, the dict `b` is mutable, and the
immutability of `foobar` doesn't stop `b` from being changed.

## 抽象基类(Abstract Base Classes)

Pydantic models can be used alongside Python's
[Abstract Base Classes](https://docs.python.org/3/library/abc.html) (ABCs).

{!.tmp_examples/models_abc.md!}

## 字段顺序(Field Ordering)

Field order is important in models for the following reasons:

* validation is performed in the order fields are defined; [fields validators](validators.md)
  can access the values of earlier fields, but not later ones
* field order is preserved in the model [schema](schema.md)
* field order is preserved in [validation errors](#error-handling)
* field order is preserved by [`.dict()` and `.json()` etc.](exporting_models.md#modeldict)

As of **v1.0** all fields with annotations (whether annotation-only or with a default value) will precede
all fields without an annotation. Within their respective groups, fields remain in the order they were defined.

{!.tmp_examples/models_field_order.md!}

!!! warning
    As demonstrated by the example above, combining the use of annotated and non-annotated fields
    in the same model can result in surprising field orderings. (This is due to limitations of Python)

    Therefore, **we recommend adding type annotations to all fields**, even when a default value
    would determine the type by itself to guarantee field order is preserved.

## 必须字段(Required fields)

To declare a field as required, you may declare it using just an annotation, or you may use an ellipsis (`...`)
as the value:

{!.tmp_examples/models_required_fields.md!}

Where `Field` refers to the [field function](schema.md#field-customization).

Here `a`, `b` and `c` are all required. However, use of the ellipses in `b` will not work well
with [mypy](mypy.md), and as of **v1.0** should be avoided in most cases.

### 必须但可选字段(Required Optional fields)

!!! warning
    Since version **v1.2** annotation only nullable (`Optional[...]`, `Union[None, ...]` and `Any`) fields and nullable
    fields with an ellipsis (`...`) as the default value, no longer mean the same thing.

    In some situations this may cause **v1.2** to not be entirely backwards compatible with earlier **v1.*** releases.

If you want to specify a field that can take a `None` value while still being required,
you can use `Optional` with `...`:

{!.tmp_examples/models_required_field_optional.md!}

In this model, `a`, `b`, and `c` can take `None` as a value. But `a` is optional, while `b` and `c` are required.
`b` and `c` require a value, even if the value is `None`.

## 具有动态默认值的字段(Field with dynamic default value)

When declaring a field with a default value, you may want it to be dynamic (i.e. different for each model).
To do this, you may want to use a `default_factory`.

!!! info "In Beta"
    The `default_factory` argument is in **beta**, it has been added to *pydantic* in **v1.5** on a
    **provisional basis**. It may change significantly in future releases and its signature or behaviour will not
    be concrete until **v2**. Feedback from the community while it's still provisional would be extremely useful;
    either comment on [#866](https://github.com/pydantic/pydantic/issues/866) or create a new issue.

Example of usage:

{!.tmp_examples/models_default_factory.md!}

Where `Field` refers to the [field function](schema.md#field-customization).

!!! warning
    The `default_factory` expects the field type to be set.

## 自动排除的属性(Automatically excluded attributes)

Class variables which begin with an underscore and attributes annotated with `typing.ClassVar` will be
automatically excluded from the model.

## 私有模型属性(Private model attributes)

If you need to vary or manipulate internal attributes on instances of the model, you can declare them
using `PrivateAttr`:

{!.tmp_examples/private_attributes.md!}

Private attribute names must start with underscore to prevent conflicts with model fields: both `_attr` and `__attr__`
are supported.

If `Config.underscore_attrs_are_private` is `True`, any non-ClassVar underscore attribute will be treated as private:
{!.tmp_examples/private_attributes_underscore_attrs_are_private.md!}

Upon class creation pydantic constructs `__slots__` filled with private attributes.

## 将数据解析为指定类型(Parsing data into a specified type)

Pydantic includes a standalone utility function `parse_obj_as` that can be used to apply the parsing
logic used to populate pydantic models in a more ad-hoc way. This function behaves similarly to
`BaseModel.parse_obj`, but works with arbitrary pydantic-compatible types.

This is especially useful when you want to parse results into a type that is not a direct subclass of `BaseModel`.
For example:

{!.tmp_examples/parse_obj_as.md!}

This function is capable of parsing data into any of the types pydantic can handle as fields of a `BaseModel`.

Pydantic also includes two similar standalone functions called `parse_file_as` and `parse_raw_as`,
which are analogous to `BaseModel.parse_file` and `BaseModel.parse_raw`.

## 数据转换(Data Conversion)

*pydantic* may cast input data to force it to conform to model field types,
and in some cases this may result in a loss of information.
For example:

{!.tmp_examples/models_data_conversion.md!}

This is a deliberate decision of *pydantic*, and in general it's the most useful approach. See
[here](https://github.com/pydantic/pydantic/issues/578) for a longer discussion on the subject.

Nevertheless, [strict type checking](types.md#strict-types) is partially supported.

## 模型签名(Model signature)

All *pydantic* models will have their signature generated based on their fields:

{!.tmp_examples/models_signature.md!}

An accurate signature is useful for introspection purposes and libraries like `FastAPI` or `hypothesis`.

The generated signature will also respect custom `__init__` functions:

{!.tmp_examples/models_signature_custom_init.md!}

To be included in the signature, a field's alias or name must be a valid Python identifier.
*pydantic* prefers aliases over names, but may use field names if the alias is not a valid Python identifier.

If a field's alias and name are both invalid identifiers, a `**data` argument will be added.
In addition, the `**data` argument will always be present in the signature if `Config.extra` is `Extra.allow`.

!!! note
    Types in the model signature are the same as declared in model annotations,
    not necessarily all the types that can actually be provided to that field.
    This may be fixed one day once [#1055](https://github.com/pydantic/pydantic/issues/1055) is solved.

## 结构模式匹配(Structural pattern matching)

*pydantic* supports structural pattern matching for models, as introduced by [PEP 636](https://peps.python.org/pep-0636/) in Python 3.10.

{!.tmp_examples/models_structural_pattern_matching.md!}

!!! note
    A match-case statement may seem as if it creates a new model, but don't be fooled;  
    it is just syntactic sugar for getting an attribute and either comparing it or declaring and initializing it.
