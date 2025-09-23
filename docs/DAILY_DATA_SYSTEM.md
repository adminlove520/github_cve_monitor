# GitHub CVE Monitor 每日数据生成系统

## 📊 概述

这个系统解决了您提到的两个关键问题：

1. **增长率负值问题** - 修复了stats.html中增长率计算的逻辑错误
2. **缺失JSON文件问题** - 自动生成完整的每日数据文件，填补缺失日期

## 🚀 核心功能

### 1. 增强版数据生成器 (`enhanced_daily_data_generator.py`)

```bash
# 基本使用
python enhanced_daily_data_generator.py --readme ../docs/README.md --output ../docs/Data/daily

# 完整功能（推荐）
python enhanced_daily_data_generator.py \
  --readme ../docs/README.md \
  --output ../docs/Data/daily \
  --fill-gaps \
  --verbose
```

**主要特性：**
- 从README.md解析CVE数据
- 按日期自动分组
- 填补缺失日期（生成空JSON文件）
- 计算正确的增长率统计
- 生成详细的汇总报告

### 2. 快速修复工具 (`fix_growth_rate.py`)

```bash
# 修复现有数据问题
python fix_growth_rate.py \
  --daily-dir ../docs/Data/daily \
  --create-missing \
  --verbose
```

**修复内容：**
- 分析现有文件
- 创建缺失日期的空文件
- 重新计算正确的增长率
- 更新daily_summary.json

### 3. 自动化工作流 (`.github/workflows/generate-daily-data.yml`)

```yaml
# 触发条件：
- 每天早上8点自动运行
- README.md更新时触发
- 手动触发（支持参数）
```

## 🔧 问题解决

### 原问题1：增长率负值
**原因：** stats.html中的增长率计算使用了错误的数组索引
```javascript
// 错误的代码
const prevDay = trendData[index + 1];

// 修复后的代码  
const prevDay = trendData[index - 1];
```

**结果：** 现在增长率正确显示，正值表示增长，负值表示下降

### 原问题2：缺失JSON文件
**原因：** 只有有CVE数据的日期才会生成JSON文件
**解决：** 
- 自动填补所有缺失日期
- 生成空的JSON文件（count: 0）
- 确保完整的时间序列

## 📈 数据统计改进

### 新增统计指标
```json
{
  "statistics": {
    "avg_daily_cves": 4.51,
    "max_daily_cves": 811,
    "min_daily_cves": 0,
    "empty_days": 2900,
    "active_days": 3052
  },
  "growth_analysis": [
    {
      "date": "2025-09-17",
      "daily_count": 14,
      "cumulative_total": 26815,
      "growth_rate": 7.7
    }
  ],
  "recent_7_days": [...],
  "recent_30_days": [...]
}
```

### 增长率计算逻辑
```python
if i > 0:
    prev_count = sorted_files[i-1]['count']
    if prev_count > 0:
        growth_rate = ((file_data['count'] - prev_count) / prev_count) * 100
    else:
        growth_rate = 0 if file_data['count'] == 0 else 100
else:
    growth_rate = 0
```

## 🎯 使用建议

### 日常维护
1. **自动运行** - GitHub Actions会每天自动更新数据
2. **手动更新** - 当README.md有大量更新时手动触发
3. **数据验证** - 检查stats.html确认增长率显示正常

### 开发调试
```bash
# 只生成特定日期范围的数据
python enhanced_daily_data_generator.py \
  --start-date 2025-09-01 \
  --end-date 2025-09-23 \
  --fill-gaps

# 快速修复现有问题
python fix_growth_rate.py --create-missing --verbose
```

## 📊 当前数据状态

运行修复后的统计：
- **总文件数**: 5,952 个JSON文件
- **总CVE数量**: 26,827 个
- **日期范围**: 2009-06-08 到 2025-09-23
- **活跃天数**: 3,052 天
- **空白天数**: 2,900 天
- **平均每日CVE**: 4.51 个

## 🔍 验证方法

### 1. 检查stats.html
访问stats.html页面，确认：
- 增长率不再出现不合理的负值
- 每日趋势表格正常显示
- 不再有"未找到XXX.json"的错误

### 2. 验证JSON文件
```bash
# 检查特定日期的文件
ls docs/Data/daily/2025-09-17.json

# 验证文件内容
cat docs/Data/daily/2025-09-17.json | jq '.count'
```

### 3. 监控增长率
查看recent_7_days中的growth_rate字段，确认：
- 有新增CVE的日期显示正增长率
- 无CVE的日期显示0或合理的负增长率

## 🚦 故障排除

### 常见问题
1. **权限错误** - 确保脚本有写入docs/Data/daily目录的权限
2. **日期格式** - README.md中的日期必须是标准格式
3. **编码问题** - 确保所有文件使用UTF-8编码

### 调试命令
```bash
# 详细输出模式
python enhanced_daily_data_generator.py --verbose

# 检查现有文件状态
python fix_growth_rate.py --daily-dir ../docs/Data/daily --verbose
```

## 📝 总结

通过这套解决方案：

✅ **解决了增长率负值问题** - 修复JavaScript计算逻辑
✅ **解决了缺失JSON文件问题** - 自动生成完整数据集
✅ **提供了自动化工具** - GitHub Actions定时处理
✅ **增强了数据质量** - 详细统计和验证机制

现在您的CVE监控系统应该能够：
- 正确显示每日增长趋势
- 消除"未找到文件"的错误
- 提供准确的统计数据
- 自动维护数据完整性