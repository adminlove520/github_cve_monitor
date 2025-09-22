from functools import total_ordering
import requests
from peewee import *
from datetime import datetime
import html
import time
import random
import math
import re
import os
import locale
from pathlib import Path

# 设置中文环境
try:
    locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Chinese_China.936')
    except:
        pass  # 如果设置失败，使用系统默认

db = SqliteDatabase("db/cve.sqlite")

class CVE_DB(Model):
    id = IntegerField()
    full_name = CharField(max_length=1024)
    description = CharField(max_length=4098)
    url = CharField(max_length=1024)
    created_at = CharField(max_length=128)
    cve = CharField(max_length=64)

    class Meta:
        database = db

db.connect()
db.create_tables([CVE_DB])

def init_file():
    newline = "# Github CVE Monitor\n\n> Automatic monitor github cve using Github Actions \n\n Last generated : {}\n\n| CVE | 名称 | 描述 | 日期 |\n|---|---|---|---|\n".format(datetime.now())
    with open('docs/README.md','w', encoding='utf-8') as f:
        f.write(newline) 
    f.close()

def write_file(new_contents):
    with open('docs/README.md','a', encoding='utf-8') as f:
        f.write(new_contents)
    f.close()

def init_daily_file(date_str):
    """初始化每日报告文件"""
    # 创建日期目录
    today = datetime.now()
    year = today.year
    week_number = today.strftime("%W")
    month = today.strftime("%m")
    day = today.strftime("%d")
    
    # 创建目录结构 /Data/YYYY-W-mm-dd
    dir_path = f"docs/Data/{year}-W{week_number}-{month}-{day}"
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # 创建每日报告文件
    file_path = f"{dir_path}/daily_{date_str}.md"
    newline = f"""# 每日 情报速递 报告 ({date_str})

> Automatic monitor Github CVE using Github Actions 

## 报告信息
- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **数据来源**: GitHub CVE 数据库

## 今日 情报速递

| CVE | 名称 | 描述 | 日期 |
|:---|:---|:---|:---|
"""
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(newline)
    
    return file_path

def write_daily_file(file_path, new_contents):
    """写入每日报告文件"""
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(new_contents)
    f.close()

def update_daily_index():
    """更新每日报告索引文件"""
    data_dir = Path("docs/Data")
    if not data_dir.exists():
        return
    
    # 创建索引文件
    index_path = data_dir / "index.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("# 每日 CVE 监控报告索引\n\n")
        f.write("> Automatic monitor Github CVE using Github Actions\n\n")
        f.write("## 可用报告\n\n")
    
    # 遍历所有日期目录
    date_dirs = sorted([d for d in data_dir.glob("*-W*-*-*")], reverse=True)
    
    for date_dir in date_dirs:
        dir_name = date_dir.name
        with open(index_path, 'a', encoding='utf-8') as f:
            f.write(f"### {dir_name}\n\n")
        
        # 遍历该目录下的所有daily报告
        daily_files = sorted([f for f in date_dir.glob("daily_*.md")], reverse=True)
        
        for daily_file in daily_files:
            file_name = daily_file.name
            relative_path = f"Data/{date_dir.name}/{file_name}"
            date_str = file_name.replace("daily_", "").replace(".md", "")
            
            # 格式化日期显示
            try:
                formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
            except:
                formatted_date = date_str
            
            with open(index_path, 'a', encoding='utf-8') as f:
                f.write(f"- [{formatted_date} 每日报告]({relative_path})\n")
        
        with open(index_path, 'a', encoding='utf-8') as f:
            f.write("\n")
    
    # 更新侧边栏，添加每日报告链接
    update_sidebar()

