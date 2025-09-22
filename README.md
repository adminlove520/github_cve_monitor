
# Github CVE 监控 ![版本](https://img.shields.io/badge/version-2.1-blue.svg)

> 使用 Github Actions 自动监控 Github 上的 CVE 信息

[![github-cve-monitor](https://github.com/adminlove520/github_cve_monitor/actions/workflows/run.yml/badge.svg)](https://github.com/adminlove520/github_cve_monitor/actions/workflows/run.yml)[![pages-build-deployment](https://github.com/adminlove520/github_cve_monitor/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/adminlove520/github_cve_monitor/actions/workflows/pages/pages-build-deployment)

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/adminlove520/github_cve_monitor/blob/main/LICENSE)

## 文档 📖 

访问 [cve-monitor](https://adminlove520.github.io/github_cve_monitor/) 查看演示。 

### 命令行使用  💻

执行  `python main.py` 

### 使用 Github-Action ⚙️

查看 [run.yml](https://github.com/adminlove520/github_cve_monitor/blob/main/.github/workflows/run.yml) 文件

## 安装 💿

### 依赖项

```
pip install -r requirements.txt
```

## ⚠️ 限制 

Github API 每页限制返回 100 条记录 

### GitHub API 限制解决方案

为了解决GitHub API的请求限制问题，本项目现已支持使用GitHub Token进行认证，这可以将API请求限制从每小时60次提升到每小时5000次。

#### 配置GitHub Token

1. **本地运行**：
   - 创建一个GitHub个人访问令牌 (Personal Access Token)
   - 设置环境变量 `GITHUB_TOKEN` 为你的令牌值
   ```bash
   export GITHUB_TOKEN=your_token_here  # Linux/Mac
   set GITHUB_TOKEN=your_token_here     # Windows
   ```

2. **GitHub Actions**：
   - 在GitHub仓库设置中添加名为 `GH_TOKEN` 的Secret
   - 工作流程已配置为自动使用此令牌

## 路线图

| 状态 | 任务  | 版本 |
|---|---|---|
| 🛠 | 添加描述（译文）功能【】 | 2.1 |
| 🛠 | 添加统计功能 | 2.1 |
| ✅ | ~~修复CVE字段的bug~~ | 2.0c | 
| ✅ | ~~按CVE排序~~ | 2.0b |  
| ✅ | ~~提取CVE~~ | 2.0 |  
| ✅ | ~~增加API调用的响应数量（现在是30）~~ | 2.0 |
| ✅ | 绕过API限制 | 3.0 | 

#### 图例

| 状态 | 描述 |
|---|---|
| ✅ | 已完成 |
| 🛠 | 进行中 |
| 🟢 | 待办 | 
| 🟡 | 可能有一天会做 |
| 🔴 | 永不  |
