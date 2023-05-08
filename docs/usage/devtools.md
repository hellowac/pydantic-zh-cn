!!! note
    **承认:** 我（*pydantic* 的主要开发人员）也开发了 python-devtools。

[python-devtools](https://python-devtools.helpmanual.io/) (`pip install devtools`) 提供了许多在 Python 开发过程中非常有用的工具，包括`debug()` 作为`print( )` 以比 `print` 更容易阅读的方式格式化输出，并提供有关打印语句所在的文件/行以及打印的值的信息。

*pydantic* 通过在大多数公共类上实现 `__pretty__` 方法与 *devtools* 集成。

特别是 `debug()` 在检查模型时很有用：

{!.tmp_examples/devtools_main.md!}

将在您的终端输出：

{!.tmp_examples/devtools_main.html!}
