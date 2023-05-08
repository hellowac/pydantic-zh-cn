我们希望您能为 *pydantic* 做出贡献！

## 问题 Issues

欢迎问题、功能请求和错误报告作为 [讨论或问题](https://github.com/pydantic/pydantic/issues/new/choose)。 **但是，要报告安全漏洞，请参阅我们的[安全政策](https://github.com/pydantic/pydantic/security/policy)。**

为了让我们尽可能简单地帮助您，请在您的问题中包含以下调用的输出：

```bash
python -c "import pydantic.utils; print(pydantic.utils.version_info())"
```

如果您在 **v1.3** 之前使用 *pydantic*（添加 `version_info()` 时），请手动包括操作系统、Python 版本和 pydantic 版本。

请尝试始终包括以上内容，除非您无法安装 *pydantic* 或 **知道** 它与您的问题或功能请求无关。

## 拉取请求 Pull Requests

开始创建合并请求应该非常简单。 *pydantic* 定期发布，因此您应该会在几天或几周内看到您的改进版本。

!!! note
    除非您的更改是微不足道的（错字、文档调整等），否则请在创建拉取请求之前创建一个问题来讨论更改。

如果您正在寻找让您咬牙切齿的东西，请查看github 上的[“需要帮助”](https://github.com/pydantic/pydantic/issues?q=is%3Aopen+is%3Aissue+label%3A %22help+wanted%22) 标签。

为了尽可能简单快速地做出贡献，您需要在本地运行测试和 linting。 幸运的是，*pydantic* 几乎没有依赖项，不需要编译，测试不需要访问数据库等。因此，设置和运行测试应该非常简单。

您需要安装 **Python 3.7 和 3.11**、**virtualenv**、**git** 和 **make** 之间的版本。

```bash
# 1. 克隆你fork的仓库并cd到该目录下
git clone git@github.com:<your username>/pydantic.git
cd pydantic

# 2. 设置用于测试的虚拟环境
virtualenv -p `which python3.8` env
source env/bin/activate
# 构建文档需要 3.8。 如果您不需要构建文档，则可以使用任何版本； 3.7 也可以。

# 3. 安装pydantic、依赖、测试依赖和doc依赖
make install

# 4. 签出一个新分支并进行更改
git checkout -b my-new-feature-branch
# 进行更改...

# 5. 修复格式和导入
make format
# Pydantic 使用black来强制格式化并使用 isort 来完善导入
# (https://github.com/ambv/black, https://github.com/timothycrosley/isort)

# 6. 运行测试和 linting
make
# Makefile 中有一些子命令，例如您可能想要使用的 `test`、`testcov` 和 `lint`，但通常您只需要 `make` 就可以了

# 7. 构建文档
make docs
# 如果您更改了文档，请确保它成功构建，您还可以使用 `make docs-serve` 在 localhost:8000 提供文档

# ... commit, push, 并创建您的拉取请求
```

**总结**: 使用 `make format` 完善格式，`make` 运行测试和 linting 同时使用 `make docs` 构建文档。
