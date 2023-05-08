# pydantic-zh-cn

使用 Python 类型提示进行数据验证 - 中文版文档

## 包管理工具

参考: <https://pdm.fming.dev/latest/>

这里使用pdm

初始化:

```powershell
pdm init
```

添加包:

```powershell
pdm add <package name>
```

## 文档版本工具

* 参考: <https://squidfunk.github.io/mkdocs-material/setup/setting-up-versioning/#publishing-a-new-version>
* 参考: <https://pypi.org/project/mike/>

这里使用mike

安装:

```shell
pip install mike
```

## 前期准备

1. 生成静态文件之前，需要现在项目目录下，执行`python docs/build/main.py` 将 示例中的 python 代码文件执行一遍，主要为了将示例输出添加到生成markdown文件中。
1. 然后再进行`mike deploy <version>` 版本打包发布以及推送分支。
