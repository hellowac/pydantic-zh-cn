虽然 pydantic 可以与任何开箱即用的 IDE 配合使用，但 PyCharm 的插件仓库 上提供了一个 [PyCharm 插件](https://plugins.jetbrains.com/plugin/12861-pydantic)，它提供了改进的 pydantic 集成。 您可以从插件市场（PyCharm 的首选项 -> 插件 -> 市场 -> 搜索“pydantic”）免费安装该插件。

该插件目前支持以下功能：

* 对于 `pydantic.BaseModel.__init__`:
  * 审查
  * 自动完成
  * 类型检查

* 对于 pydantic.BaseModel 的字段：
  * 重构重命名字段会更新 `__init__` 调用，并影响子类和超类
  * 重构重命名 `__init__` 关键字参数会更新字段名称，并影响子类和超类

可以在 [官方插件页面](https://plugins.jetbrains.com/plugin/12861-pydantic) 和 [Github 存储库](https://github.com/koxudaxi/pydantic-pycharm-plugin)获取更多信息.
