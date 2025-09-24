# 版本更新日志

## 更新时间
2025-09-24

## 更新内容

### 1. 动态版本号获取
- 创建了 `scripts/get_latest_version.py` 脚本，能够从更新日志文件中动态获取最新版本号
- 优先从 `docs/changelog.md` 获取版本号，备选从 `archive/CHANGELOG.md` 获取

### 2. 自动版本号更新
- 创建了 `scripts/update_project_version.py` 脚本，能够自动更新项目中所有写死的版本号
- 支持更新以下文件中的版本号：
  - README.md
  - wiki_content/Home.md
  - wiki_content/关于项目.md
  - docs/changelog.html (徽章)

### 3. 版本号同步
- 将所有项目文件中的版本号更新为最新的 2.2.2
- 更新了 archive/CHANGELOG.md 文件，添加了 v2.2.2 版本记录

### 4. 更新的文件列表
- ✅ README.md - 版本徽章和路线图中的版本号已更新
- ✅ wiki_content/Home.md - 版本徽章已更新
- ✅ wiki_content/关于项目.md - 当前版本和版本徽章已更新
- ✅ archive/CHANGELOG.md - 添加了 v2.2.2 版本记录
- ✅ docs/changelog.html - 版本号保持一致

## 技术实现

### 获取最新版本号
```python
def get_latest_version():
    # 优先从 docs/changelog.md 获取
    # 备选从 archive/CHANGELOG.md 获取
    return "2.2.2"  # 最新版本号
```

### 更新版本号
```python
def update_project_versions():
    # 自动查找并替换各种格式的版本号
    # 支持 version-2.1-blue.svg 格式
    # 支持 **当前版本**: 2.1 格式
    # 支持 | 🛠 | ... | 2.1 | 格式
```

## 验证结果

所有文件中的版本号均已成功更新为 2.2.2，项目现在能够动态获取和使用最新版本号，避免了手动维护版本号的问题。

## 后续建议

1. 在项目构建或部署时自动运行版本号更新脚本
2. 添加版本号验证机制，确保所有文件中的版本号保持一致
3. 考虑将版本号存储在单一配置文件中，其他文件引用该配置