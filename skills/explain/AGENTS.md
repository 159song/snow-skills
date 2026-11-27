# explain

本包负责单次按需讲解。入口和四种交付形式的选择规则集中在 `SKILL.md`。

Claude Code 通过插件清单加载本包。用户运行 `/snow-skills:explain 为什么缓存会击穿？` 后，先通过 `AskUserQuestion` 取得本次单选结果，再结合主题与当前对话讲解。保持 `disable-model-invocation: true`，让用户控制启用时机。

文本和 Mermaid 可以直接生成。交互页面和动画使用当前环境可用的工具。变更后在插件根目录运行 `claude plugin validate .`，确认清单列出 `snow-skills:explain`。本地启动 `claude --plugin-dir .` 后分别运行带主题与不带主题的命令，检查首步均为四级单选，提交前不生成产物。

Codex 通过插件发现同一份 `SKILL.md`，在 `agents/openai.yaml` 中设置仅显式调用。维护四级菜单时同时验证 Claude Code 和 Codex 的输入通道。按根目录 README 的归档步骤安装本地已提交版本，重启后输入 `$` 选择 explain。
