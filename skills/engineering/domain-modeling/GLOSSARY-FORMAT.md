# GLOSSARY.md 格式

## 结构

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## 规则

- **要有主见。** 同一概念存在多个词时，挑最好的那个，其余列进 `_Avoid_`。
- **定义要紧。** 最多一两句。定义它*是*什么，不是它*做*什么。
- **只收录本项目上下文特有的术语。** 一般编程概念（超时、错误类型、工具模式）不属于这里，哪怕项目大量使用它们。加术语前问自己：这是本上下文独有的概念，还是一般编程概念？只有前者属于这里。
- 当自然聚簇出现时，**把术语分组到子标题下**。如果所有术语同属一个内聚区域，平铺清单也可以。

## 单上下文与多上下文仓库

**单上下文（大多数仓库）：** 仓库根一个 `GLOSSARY.md`。

**多上下文：** 仓库根的 `GLOSSARY-MAP.md` 列出各上下文、它们住哪、彼此什么关系：

```md
# Glossary Map

## Contexts

- [Ordering](./src/ordering/GLOSSARY.md): receives and tracks customer orders
- [Billing](./src/billing/GLOSSARY.md): generates invoices and processes payments
- [Fulfillment](./src/fulfillment/GLOSSARY.md): manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

skill 推断适用哪种结构：

- 存在 `GLOSSARY-MAP.md` 就读它找上下文
- 只存在根 `GLOSSARY.md` 就是单上下文
- 都不存在就在第一个术语敲定时惰性创建根 `GLOSSARY.md`

存在多个上下文时，推断当前话题与哪个相关。不清楚就问。
