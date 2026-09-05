# Ontology Companion Contracts — 文档

[English](../README.md) | [한국어](../ko/README.md) | [日本語](../ja/README.md) | [简体中文](README.md) | [Русский](../ru/README.md)

请先阅读本地预览与限制。Context 的编号设计文档描述长期路线图，不扩展当前运行时支持范围。

- [运行本地预览](../../README.zh-CN.md)
- [macOS / Windows / Linux 指南](PLATFORMS.md)
- [架构与路线图](ARCHITECTURE_AND_ROADMAP.md)
- [版本政策](VERSION_POLICY.md)
- [发布与回滚](RELEASE_POLICY.md)
- [安全](SECURITY.md)
- [隐私](PRIVACY.md)
- [支持](SUPPORT.md)
- [贡献](CONTRIBUTING.md)
- [变更记录](../../CHANGELOG.md)
- [Apache-2.0](../../LICENSE)

本地运行时离线验证交换 envelope 草案及独立的 Code/Context 配置规范。它读取明确选择的 JSON 并输出结构化结果，也已实现可在宿主中手动配置的可选 stdio 适配器。本地合成测试已通过。公开插件安装、实际迁移执行、真实数据使用及实际宿主集成仍不受支持或待完成。

Code、Context 和 Contracts 是独立产品。消费者无需安装 Contracts 插件即可固定版本或随包包含契约产物。这不意味着共享数据库、继承权限、自动跨插件调用或修改现有 Code 产品。
