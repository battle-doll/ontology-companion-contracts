# Ontology Companion Contracts — 版本政策

设计版本不是运行时或插件版本。区分 schema/profile、validator 和消费者版本，固定受支持产物及 digest。兼容性需要明确的 producer→consumer 组合和已执行 fixtures，不能仅凭版本号推断。保留历史草案并拒绝不支持的版本。

本地运行时离线验证交换 envelope 草案及独立的 Code/Context 配置规范。它读取明确选择的 JSON 并输出结构化结果，也已实现可在宿主中手动配置的可选 stdio 适配器。本地合成测试已通过。公开插件安装、实际迁移执行、真实数据使用及实际宿主集成仍不受支持或待完成。

[详细政策（英文）](../VERSION_POLICY.md) · [文档索引](README.md)
