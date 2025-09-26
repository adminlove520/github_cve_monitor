# Github CVE 监控 ![版本](https://img.shields.io/badge/version-3.0-blue.svg)

> 使用 Github Actions 自动监控 Github 上的 CVE 信息


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

### 数据获取与安全改进

为了解决GitHub API的请求限制问题并提高安全性，本项目实现了新的数据获取和缓存机制。

#### 新的数据获取方式

我们引入了一个专门的工作流`data_fetch.yml`，该工作流：
- 每30分钟自动运行一次
- 优先使用`secrets.GH_TOKEN`，其次使用`GITHUB_TOKEN`进行认证
- 获取统计数据和每日报告数据
- 将数据缓存为JSON文件存储在仓库中

#### 安全改进

- **移除前端token依赖**：统计数据和每日报告页面现在直接从缓存的JSON文件读取数据，不再在前端代码中使用或暴露GitHub Token
- **降低API调用频率**：通过缓存机制显著减少了API调用次数，避免触发速率限制
- **提高页面加载速度**：从本地JSON文件读取数据比实时调用API更快
- **增强稳定性**：即使GitHub API暂时不可用，页面仍能显示缓存的数据

#### 缓存文件

数据存储在以下位置：
- `docs/Data/cache/stats.json` - 统计数据缓存
- `docs/Data/cache/reports.json` - 每日报告数据缓存

#### 配置GitHub Token（后端使用）

要配置用于后端数据获取的GitHub Token：

1. **GitHub Actions**：
   - 在GitHub仓库设置中添加名为 `GH_TOKEN` 的Secret
     - 进入仓库 > Settings > Secrets and variables > Actions
     - 点击"New repository secret"
     - Name: `GH_TOKEN`
     - Secret: 你的GitHub个人访问令牌
   - 工作流程已配置为自动使用此令牌

2. **本地运行**（仅用于测试）：
   - 设置环境变量 `GITHUB_TOKEN` 为你的令牌值
   ```bash
   export GITHUB_TOKEN=your_token_here  # Linux/Mac
   set GITHUB_TOKEN=your_token_here     # Windows
   ```

#### Token权限要求

GitHub Token需要以下权限：
- `public_repo` - 访问公共仓库信息
- `repo` (可选) - 如果需要访问私有仓库

## 路线图

| 状态 | 任务  | 版本 |
|---|---|---|
| 🛠 | 修复增长率显示baseline问题&本周热点CVE时间维度显示不正确（滞后性bug）&修正API错误: GitHub API 调用失败: 403以及敏感信息特殊过滤 | 3.0 |
| 🛠 | 修复每日 情报速递 报告的当日获取逻辑问题&以及原始条数&判断依据由created_at改为updated_at（*有待商榷*） | 3.0 |
| 🛠 | 解决UTC*CN*时区问题&导致出现 24 小时延迟的问题，即出现23日的 情报速递 报告 而不是 22 日的 情报速递 报告 | 3.0 |
| 🛠 | 添加**钉钉**、**飞书**推送*当日 情报速递 报告* | 3.0 |
| 🛠 | 添加描述（译文）功能【暂定采用主翻译（**有道**）次翻译（**Google Translate**）】 | 3.0 |
| 🛠 | 添加统计功能 | 3.0 |
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
#### Author
- [Anonymous](https://github.com/adminlove520)
- [**东方隐侠安全实验室**](https://www.dfyxsec.com/)