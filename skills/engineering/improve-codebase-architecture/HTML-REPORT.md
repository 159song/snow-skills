# HTML 报告格式

架构 review 渲染为 OS 临时目录里的一个自包含 HTML 文件。Tailwind 和 Mermaid 都来自 CDN。Mermaid 处理图形状的图很可靠；手工搭的 div 和内联 SVG 负责更有编辑感的可视化（质量图、剖面图）。两者混用：不要什么都靠 Mermaid，那会开始显得千篇一律。

## 脚手架

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review for {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* small custom layer for things Tailwind doesn't cover cleanly:
         dashed seam lines, hand-drawn-feeling arrow heads, etc. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## 页头

仓库名、日期，和一个紧凑的图例：实线框 = 模块，虚线 = seam，红箭头 = 泄漏，粗黑框 = 深模块。没有介绍段落。直入候选。

## 候选卡片

图承担分量。文字稀少、平实，使用词汇表术语（来自 `/codebase-design` skill）而不加仪式。

每个候选是一个 `<article>`：

- **标题**：简短，点名深化动作（如"收拢 Order 接单管道"）。
- **徽章行**：推荐强度（`Strong` = 翠绿，`Worth exploring` = 琥珀，`Speculative` = 石板灰），外加依赖类别的标签（`in-process`、`local-substitutable`、`ports & adapters`、`mock`）。
- **文件**：等宽字体清单，`font-mono text-sm`。
- **Before / After 图**：核心。两栏并排。见下面的模式。
- **问题**：一句话。什么在疼。
- **方案**：一句话。什么改变。
- **收益**：条目，每条 ≤6 个词。例如 "测试只打一个 interface"、"定价逻辑不再泄漏"、"删掉 4 个浅包装"。
- **ADR 标注**（如适用）：琥珀色底框里的一行。

不要成段的解释。如果一张图需要一段话才能被理解，重画这张图。

## 图模式

选适合候选的模式。混着用。别让每张图长得一样。变化本身就是目的的一部分。

### Mermaid 图（依赖/调用流的主力）

当重点是"X 调 Y 调 Z，看看这团糟"时，用 Mermaid `flowchart` 或 `graph`。包在 Tailwind 样式的卡片里，免得显得空降。用 classDef 把泄漏边涂红、深模块涂深。时序图很适合"before：6 次往返；after：1 次"。

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### 手工盒子加箭头（当 Mermaid 的布局跟你作对时）

模块用带边框和标签的 `<div>`。箭头用绝对定位在相对容器上的内联 SVG `<line>` 或 `<path>`。当你想让 "after" 图看起来像一个粗边框深模块、内部灰显时用这招，因为 Mermaid 渲染不出那种分量。

### 剖面图（适合分层浅薄）

堆水平条带（`h-12 border-l-4`）展示一次调用穿过的层。Before：6 个薄层各自无所事事。After：1 个粗条带，标注合并后的职责。

### 质量图（适合"interface 和实现一样宽"）

每个模块两个矩形：一个表示 interface 表面积，一个表示实现。Before：interface 矩形几乎和实现矩形一样高（浅）。After：interface 矩形矮，实现矩形高（深）。

### 调用图坍缩

Before：函数调用树渲染成嵌套盒子。After：同一棵树坍缩成一个盒子，如今内部的调用在盒子里灰显。

## 风格指引

- 偏编辑风，不要企业仪表盘风。留白慷慨。标题可用衬线（`font-serif` 与 stone/slate 搭得好）。
- 用色克制：一个强调色（翠绿或靛蓝），加红色标泄漏、琥珀色标警告。
- 图保持约 320px 高，让 before/after 并排放得舒服、不用滚动。
- 图内模块标签用 `text-xs uppercase tracking-wider`，读起来像示意图而不是 UI。
- 脚本只有 Tailwind CDN 和 Mermaid ESM import。报告其余部分是静态的：没有应用代码，没有 Mermaid 自身渲染之外的交互。

## 顶部推荐区

一张更大的卡片。候选名、一句为什么、指向其卡片的锚链接。就这些。

## 语气

平实语言、简洁，但架构名词和动词全部直接来自 `/codebase-design` skill。简洁不是漂移的借口。

**精确使用**：module、interface、implementation、depth、deep、shallow、seam、adapter、leverage、locality。

**绝不替换为**：component、service、unit（指 module 时）· API、signature（指 interface 时）· boundary（指 seam 时）· layer、wrapper（指 module 时，当你本意就是 module）。

**符合这套风格的措辞**：

- "Order 接单模块很浅：interface 几乎匹配实现。"
- "定价跨 seam 泄漏。"
- "深化：一个 interface，一处测试。"
- "两个 adapter 证成这个 seam：生产 HTTP，测试内存。"

**收益条目**用词汇表的术语点名收益：*"locality：bug 集中在一个模块"*、*"leverage：一个 interface，N 个调用点"*、*"interface 收缩；实现吸收包装层"*。不要写 *"更好维护"* 或 *"更干净的代码"*，这些词不在词汇表里，配不上它们的位置。

不含糊、不清嗓、不写"值得注意的是…"。一句话能变条目就变条目。一条条目能删就删。一个术语不在 `/codebase-design` 词汇表里，先找一个在的，再考虑发明新的。
