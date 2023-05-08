[datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator/) 项目是一个库和命令行实用程序，用于从几乎任何数据源生成 pydantic 模型，包括：

* OpenAPI 3 (YAML/JSON)
* JSON Schema
* JSON/YAML 数据（将转换为 JSON Schema）

每当您发现自己有任何数据可转换的 JSON 但没有 pydantic 模型时，此工具将允许您按需生成类型安全的模型层次结构。

## 安装 Installation

```bash
pip install datamodel-code-generator
```

## 例子 Example

在这种情况下，datamodel-code-generator 从 JSON 模式文件创建 pydantic 模型。

```bash
datamodel-codegen  --input person.json --input-file-type jsonschema --output model.py
```

person.json:

```json
{
  "$id": "person.json",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Person",
  "type": "object",
  "properties": {
    "first_name": {
      "type": "string",
      "description": "The person's first name."
    },
    "last_name": {
      "type": "string",
      "description": "The person's last name."
    },
    "age": {
      "description": "Age in years.",
      "type": "integer",
      "minimum": 0
    },
    "pets": {
      "type": "array",
      "items": [
        {
          "$ref": "#/definitions/Pet"
        }
      ]
    },
    "comment": {
      "type": "null"
    }
  },
  "required": [
      "first_name",
      "last_name"
  ],
  "definitions": {
    "Pet": {
      "properties": {
        "name": {
          "type": "string"
        },
        "age": {
          "type": "integer"
        }
      }
    }
  }
}
```

model.py:
{!.tmp_examples/generate_models_person_model.md!}

更多信息可以在[官方文档](https://koxudaxi.github.io/datamodel-code-generator/)中找到
