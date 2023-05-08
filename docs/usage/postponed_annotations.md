!!! note
    通过 `future import` 和 `ForwardRef` 推迟的注释都需要 Python 3.7+。

延时注解（如 [PEP563](https://www.python.org/dev/peps/pep-0563/) 中所述）“正常工作”。

{!.tmp_examples/postponed_annotations_main.md!}

在内部，*pydantic* 将调用类似于`typing.get_type_hints`的方法来解析注释。

在尚未定义引用类型的情况下，可以使用`ForwardRef`（尽管在 [自引用模型](#self-referencing-models) 的情况下，直接引用类型或通过其字符串引用是一种更简单的解决方案） .

在某些情况下，`ForwardRef`在模型创建期间将无法解析。 例如，只要模型将自身引用为字段类型，就会发生这种情况。 发生这种情况时，您需要在创建模型后调用 `update_forward_refs` 才能使用它：

{!.tmp_examples/postponed_annotations_forward_ref.md!}

!!! warning
    要将字符串（类型名称）解析为注释（类型），*pydantic* 需要一个名称空间字典来执行查找。 为此，它使用 `module.__dict__` ，就像 `get_type_hints` 一样。

    这意味着 *pydantic* 可能无法很好地处理未在模块全局范围内定义的类型。

例如，这个可以正常工作：

{!.tmp_examples/postponed_annotations_works.md!}

但这个就会中断：

{!.tmp_examples/postponed_annotations_broken.md!}

解决这个问题超出了对 *pydantic* 的调用：要么删除未来的导入，要么在全局范围内声明类型。

## 自引用模型(Self-referencing Models)

还支持具有自引用模型的数据结构。 自引用字段将在模型创建后自动解析。

在模型中，您可以使用字符串引用尚未构建的模型：

{!.tmp_examples/postponed_annotations_self_referencing_string.md!}

从 Python 3.7 开始，你也可以通过它的类型来引用它，前提是你导入了`annotations`（参见 [上面](postponed_annotations.md) 以获得依赖于 Python 和 *pydantic* 版本的支持）。

{!.tmp_examples/postponed_annotations_self_referencing_annotations.md!}
