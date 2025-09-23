#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub CVE Monitor - 每日数据生成脚本
从README.md中提取CVE数据，按日期分组生成每日JSON文件
"""

import os
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict
import argparse

def parse_readme(readme_path):
    """解析README.md文件，提取CVE数据"""
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ README文件未找到: {readme_path}")
        return []
    
    # 查找表格数据开始位置
    table_start = content.find('| CVE | 相关仓库')
    if table_start == -1:
        print("❌ 未找到CVE表格数据")
        return []
    
    # 提取表格部分
    table_section = content[table_start:]
    lines = table_section.split('\n')[2:]  # 跳过表头
    
    cve_data = []
    print(f"📋 开始解析CVE数据...")
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or not line.startswith('|'):
            continue
            
        # 分割表格列
        cols = [col.strip() for col in line.split('|') if col.strip()]
        if len(cols) < 4:
            continue
            
        try:
            # 提取CVE ID
            cve_match = re.search(r'CVE[_-]?\d{4}[_-]?\d+', cols[0])
            if not cve_match:
                continue
            cve_id = cve_match.group()
            
            # 提取仓库信息
            repo_info = cols[1]
            
            # 提取描述
            description = cols[2]
            
            # 提取日期 - 支持多种格式
            date_str = cols[3].strip()
            date_patterns = [
                r'(\d{4}-\d{2}-\d{2})T\d{2}:\d{2}:\d{2}Z',  # ISO格式
                r'(\d{4}-\d{2}-\d{2})',  # 简单日期格式
            ]
            
            parsed_date = None
            for pattern in date_patterns:
                date_match = re.search(pattern, date_str)
                if date_match:
                    try:
                        parsed_date = datetime.strptime(date_match.group(1), '%Y-%m-%d').date()
                        break
                    except ValueError:
                        continue
            
            if not parsed_date:
                print(f"⚠️  第{line_num}行日期格式无法解析: {date_str}")
                continue
            
            cve_data.append({
                'cve_id': cve_id,
                'repo_info': repo_info,
                'description': description,
                'date': parsed_date.isoformat(),
                'raw_date': date_str
            })
            
            if line_num % 1000 == 0:
                print(f"📊 已处理 {line_num} 行，提取到 {len(cve_data)} 个CVE")
                
        except Exception as e:
            print(f"⚠️  第{line_num}行解析失败: {e}")
            continue
    
    print(f"✅ 解析完成！总计提取到 {len(cve_data)} 个CVE")
    return cve_data

def group_by_date(cve_data):
    """按日期分组CVE数据"""
    daily_data = defaultdict(list)
    
    for cve in cve_data:
        date_key = cve['date']
        daily_data[date_key].append(cve)
    
    # 转换为普通字典并排序
    sorted_daily = dict(sorted(daily_data.items()))
    
    print(f"📅 数据分组完成:")
    print(f"   - 日期范围: {min(sorted_daily.keys())} 到 {max(sorted_daily.keys())}")
    print(f"   - 总天数: {len(sorted_daily)} 天")
    
    return sorted_daily

def generate_json_files(daily_data, output_dir):
    """生成每日JSON文件"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 创建输出目录: {output_dir}")
    
    generated_files = []
    
    for date_str, cves in daily_data.items():
        # 文件名格式: YYYY-MM-DD.json
        filename = f"{date_str}.json"
        filepath = os.path.join(output_dir, filename)
        
        # 准备JSON数据
        json_data = {
            'date': date_str,
            'count': len(cves),
            'cves': cves,
            'generated_at': datetime.now().isoformat(),
            'metadata': {
                'total_cves': len(cves),
                'date_range': date_str,
                'source': 'README.md'
            }
        }
        
        # 写入JSON文件
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            generated_files.append({
                'file': filename,
                'date': date_str,
                'count': len(cves),
                'path': filepath
            })
            
        except Exception as e:
            print(f"❌ 生成文件失败 {filename}: {e}")
    
    return generated_files

def generate_summary(generated_files, output_dir):
    """生成汇总信息"""
    summary = {
        'generated_at': datetime.now().isoformat(),
        'total_files': len(generated_files),
        'total_cves': sum(f['count'] for f in generated_files),
        'date_range': {
            'start': min(f['date'] for f in generated_files) if generated_files else None,
            'end': max(f['date'] for f in generated_files) if generated_files else None
        },
        'daily_stats': generated_files,
        'recent_7_days': []
    }
    
    # 计算最近7天数据
    if generated_files:
        recent_files = sorted(generated_files, key=lambda x: x['date'])[-7:]
        summary['recent_7_days'] = recent_files
    
    # 保存汇总文件
    summary_path = os.path.join(output_dir, 'daily_summary.json')
    try:
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"📊 汇总文件已生成: {summary_path}")
    except Exception as e:
        print(f"❌ 生成汇总文件失败: {e}")
    
    return summary

def main():
    parser = argparse.ArgumentParser(description='生成每日CVE数据JSON文件')
    parser.add_argument('--readme', '-r', 
                       default='../docs/README.md',
                       help='README.md文件路径 (默认: ../docs/README.md)')
    parser.add_argument('--output', '-o',
                       default='../docs/Data/daily',
                       help='输出目录 (默认: ../docs/Data/daily)')
    parser.add_argument('--verbose', '-v', 
                       action='store_true',
                       help='显示详细输出')
    
    args = parser.parse_args()
    
    print("🚀 GitHub CVE Monitor - 每日数据生成器")
    print("=" * 50)
    
    # 解析README
    print(f"📖 读取README文件: {args.readme}")
    cve_data = parse_readme(args.readme)
    
    if not cve_data:
        print("❌ 未提取到CVE数据，脚本退出")
        return 1
    
    # 按日期分组
    print("\n📅 按日期分组数据...")
    daily_data = group_by_date(cve_data)
    
    # 生成JSON文件
    print(f"\n📝 生成JSON文件到: {args.output}")
    generated_files = generate_json_files(daily_data, args.output)
    
    # 生成汇总
    print("\n📊 生成汇总信息...")
    summary = generate_summary(generated_files, args.output)
    
    # 输出结果
    print("\n" + "=" * 50)
    print("✅ 处理完成！")
    print(f"📁 生成文件数: {len(generated_files)}")
    print(f"📊 总CVE数量: {summary['total_cves']}")
    print(f"📅 日期范围: {summary['date_range']['start']} 到 {summary['date_range']['end']}")
    
    if args.verbose and generated_files:
        print("\n📋 最近生成的文件:")
        for f in generated_files[-5:]:  # 显示最近5个文件
            print(f"   - {f['file']}: {f['count']} 个CVE")
    
    return 0

if __name__ == '__main__':
    exit(main())