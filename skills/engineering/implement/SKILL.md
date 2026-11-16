---
name: implement
description: "基于 spec 或一组 ticket 实现一件工作。"
disable-model-invocation: true
---

实现用户在 spec 或 ticket 中描述的工作。

如果用户传入了 ticket 引用，从 issue tracker 取回它并在开始前陈述其标题。如果引用有歧义，先问。

在可能的情况下、在事先约定的 seam 处，调用 Skill 工具运行 "tdd"。

定期跑类型检查，定期跑单个测试文件，最后跑一次完整测试套件。

完成后，调用 Skill 工具运行 "code-review" 来 review 这项工作。

把你的工作提交到当前分支。
