#!/usr/bin/env python3
"""
自动更新项目中所有写死版本号的脚本
"""

import os
import re
from get_latest_version import get_latest_version

def update_project_versions():
    """
    更新项目中所有写死的版本号
    """
    latest_version = get_latest_version()
    print(f"当前最新版本号: {latest_version}")
    
    # 需要更新的文件列表
    files_to_update = [
        'README.md',
        'wiki_content/Home.md',
        'wiki_content/关于项目.md',
        'docs/changelog.html',
        'docs/index.html'
    ]
    
    # 项目根目录
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    # 遍历需要更新的文件
    for file_relative_path in files_to_update:
        file_path = os.path.join(project_root, file_relative_path)
        
        if not os.path.exists(file_path):
            print(f"警告: 文件不存在 {file_path}")
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 保存原始内容用于比较
            original_content = content
            
            # 定义版本号模式和替换规则
            version_patterns = [
                # 匹配类似 version-2.1-blue.svg 的版本号
                (r'version-(\d+\.\d+(?:\.\d+)?)', f'version-{latest_version}'),
                # 匹配类似 **当前版本**: 2.1 的版本号
                (r'\*\*当前版本\*\*:\s*(\d+\.\d+(?:\.\d+)?)', f'**当前版本**: {latest_version}'),
                # 匹配类似 - **当前版本**: 2.1 的版本号
                (r'-\s*\*\*当前版本\*\*:\s*(\d+\.\d+(?:\.\d+)?)', f'- **当前版本**: {latest_version}'),
                # 匹配类似 当前版本: **2.1** 的版本号
                (r'当前版本:\s*\*\*(\d+\.\d+(?:\.\d+)?)\*\*', f'当前版本: **{latest_version}**'),
                # 匹配类似 | 🛠 | ... | 2.1 | 的版本号（在路线图中）
                (r'(\|\s*🛠\s*\|.*\|\s*)(\d+\.\d+(?:\.\d+)?)(\s*\|)', f'\\g<1>{latest_version}\\g<3>'),
            ]
            
            # 应用所有替换规则
            for pattern, replacement in version_patterns:
                content = re.sub(pattern, replacement, content)
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ 成功更新 {file_relative_path} 中的版本号")
            else:
                print(f"ℹ️  {file_relative_path} 中未找到需要更新的版本号")
                
        except Exception as e:
            print(f"❌ 更新 {file_relative_path} 时发生错误: {e}")

def update_html_version_badges():
    """
    特别更新HTML文件中的版本徽章
    """
    latest_version = get_latest_version()
    html_files = ['docs/changelog.html', 'wiki_content/关于项目.md', 'docs/index.html']
    
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    for file_relative_path in html_files:
        file_path = os.path.join(project_root, file_relative_path)
        
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 匹配HTML中的版本徽章
            badge_pattern = r'https://img\.shields\.io/badge/version-(\d+\.\d+(?:\.\d+)?)-blue\.svg'
            replacement = f'https://img.shields.io/badge/version-{latest_version}-blue.svg'
            content = re.sub(badge_pattern, replacement, content)
            
            # 匹配alt属性中的版本号
            alt_pattern = r'alt="Version (\d+\.\d+(?:\.\d+)?)"'
            alt_replacement = f'alt="Version {latest_version}"'
            content = re.sub(alt_pattern, alt_replacement, content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ 成功更新 {file_relative_path} 中的版本徽章")
                
        except Exception as e:
            print(f"❌ 更新 {file_relative_path} 中的版本徽章时发生错误: {e}")

if __name__ == "__main__":
    print("开始更新项目版本号...")
    update_project_versions()
    update_html_version_badges()
    print("版本号更新完成！")