# Github CVE 监控 ![版本](https://img.shields.io/badge/version-2.2.2-blue.svg)

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

### GitHub API 限制解决方案

为了解决GitHub API的请求限制问题，本项目现已支持使用GitHub Token进行认证，这可以将API请求限制从每小时60次提升到每小时5000次。

#### 配置GitHub Token

1. **本地运行**：
   - 创建一个GitHub个人访问令牌 (Personal Access Token)
     - 访问GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
     - 点击"Generate new token (classic)"
     - 选择适当的权限范围（至少需要`public_repo`权限）
     - 复制生成的token
   - 设置环境变量 `GITHUB_TOKEN` 为你的令牌值
   ```bash
   export GITHUB_TOKEN=your_token_here  # Linux/Mac
   set GITHUB_TOKEN=your_token_here     # Windows
   ```

2. **GitHub Actions**：
   - 在GitHub仓库设置中添加名为 `GH_TOKEN` 的Secret
     - 进入仓库 > Settings > Secrets and variables > Actions
     - 点击"New repository secret"
     - Name: `GH_TOKEN`
     - Secret: 你的GitHub个人访问令牌
   - 工作流程已配置为自动使用此令牌

#### Token权限要求

GitHub Token需要以下权限：
- `public_repo` - 访问公共仓库信息
- `repo` (可选) - 如果需要访问私有仓库

#### 配置文件支持

程序现在支持从以下位置的配置文件读取token（优先级从高到低）：
1. 环境变量 `GITHUB_TOKEN`
2. `docs/Data/config.json`
3. `docs/config.json`
4. `config.json`

配置文件格式示例：
```json
{
  "github_token": "your_token_here",
  "api_base_url": "https://api.github.com",
  "repository": "adminlove520/github_cve_monitor"
}
```

## 路线图

| 状态 | 任务  | 版本 |
|---|---|---|
| 🛠 | 修复增长率显示baseline问题&本周热点CVE时间维度显示不正确（滞后性bug）&修正API错误: GitHub API 调用失败: 403以及敏感信息特殊过滤 | 2.2.2 |
| 🛠 | 修复每日 情报速递 报告的当日获取逻辑问题&以及原始条数&判断依据由created_at改为updated_at（*有待商榷*） | 2.2.2 |
| 🛠 | 解决UTC*CN*时区问题&导致出现 24 小时延迟的问题，即出现23日的 情报速递 报告 而不是 22 日的 情报速递 报告 | 2.2.2 |
| 🛠 | 添加**钉钉**、**飞书**推送*当日 情报速递 报告* | 2.2.2 |
| 🛠 | 添加描述（译文）功能【暂定采用主翻译（**有道**）次翻译（**Google Translate**）】 | 2.2.2 |
| 🛠 | 添加统计功能 | 2.2.2 |
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