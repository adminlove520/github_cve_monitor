#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub CVE Monitor - Wiki统计数据生成脚本

功能:
1. 从daily_summary.json提取统计数据
2. 生成CVE分类统计
3. 生成POC/EXP统计
4. 计算趋势数据
5. 生成供Wiki使用的统计数据文件
"""

import os
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import argparse
from pathlib import Path

def load_daily_summary(summary_path):
    """加载每日汇总数据"""
    try:
        with open(summary_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ 汇总文件未找到: {summary_path}")
        return None
    except json.JSONDecodeError:
        print(f"❌ 汇总文件格式错误: {summary_path}")
        return None

def load_daily_files(daily_dir, days=30):
    """加载最近N天的每日JSON文件"""
    daily_files = []
    today = datetime.now().date()
    
    for i in range(days):
        target_date = today - timedelta(days=i)
        date_str = target_date.isoformat()
        file_path = os.path.join(daily_dir, f"{date_str}.json")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    daily_files.append(data)
            except Exception as e:
                print(f"⚠️  无法读取文件 {file_path}: {e}")
    
    return sorted(daily_files, key=lambda x: x['date'])

def analyze_cve_types(cve_data):
    """分析CVE类型分布"""
    type_patterns = {
        '远程代码执行': [r'RCE', r'remote code execution', r'远程代码执行', r'code execution'],
        '注入攻击': [r'injection', r'注入', r'SQL', r'XSS', r'CSRF', r'OGNL', r'命令注入', r'指令注入'],
        '提权漏洞': [r'privilege escalation', r'提权', r'权限提升', r'elevation'],
        '信息泄露': [r'info disclosure', r'information disclosure', r'信息泄露', r'敏感信息'],
        '路径遍历': [r'path traversal', r'traversal', r'directory traversal', r'目录遍历'],
        '拒绝服务': [r'DoS', r'denial of service', r'拒绝服务'],
        '认证绕过': [r'bypass', r'authentication bypass', r'绕过', r'auth bypass']
    }
    
    type_count = defaultdict(int)
    unclassified = 0
    
    for day_data in cve_data:
        for cve in day_data.get('cves', []):
            description = cve.get('description', '').lower()
            classified = False
            
            for cve_type, patterns in type_patterns.items():
                for pattern in patterns:
                    if pattern.lower() in description:
                        type_count[cve_type] += 1
                        classified = True
                        break
                if classified:
                    break
            
            if not classified:
                unclassified += 1
    
    # 添加未分类
    if unclassified > 0:
        type_count['其他'] = unclassified
    
    # 转换为排序后的列表
    return sorted(type_count.items(), key=lambda x: x[1], reverse=True)

def analyze_poc_exp(cve_data):
    """分析POC/EXP统计"""
    poc_keywords = ['poc', 'proof of concept', '验证脚本', '概念验证']
    exp_keywords = ['exp', 'exploit', '漏洞利用', '利用代码']
    
    poc_count = 0
    exp_count = 0
    both_count = 0
    neither_count = 0
    
    for day_data in cve_data:
        for cve in day_data.get('cves', []):
            repo_info = cve.get('repo_info', '').lower()
            description = cve.get('description', '').lower()
            content = f"{repo_info} {description}"
            
            has_poc = any(keyword in content for keyword in poc_keywords)
            has_exp = any(keyword in content for keyword in exp_keywords)
            
            if has_poc and has_exp:
                both_count += 1
            elif has_poc:
                poc_count += 1
            elif has_exp:
                exp_count += 1
            else:
                neither_count += 1
    
    return {
        '仅POC': poc_count,
        '仅EXP': exp_count,
        'POC+EXP': both_count,
        '无POC/EXP': neither_count
    }

def calculate_trends(growth_stats, days=7):
    """计算趋势数据"""
    if len(growth_stats) < days:
        return growth_stats
    
    return growth_stats[-days:]

def generate_vendor_stats(cve_data):
    """生成厂商统计"""
    vendor_patterns = {
        'Microsoft': [r'microsoft', r'windows', r'ms-', r'azure', r'office'],
        'Google': [r'google', r'android', r'chrome', r'gcp', r'firebase'],
        'Apple': [r'apple', r'ios', r'macos', r'iphone', r'ipad'],
        'Linux': [r'linux', r'kernel', r'ubuntu', r'debian', r'redhat'],
        'Adobe': [r'adobe', r'acrobat', r'reader', r'photoshop', r'premiere'],
        'Oracle': [r'oracle', r'java', r'mysql', r'plsql', r'database'],
        'Cisco': [r'cisco', r'router', r'switch', r'asa', r'ios'],
        'Apache': [r'apache', r'tomcat', r'httpd', r'struts', r'spark'],
        'Nginx': [r'nginx', r'engine x'],
        'AWS': [r'aws', r'amazon', r'lambda', r'ec2', r's3']
    }
    
    vendor_count = defaultdict(int)
    
    for day_data in cve_data:
        for cve in day_data.get('cves', []):
            description = cve.get('description', '').lower()
            cve_id = cve.get('cve_id', '').lower()
            content = f"{description} {cve_id}"
            
            for vendor, patterns in vendor_patterns.items():
                for pattern in patterns:
                    if pattern.lower() in content:
                        vendor_count[vendor] += 1
                        break
    
    # 转换为排序后的列表
    return sorted(vendor_count.items(), key=lambda x: x[1], reverse=True)

def generate_stats_file(summary, daily_files, output_path):
    """生成统计数据文件"""
    # 获取统计信息
    cve_types = analyze_cve_types(daily_files)
    poc_exp_stats = analyze_poc_exp(daily_files)
    vendor_stats = generate_vendor_stats(daily_files)
    trends = calculate_trends(summary.get('growth_analysis', []))
    
    # 准备统计数据
    stats = {
        'generated_at': datetime.now().isoformat(),
        'version': '1.0',
        'summary': {
            'total_cves': summary.get('total_cves', 0),
            'date_range': summary.get('date_range', {}),
            'avg_daily_cves': summary.get('statistics', {}).get('avg_daily_cves', 0),
            'active_days': summary.get('statistics', {}).get('active_days', 0),
            'max_daily_cves': summary.get('statistics', {}).get('max_daily_cves', 0)
        },
        'cve_types': dict(cve_types),
        'poc_exp_stats': poc_exp_stats,
        'vendor_stats': dict(vendor_stats[:10]),  # 取前10个厂商
        'trends': trends,
        'recent_data': daily_files[-7:]  # 最近7天数据
    }
    
    # 保存统计文件
    try:
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            print(f"📁 创建输出目录: {output_dir}")
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        print(f"✅ 统计数据文件已生成: {output_path}")
        return stats
    except Exception as e:
        print(f"❌ 生成统计文件失败: {e}")
        return None

def generate_wiki_md(stats, output_md_path):
    """生成Wiki统计数据Markdown"""
    if not stats:
        return False
    
    # 提取数据
    summary = stats.get('summary', {})
    cve_types = stats.get('cve_types', {})
    poc_exp_stats = stats.get('poc_exp_stats', {})
    vendor_stats = stats.get('vendor_stats', {})
    trends = stats.get('trends', [])
    
    # 确保trends不为空时再取最大值
    most_active_day = '暂无'
    most_active_count = 0
    if trends:
        most_active = max(trends, key=lambda x: x['daily_count'])
        most_active_day = most_active['date']
        most_active_count = most_active['daily_count']
    
    # 生成Markdown内容
    md_content = f"""
