---
name: release-it
description: "应用 Michael Nygard《发布！》（Release It!）的生产可靠性规则：设计失败处理、超时、重试、熔断器、舱壁、可观测性或部署行为时使用。触发词：熔断器、舱壁、超时、重试、稳定模式、生产故障。"
license: MIT
---

# 《发布！》（Release It!，Michael T. Nygard）规则集

来自 [ciembor/agent-rules-books](https://github.com/ciembor/agent-rules-books)（MIT，冻结副本）。三档规则按需加载：

1. 默认先读并应用 [mini 版](release-it.mini.md)——包含本书的核心决策规则，多数任务足够。
2. 上下文预算紧张时改用 [nano 版](release-it.nano.md)。
3. 仅当 mini 规则不足以支撑当前权衡时，才把 [full 版](release-it.md)当深入参考查阅。
