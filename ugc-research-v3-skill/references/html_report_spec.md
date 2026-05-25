# HTML交互报告规范

## 1. 技术实现规范

### 1.1 数据嵌入
- 必须用Python `json.dumps()` 将数据嵌入HTML
- 禁止子Agent直接写JSON到HTML
- 数据格式：
```python
import json

ugc_data = [...]  # Python列表/字典
html = f"""
<script>
var ugcData = {json.dumps(ugc_data, ensure_ascii=False)};
</script>
"""
```

### 1.2 JavaScript规范
- 使用传统函数：`function(){}`
- **禁止箭头函数**：`()=>{}` 在某些环境下不兼容
- 函数声明：
```javascript
// ✅ 正确
function showPanel(id) {
    document.querySelectorAll('.panel').forEach(function(p) {
        p.classList.remove('active');
    });
}

// ❌ 错误
const showPanel = (id) => {
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
};
```

### 1.3 引号处理
- 必须检查单引号嵌套
- onclick内部引号冲突常见：
```javascript
// ❌ 错误：单引号冲突
<button onclick='showPanel('creator')'>创作者</button>

// ✅ 正确：使用转义或双引号
<button onclick="showPanel('creator')">创作者</button>
<button onclick='showPanel(\"creator\")'>创作者</button>
```

### 1.4 语法验证
- 生成后必须用 `node --check` 验证JS语法
```bash
node --check /path/to/report.html
```
- 验证不通过必须修复后再交付

### 1.5 字段名一致性
- 多批次并行时必须强制统一字段名
- 常见不一致：
  - `signal_types` vs `signals`
  - `note_id` vs `id`
  - `platform` vs `source`
- 在脚本中统一映射：
```python
# 统一字段名
for item in batch_data:
    item['signal_types'] = item.get('signal_types') or item.get('signals', [])
```

## 2. 内容规范

### 2.1 逻辑链路
每个产品建议必须包含完整链路：
1. **UGC原文**：15-20条真实UGC
2. **分类依据**：为什么归到这一类
3. **分布统计**：该类别占比、互动量
4. **交互量分析**：点赞/评论/转发数据
5. **产品建议推导**：基于以上数据推导建议

### 2.2 数据可视化
- 使用纯CSS实现，禁止外部CDN
- 常用图表：
```html
<!-- 条形图 -->
<div style="background:#e2e8f0;height:20px;border-radius:10px;overflow:hidden">
  <div style="background:linear-gradient(90deg,#4f46e5,#7c3aed);height:100%;width:45%;border-radius:10px"></div>
</div>

<!-- 饼图用CSS conic-gradient -->
<div style="width:200px;height:200px;border-radius:50%;background:conic-gradient(#4f46e5 0% 45%, #10b981 45% 70%, #f59e0b 70% 100%)"></div>
```

### 2.3 交互功能
- 标签页切换
- 筛选（按平台/主题/情绪）
- 排序（按互动量/时间）
- 搜索

## 3. 验证清单

交付前必须完成：
- [ ] HTML文件可双击打开正常显示
- [ ] JS语法通过 `node --check` 验证
- [ ] 数据字段名跨批次一致
- [ ] 统计数据与JSON源文件一致
- [ ] 每个结论有≥15条UGC原文支撑
- [ ] 无外部CDN依赖
- [ ] 无箭头函数
- [ ] 无单引号嵌套冲突
