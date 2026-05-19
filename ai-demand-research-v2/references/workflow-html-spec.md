# 工作流HTML可视化规范

## 设计目标

提供一个直观、实时、可交互的工作流展示界面，让用户能够：
1. 一眼看清当前项目进度
2. 点击任意步骤查看详细输入/代码/输出
3. 识别哪些步骤是重新生成的（回滚标记）
4. 快速导航到相关文件

## 视觉设计

### 色彩系统

```css
:root {
  --bg-primary: #0a0a0f;
  --bg-secondary: #12121a;
  --bg-card: #1a1a2e;
  --border: #2a2a3e;
  --text-primary: #e0e0e0;
  --text-secondary: #8888a0;
  --accent: #6366f1;
  --accent-glow: rgba(99, 102, 241, 0.3);
  --success: #10b981;
  --warning: #f59e0b;
  --error: #ef4444;
  --info: #3b82f6;
  --archived: #6b7280;
}
```

### 节点状态样式

| 状态 | 颜色 | 图标 | 说明 |
|------|------|------|------|
| 待执行 | `--text-secondary` | ○ | 灰色空心圆 |
| 执行中 | `--info` | ⟳ | 蓝色旋转动画 |
| 已完成 | `--success` | ✓ | 绿色实心圆 |
| 已归档 | `--archived` | ⌘ | 灰色带删除线 |
| 重新生成 | `--warning` | ↻ | 橙色闪烁标记 |

## 布局结构

### 顶部导航栏
- 项目名称
- 当前阶段进度条
- 最后更新时间
- 刷新按钮

### 主工作流图
- 垂直时间线布局
- 每个阶段一个卡片组
- 阶段内步骤水平排列
- 连接线带流动动画

### 详情面板（点击展开）
- 步骤基本信息
- 输入文件列表（可点击打开）
- 代码预览（语法高亮）
- 输出结果摘要
- manifest.json 完整内容

## 交互设计

### 点击节点
1. 节点高亮
2. 右侧/下方展开详情面板
3. 显示该步骤的 input/code/output 清单
4. 提供"查看完整代码"、"下载输出"按钮

### 悬停节点
- 显示步骤名称和状态
- 显示完成时间
- 显示输出文件数量

### 重新生成标记
- 被重新生成的步骤显示橙色边框
- 鼠标悬停显示"v2 重新生成于 2026-05-14 14:20"
- 点击可查看历史版本对比

## 技术实现

### 文件结构
```
workflow.html
├── 内嵌 CSS（Tailwind-like 工具类）
├── 内嵌 JavaScript（无外部依赖）
└── 数据注入点（由脚本自动更新）
```

### 数据格式

workflow.html 内嵌一个 `WORKFLOW_DATA` 对象：

```javascript
const WORKFLOW_DATA = {
  project: {
    name: "parenting-sleep-2026-05-14",
    topic: "育儿睡眠场景调研",
    created: "2026-05-14T10:00:00+08:00",
    updated: "2026-05-14T16:30:00+08:00"
  },
  phases: [
    {
      id: "phase1",
      name: "场景发现",
      status: "completed",
      steps: [
        {
          id: "phase1-step1",
          name: "数据加载与清洗",
          status: "completed",
          version: 1,
          timestamp: "2026-05-14T10:30:00+08:00",
          inputFiles: ["01-raw-data/input/data.xlsx"],
          codeFile: "02-cleaned/code/data_cleaning.py",
          outputFiles: ["02-cleaned/output/cleaned_data.parquet"],
          parameters: {"min_interaction": 100},
          notes: ""
        }
      ]
    }
  ]
};
```

### 自动更新机制

每次完成一个步骤后，执行 `scripts/update_workflow.py`：
1. 读取项目目录结构
2. 收集所有 manifest.json
3. 生成最新的 WORKFLOW_DATA
4. 注入到 workflow.html 模板
5. 保存到 `00-meta/workflow.html`

## 响应式设计

- 桌面端：左右分栏，左侧工作流图，右侧详情面板
- 平板端：上下分栏
- 手机端：全屏工作流图，点击后全屏详情

## 动画效果

1. **进度流动**：已完成步骤之间的连线有流动光效
2. **状态切换**：步骤状态变化时有平滑过渡动画
3. **详情展开**：面板展开/收起有 slide 动画
4. **重新生成标记**：橙色边框有呼吸灯效果