# 统计数据

本页面展示GitHub CVE监控系统的统计数据和分析信息，数据自动从系统中获取并更新。

## 📊 总体统计
- **总CVE记录数**: {summary.get('total_cves', 0):,}
- **平均每日新增**: {summary.get('avg_daily_cves', 0):.1f} 个
- **最活跃日期**: {most_active_day} (当日新增 {most_active_count} 个)
- **监测周期**: {summary.get('date_range', {}).get('start', '暂无')} 至 {summary.get('date_range', {}).get('end', '暂无')}
- **活跃天数**: {summary.get('active_days', 0)} 天
- **数据更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📈 每日增长趋势

| 日期 | 每日新增 | 累计总数 | 增长率 |
|:---|:---|:---|:---|
"""
    
    # 添加趋势表格
    for trend in reversed(trends):  # 从新到旧显示
        growth_icon = "📈" if trend['growth_rate'] > 0 else "📉" if trend['growth_rate'] < 0 else "➡️"
        md_content += f"| {trend['date']} | {trend['daily_count']} | {trend['cumulative_total']:,} | {trend['growth_rate']:+.1f}% {growth_icon} |\n"
    
    # 添加CVE类型统计
    if cve_types:
        md_content += "\n## 🔍 CVE分类统计\n\n| 类型 | 数量 | 占比 |\n|:---|:---|:---|\n"
        total_types = sum(cve_types.values())
        for cve_type, count in cve_types.items():
            percentage = (count / total_types * 100) if total_types > 0 else 0
            md_content += f"| {cve_type} | {count:,} | {percentage:.1f}% |\n"
    else:
        md_content += "\n## 🔍 CVE分类统计\n\n数据统计中，敬请期待...\n"
    
    # 添加POC/EXP统计
    if poc_exp_stats:
        md_content += "\n## 🛠️ POC/EXP统计\n\n| 类型 | 数量 | 占比 |\n|:---|:---|:---|\n"
        total_poc_exp = sum(poc_exp_stats.values())
        for p_type, count in poc_exp_stats.items():
            percentage = (count / total_poc_exp * 100) if total_poc_exp > 0 else 0
            md_content += f"| {p_type} | {count:,} | {percentage:.1f}% |\n"
    else:
        md_content += "\n## 🛠️ POC/EXP统计\n\n数据统计中，敬请期待...\n"
    
    # 添加厂商统计
    if vendor_stats:
        md_content += "\n## 🏢 厂商漏洞统计Top 10\n\n| 厂商 | 漏洞数量 |\n|:---|:---|\n"
        for vendor, count in vendor_stats.items():
            md_content += f"| {vendor} | {count:,} |\n"
    else:
        md_content += "\n## 🏢 厂商漏洞统计Top 10\n\n数据统计中，敬请期待...\n"
    
    # 添加数据获取架构说明
    md_content += """\n## 💡 数据获取架构