def update_sidebar():
    """更新侧边栏，添加每日报告链接"""
    sidebar_path = Path("docs/_sidebar.md")
    if not sidebar_path.exists():
        return
    
    # 读取现有侧边栏内容
    with open(sidebar_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 检查是否已有每日报告链接
    daily_report_exists = False
    for line in lines:
        if "每日报告" in line:
            daily_report_exists = True
            break
    
    # 如果没有每日报告链接，添加到侧边栏
    if not daily_report_exists:
        # 找到合适的位置插入链接
        new_lines = []
        for line in lines:
            new_lines.append(line)
            # 在主页链接后添加每日报告链接
            if "- [主页](README.md)" in line or "- [Home](README.md)" in line:
                new_lines.append("- [每日报告](/Data/index.md)\n")
        
        # 写回文件
        with open(sidebar_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

def get_info(year):
    try:
        api = "https://api.github.com/search/repositories?q=CVE-{}&sort=updated&page=1&per_page=100".format(year)
        # 获取GitHub Token（如果存在）
        github_token = os.environ.get('GITHUB_TOKEN')
        headers = {}
        
        # 如果有Token，添加到请求头中
        if github_token:
            headers['Authorization'] = f'token {github_token}'
            print(f"Using GitHub Token for authentication (Year: {year})")
            # 有token时使用更大的per_page值
            api = "https://api.github.com/search/repositories?q=CVE-{}&sort=updated&page=1&per_page=100".format(year)
        else:
            print(f"No GitHub Token found, using unauthenticated request (Year: {year})")
            # 无token时使用默认的per_page值
            api = "https://api.github.com/search/repositories?q=CVE-{}&sort=updated&page=1&per_page=30".format(year)
        
        # API请求
        response = requests.get(api, headers=headers)
        
        # 输出API限制信息（如果可用）
        if 'X-RateLimit-Limit' in response.headers:
            print(f"API Rate Limit: {response.headers.get('X-RateLimit-Remaining')}/{response.headers.get('X-RateLimit-Limit')}")
        
        req = response.json()
        items = req["items"]
        return items
    except Exception as e:
        print("An error occurred in the network request", e)
        return None


def db_match(items):
    r_list = []
    regex = r"[Cc][Vv][Ee][-_]\d{4}[-_]\d{4,7}"
    cve = ''
    for item in items:
        id = item["id"]
        if CVE_DB.select().where(CVE_DB.id == id).count() != 0:
            continue
        full_name = html.escape(item["full_name"])
        description = item["description"]
        if description == "" or description == None:
            description = 'no description'
        else:
            description = html.escape(description.strip())
        url = item["html_url"]
### EXTRACT CVE 
        matches = re.finditer(regex, url, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            cve = match.group()
        if not cve:
            matches = re.finditer(regex, description, re.MULTILINE)
            cve = "CVE Not Found"
            for matchNum, match in enumerate(matches, start=1):
                cve = match.group()
### 
        created_at = item["created_at"]
        r_list.append({
            "id": id,
            "full_name": full_name,
            "description": description,
            "url": url,
            "created_at": created_at,
            "cve": cve.replace('_','-')
        })
        CVE_DB.create(id=id,
                      full_name=full_name,
                      description=description,
                      url=url,
                      created_at=created_at,
                      cve=cve.upper().replace('_','-'))

    return sorted(r_list, key=lambda e: e.__getitem__('created_at'))

def main():
    # 获取当前日期
    today = datetime.now()
    date_str = today.strftime("%Y%m%d")
    year = today.year
    
    # 初始化全量数据文件
    init_file()
    
    # 初始化每日报告文件
    daily_file_path = init_daily_file(date_str)
    
    # 收集数据
    sorted_list = []
    today_list = []  # 存储当日数据
    
    # 首先获取当年的数据（当日数据）
    print(f"获取当年 ({year}) 的CVE数据...")
    item = get_info(year)
    if item is not None and len(item) > 0:
        print(f"年份: {year} : 获取到 {len(item)} 条原始数据")
        sorted_data = db_match(item)
        if len(sorted_data) != 0:
            print(f"年份 {year} : 更新 {len(sorted_data)} 条记录")
            
            # 筛选当日数据
            for entry in sorted_data:
                try:
                    created_date = datetime.fromisoformat(entry["created_at"].replace("Z", "+00:00"))
                    # 判断是否为当日数据（使用日期字符串比较，考虑到2025-09-22T13:53:14Z这样的格式）
                    # 注意：这里需要使用created_date的日期，不转换为本地时间
                    created_date_str = created_date.strftime("%Y-%m-%d")
                    today_str = today.strftime("%Y-%m-%d")
                    if created_date_str == today_str:
                        today_list.append(entry)
                except Exception as e:
                    print(f"日期解析错误: {e}")
            
            sorted_list.extend(sorted_data)
        
        # 随机等待以避免API限制
        count = random.randint(3, 15)
        time.sleep(count)
    
    # 获取历史数据
    for i in range(year-1, 1999, -1):
        item = get_info(i)
        if item is None or len(item) == 0:
            continue
        print(f"年份: {i} : 获取到 {len(item)} 条原始数据")
        sorted_data = db_match(item)
        if len(sorted_data) != 0:
            print(f"年份 {i} : 更新 {len(sorted_data)} 条记录")
            sorted_list.extend(sorted_data)
        count = random.randint(3, 15)
        time.sleep(count)
    
    # 生成全量数据报告
    cur = db.cursor()
    cur.execute("SELECT * FROM CVE_DB ORDER BY cve DESC;")
    result = cur.fetchall()
    
    # 写入报告头部
    newline = f"""# 全量 CVE 数据报告

> Automatic monitor Github CVE using Github Actions 

## 报告信息
- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **数据来源**: GitHub CVE 数据库
- **总记录数**: {len(result)}

## CVE 完整列表

| CVE | 名称 | 描述 | 日期 |
|:---|:---|:---|:---|
"""
    write_file(newline)
    
    # 写入每条记录
    for row in result:
        Publish_Date = row[4]
        Description = row[2].replace('|','-')
        if row[5].upper() == "CVE NOT FOUND":
            newline = "| " + row[5].upper() + " | [" + row[1] + "](" + row[3] + ") | " + Description + " | " + Publish_Date + "|\n"
        else:
            newline = "| [" + row[5].upper() + "](https://www.cve.org/CVERecord?id=" + row[5].upper() + ") | [" + row[1] + "](" + row[3] + ") | " + Description + " | " + Publish_Date + "|\n"
        write_file(newline)
    
    # 生成当日报告
    
    # 记录原始today_list长度
    original_today_list_len = len(today_list)
    print(f"生成当日报告，共 {len(today_list)} 条记录")
    
    # 如果当日没有数据，使用最近的数据
    if len(today_list) == 0:
        print("当日无数据，尝试获取最近7天的数据...")
        # 先尝试获取最近7天的数据
        cur = db.cursor()
        # 获取7天内的数据
        from datetime import timedelta
        seven_days_ago = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        cur.execute(f"SELECT * FROM CVE_DB WHERE created_at >= '{seven_days_ago}' ORDER BY created_at DESC;")
        recent_records = cur.fetchall()
        
        # 如果7天内没有数据，则获取最近的10条记录
        if len(recent_records) == 0:
            print("最近7天无数据，获取最近10条记录...")
            cur.execute("SELECT * FROM CVE_DB ORDER BY created_at DESC LIMIT 10;")
            recent_records = cur.fetchall()
        
        # 转换为与today_list相同的格式
        for row in recent_records:
            today_list.append({
                "cve": row[5],
                "full_name": row[1],
                "description": row[2],
                "url": row[3],
                "created_at": row[4]
            })
        
        print(f"当日无数据，使用最近 {len(today_list)} 条记录")
    
    # 初始化每日报告文件
    date_str = datetime.now().strftime("%Y%m%d")
    daily_file_path = init_daily_file(date_str)
    
    # 写入每日报告文件
    if len(today_list) > 0:
        # 如果是使用最近记录，则在报告中增加说明
        if original_today_list_len == 0:
            with open(daily_file_path, 'a', encoding='utf-8') as f:
                f.write("\n\n> 由于没有获取到当日数据，使用近7天记录\n\n")
        print(f"成功写入 {len(today_list)} 条记录到每日报告")
    
    # 写入每日报告
    for entry in today_list:
        cve = entry["cve"]
        full_name = entry["full_name"]
        description = entry["description"].replace('|','-')
        url = entry["url"]
        created_at = entry["created_at"]
        
        if cve.upper() == "CVE NOT FOUND":
            newline = f"| {cve.upper()} | [{full_name}]({url}) | {description} | {created_at}|\n"
        else:
            newline = f"| [{cve.upper()}](https://www.cve.org/CVERecord?id={cve.upper()}) | [{full_name}]({url}) | {description} | {created_at}|\n"
        
        # 写入每日报告文件
        write_daily_file(daily_file_path, newline)
    
    # 更新索引文件，列出所有每日报告
    update_daily_index()
    
    # Statistics
    ## TODO HERE WILL COME THE CODE FOR STATISTICS 
        
if __name__ == "__main__":
    init_file()
    main()
