# Ontology Companion Contracts

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [Русский](README.ru.md)

离线验证 Context 和 Code 交换产物，比较支持的契约版本，并将选定的 Code Ontology 数据转换为 `code-reference` 产物，同时说明转换中丢失或省略的信息。

支持 macOS、Windows 和 Linux，需要 Python 3.11 或更高版本。无需安装 Code 或 Context 插件，也不需要 API 密钥或远程服务。

## 安装

```text
codex plugin marketplace add battle-doll/ontology-companion-contracts
codex plugin add ontology-companion-contracts@ontology-contracts-preview
```

请安装完整插件，以便技能、服务器和模式文件保持配套。安装后，在项目中打开新的 Codex 任务，即可使用已安装的技能。

## 应用于当前对话

```text
$apply-ontology-contracts
请将 Contracts 应用于当前对话，并将选定的 context-export.json 按 context-decision 配置类型验证。
```

应用技能使用当前可调用的 MCP 工具或已确认的内置 CLI，将验证结果绑定到实际文件及其内容哈希，然后继续当前任务。缺少输入时保持未完成。通用本体设置只选择当前可运行的产品，明确指定的产品优先。对话中的共享记录避免重复应用，不修改项目或全局设置。直接验证和转换仍使用 `$validate-ontology-contract`。

## 连接项目

在目标项目的新 Codex 任务中发送：

```text
$validate-ontology-contract
请为当前项目设置此插件的本地 MCP 连接。
```

设置完成后，在同一项目中打开新任务即可使用 MCP 工具。直接运行的命令、已安装插件的路径和各操作系统的说明，请参阅[本地 MCP 设置](docs/LOCAL_MCP.md)或 [Windows 快速入门](docs/WINDOWS_QUICKSTART.md)。

## 使用

将文件名替换为项目中需要验证的文件：

```text
$validate-ontology-contract
请验证 context-export.json，并解释其中的格式错误。
```

也可以转换选定的 Code Ontology 快照：

```text
$validate-ontology-contract
请选择 ontology.json 中的 src 路径，转换为 code-reference 产物。
显示转换中省略的信息。
如果需要输入中没有的仓库标识或修订版本，请向我确认。
```

[本地使用指南](docs/LOCAL_USE.md)介绍验证、转换、版本比较和迁移规划，并提供无需 MCP 的 CLI 命令。CLI 转换可以创建新的输出文件，但不会覆盖已有文件。

支持的交换格式为 `0.1.0-draft.1`，配置类型为 `context-decision` 和 `code-reference`。Code 转换接受 Code Ontology Companion `0.6.0` 生成的原始模式 `1.0` 快照，以及原生 `code-ontology-reference` 版本 `1.0.0` 产物。可以按符号或路径选择所需内容；省略的数据会一并报告。

验证检查结构和配置类型规则，不证明内容的真实性、提供的修订版本与快照的对应关系或运行时行为。不会执行引用的代码，也不会获取远程模式。仅在云端运行的宿主需要另外连接本地运行时。

## 更新

```text
codex plugin marketplace upgrade ontology-contracts-preview
codex plugin add ontology-companion-contracts@ontology-contracts-preview
```

更新后，请在项目中打开新的 Codex 任务以加载更新后的技能。在该任务中再次发送上面的项目连接请求，然后再打开一个新任务，即可使用更新后的 MCP 连接。

## 帮助

[文档](docs/zh-CN/README.md) · [支持](SUPPORT.md) · [隐私](PRIVACY.md) · [安全](SECURITY.md) · [更新日志](CHANGELOG.md)

采用 [Apache-2.0](LICENSE) 许可证。
