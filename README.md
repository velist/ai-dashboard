# AI病例研习平台 - 数据仪表盘

## 📊 项目简介

这是一个为AI病例研习平台设计的数据分析仪表盘，提供用户行为分析、留存分析、转化漏斗等核心指标的可视化展示。

**在线访问**: [bltestdata.aipush.fun](https://bltestdata.aipush.fun)

## 🏗️ 系统架构

\`\`\`
┌─────────────────┐
│  API数据源      │
│ (每小时更新)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ GitHub Actions  │  ← 自动化数据获取
│  定时任务       │     和清洗
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  data/latest.json│  ← 清洗后的静态数据
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Cloudflare Pages│  ← 静态网站托管
│  CDN加速        │
└─────────────────┘
\`\`\`

## ✨ 核心功能

### 1. 关键指标卡片 (8个KPI)
- **总用户数**: 时间范围内的独立用户数
- **进入问诊率**: 进入问诊的用户占比
- **诊断行为率**: 有诊断行为的用户占比
- **完成率**: 查看评分的用户占比
- **次日留存率**: 用户次日回访比例
- **平台累计用户**: 所有时间的累计用户总数
- **回访用户数**: 直接进入问诊的用户（跳过引导）
- **首次用户数**: 完成科室选择的新用户

每个KPI都显示与上周同期的对比变化（↑/↓百分比）

### 2. 数据可视化图表 (5类)
- **转化漏斗分析**: 从引导页到查看评分的用户流失情况
- **用户趋势分析**: 每日活跃用户数折线图
- **用户结构分析**:
  - 首次用户 vs 回访用户饼图
  - Top 10 科室选择分布柱状图
- **功能使用分析**: 各功能使用率统计

### 3. 数据筛选功能
- **日期范围选择**: 自定义时间段
- **快捷日期**: 最近7天/14天/30天
- **用户类型筛选**: 全部/首次/回访用户
- **默认展示**: 昨天往前7天（避免当天数据不完整）

## 📂 项目结构

\`\`\`
dashboard-deploy/
├── index.html              # 仪表盘主页面
├── data/                   # 数据目录
│   └── latest.json         # 最新清洗后的数据
├── scripts/                # Python脚本
│   └── fetch_data.py       # 数据获取和清洗脚本
├── .github/
│   └── workflows/
│       └── update-data.yml # GitHub Actions工作流
└── README.md               # 项目文档
\`\`\`

## 🔄 自动化数据更新

### 工作流程
1. **GitHub Actions定时任务**: 每小时执行一次
2. **数据获取**: 从API获取最新Excel数据
3. **数据清洗**:
   - 排除22个测试ID
   - 排除ksbaoUserId为空的记录
   - 转换时间格式
4. **保存数据**:
   - 保存到 \`data/latest.json\`（带元数据）
   - 保存历史备份文件
5. **自动提交**: 推送更新后的数据到GitHub
6. **自动部署**: Cloudflare Pages检测到更新后自动重新部署

### 手动触发
可以在GitHub Actions界面手动触发数据更新：
1. 进入仓库的 Actions 标签
2. 选择 "更新数据" 工作流
3. 点击 "Run workflow"

## 🚀 本地开发

### 环境要求
- Python 3.8+
- 现代浏览器（Chrome/Firefox/Edge/Safari）

### 安装依赖
\`\`\`bash
pip install pandas requests openpyxl
\`\`\`

### 运行数据获取脚本
\`\`\`bash
python scripts/fetch_data.py
\`\`\`

### 启动本地服务器
\`\`\`bash
# 使用Python内置服务器
python -m http.server 8000

# 或使用Node.js的http-server
npx http-server
\`\`\`

然后访问 \`http://localhost:8000\`

## 📊 数据格式

### latest.json 结构
\`\`\`json
{
  "updateTime": "2026-01-27T10:00:00",
  "dataCount": 706,
  "userCount": 196,
  "timeRange": {
    "start": "2026-01-19T01:52:08",
    "end": "2026-01-25T23:33:39"
  },
  "data": [
    {
      "user_id": "user123",
      "element": "引导页访问",
      "time": "2026-01-19T10:30:45",
      "ksbaoUserId": "ks123",
      ...
    }
  ]
}
\`\`\`

## 🔧 技术栈

- **前端框架**: 无框架，原生JavaScript
- **UI样式**: Tailwind CSS (CDN)
- **图表库**: Apache ECharts 5.4.3
- **日期选择**: Flatpickr
- **自动化**: GitHub Actions
- **托管**: Cloudflare Pages
- **数据处理**: Python (pandas, requests)

## 📝 配置说明

### GitHub Actions环境变量
无需配置额外环境变量，使用默认的 \`GITHUB_TOKEN\`

### Cloudflare Pages设置
1. **构建命令**: 无（静态站点）
2. **构建输出目录**: \`/\`
3. **根目录**: \`/\`
4. **自定义域名**: \`bltestdata.aipush.fun\`

## 🐛 故障排查

### 数据未更新
1. 检查GitHub Actions是否正常运行
2. 查看Actions日志中的错误信息
3. 确认API接口是否可访问

### 仪表盘加载失败
1. 打开浏览器控制台查看错误
2. 确认 \`data/latest.json\` 文件存在
3. 检查JSON格式是否正确

---

**最后更新**: 2026-01-27  
**版本**: 1.0.0
