*pydantic* 模型与 [mypy](http://mypy-lang.org/) 一起使用，前提是您使用必填字段的仅注释版本：

{!.tmp_examples/mypy_main.md!}

你可以通过 mypy 运行你的代码：

```bash
mypy \
  --ignore-missing-imports \
  --follow-imports=skip \
  --strict-optional \
  pydantic_mypy_test.py
```

如果您在上面的示例代码中调用 mypy，您应该会看到 mypy 检测到属性访问错误：

```python
13: error: "Model" has no attribute "middle_name"
```

## 严格可选项(Strict Optional)

为了让您的代码通过 `--strict-optional` 传递，您需要使用 `Optional[]` 或 `Optional[]` 的别名，用于默认为 `None` 的所有字段。 （这是 mypy 的标准。）

Pydantic 提供了一些有用的可选或联合类型：

* `NoneStr` aka. `Optional[str]`
* `NoneBytes` aka. `Optional[bytes]`
* `StrBytes` aka. `Union[str, bytes]`
* `NoneStrBytes` aka. `Optional[StrBytes]`

如果这些还不够，您当然可以定义自己的。

## Mypy 插件(Plugin)

Pydantic 附带一个 mypy 插件，该插件向 mypy 添加了许多重要的 pydantic 特定功能，以提高其对代码进行类型检查的能力。

有关详细信息，请参阅 [pydantic mypy 插件文档](../mypy_plugin.md)。

## 其他接口(Other pydantic interfaces)

Pydantic [dataclasses](dataclasses.md) 和 [`validate_arguments` 装饰器](validation_decorator.md)
也应该与 mypy 一起工作。