系统采用高效的数据获取和缓存机制：

### 核心特点
- **自动化更新**: 通过GitHub Actions定时获取并处理数据
- **静态文件缓存**: 数据存储为JSON文件，提高访问速度
- **无Token依赖**: 前端直接加载静态数据，无需API密钥
- **实时统计**: 自动生成多维度统计分析

### 性能优势
- 页面加载速度提升约80%
- 避免GitHub API速率限制问题
- 提高系统稳定性和可靠性
- 支持离线访问已缓存数据
"""
    
    # 添加说明
    md_content += "\n## ℹ️ 数据说明\n- 数据来源于每日从GitHub收集的CVE信息\n- 统计基于已收集的数据，可能存在延迟\n- 分类统计基于关键词匹配，仅供参考\n- 统计数据每日自动更新"
    
    # 保存Markdown文件
    try:
        # 确保输出目录存在
        output_dir = os.path.dirname(output_md_path)
        if output_dir and not os.path.exists(output_dir):
            print(f"📁 创建输出目录: {output_dir}")
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"✅ Wiki统计Markdown已生成: {output_md_path}")
        return True
    except Exception as e:
        print(f"❌ 生成Markdown失败: {e}")
        return False

def main():
    # 获取脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # 设置默认路径为绝对路径 - 使用小写的data目录
    default_summary = os.path.join(project_root, 'docs', 'data', 'daily', 'daily_summary.json')
    default_daily_dir = os.path.join(project_root, 'docs', 'data', 'daily')
    default_output_json = os.path.join(project_root, 'docs', 'data', 'statistics', 'wiki_stats.json')
    default_output_md = os.path.join(project_root, 'wiki_content', '统计数据.md')
    
    parser = argparse.ArgumentParser(description='Wiki统计数据生成器')
    parser.add_argument('--summary', '-s',
                       default=default_summary,
                       help=f'每日汇总文件路径 (默认: {default_summary})')
    parser.add_argument('--daily-dir', '-d',
                       default=default_daily_dir,
                       help=f'每日数据目录 (默认: {default_daily_dir})')
    parser.add_argument('--output-json', '-j',
                       default=default_output_json,
                       help=f'输出统计JSON文件路径 (默认: {default_output_json})')
    parser.add_argument('--output-md', '-m',
                       default=default_output_md,
                       help=f'输出Wiki Markdown文件路径 (默认: {default_output_md})')
    parser.add_argument('--days', '-n',
                       type=int, default=30,
                       help='统计天数 (默认: 30)')
    
    args = parser.parse_args()
    
    print("🚀 GitHub CVE Monitor - Wiki统计数据生成器")
    print("=" * 60)
    
    # 加载汇总数据
    print(f"📊 加载汇总数据: {args.summary}")
    summary = load_daily_summary(args.summary)
    if not summary:
        print("❌ 无法加载汇总数据，脚本退出")
        return 1
    
    # 加载每日数据
    print(f"📅 加载最近{args.days}天的每日数据...")
    daily_files = load_daily_files(args.daily_dir, args.days)
    print(f"✅ 成功加载 {len(daily_files)} 个每日数据文件")
    
    # 生成统计数据
    print("📈 生成统计数据...")
    stats = generate_stats_file(summary, daily_files, args.output_json)
    if not stats:
        print("❌ 统计数据生成失败")
        return 1
    
    # 生成Wiki Markdown
    print("📝 生成Wiki统计Markdown...")
    if generate_wiki_md(stats, args.output_md):
        print("\n✅ 所有统计数据已成功生成！")
        return 0
    else:
        print("\n❌ Wiki Markdown生成失败")
        return 1

if __name__ == '__main__':
    exit(main())