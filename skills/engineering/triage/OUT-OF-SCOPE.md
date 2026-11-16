# 范围外知识库（Out-of-Scope Knowledge Base）

仓库中的 `.out-of-scope/` 目录存放被拒绝的功能请求的持久记录。它有两个用途：

1. **制度记忆**：一个功能为什么被拒，这样 issue 关闭后推理过程不会丢失
2. **去重**：当匹配此前被拒请求的新 issue 进来时，skill 可以把先前的决策摆出来，而不是重新吵一遍

## 目录结构

```
.out-of-scope/
├── dark-mode.md
├── plugin-system.md
└── graphql-api.md
```

每个**概念**一个文件，而不是每个 issue 一个。请求同一件事的多个 issue 归在同一文件下。

## 文件格式

文件应当用松弛、可读的风格来写，更像一篇短设计文档而不是一条数据库记录。用段落、代码示例和例子把推理讲清楚，让第一次撞见它的人觉得有用。

```markdown
# Dark Mode

This project does not support dark mode or user-facing theming.

## Why this is out of scope

The rendering pipeline assumes a single color palette defined in
`ThemeConfig`. Supporting multiple themes would require:

- A theme context provider wrapping the entire component tree
- Per-component theme-aware style resolution
- A persistence layer for user theme preferences

This is a significant architectural change that doesn't align with the
project's focus on content authoring. Theming is a concern for downstream
consumers who embed or redistribute the output.

```ts
// The current ThemeConfig interface is not designed for runtime switching:
interface ThemeConfig {
  colors: ColorPalette; // single palette, resolved at build time
  fonts: FontStack;
}
```

## Prior requests

- #42: "Add dark mode support"
- #87: "Night theme for accessibility"
- #134: "Dark theme option"
```

### 给文件命名

给概念起一个简短、描述性的 kebab-case 名字：`dark-mode.md`、`plugin-system.md`、`graphql-api.md`。名字要有足够的辨识度，让浏览目录的人不打开文件就知道被拒的是什么。

### 撰写理由

理由应当有实质内容：不是"我们不想要"，而是为什么。好理由会引用：

- 项目范围或理念（"本项目聚焦 X；主题化是下游的关切"）
- 技术约束（"支持它需要 Y，而 Y 与我们的 Z 架构冲突"）
- 战略决策（"我们选择用 A 而不是 B，因为……"）

理由应当耐久。避免引用临时状况（"我们现在太忙了"）；那不是真正的拒绝，那是搁置。

## 什么时候查 `.out-of-scope/`

triage 期间（第 1 步：收集上下文），读 `.out-of-scope/` 里的所有文件。评估新 issue 时：

- 检查请求是否匹配一个既有的范围外概念
- 匹配按概念相似度，不按关键词："夜间主题" 匹配 `dark-mode.md`
- 如果匹配，把它摆到维护者面前："这与 `.out-of-scope/dark-mode.md` 相似。我们之前拒绝过，因为[理由]。你现在还是同样的看法吗？"

维护者可以：

- **确认**：新 issue 被加进既有文件的 "Prior requests" 列表，然后关闭
- **重新考虑**：范围外文件被删除或更新，issue 走正常 triage
- **不同意**：这些 issue 相关但不同，走正常 triage

## 什么时候写 `.out-of-scope/`

仅当某个 **enhancement**（不是 bug）被作为 `wontfix` *拒绝*时。这对 enhancement PR 与对 issue 完全一样适用：被拒的 PR 记录在这里，同一个请求就不会以新代码的面目卷土重来。

当某个东西因为**已实现**而被作为 `wontfix` 关闭时，**不要**写到这里。那是已建成的功能，不是被拒的；记录它会用假拒绝毒化去重检查。这种情况下，关闭评论指出该功能已经存在于哪里。

流程：

1. 维护者认定某个功能请求超出范围
2. 检查匹配的 `.out-of-scope/` 文件是否已存在
3. 如果存在：把新 issue 追加到 "Prior requests" 列表
4. 如果不存在：用概念名、决策、理由和第一条先前请求创建新文件
5. 在 issue 上发评论解释决策并提到 `.out-of-scope/` 文件
6. 带 `wontfix` 标签关闭 issue

## 更新或移除范围外文件

如果维护者对先前被拒的概念改了主意：

- 删除 `.out-of-scope/` 文件
- skill 不需要重开旧 issue；它们是历史记录
- 触发这次重新考虑的新 issue 走正常 triage
