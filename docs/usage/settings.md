pydantic 最有用的应用程序之一是配置管理。

如果您创建一个继承自 `BaseSettings` 的模型，模型初始化程序将尝试通过从环境中读取来确定未作为关键字参数传递的任何字段的值。 （如果未设置匹配的环境变量，仍将使用默认值。）

这使得很容易：

* 创建明确定义的类型提示应用程序配置类
* 自动从环境变量中读取对配置的修改
* 在需要的地方手动覆盖初始化程序中的特定设置（例如在单元测试中）

例如：

{!.tmp_examples/settings_main.md!}

## 环境变量名称(Environment variable names)

以下规则用于确定为给定字段读取哪些环境变量：

* 默认情况下，环境变量名称是通过连接前缀和字段名称构建的。
  * 例如，要覆盖上面的 `special_function`，您可以使用：

        export my_prefix_special_function='foo.bar'

  * 注1: 默认前缀是一个空字符串。
  * 注2: 构建环境变量名称时忽略字段别名。

* 可以通过两种方式设置自定义环境变量名称：
  * `Config.fields['field_name']['env']` (见上面的 `auth_key` 和 `redis_dsn` )
  * `Field(..., env=...)` (见上面的 `api_key` )
* 在指定自定义环境变量名称时，可以提供字符串或字符串列表。
  * 指定字符串列表时，顺序很重要：使用第一个检测到的值。
  * 例如，对于上面的`redis_dsn`，`service_redis_dsn`将优先于`redis_url`。

!!! warning
    由于 **v1.0** *pydantic* 在查找环境变量以填充设置模型时不考虑字段别名，因此请如上所述使用 `env`。

    为了帮助从别名过渡到 `env`，当在没有自定义环境变量名称的设置模型上使用别名时，将发出警告。 如果你真的想使用别名，要么忽略警告，要么设置 `env` 来抑制它。

区分大小写可以通过 `Config` 打开：

{!.tmp_examples/settings_case_sensitive.md!}

当 `case_sensitive` 为 `True` 时，环境变量名称必须与字段名称匹配（可选地带有前缀），因此在此示例中，`redis_host` 只能通过 `export redis_host` 进行修改。 如果你想命名环境变量全部大写，你也应该命名属性全部大写。 您仍然可以通过`Field(..., env=...)`随意命名环境变量。

在 Pydantic **v1** 中，`case_sensitive` 默认为 `False`，并且所有变量名称都在内部转换为小写。 如果你想在嵌套模型上定义大写变量名，比如 `SubModel`，你必须设置 `case_sensitive=True` 来禁用这种行为。

!!! note
    在 Windows 上，Python 的 `os` 模块始终将环境变量视为不区分大小写，因此 `case_sensitive` 配置设置将无效 - 设置将始终忽略大小写进行更新。

## 解析环境变量值(Parsing environment variable values)

对于大多数简单字段类型（例如`int`、`float`、`str`等），环境变量值的解析方式与直接传递给初始化程序（作为字符串）时的解析方式相同。

`list`、`set`、`dict` 和子模型等复杂类型是通过将环境变量的值视为 JSON 编码字符串来从环境中填充的。

填充嵌套复杂变量的另一种方法是使用 `env_nested_delimiter` 配置设置配置模型，然后使用名称指向嵌套模块字段的环境变量。 它所做的只是将您的变量分解为嵌套模型或字典。 因此，如果您定义一个变量 `FOO__BAR__BAZ=123`，它会将其转换为 `FOO={'BAR': {'BAZ': 123}}` 如果您有多个具有相同结构的变量，它们将被合并。

使用以下环境变量：

```bash
# 你的环境
export V0=0
export SUB_MODEL='{"v1": "json-1", "v2": "json-2"}'
export SUB_MODEL__V2=nested-2
export SUB_MODEL__V3=3
export SUB_MODEL__DEEP__V4=v4
```

您可以这样加载设置模块：

{!.tmp_examples/settings_nested_env.md!}

`env_nested_delimiter` 可以通过如上所示的 `Config` 类进行配置，或者通过实例化时的 `_env_nested_delimiter` 关键字参数进行配置。

JSON 仅在顶级字段中解析，如果您需要在子模型中解析 JSON，则需要在这些模型上实现验证器。

嵌套环境变量优先于顶级环境变量 JSON（例如，在上面的示例中，`SUB_MODEL__V2` 胜过 `SUB_MODEL`）。

您还可以通过向 Config 对象中的 `parse_env_var` 类方法提供您自己的解析函数来填充复杂类型。

{!.tmp_examples/settings_with_custom_parsing.md!}

## Dotenv (.env) 支持(support)

