#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速修复增长率计算和缺失文件问题

这个脚本将:
1. 分析现有的daily目录
2. 生成缺失日期的JSON文件 
3. 重新计算正确的增长率
4. 更新daily_summary.json
"""

import os
import json
import re
from datetime import datetime, timedelta, date
from collections import defaultdict
import argparse
from pathlib import Path

def analyze_existing_files(daily_dir):
    """分析现有的每日文件"""
    existing_files = []
    daily_counts = {}
    
    if not os.path.exists(daily_dir):
        print(f"❌ 目录不存在: {daily_dir}")
        return existing_files, daily_counts
    
    print(f"🔍 分析目录: {daily_dir}")
    
    for filename in os.listdir(daily_dir):
        if filename.endswith('.json') and filename != 'daily_summary.json':
            # 提取日期
            date_match = re.match(r'(\d{4}-\d{2}-\d{2})\.json', filename)
            if date_match:
                date_str = date_match.group(1)
                filepath = os.path.join(daily_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    count = data.get('count', 0)
                    existing_files.append({
                        'file': filename,
                        'date': date_str,
                        'count': count,
                        'path': filepath
                    })
                    daily_counts[date_str] = count
                    
                except Exception as e:
                    print(f"⚠️ 读取文件失败 {filename}: {e}")
    
    # 按日期排序
    existing_files.sort(key=lambda x: x['date'])
    
    print(f"✅ 分析完成，找到 {len(existing_files)} 个有效文件")
    return existing_files, daily_counts

def find_missing_dates(daily_counts):
    """找出缺失的日期"""
    if not daily_counts:
        return []
    
    dates = list(daily_counts.keys())
    start_date = datetime.strptime(min(dates), '%Y-%m-%d').date()
    end_date = datetime.strptime(max(dates), '%Y-%m-%d').date()
    
    missing_dates = []
    current_date = start_date
    
    while current_date <= end_date:
        date_str = current_date.isoformat()
        if date_str not in daily_counts:
            missing_dates.append(date_str)
        current_date += timedelta(days=1)
    
    print(f"🔍 发现 {len(missing_dates)} 个缺失日期")
    return missing_dates

def create_empty_json_files(missing_dates, daily_dir):
    """为缺失的日期创建空的JSON文件"""
    created_files = []
    
    for date_str in missing_dates:
        filename = f"{date_str}.json"
        filepath = os.path.join(daily_dir, filename)
        
        json_data = {
            'date': date_str,
            'count': 0,
            'cves': [],
            'generated_at': datetime.now().isoformat(),
            'metadata': {
                'total_cves': 0,
                'date_range': date_str,
                'source': 'auto_generated_empty',
                'script_version': '2.0'
            }
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            created_files.append({
                'file': filename,
                'date': date_str,
                'count': 0,
                'path': filepath
            })
            
        except Exception as e:
            print(f"❌ 创建文件失败 {filename}: {e}")
    
    print(f"✅ 创建了 {len(created_files)} 个空文件")
    return created_files

def calculate_growth_stats(all_files):
    """计算正确的增长统计信息"""
    if len(all_files) < 2:
        return []
    
    # 按日期排序
    sorted_files = sorted(all_files, key=lambda x: x['date'])
    growth_stats = []
    cumulative_total = 0
    
    print(f"📈 计算增长率...")
    
    for i, file_data in enumerate(sorted_files):
        cumulative_total += file_data['count']
        
        # 计算增长率 - 修复后的逻辑
        if i > 0:
            prev_count = sorted_files[i-1]['count']
            if prev_count > 0:
                growth_rate = ((file_data['count'] - prev_count) / prev_count) * 100
            else:
                growth_rate = 0 if file_data['count'] == 0 else float('inf')
                # 处理无穷大的情况
                if growth_rate == float('inf'):
                    growth_rate = 100.0
        else:
            growth_rate = 0
        
        growth_stats.append({
            'date': file_data['date'],
            'daily_count': file_data['count'],
            'cumulative_total': cumulative_total,
            'growth_rate': round(growth_rate, 2) if growth_rate != float('inf') else 100.0
        })
    
    print(f"✅ 计算完成，{len(growth_stats)} 个数据点")
    return growth_stats

def update_summary_file(all_files, daily_dir):
    """更新daily_summary.json文件"""
    growth_stats = calculate_growth_stats(all_files)
    
    summary = {
        'generated_at': datetime.now().isoformat(),
        'script_version': '2.0_hotfix',
        'total_files': len(all_files),
        'total_cves': sum(f['count'] for f in all_files),
        'date_range': {
            'start': min(f['date'] for f in all_files) if all_files else None,
            'end': max(f['date'] for f in all_files) if all_files else None
        },
        'statistics': {
            'avg_daily_cves': round(sum(f['count'] for f in all_files) / len(all_files), 2) if all_files else 0,
            'max_daily_cves': max(f['count'] for f in all_files) if all_files else 0,
            'min_daily_cves': min(f['count'] for f in all_files) if all_files else 0,
            'empty_days': len([f for f in all_files if f['count'] == 0]),
            'active_days': len([f for f in all_files if f['count'] > 0])
        },
        'growth_analysis': growth_stats,
        'recent_7_days': growth_stats[-7:] if len(growth_stats) >= 7 else growth_stats,
        'recent_30_days': growth_stats[-30:] if len(growth_stats) >= 30 else growth_stats,
        'daily_stats': all_files,
        'hotfix_notes': '修复了增长率计算错误，添加了缺失日期的空文件'
    }
    
    # 保存汇总文件
    summary_path = os.path.join(daily_dir, 'daily_summary.json')
    try:
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"📊 汇总文件已更新: {summary_path}")
        return summary
    except Exception as e:
        print(f"❌ 更新汇总文件失败: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='快速修复每日数据的增长率计算和缺失文件问题')
    parser.add_argument('--daily-dir', '-d',
                       default='../docs/Data/daily',
                       help='每日数据目录 (默认: ../docs/Data/daily)')
    parser.add_argument('--create-missing', '-c',
                       action='store_true',
                       help='创建缺失日期的空JSON文件')
    parser.add_argument('--verbose', '-v', 
                       action='store_true',
                       help='显示详细输出')
    
    args = parser.parse_args()
    
    print("🔧 GitHub CVE Monitor - 快速修复工具")
    print("=" * 50)
    
    # 分析现有文件
    existing_files, daily_counts = analyze_existing_files(args.daily_dir)
    
    if not existing_files:
        print("❌ 未找到任何有效的数据文件")
        return 1
    
    all_files = existing_files.copy()
    
    # 处理缺失日期
    if args.create_missing:
        missing_dates = find_missing_dates(daily_counts)
        if missing_dates:
            created_files = create_empty_json_files(missing_dates, args.daily_dir)
            all_files.extend(created_files)
            print(f"✅ 成功创建 {len(created_files)} 个缺失文件")
        else:
            print("ℹ️ 没有发现缺失的日期")
    
    # 更新汇总文件
    print("\n📊 更新汇总统计...")
    summary = update_summary_file(all_files, args.daily_dir)
    
    if summary:
        print("\n" + "=" * 50)
        print("✅ 修复完成！")
        print(f"📁 总文件数: {summary['total_files']}")
        print(f"📊 总CVE数量: {summary['total_cves']}")
        print(f"📅 日期范围: {summary['date_range']['start']} 到 {summary['date_range']['end']}")
        print(f"📈 平均每日CVE: {summary['statistics']['avg_daily_cves']}")
        print(f"🎯 活跃天数: {summary['statistics']['active_days']}")
        print(f"💤 空白天数: {summary['statistics']['empty_days']}")
        
        if args.verbose:
            print("\n📈 最近7天增长趋势:")
            recent_growth = summary['recent_7_days']
            for day in recent_growth[-7:]:
                growth_indicator = "📈" if day['growth_rate'] > 0 else "📉" if day['growth_rate'] < 0 else "➡️"
                print(f"   - {day['date']}: {day['daily_count']} 个CVE (增长率: {day['growth_rate']:+.1f}%) {growth_indicator}")
    
    return 0

if __name__ == '__main__':
    exit(main())