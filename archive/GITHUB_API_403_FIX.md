# GitHub API 403错误修复方案

## 问题描述
项目在运行时遇到GitHub API返回403 Forbidden错误，导致无法正常获取CVE数据。错误表现为：
- GitHub API调用失败，状态码403
- Token认证失败
- 无法获取仓库搜索结果

## 问题分析
通过代码分析和测试，发现问题的根本原因包括：

1. **Token获取逻辑不完整**：原始代码只从环境变量`GITHUB_TOKEN`获取token，不支持从配置文件读取
2. **配置文件读取缺失**：虽然GitHub Actions会生成包含token的配置文件，但程序代码中没有读取这些文件的逻辑
3. **错误诊断不足**：缺乏详细的错误信息，难以定位具体问题

## 解决方案

### 1. 增强Token获取逻辑
修改[main.py](file:///d:/safePro/github_cve_monitor/main.py)文件，添加了以下功能：

```python
def load_config():
    """从配置文件加载配置信息"""
    config_paths = [
        "docs/Data/config.json",
        "docs/config.json",
        "config.json"
    ]
    
    for config_path in config_paths:
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config
            except Exception as e:
                print(f"警告: 无法读取配置文件 {config_path}: {e}")
    
    return {}

def get_github_token():
    """获取GitHub Token，优先级：环境变量 > 配置文件"""
    # 首先检查环境变量
    github_token = os.environ.get('GITHUB_TOKEN')
    if github_token:
        print(f"DEBUG: 从环境变量获取到GITHUB_TOKEN")
        return github_token
    
    # 然后检查配置文件
    config = load_config()
    github_token = config.get('github_token')
    if github_token and github_token != "your_token_here":
        print(f"DEBUG: 从配置文件获取到github_token")
        return github_token
    
    print("DEBUG: 未找到有效的GitHub Token")
    return None
```

### 2. 改进错误处理
增强了GitHub API调用的错误处理：

```python
# 处理403错误
if response.status_code == 403:
    print(f"错误: GitHub API返回403 Forbidden")
    print(f"响应内容: {response.text}")
    if 'X-GitHub-SSO' in response.headers:
        print(f"SSO要求: {response.headers.get('X-GitHub-SSO')}")
    break
```

### 3. 完善文档说明
更新了[README.md](file:///d:/safePro/github_cve_monitor/README.md)，提供了详细的配置说明：

- GitHub Token生成和配置步骤
- 环境变量和配置文件两种配置方式
- Token权限要求说明
- 故障排除指南

## 验证结果
通过[test_github_api.py](file:///d:/safePro/github_cve_monitor/test_github_api.py)和[verify_fix.py](file:///d:/safePro/github_cve_monitor/verify_fix.py)脚本验证：

1. ✅ 配置文件加载功能正常
2. ✅ Token获取逻辑按优先级工作
3. ✅ 错误处理机制完善
4. ✅ 兼容环境变量和配置文件两种方式

## 部署建议

### GitHub Actions环境
1. 确保在仓库Settings > Secrets中正确设置了`GH_TOKEN`
2. 验证token具有`public_repo`权限
3. 检查GitHub Actions工作流配置是否正确传递secret

### 本地开发环境
1. 创建GitHub个人访问令牌
2. 通过环境变量或配置文件设置token：
   ```bash
   # 环境变量方式
   export GITHUB_TOKEN=your_actual_token_here
   
   # 或者修改config.json文件
   {
     "github_token": "your_actual_token_here",
     "api_base_url": "https://api.github.com",
     "repository": "adminlove520/github_cve_monitor"
   }
   ```

## 总结
本次修复通过增强token获取逻辑和完善错误处理，解决了GitHub API 403错误问题。新的实现支持多种配置方式，提高了系统的健壮性和易用性，同时提供了详细的错误信息便于问题诊断。