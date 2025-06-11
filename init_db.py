import sqlite3


def init_db():
    # 连接到数据库（如果不存在会自动创建）
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # 读取 schema.sql 文件内容并执行
    with open("schema.sql", "r") as f:
        schema_sql = f.read()

    cursor.executescript(schema_sql)

    # 测试数据 content都是markdown格式
    notes = [
        ("测试笔记1", "# 标题1\n\n这是第一段内容，包含**加粗**和*斜体*"),
        (
            "随机笔记",
            "## 二级标题\n\n- 列表项1\n- 列表项2\n- 列表项3\n\n[示例链接](https://example.com)",
        ),
        ("开发笔记", '```python\nprint("Hello World")\n```\n\n代码块示例'),
        ("备忘", "### 提醒\n\n* 重要事项1\n* 重要事项2\n\n`行内代码`示例"),
        (
            "学习记录",
            "## 今日学习\n\n1. Python基础\n2. SQL语法\n3. Markdown使用\n\n> 引用内容",
        ),
        (
            "项目计划",
            "# 项目A\n\n- [x] 需求分析\n- [ ] 技术调研\n- [ ] 原型设计\n\n**截止日期**: 2023-12-31",
        ),
        (
            "会议记录",
            "## 周会纪要\n\n**参会人**: Alice, Bob\n\n1. 进度汇报\n2. 问题讨论\n3. 下周计划\n\n`action: 更新文档`",
        ),
        (
            "技术备忘",
            '```javascript\nconst fetchData = async () => {\n  const res = await fetch("/api/data");\n  return res.json();\n}```',
        ),
        (
            "读书笔记",
            "# 《Clean Code》\n\n> 好的代码应该像优美的散文\n\n- 命名要有意义\n- 函数短小精悍\n- 避免重复代码",
        ),
        (
            "购物清单",
            "## 超市采购\n\n* 🥛 牛奶\n* 🥚 鸡蛋\n* 🍎 水果\n* 🧻 纸巾\n\n预算: `200元`",
        ),
        (
            "旅行攻略",
            "# 东京行程\n\n### Day1\n- 浅草寺\n- 晴空塔\n\n[参考链接](https://travel.example.com)",
        ),
        (
            "健身计划",
            "## 周一训练\n\n1. 深蹲 3x12\n2. 卧推 3x10\n3. 引体向上 3x8\n\n`注意保持姿势`",
        ),
        (
            "Git命令",
            '```bash\ngit checkout -b feature/new\n# 提交所有更改\ngit commit -am "message"\ngit push origin HEAD```',
        ),
        (
            "电影推荐",
            "# 年度最佳\n\n1. **盗梦空间**\n   > 经典烧脑片\n2. *星际穿越*\n   - 科幻神作\n3. `泰坦尼克号`",
        ),
        (
            "错误排查",
            "## Error 500\n\n可能原因:\n\n- 服务未启动\n- 数据库连接失败\n- 内存溢出\n\n`检查日志:` `tail -f app.log`",
        ),
        (
            "食谱",
            "# 番茄炒蛋\n\n**材料**:\n* 番茄 2个\n* 鸡蛋 3个\n* 盐适量\n\n[详细步骤](https://cook.example.com)",
        ),
        (
            "学习计划",
            "## Python进阶\n\n- [ ] 装饰器\n- [ ] 多线程\n- [ ] 异步IO\n\n> 每天2小时",
        ),
        (
            "联系方式",
            "# 重要联系人\n\n| 姓名   | 电话       |\n|--------|------------|\n| 张经理 | 13800138000|\n| 李医生 | 15912345678|",
        ),
        (
            "日报",
            "# 2023-11-20\n\n**完成工作**:\n- 修复登录BUG\n- 优化API响应\n\n**问题**:\n1. 缓存穿透",
        ),
        (
            "算法笔记",
            "```python\ndef quick_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[0]\n    left = [x for x in arr[1:] if x < pivot]\n    right = [x for x in arr[1:] if x >= pivot]\n    return quick_sort(left) + [pivot] + quick_sort(right)```",
        ),
        (
            "会议提醒",
            "### 周五例会\n\n⏰ 时间: 14:00\n📍 地点: 3楼会议室\n\n**议程**:\n1. 季度总结\n2. 新人介绍",
        ),
        (
            "软件推荐",
            "# 开发工具\n\n- **VS Code** - 轻量级编辑器\n- *Postman* - API测试\n- `Docker` - 容器化部署",
        ),
        (
            "英语学习",
            "## 今日单词\n\n- **persistent** /pərˈsɪstənt/ adj. 持续的\n- *ambiguous* adj. 模棱两可的\n\n`例句`: The error is persistent.",
        ),
        (
            "项目问题",
            "# Bug报告\n\n**描述**: 页面加载缓慢\n\n**重现步骤**:\n1. 打开首页\n2. 点击搜索\n3. 等待5秒\n\n`环境`: Chrome 118",
        ),
        (
            "投资笔记",
            "## 2023Q4\n\n- 沪深300: 📉 -5.2%\n- 比特币: 📈 +18%\n\n> 控制仓位风险",
        ),
    ]
    cursor.executemany("INSERT INTO notes (title,content) VALUES (?, ?)", notes)
    conn.commit()
    conn.close()
    print("数据库初始化完成！")


if __name__ == "__main__":
    init_db()
