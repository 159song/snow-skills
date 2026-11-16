---
name: handoff
description: 将当前对话压缩成一份交接文档，供另一个 agent 接手继续。
argument-hint: "下一个会话将用来做什么？"
disable-model-invocation: true
---

撰写一份交接文档，总结当前对话，让一个全新的 agent 能够继续这项工作。保存到用户操作系统的临时目录（`$TMPDIR`，否则用 `/tmp`；Windows 上是 `%TEMP%`）——而不是当前工作区。

在文档中加入一个「建议技能」小节，指明下一个 agent 应当对哪些 skill 调用 Skill 工具。

不要重复其他工件（spec、计划、ADR、issue、commit、diff）中已经记录的内容，改为按路径或 URL 引用它们。

遮蔽任何敏感信息，例如 API 密钥、密码或个人身份信息。

如果用户传入了参数，把它当作对下一个会话重点的描述，并据此定制文档。
