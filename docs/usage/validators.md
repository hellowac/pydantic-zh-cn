自定义验证和对象之间的复杂关系可以使用 `validator` 装饰器来实现。

{!.tmp_examples/validators_simple.md!}

关于验证器的一些注意事项：

* 验证器是“类方法”，因此它们收到的第一个参数值是 `UserModel` 类，而不是`UserModel`的实例。
* 第二个参数始终是要验证的字段值； 它可以随意命名
* 您还可以将以下参数的任何子集添加到签名中（但名称**必须**匹配）：
  * `values`: 包含任何先前验证字段的名称到值映射的字典
  * `config`: 模型配置
  * `field`: 正在验证的字段。 对象的类型是 `pydantic.fields.ModelField`。
  * `**kwargs`: 如果提供，这将包括上面未在签名中明确列出的参数
* 验证器应该返回解析后的值或引发 `ValueError`、`TypeError` 或 `AssertionError`（可以使用 ``assert`` 语句）。

!!! warning
    如果您使用 `assert` 语句，请记住使用 [`-O` 优化标志](https://docs.python.org/3/using/cmdline.html#cmdoption-o) 运行 Python 会禁用 `assert` 语句，**验证器将停止工作**。

* 在验证器依赖于其他值的地方，你应该知道：

  * 验证时基于定义时的字段顺序.
    例如。 在上面的示例中，`password2` 可以访问 `password1`（和 `name`），但是 `password1` 不能访问 `password2`。 有关字段如何排序的更多信息，请参阅 [字段排序](models.md#field-ordering)

  * 如果在另一个字段上验证失败（或该字段丢失），它将不会包含在`values`中，比如在本例中的 “if 'password1' in values and ...”。

## 前验证器和每项验证器(Pre and per-item validators)

验证器可以做一些更复杂的事情：

{!.tmp_examples/validators_pre_item.md!}

还有几点需要注意：

* 通过传递多个字段名称，单个验证器可以应用于多个字段
* 通过传递特殊值`“*”`，也可以在*所有*字段上调用单个验证器
* 关键字参数 `pre` 将导致验证器在其他验证之前被调用
* 传递 `each_item=True` 将导致验证器应用于单个值（例如 `List`、`Dict`、`Set` 等），而不是整个对象

## 子类验证器和 `each_item`(Subclass Validators and `each_item`)

如果将验证器与引用父类上的`List`类型字段的子类一起使用，则使用`each_item=True`将导致验证器不运行； 相反，列表必须以编程方式迭代。

{!.tmp_examples/validators_subclass_each_item.md!}

## 始终验证(Validate Always)

出于性能原因，默认情况下，当未提供值时，不会为字段调用验证器。

然而，在某些情况下，始终调用验证器可能是有用的或需要的，例如 设置动态默认值。

{!.tmp_examples/validators_always.md!}

您通常希望将它与 `pre` 一起使用，因为否则与 `always=True` *pydantic* 会尝试验证默认的 `None`，这会导致错误。

## 重用校验器(Reuse validators)

有时，您会希望在多个字段/模型上使用相同的验证器（例如，规范化一些输入数据）。 比较“naive”的写法是编写一个单独的函数，然后从多个装饰器中调用它。 显然，这需要大量重复和样板代码。 为了避免这种情况，`allow_reuse` 参数已添加到 **v1.2** 中的 `pydantic.validator`（默认情况下为 `False`）：

{!.tmp_examples/validators_allow_reuse.md!}

很明显，重复已经减少，模型再次变得几乎是声明性的。

!!! tip
    如果您有很多要验证的字段，定义一个帮助函数通常是有意义的，您可以使用它来避免一遍又一遍地设置 `allow_reuse=True` 。

## 根验证器(Root Validators)

还可以对整个模型的数据执行验证。

{!.tmp_examples/validators_root.md!}

如果 `pre=True` 根验证器引发错误，则不会进行字段验证。 与字段验证器一样，即使先前的验证器失败，默认情况下也会调用“post”（即 `pre=False`）根验证器； 可以通过为验证器设置 `skip_on_failure=True` 关键字参数来更改此行为。

`values` 参数将是一个字典，其中包含通过字段验证的值和适用的字段默认值。

## 字段检查(Field Checks)

在创建类时，会检查验证器以确认它们指定的字段确实存在于模型中。

然而，有时这是不可取的：例如 如果您定义一个验证器来验证继承模型上的字段。 在这种情况下，您应该在验证器上设置 `check_fields=False`。

## 数据类验证器(Dataclass Validators)

验证器还可以与 *pydantic* 数据类一起使用。

{!.tmp_examples/validators_dataclass.md!}