!!! note
    dotenv 文件解析需要安装 [python-dotenv](https://pypi.org/project/python-dotenv/)。 这可以通过`pip install python-dotenv`或`pip install pydantic[dotenv]`来完成。

Dotenv 文件（通常命名为`.env`）是一种常见的模式，可以轻松地以独立于平台的方式使用环境变量。

dotenv 文件遵循所有环境变量的相同一般原则，看起来像：

```bash
# ignore comment
ENVIRONMENT="production"
REDIS_ADDRESS=localhost:6379
MEANING_OF_LIFE=42
MY_VAR='Hello world'
```

一旦你的 `.env` 文件充满了变量，*pydantic* 支持以两种方式加载它：

**1.** 在 `BaseSettings` 类的 `Config` 上设置 `env_file`（如果您不想使用操作系统的默认编码，则设置 `env_file_encoding`）：

```py
class Settings(BaseSettings):
    ...

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
```

**2.** 使用 `_env_file` 关键字参数（以及 `_env_file_encoding` 如果需要）实例化 `BaseSettings` 派生类：

```py
settings = Settings(_env_file='prod.env', _env_file_encoding='utf-8')
```

在任何一种情况下，传递的参数的值都可以是任何有效的路径或文件名，可以是相对于当前工作目录的绝对路径或相对路径。 从那里，*pydantic* 将通过加载变量并验证它们来为您处理所有事情。

!!! note
    如果为 `env_file` 指定了文件名，Pydantic 将只检查当前工作目录，而不会检查 `.env` 文件的任何父目录。

即使在使用 dotenv 文件时，*pydantic* 仍会读取环境变量以及 dotenv 文件，**环境变量将始终优先于从 dotenv 文件加载的值**。

在实例化时通过 `_env_file` 关键字参数传递文件路径（方法 2）将覆盖在 `Config` 类上设置的值（如果有）。 如果结合使用上述代码片段，将加载 `prod.env` 而忽略 `.env` 。

如果您需要加载多个 dotenv 文件，您可以将文件路径作为 `list` 或 `tuple` 传递。

列表/元组中后面的文件将优先于前面的文件。

```py
from pydantic import BaseSettings

class Settings(BaseSettings):
    ...

    class Config:
        # `.env.prod` takes priority over `.env`
        env_file = '.env', '.env.prod'
```

您还可以使用关键字参数覆盖告诉 Pydantic 根本不要加载任何文件（即使在 `Config` 类中设置了一个文件）通过将 `None` 作为实例化关键字参数传递，例如 `settings = Settings(_env_file=None)`。

因为 python-dotenv 用于解析文件，所以可以使用类似 bash 的语义，例如 `export`，这（取决于您的操作系统和环境）可能允许您的 dotenv 文件也可以与 `source` 一起使用，请参阅 [python-dotenv 的文档](https://saurabh-kumar.com/python-dotenv/#usages) 了解更多详情。

## 保密支持(Secret Support)

在文件中放置秘密值是为应用程序提供敏感配置的常见模式。

秘密文件遵循与 dotenv 文件相同的原则，只是它只包含一个值并且文件名用作密钥。 秘密文件如下所示：

`/var/run/database_password`:

```text
super_secret_database_password
```

一旦你有了你的秘密文件，*pydantic* 支持以两种方式加载它：

**1.** 将 `BaseSettings` 类中 `Config` 的 `secrets_dir` 设置为存储秘密文件的目录：

```py
class Settings(BaseSettings):
    ...
    database_password: str

    class Config:
        secrets_dir = '/var/run'
```

**2.** 使用 `_secrets_dir` 关键字参数实例化 `BaseSettings` 派生类：

```py
settings = Settings(_secrets_dir='/var/run')
```

在任何一种情况下，传递的参数的值都可以是任何有效目录，可以是相对于当前工作目录的绝对目录或相对目录。 **请注意，不存在的目录只会生成警告**。 从那里，*pydantic* 将通过加载变量并验证它们来为您处理所有事情。

即使在使用 secrets 目录时，*pydantic* 仍会从 dotenv 文件或环境中读取环境变量，**dotenv 文件和环境变量将始终优先于从 secrets 目录加载的值**。

在实例化时通过 `_secrets_dir` 关键字参数传递文件路径（方法 2）将覆盖在 `Config` 类上设置的值（如果有）。

### 使用案例(Use Case: Docker Secrets)

Docker Secrets 可用于为在 Docker 容器中运行的应用程序提供敏感配置。

要在 *pydantic* 应用程序中使用这些秘密，过程很简单。 有关在 Docker 中创建、管理和使用机密的更多信息，请参阅官方 [Docker 文档](https://docs.docker.com/engine/reference/commandline/secret/)。

首先，定义您的配置

```py
class Settings(BaseSettings):
    my_secret_data: str

    class Config:
        secrets_dir = '/run/secrets'
```

!!! note
    默认情况下，Docker 使用`/run/secrets`作为目标挂载点。 如果您想使用不同的位置，请相应地更改`Config.secrets_dir`。

然后，通过 Docker CLI 创建您的秘密

```bash
printf "This is a secret" | docker secret create my_secret_data -
```

最后，在 Docker 容器中运行您的应用程序并提供您新创建的密钥

```bash
docker service create --name pydantic-with-secrets --secret my_secret_data pydantic-app:latest
```

## 字段值优先级(Field value priority)

在以多种方式为同一 `Settings` 字段指定值的情况下，选择的值确定如下（按优先级降序排列）：

1. 传递给`Settings`类初始化程序的参数。
2. 环境变量，例如 `my_prefix_special_function` 如上所述。
3. 从 dotenv (`.env`) 文件加载的变量。
4. 从 secrets 目录加载的变量。
5. `Settings`模型的默认字段值。

## 自定义设置源(Customise settings sources)

如果默认的优先级顺序不符合您的需要，可以通过覆盖 `Settings` 的 `Config` 类上的 `customise_sources` 方法来更改它。

`customise_sources` 将三个可调用对象作为参数，并以元组形式返回任意数量的可调用对象。 依次调用这些可调用对象来构建对设置类字段的输入。

每个可调用对象都应将设置类的一个实例作为其唯一参数并返回一个`dict`。

### 更改优先级(Changing Priority)

返回的可调用对象的顺序决定了输入的优先级； 第一项是最高优先级。

{!.tmp_examples/settings_env_priority.md!}

通过翻转 `env_settings` 和 `init_settings`，环境变量现在优先于 `__init__` kwargs。

### 添加源(Adding sources)

如前所述，*pydantic* 附带多个内置设置源。 但是，您可能偶尔需要添加自己的自定义源，`customise_sources` 使这变得非常简单：

{!.tmp_examples/settings_add_custom_source.md!}

### 删除源(Removing sources)

您可能还想禁用源：

{!.tmp_examples/settings_disable_source.md!}
