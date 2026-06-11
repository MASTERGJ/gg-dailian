# Game UI AI Pipeline — GitHub Ecosystem & Architecture Map

分析日期: 2026-06-02

## 核心模式：契约层 (Contract Layer)

AI 和游戏引擎之间**不能直连**，必须有结构化中间层解耦：

```
截图 → AI多模态(视觉分析) → 中间描述JSON → 引擎侧脚本 → Prefab/Scene
```

这个模式在 Unity、Cocos、Godot 中完全一致，差异仅在脚本语言（C# / TS / GDScript）和引擎 API。

## 两条已证实的管线

### 管线 A：截图→预制体（文章1）
- 来源：《我用 Codex 将一张游戏截图，直接搓成 Cocos 预制体》
- 架构：AI(json_agent_mode) → 中间描述 JSON → AutoBuildUI.ts → Cocos Prefab
- JSON 字段：节点层级、位置/大小、颜色/图片资源名、文本内容
- 桥接层：TypeScript 脚本递归遍历 JSON，调用 Cocos API 创建 Node/Prefab

### 管线 B：素材图集生成（文章2）
- 来源：《Codex+Image2生成爆款小游戏UI素材！》
- 架构：风格描述 → AI 多轮图像生成（skill编排） → PNG 图集 + 坐标 JSON
- 关键：Context-passing 保持风格一致性（每轮产出注入下一轮 context）
- 产物：PNG atlas + 坐标 JSON → 可被管线 A 引用

### 串联可行性
管线 B 的素材图集输出 → 管线 A 的 JSON 中引用素材名和坐标 → 完整全链路

## GitHub 生态全景 (2026-06-02)

### Unity 生态

| 项目 | Stars | 定位 |
|------|-------|------|
| phucnguyen752/unity-ui-mcp | 1★ | **精准匹配**：MCP Server 在 Unity Editor 内，接收 JSON → 构建 Prefab。截图→get_editor_config→分析→写JSON→build_ui_from_json |
| Glade-tool/glade-mcp | 149★ | 跨引擎 MCP（Unity + Godot），235+ 工具，无 UI 生成专项 |
| Signal-Loop/UnityCodeMCPServer | 14★ | 通用 Unity MCP，AI 操作编辑器 |

unity-ui-mcp 关键设计：
- MCP Server 内嵌 Unity Editor（SSE transport, port 7890）
- JSON Schema：type/name/anchor/size/position/color/spritePath/ppum/children/text/fontSize/layout/spacing/padding
- 配套 AI_SKILL.md 定义强制工作流：get_editor_config → 分析截图计算百分比 → 写 JSON → build_ui_from_json
- 支持圆角（9-sliced sprite + PPUM）、LayoutGroup、Rounded corners
- 仅 1 star，2026-05 才上线，非常早期

### Godot 生态

| 项目 | Stars | 定位 |
|------|-------|------|
| Coding-Solo/godot-mcp | 3,973★ | MCP server for Godot |
| hi-godot/godot-ai | 448★ | Production-grade MCP |
| youichi-uda/godot-mcp-pro | 403★ | 162 tools for Godot 4 |
| yurineko73/Godot-MCP-Native | 211★ | 154 tools，中文作者，原生 Godot 实现 |
| Glade-tool/glade-mcp | 149★ | 跨引擎（Unity + Godot） |

Godot MCP 生态最丰富，但**没有任何项目做 screenshot-to-UI 专项**。

### Cocos 生态

| 项目 | Stars | 定位 |
|------|-------|------|
| WuYunHo/figma-to-cocos-prefab | 1★ | Figma 设计 → Cocos Prefab |
| 其他 Cocos AI/MCP 项目 | — | 完全空白 |

文章作者的 AutoBuildUI.ts 是目前唯一已知的 Cocos screenshot→prefab 实现。

### 通用截图→代码

| 项目 | Stars | 定位 |
|------|-------|------|
| abi/screenshot-to-code | 72,752★ | 截图 → HTML/Tailwind/React/Vue（通用 Web） |
| emilwallner/Screenshot-to-code | 16,478★ | 神经网络方案（静态网站） |

通用方案不针对游戏引擎。

## 三种可行路线

### 路线 1：Unity 最短路径
```
截图 → MCP客户端(Hermes等) → unity-ui-mcp → Unity Prefab
```
- 优势：直接可用，端到端已实现
- 风险：项目仅 1★，质量未验证
- 适用：快速原型验证

### 路线 2：Cocos 自主路线
```
截图 → AI(多模态) → 自定义JSON → AutoBuildUI.ts → Cocos Prefab
素材需求 → AI图像生成 → 图集 + 坐标JSON ↗
```
- 优势：文章作者已有实现基础
- 缺口：需开源化/Skill化，JSON Schema 标准化
- 适用：Cocos 项目

### 路线 3：跨引擎通用（Glade 扩展）
```
截图 → MCP客户端 → Glade(Unity/Godot) → 自定义UI生成工具
```
- 优势：一个 MCP 覆盖多引擎
- 缺口：Glade 无 UI 生成专项，需贡献 PR 或包装 Skill
- 适用：长期通用方案

## 关键洞见

1. **专用 AI 游戏 UI 生成器在 GitHub 上完全空白** — 这是蓝海
2. **Godot MCP 生态最成熟但不做 UI 生成**，工具集中在场景/脚本/调试
3. **Cocos AI 工具生态几乎真空**，是最大机会（也是最大阻力）
4. **Screenshot→HTML 已有 72K star 项目**，说明视觉→结构转换的 AI 能力已成熟
5. **MCP 协议成为游戏引擎 AI 接入的事实标准**（Unity MCP、Godot MCP 均用此）
6. **context-passing 多轮图像生成**是保持图集风格一致性的关键技巧
