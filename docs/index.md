[![CI](https://github.com/pydantic/pydantic/workflows/CI/badge.svg?event=push)](https://github.com/pydantic/pydantic/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/pydantic/pydantic.svg?branch=1.10.X-fixes)](https://coverage-badge.samuelcolvin.workers.dev/redirect/pydantic/pydantic?branch=1.10.X-fixes)
[![pypi](https://img.shields.io/pypi/v/pydantic.svg)](https://pypi.python.org/pypi/pydantic)
[![CondaForge](https://img.shields.io/conda/v/conda-forge/pydantic.svg)](https://anaconda.org/conda-forge/pydantic)
[![downloads](https://pepy.tech/badge/pydantic/month)](https://pepy.tech/project/pydantic)
[![license](https://img.shields.io/github/license/pydantic/pydantic.svg)](https://github.com/pydantic/pydantic/blob/main/LICENSE)

使用 Python 类型注解的数据验证和设置管理。

*pydantic* 在运行时强制执行类型提示，并在数据无效时提供用户友好的错误。

定义数据应该如何在纯正的、规范的 Python 中； 用 *pydantic* 验证它。

## 赞助商(Sponsors)

以下赞助商使 *pydantic* 的开发成为可能：

<div class="sponsors">
  <div>
    <a rel="sponsored" target="_blank" href="https://www.salesforce.com">
      <img src="./sponsor_logos/salesforce.png" alt="Salesforce" />
      <span>Salesforce</span>
    </a>
  </div>
  <div>
    <a rel="sponsored" target="_blank" href="https://fastapi.tiangolo.com">
      <img src="./sponsor_logos/fastapi.png" alt="FastAPI" />
      <span>FastAPI</span>
    </a>
  </div>
  <div>
    <a rel="sponsored" target="_blank" href="https://aws.amazon.com">
      <img src="./sponsor_logos/aws.png" alt="AWS" />
      <span>AWS</span>
    </a>
  </div>
  <div>
    <a rel="sponsored" target="_blank" href="https://explosion.ai">
      <img src="./sponsor_logos/explosion_ai.png" alt="Explosion" />
      <span>Explosion</span>
    </a>
  </div>
  <div>
    <a rel="sponsored" target="_blank" href="https://tutorcruncher.com/?utm_source=pydantic&utm_campaign=open_source">
      <img src="./sponsor_logos/tutorcruncher.png" alt="TutorCruncher" />
      <span>TutorCruncher</span>
    </a>
  </div>
  <div>
    <a rel="sponsored" target="_blank" href="https://www.exoflare.com/open-source/?utm_source=pydantic&utm_campaign=open_source">
      <img src="./sponsor_logos/exoflare.png" alt="ExoFlare" />
      <span>ExoFlare</span>
    </a>
  </div>
  <div>
    <a rel="sponsored" target="_blank" href="https://home.robusta.dev">
      <img src="./sponsor_logos/robusta.png" alt="Robusta" />
      <span>Robusta</span>
    </a>
  </div>
  <div>
    <a rel="sponsored" target="_blank" href="https://www.sendcloud.com">
      <img src="./sponsor_logos/sendcloud.png" alt="SendCloud" />
      <span>SendCloud</span>
    </a>
  </div>
  <div>
    <a rel="sponsored" target="_blank" href="https://jina.ai">
      <img src="./sponsor_logos/jina-ai.png" alt="Jina AI" />
      <span>Jina AI</span>
    </a>
  </div>
</div>

还有更多人在 [GitHub 赞助商](https://github.com/sponsors/samuelcolvin#sponsors) 上慷慨赞助 Samuel Colvin。

<script>
  // randomize the order of sponsors
  const ul = document.querySelector('.sponsors')
  for (let i = ul.children.length; i >= 0; i--) {
    ul.appendChild(ul.children[Math.random() * i | 0])
  }
</script>

## Example

```python
{!./examples/index_main.py!}
```

这里发生了什么：

* `id` 是 int 类型； 仅注解声明告诉 *pydantic* 这个字段是必需的。 如果可能，字符串、字节或浮点数将被强制转换为整数； 否则将引发异常。
* `name` 从提供的默认值推断为字符串； 因为它有一个默认值，所以它不是必需的。
* `signup_ts` 是一个不需要的日期时间字段（如果未提供则取值 ``None``）。
  *pydantic* 将处理 unix 时间戳 int（例如 `1496498400`）或表示日期和时间的字符串。
* `friends` 使用 Python 的类型系统，并且需要一个整数列表。 与 `id` 一样，类整数对象将被转换为整数。

如果验证失败，pydantic 将引发错误并详细说明错误：

```python
{!./examples/index_error.py!}
```

## 基本原理(Rationale)

所以 *pydantic* 使用了一些很酷的新语言特性，但我为什么要真正去使用它呢？

**与您的 IDE/linter/brain 完美搭配**
: 无需学习新的模式定义微语言。 如果您知道如何使用 Python 类型提示，您就会知道如何使用 *pydantic*。 数据结构只是您使用类型注释定义的类的实例，因此自动完成、linting、[mypy](usage/mypy.md)、IDE（尤其是 [PyCharm](pycharm_plugin.md)）和您的直觉都应该有效 正确使用您的验证数据。

**双重用途**
: *pydantic* 的 [BaseSettings](usage/settings.md) 类允许 *pydantic* 在“验证此请求数据”上下文和“加载我的系统设置”上下文中使用。 主要区别在于系统设置可以从环境变量中读取，并且通常需要更复杂的对象，如 DSN 和 Python 对象。

**快速**
: *pydantic* 一直很重视性能，大部分库都是用 cython 编译的，加速了 ~50%，它通常比大多数类似的库快或更快。

**验证复杂结构**
: 使用[递归 *pydantic* 模型](usage/models.md#recursive-models)、`typing` 的 [标准类型](usage/types.md#standard-library-types)（例如 `List`、`Tuple`、`Dict` 等）和 [validators](usage/validators.md) 允许清晰、轻松地定义、验证和解析复杂的数据模式。

**可扩展的**
: *pydantic* 允许定义[自定义数据类型](usage/types.md#custom-data-types)，或者您可以在装饰有 [`validator`](usage/validators.md) 的模型上使用方法扩展验证装饰器。
  
**数据类整合**
: 除了 `BaseModel` 之外，*pydantic* 还提供了一个 [`dataclass`](usage/dataclasses.md) 装饰器，它创建（几乎）带有输入数据解析和验证的普通 Python 数据类。

## 使用 Pydantic(Using Pydantic)

数百个组织和软件包正在使用 *pydantic*，包括：

[FastAPI](https://fastapi.tiangolo.com/)
: 基于*pydantic* 和 Starlette 的高性能 API 框架，易于学习，编码速度快，可用于生产。

[Project Jupyter](https://jupyter.org/)
: Jupyter notebook 的开发人员正在使用 *pydantic* [用于子项目](https://github.com/pydantic/pydantic/issues/773)，通过基于 FastAPI 的 Jupyter 服务器 [Jupyverse](https://github.com /jupyter-server/jupyverse)，以及 [FPS](https://github.com/jupyter-server/fps) 的配置管理。

**Microsoft**
: 正在将 *pydantic*（通过 FastAPI）用于 [众多服务](https://github.com/tiangolo/fastapi/pull/26#issuecomment-463768795)，其中一些正在“集成到核心 Windows 产品中，一些 办公用品。”

**Amazon Web Services**
: 在 [gluon-ts](https://github.com/awslabs/gluon-ts) 中使用 *pydantic*，这是一个开源概率时间序列建模库。

**The NSA**
: 在开源自动化框架 [WALKOFF](https://github.com/nsacyber/WALKOFF) 中使用 *pydantic*。

**Uber**
: 在 [Ludwig](https://github.com/uber/ludwig) 中使用 *pydantic*，这是一个开源 TensorFlow 包装器。

**Cuenca**
: 是一家墨西哥新银行，它使用 *pydantic* 用于多个内部工具（包括 API 验证）和开源项目，如 [stpmex](https://github.com/cuenca-mx/stpmex-python)，用于处理 墨西哥实时 24/7 银行间转账。

[分子科学软件研究所](https://molssi.org)
: 在 [QCFractal](https://github.com/MolSSI/QCFractal) 中使用 *pydantic*，这是一个用于量子化学的大规模分布式计算框架。

[Reach](https://www.reach.vote)
: 信任 *pydantic*（通过 FastAPI）和 [*arq*](https://github.com/samuelcolvin/arq)（Samuel 出色的异步任务队列）来可靠地支持多个关键任务微服务。

[Robusta.dev](https://robusta.dev/)
: 正在使用 *pydantic* 来自动化 Kubernetes 故障排除和维护。 例如，他们的开源 [在 Kubernetes 上调试和分析 Python 应用程序的工具](https://home.robusta.dev/python/) 使用 *pydantic* 模型。

有关使用 *pydantic* 的更全面的开源项目列表，请参阅 [github 上的依赖列表](https://github.com/pydantic/pydantic/network/dependents)。

## 对 Pydantic 的讨论(Discussion of Pydantic)

讨论 pydantic 的播客和视频。

[Talk Python To Me](https://talkpython.fm/episodes/show/313/automate-your-data-exchange-with-pydantic){target=_blank}
: *pydantic* 的创始人迈克尔·肯尼迪 (Michael Kennedy) 和塞缪尔·科尔文 (Samuel Colvin) 深入探讨了 pydantic 的历史及其众多用途和好处。

[Podcast.\_\_init\_\_](https://www.pythonpodcast.com/pydantic-data-validation-episode-263/){target=_blank}
: 与 pydantic 的创造者 Samuel Colvin 讨论 *pydantic* 的起源以及它下一步可能走向何方的想法。

[Python Bytes Podcast](https://pythonbytes.fm/episodes/show/157/oh-hai-pandas-hold-my-hand){target=_blank}
: “*这是一个可爱的简单框架，解决了一些非常好的问题......使用 Python 类型注释的数据验证和设置管理，正是 Python 类型注释让我非常高兴......它自动与你的所有 IDE 一起工作 已经有了。*”——迈克尔·肯尼迪

[Python pydantic Introduction – 赋予数据类超能力](https://www.youtube.com/watch?v=WJmqgJn9TXg){target=_blank}
: Alexander Hultnér 最初在 Python Pizza 大会上的演讲，向新用户介绍了 pydantic 并介绍了 pydantic 的核心功能。
