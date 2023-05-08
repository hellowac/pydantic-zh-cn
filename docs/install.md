安装非常简单：

```bash
pip install pydantic
```

*pydantic* 除了 Python 3.7、3.8、3.9、3.10 或 3.11 和 [`typing-extensions`](https://pypi.org/project/typing-extensions/) 之外没有任何必需的依赖项。 如果您已经安装了 Python 3.7+ 和 `pip`，那么您就可以开始了。

Pydantic 也可以在 [conda](https://www.anaconda.com) 的 [conda-forge](https://conda-forge.org) 频道下获得：

```bash
conda install pydantic -c conda-forge
```

## 用 Cython 编译(Compiled with Cython)

*pydantic* 可以选择使用 [cython](https://cython.org/) 进行编译，这应该会带来 30-50% 的性能提升。

默认情况下，`pip install` 通过 [PyPI](https://pypi.org/project/pydantic/#files) 为 Linux、MacOS 和 64 位 Windows 提供优化的二进制文件。

如果您手动安装，请在安装 *pydantic* 之前安装 `cython`，编译应该会自动进行。

要测试 *pydantic* 是否编译运行：

```py
import pydantic
print('compiled:', pydantic.compiled)
```

### 性能与打包尺寸的权衡(Performance vs package size trade-off)

编译的二进制文件会增加 Python 环境的大小。 如果出于某种原因你想减少 *pydantic* 安装的大小，你可以避免使用 [`pip --no-binary`](https://pip.pypa.io/en/stable/cli/pip_install/#install-no-binary) 选项。 确保 `Cython` 不在您的环境中，或者您设置了 `SKIP_CYTHON` 环境变量以避免重新编译 *pydantic* 库：

```bash
SKIP_CYTHON=1 pip install --no-binary pydantic pydantic
```

!!! note
    `pydantic` 在这里有意重复， `--no-binary pydantic` 告诉 `pip` 你不需要 pydantic 的二进制文件，下一步 `pydantic` 告诉 `pip` 要安装哪个包。

或者，您可以使用自定义 [构建选项](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html) 重新编译 *pydantic*，这需要 [`Cython`](https ://pypi.org/project/Cython/) 在重新编译 *pydantic* 之前安装的包：

```bash
CFLAGS="-Os -g0 -s" pip install \
  --no-binary pydantic \
  --global-option=build_ext \
  pydantic
```

## 可选依赖项(Optional dependencies)

*pydantic* 有两个可选的依赖项：

* 如果您需要电子邮件验证，您可以添加 [email-validator](https://github.com/JoshData/python-email-validator)
* [dotenv 文件支持](usage/settings.md#dotenv-env-support) 其 `Settings` 需要
  [python-dotenv](https://pypi.org/project/python-dotenv)

要将它们与 *pydantic* 一起安装：

```bash
pip install pydantic[email]
# or
pip install pydantic[dotenv]
# or just
pip install pydantic[email,dotenv]
```

当然，您也可以使用`pip install email-validator`和/或`pip install python-dotenv`手动安装这些要求。

## 从存储库安装(Install from repository)

如果您更喜欢直接从存储库安装 *pydantic*：

```bash
pip install git+git://github.com/pydantic/pydantic@main#egg=pydantic
# or with extras
pip install git+git://github.com/pydantic/pydantic@main#egg=pydantic[email,dotenv]
```
