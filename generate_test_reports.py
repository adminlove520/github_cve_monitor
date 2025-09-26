#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成测试用的reports.json缓存文件，用于验证weekly/index.html页面的数据加载功能
"""

import json
import os
from datetime import datetime, timedelta

def generate_test_reports():
    """生成测试用的报告数据"""
    reports = []
    today = datetime.now()
    
    # 生成最近7天的测试数据
    for i in range(7):
        date = today - timedelta(days=i)
        year = date.year
        week_num = date.isocalendar()[1]
        month = date.month
        day = date.day
        
        # 格式化日期和路径
        date_str = date.strftime('%Y-%m-%d')
        path = f"{year}-W{week_num:02d}-{month:02d}-{day:02d}"
        filename = f"daily_{year}{month:02d}{day:02d}.md"
        
        # 生成随机的CVE数量（模拟数据）
        cves_count = 30 + i * 5
        
        # 创建报告条目
        report_entry = {
            'date': date_str,
            'path': path,
            'week': f"W{week_num:02d}",
            'filename': f"{path}/{filename}",
            'cves_count': cves_count,
            'update_time': date_str,
            'title': f"{date_str} CVE情报速递"
        }
        
        reports.append(report_entry)
    
    # 创建完整的报告数据结构
    result = {
        'reports': reports,
        'total': len(reports),
        'generated_at': datetime.utcnow().isoformat(),
        'source': 'test_data',
        'is_test': True
    }
    
    return result

def save_reports_json(data):
    """保存报告数据到JSON文件"""
    # 确保目录存在
    os.makedirs('docs/data/cache', exist_ok=True)
    
    # 保存到文件
    output_path = 'docs/data/cache/reports.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 测试报告数据已保存到: {output_path}")
    print(f"   共生成 {len(data['reports'])} 条测试报告记录")
    
    # 打印第一条记录作为示例
    if data['reports']:
        first_report = data['reports'][0]
        print(f"\n📊 示例报告数据:")
        print(f"   日期: {first_report['date']}")
        print(f"   路径: {first_report['path']}")
        print(f"   文件名: {first_report['filename']}")
        print(f"   CVE数量: {first_report['cves_count']}")

def main():
    """主函数"""
    print("🔄 开始生成测试报告数据...")
    
    try:
        # 生成测试数据
        reports_data = generate_test_reports()
        
        # 保存到文件
        save_reports_json(reports_data)
        
        print("\n✅ 测试数据生成完成！")
        print("\n📋 使用说明:")
        print("   1. 访问 docs/reports/weekly/index.html 页面")
        print("   2. 页面将从 docs/data/cache/reports.json 加载测试数据")
        print("   3. 如需更新数据，请重新运行此脚本")
        
    except Exception as e:
        print(f"❌ 生成测试数据失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()