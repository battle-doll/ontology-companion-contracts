# Ontology Companion Contracts

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [Русский](README.ru.md)

**P1a 开发预览 · [当前发布与验证状态](release-state.json)**

依据明确支持的契约检查本体交换文档，并返回确定性的结构化诊断。Ontology Companion Contracts 正在同时开发版本化契约产物和独立公开验证插件。

本地运行时离线验证交换 envelope 草案及独立的 Code/Context 配置规范。它读取明确选择的 JSON 并输出结构化结果，也已实现可在宿主中手动配置的可选 stdio 适配器。本地合成测试已通过。在 macOS 的 Codex 0.153.3 中，使用带有试用标记的产物，手动配置的本地 stdio 冒烟测试也已通过。通过公开 GitHub 插件市场安装，以及运行已安装代码的冒烟测试，也已在 macOS 上通过。托管式 ChatGPT 集成和实际人工批准仍未验证；universal Directory 是独立的提交流程，目前尚未提交。实际迁移执行和生产环境中的真实数据使用仍不受支持。

## 安装公开预览

公开预览现已可以安装。请使用支持插件的 Codex CLI 安装完整包：

```sh
codex plugin marketplace add battle-doll/ontology-companion-contracts
codex plugin add ontology-companion-contracts@ontology-contracts-preview
```

在新的 Codex 任务中调用 `$validate-ontology-contract`，请它验证已安装包的 `examples/context-decision.json`。运行代码和 schema 资源均不可缺少，因此请保留完整包，不要仅复制 `SKILL.md`。此验证无需安装 Code 或 Context 插件。

[Windows 快速开始](docs/WINDOWS_QUICKSTART.md) · [当前发布状态](release-state.json)。从 GitHub 插件市场安装与在 universal Directory 发布是不同状态。下方 CI 证据对应链接中的已完成运行；后续发布与操作系统验证结果请查阅发布状态文件。

## 运行本地预览

请在本仓库目录中使用 Python 3.11 或更新版本。预览命令无需额外 Python 包。虚拟环境和 Windows 命令见操作系统指南。

```sh
python3 --version
python3 scripts/run.py validate examples/context-decision.json
python3 scripts/check.py
```

这些命令运行本地开发代码，不会安装插件或创建托管服务。示例数据均为合成数据。

## 操作系统与验证证据

目标支持 **macOS、Windows 和 Linux**。源码可移植性、已执行的系统测试和可用的插件宿主是独立事项。下方链接的 CI 已通过 3 个系统 × 3 个 Python 版本的全部 9 个组合；宿主安装需单独验证。

| OS | 执行证据 |
| --- | --- |
| macOS | CI PASS — Python 3.11、3.12、3.13（3/3） |
| Windows | CI PASS — Python 3.11、3.12、3.13（3/3）；Windows Codex 宿主安装未测试 |
| Linux | CI PASS — Python 3.11、3.12、3.13（3/3）；Linux Codex 宿主安装未测试 |
| 插件宿主集成 | macOS Codex 0.153.3 本地 stdio 及公开 GitHub 插件市场安装已通过；Windows/Linux 宿主安装、托管式 ChatGPT 和实际人工批准未验证 |

[CI 证据：全部 9 个作业通过](https://github.com/battle-doll/ontology-companion-contracts/actions/runs/33975563666).

[macOS / Windows / Linux 指南](docs/zh-CN/PLATFORMS.md)

## 产品边界

Code、Context 和 Contracts 是独立产品。消费者无需安装 Contracts 插件即可固定版本或随包包含契约产物。这不意味着共享数据库、继承权限、自动跨插件调用或修改现有 Code 产品。

验证通过只表示实际执行的检查通过，不证明内容真实、作者身份、用户权限或运行时行为。不支持的版本保持不支持，未执行层保持 `not_checked`，不会静默获取外部 schema。

## 文档

[文档索引](docs/zh-CN/README.md) · [架构与路线图](docs/zh-CN/ARCHITECTURE_AND_ROADMAP.md) · [版本政策](docs/zh-CN/VERSION_POLICY.md) · [发布与回滚](docs/zh-CN/RELEASE_POLICY.md)

[安全](docs/zh-CN/SECURITY.md) · [隐私](docs/zh-CN/PRIVACY.md) · [支持](docs/zh-CN/SUPPORT.md) · [贡献](docs/zh-CN/CONTRIBUTING.md) · [变更记录](CHANGELOG.md)

采用 [Apache-2.0 许可证](LICENSE)。当前发布与验证状态请参阅 [release-state.json](release-state.json)。
