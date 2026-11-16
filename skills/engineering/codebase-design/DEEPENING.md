# 深化（Deepening）

如何在给定依赖的情况下安全地深化一组浅模块。假设你已掌握 [SKILL.md](SKILL.md) 中的词汇：**module（模块）**、**interface（接口）**、**seam（缝）**、**adapter（适配器）**。

## 依赖类别

评估深化候选时，先给它的依赖分类。类别决定深化后的模块如何跨 seam 测试。

### 1. 进程内（In-process）

纯计算、内存状态、无 I/O。永远可深化：合并模块，直接通过新 interface 测试。不需要 adapter。

### 2. 本地可替换（Local-substitutable）

有本地测试替身的依赖（用 PGLite 替 Postgres、内存文件系统）。只要替身存在就可深化。深化后的模块在测试套件中跑着替身来测试。seam 是内部的；模块对外 interface 上没有 port。

### 3. 远程但自有（Ports & Adapters）

跨网络边界的你自己的服务（微服务、内部 API）。在 seam 处定义一个 **port（端口）**（interface）。深模块持有逻辑；传输作为 **adapter** 注入。测试用内存 adapter。生产用 HTTP/gRPC/队列 adapter。

建议的形状：*"在 seam 处定义一个 port，为生产实现一个 HTTP adapter、为测试实现一个内存 adapter，这样尽管跨网络部署，逻辑仍坐在一个深模块里。"*

### 4. 真外部（Mock）

你不控制的第三方服务（Stripe、Twilio 等）。深化后的模块把外部依赖当作注入的 port；测试提供 mock adapter。

## seam 纪律

- **一个 adapter 意味着假想的 seam。两个 adapter 才是真 seam。** 除非至少有两个 adapter 说得通（通常是生产 + 测试），否则不要引入 port。单 adapter 的 seam 只是间接层。
- **内部 seam 与外部 seam。** 深模块可以有内部 seam（对其实现私有、由它自己的测试使用），以及 interface 处的外部 seam。不要仅因为测试用了内部 seam 就把它们暴露到 interface 上。

## 测试策略：替换，不要叠层

- 浅模块上的旧单元测试在深化模块 interface 处的测试存在后就是废物；删掉。
- 在深化模块的 interface 处写新测试。**interface 就是测试面**。
- 测试断言通过 interface 可观察的结果，而非内部状态。
- 测试应能在内部重构后存活，因为它们描述行为而非实现。如果实现一变测试就得变，它测过了 interface。
