# GitHub API 403 错误解决方案

## 问题描述

在访问GitHub CVE Monitor的每日报告页面时，可能会遇到以下错误：

1. `GET https://adminlove520.github.io/github_cve_monitor/data/config.json 404 (Not Found)`
2. `GET https://api.github.com/repos/adminlove520/github_cve_monitor/contents/docs/data 403 (Forbidden)`

这些错误通常与GitHub API认证和配置文件缺失有关。

## 解决方案

### 1. 配置GitHub Personal Access Token

为了提高GitHub API的请求限制（从60次/小时提升到5000次/小时），需要配置Personal Access Token：

1. 访问GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
2. 点击"Generate new token (classic)"
3. 选择适当的权限范围（至少需要`public_repo`权限）
4. 复制生成的token

### 2. 在GitHub仓库中添加Secret

1. 进入仓库 > Settings > Secrets and variables > Actions
2. 点击"New repository secret"
3. Name: `GH_TOKEN`
4. Secret: 你的GitHub个人访问令牌

### 3. 本地运行时设置环境变量

如果在本地运行，设置环境变量：
```bash
# Linux/Mac
export GITHUB_TOKEN=your_token_here

# Windows
set GITHUB_TOKEN=your_token_here
```

### 4. 配置文件支持

程序支持从以下位置的配置文件读取token（优先级从高到低）：
1. 环境变量 `GITHUB_TOKEN`
2. `docs/data/config.json`
3. `docs/config.json`
4. `config.json`

配置文件格式示例：
```json
{
  "github_token": "your_token_here",
  "api_base_url": "https://api.github.com",
  "repository": "adminlove520/github_cve_monitor",
  "generated_at": "2025-09-24T00:00:00Z"
}
```

## 备用加载机制

当GitHub API调用失败时（如403错误），前端代码会自动切换到备用加载机制，通过解析本地目录结构来显示报告列表。

## 验证修复

1. 确保GitHub Actions工作流已成功运行
2. 检查`docs/data/config.json`文件是否存在
3. 访问每日报告页面，确认错误已解决

## 常见问题

### 为什么会出现403错误？

1. **未配置Token**: 使用未认证的API调用，请求限制较低
2. **Token权限不足**: Token缺少必要的权限
3. **Token过期**: Personal Access Token已过期
4. **速率限制**: 超过了API请求限制

### 为什么会出现404错误？

1. **配置文件缺失**: `config.json`文件未生成或未正确部署
2. **路径错误**: 文件路径配置不正确
3. **部署问题**: GitHub Pages未正确部署文件

## 进一步帮助

如果问题仍然存在，请检查：
1. GitHub Actions工作流执行日志
2. GitHub Pages部署状态
3. 网络连接和防火墙设置