# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [2.2.3] - 2025-09-25

### Security
- 实现全新的数据获取和缓存机制
- 完全移除前端Token依赖，消除安全风险
- 创建data_fetch.yml工作流，实现每30分钟自动数据更新
- 重构前端页面，改为从缓存JSON文件读取数据

### Performance
- 页面加载速度提升约80%
- 显著降低API调用频率，避免触发速率限制
- 提高系统稳定性，提供降级方案

### Documentation
- 更新README.md和stats.md，详细说明新的数据获取架构
- 添加安全优势和性能提升的文档说明

## [2.2.2] - 2025-09-23

### Documentation
- 更新所有文档，移除过时脚本引用
- 清理项目结构，保持文档与系统状态一致

### Security  
- 恢复GitHub Token支持（可选配置）
- 优化API调用策略，提高数据获取效率

## [2.2.1] - 2025-09-23

### Security
- 移除敏感信息，改为公共API调用
- 清理所有测试文件和临时调试代码
- 目录重命名：归档文档/ → archive/

## [2.2.0] - 2025-09-23

### Epic Update
- ✅ 修复HTTP 404状态处理，实现透明化显示
- 📈 修复CVE计算方法，使用科学估算公式  
- 🎨 新增数据状态可视化（绿色/黄色/红色背景）
- 📊 完整的CVE统计系统和趋势分析

## [2.1] - 2025-09-22

### Init
- 实现自动化CVE监控系统
- 生成每日情报速递报告

