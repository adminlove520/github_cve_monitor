#!/usr/bin/env python3
"""
测试CVE过滤功能的脚本
"""

import sqlite3
import os
from datetime import datetime

def test_cve_filtering():
    """测试CVE过滤功能"""
    # 连接到数据库
    if not os.path.exists("db/cve.sqlite"):
        print("错误: 数据库文件不存在")
        return
    
    conn = sqlite3.connect("db/cve.sqlite")
    cursor = conn.cursor()
    
    # 查询所有记录
    cursor.execute("SELECT * FROM CVE_DB ORDER BY cve DESC;")
    all_records = cursor.fetchall()
    
    print(f"总记录数: {len(all_records)}")
    
    # 分离有CVE编号和无CVE编号的数据
    valid_cve_records = []
    others_records = []
    
    for row in all_records:
        if row[5].upper() == "CVE NOT FOUND":
            others_records.append(row)
        else:
            valid_cve_records.append(row)
    
    print(f"有效CVE记录数: {len(valid_cve_records)}")
    print(f"无CVE记录数: {len(others_records)}")
    
    # 显示前几个无CVE编号的记录
    print("\n前5个无CVE编号的记录:")
    for i, row in enumerate(others_records[:5]):
        print(f"{i+1}. {row[1]} - {row[2][:50]}...")
    
    # 显示前几个有效CVE记录
    print("\n前5个有效CVE记录:")
    for i, row in enumerate(valid_cve_records[:5]):
        print(f"{i+1}. {row[5]} - {row[1]}")
    
    conn.close()
    
    # 检查文件是否生成
    if os.path.exists("docs/others.md"):
        print("\n✅ others.md 文件已生成")
        # 读取文件大小
        size = os.path.getsize("docs/others.md")
        print(f"   文件大小: {size} 字节")
    else:
        print("\n❌ others.md 文件未生成")

if __name__ == "__main__":
    test_cve_filtering()