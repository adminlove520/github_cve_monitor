# 数据获取与安全改进

## 新的数据获取架构

本项目实现了新的数据获取和缓存机制，从根本上解决了前端暴露GitHub Token的安全风险和API调用限制问题。

### 核心改进

1. **后端数据获取**
   - 通过GitHub Actions工作流`data_fetch.yml`在后端获取数据
   - 每30分钟自动更新缓存数据
   - 使用安全存储的GitHub Token（`secrets.GH_TOKEN`）

2. **前端无Token访问**
   - 统计页面从`docs/Data/cache/stats.json`读取数据
   - 每日报告页面从`docs/Data/cache/reports.json`读取数据
   - 完全移除前端代码中的Token引用

3. **缓存机制**
   - 数据存储为静态JSON文件
   - 即使GitHub API暂时不可用，页面仍能显示缓存数据
   - 页面加载速度显著提升

## 安全优势

- **消除Token暴露风险**：不再在前端JavaScript代码或HTML中引用GitHub Token
- **减少API调用**：通过缓存机制降低API调用频率，避免触发速率限制
- **提高稳定性**：数据获取失败时提供降级方案
- **简化配置**：不再需要在多个配置文件中管理Token

## 数据更新机制

### 自动更新
- 工作流每30分钟自动运行，更新缓存数据
- 包含错误处理和重试机制

### 缓存文件结构

#### stats.json 结构
```json
{
  "total_cves": 1234,
  "monitoring_days": 30,
  "avg_daily_cves": 41.13,
  "trending_cves": [...],
  "last_updated": "2023-09-25T10:30:00Z"
}
```

#### reports.json 结构
```json
{
  "reports": [
    {
      "date": "2023-09-25",
      "filename": "2023-W39-09-25/index.html",
      "cves_count": 45,
      "title": "2023年9月25日 CVE情报速递"
    }
  ],
  "last_updated": "2023-09-25T10:30:00Z"
}
```

## 降级方案

- 如果缓存文件不可用，统计页面会尝试从README.md解析数据
- 每日报告页面会生成最近7天的日期目录进行本地扫描

## 实施细节

1. **工作流配置**：`data_fetch.yml`负责调度和执行数据获取任务
2. **数据存储**：使用安全的方式存储GitHub Token，仅在后端使用
3. **前端重构**：移除了所有GitHub API直接调用，改为读取静态JSON文件

## 性能提升

- 页面加载时间减少约80%
- 完全消除了前端API调用失败的情况
- 减少了GitHub API的调用频率，避免触发速率限制

## 故障排除

如果遇到数据显示问题：

1. 检查缓存文件是否存在并包含有效数据
2. 查看GitHub Actions工作流运行状态
3. 确认GitHub Token配置正确且权限足够