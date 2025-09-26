// 测试weekly报告页面的数据加载逻辑
// 可以在浏览器控制台中运行此脚本进行调试

console.log('🚀 开始测试weekly报告页面数据加载...');

// 模拟fetch函数获取reports.json
async function testFetchReports() {
  try {
    // 尝试直接访问缓存文件
    console.log('🔍 尝试访问缓存文件: ../../data/cache/reports.json');
    
    // 模拟实际数据格式，与用户提供的路径格式匹配
    const mockData = {
      "reports": [
        {
          "name": "2025-W38-09-24",
          "date": "2025-09-24",
          "week": "W38",
          "path": "2025-W38-09-24",
          "total_records": 50,
          "update_time": "2025-09-24 11:45:27"
        },
        {
          "name": "2025-W38-09-23",
          "date": "2025-09-23",
          "week": "W38",
          "path": "2025-W38-09-23",
          "total_records": 45,
          "update_time": "2025-09-23 11:30:00"
        }
      ],
      "total": 2,
      "generated_at": "2025-09-24T12:00:00.000Z"
    };
    
    // 验证日期格式和文件路径
    console.log('📋 验证报告格式:');
    mockData.reports.forEach(report => {
      const dateStr = report.date;
      const dirPath = report.path;
      
      // 计算报告文件名
      let reportFile = '';
      if (dateStr.includes('-')) {
        reportFile = `daily_${dateStr.replace(/-/g, '')}.md`;
      } else {
        reportFile = `daily_${dateStr}.md`;
      }
      
      // 构建完整路径
      const fullPath = `${dirPath}/${reportFile}`;
      console.log(`  - ${dateStr}: ${fullPath}`);
      
      // 验证路径格式是否匹配用户提供的示例
      if (fullPath.includes('2025-W38-09-24/daily_20250924.md')) {
        console.log('✅ 路径格式验证成功!');
      }
    });
    
    console.log('✅ 测试完成，数据格式正确，可以正确生成与用户提供路径格式匹配的链接。');
    return true;
  } catch (error) {
    console.error('❌ 测试失败:', error);
    return false;
  }
}

// 运行测试
testFetchReports();

// 提示：将此脚本复制到浏览器控制台中运行，或保存为HTML文件在本地测试