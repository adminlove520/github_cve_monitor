#!/usr/bin/env python3
"""
从更新日志中动态获取最新版本号的脚本
"""

import re
import os

def get_latest_version():
    """
    从更新日志文件中提取最新版本号
    优先级: docs/changelog.md > archive/CHANGELOG.md
    """
    # 检查docs/changelog.md (优先)
    docs_changelog = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs', 'changelog.md')
    # 检查archive/CHANGELOG.md
    archive_changelog = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'archive', 'CHANGELOG.md')
    
    version = None
    
    # 首先尝试从docs/changelog.md获取
    if os.path.exists(docs_changelog):
        try:
            with open(docs_changelog, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 匹配类似 [2.2.2] 的版本号
            version_pattern = r'##\s*\[(\d+\.\d+\.\d+)\]'
            matches = re.findall(version_pattern, content)
            
            if matches:
                version = matches[0]
                print(f"从 docs/changelog.md 获取到版本号: {version}")
                return version
        except Exception as e:
            print(f"警告: 读取 docs/changelog.md 时发生异常: {e}")
    
    # 如果docs/changelog.md中没有找到，尝试从archive/CHANGELOG.md获取
    if os.path.exists(archive_changelog):
        try:
            with open(archive_changelog, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 匹配类似 [v2.2.1] 或 [2.1] 的版本号
            version_pattern = r'##\s*\[v?(\d+\.\d+\.\d+)\]'
            matches = re.findall(version_pattern, content)
            
            if matches:
                version = matches[0]
                print(f"从 archive/CHANGELOG.md 获取到版本号: {version}")
                return version
            else:
                # 尝试匹配不带v的版本号
                version_pattern = r'##\s*\[(\d+\.\d+(?:\.\d+)?)\]'
                matches = re.findall(version_pattern, content)
                if matches:
                    version = matches[0]
                    print(f"从 archive/CHANGELOG.md 获取到版本号: {version}")
                    return version
        except Exception as e:
            print(f"警告: 读取 archive/CHANGELOG.md 时发生异常: {e}")
    
    if version:
        return version
    
    print("警告: 未找到任何版本号，使用默认版本")
    return "2.1"  # 默认版本

def update_version_in_file(file_path, old_version, new_version):
    """
    更新文件中的版本号
    """
    if not os.path.exists(file_path):
        print(f"警告: 文件不存在 {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换版本号
        updated_content = content.replace(old_version, new_version)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ 成功更新 {file_path} 中的版本号: {old_version} -> {new_version}")
        return True
        
    except Exception as e:
        print(f"错误: 更新 {file_path} 时发生异常: {e}")
        return False

if __name__ == "__main__":
    latest_version = get_latest_version()
    print(f"最新版本号: {latest_version}")