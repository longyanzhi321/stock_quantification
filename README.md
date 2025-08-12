# News crawling and intelligent analysis system - 新闻爬取与智能分析系统

本项目是一个自动化新闻爬取和智能分析系统，可以从多个新闻网站获取新闻内容，并使用AI模型进行分析，然后可以将分析结果发送到手机上。

## 功能特性

1. **网站爬虫**
   - 支持登录验证的网站爬取
   - 自动处理验证字段
   - 提取指定CSS类内容并保存为CSV文件
   - 数据精简功能，限制爬取的新闻数量

2. **文本分析器**
   - 使用DeepSeek大模型对新闻内容进行智能分析
   - 输出结构化分析结果到新的CSV文件
   - 数据精简功能，限制分析的新闻数量以减少API调用

3. **通知服务**
   - 将分析结果通过邮件发送到手机
   - 支持数据精简显示，避免信息过载
   - 支持短信通知扩展（需集成第三方服务）

## 文件说明

- [web_scraper.py](file:///C:/Users/Administrator/PY_NEWS_AI/web_scraper.py): 网站爬虫模块，用于从网站抓取新闻内容
- [text_analyse.py](file:///C:/Users/Administrator/PY_NEWS_AI/text_analyse.py): 文本分析模块，使用AI模型分析新闻内容
- [notification_service.py](file:///C:/Users/Administrator/PY_NEWS_AI/notification_service.py): 通知服务模块，用于将分析结果发送到手机
- [main.py](file:///C:/Users/Administrator/PY_NEWS_AI/main.py): 主程序入口，用于一次性运行所有模块
- [.env](file:///C:/Users/Administrator/PY_NEWS_AI/.env): 环境变量配置文件（需要根据实际信息修改）
- [ENCODING_GUIDE.md](file:///C:/Users/Administrator/PY_NEWS_AI/ENCODING_GUIDE.md): 项目编码设置指南，说明如何确保整个项目使用UTF-8编码

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 一次性运行所有模块（推荐）

```bash
python main.py
```

该命令将依次执行：网页爬虫 -> 文本分析 -> 通知服务

### 2. 配置环境变量

项目使用 `.env` 文件来管理敏感信息。请编辑项目根目录下的 `.env` 文件，填入您的实际信息：

```
SENDER_EMAIL=your_real_email@example.com
SENDER_PASSWORD=your_real_password
RECEIVER_EMAIL=receiver_email@example.com
DEEPSEEK_API_KEY=your_actual_api_key
```

### 2. 爬取新闻内容

```bash
python web_scraper.py
```

默认情况下，爬虫会从每个新闻网站最多获取5条新闻，避免数据过多。

### 3. 分析新闻内容

```bash
python text_analyse.py
```

程序会尝试从环境变量获取DeepSeek API密钥，如果不存在会要求输入。分析时默认每个文件只分析5条记录以节省API调用，分析完成后会自动生成分析结果文件，并尝试通过邮件将结果发送到手机。

### 4. 手动发送分析结果到手机

```bash
python notification_service.py
```

默认显示分析结果中的前5条，避免信息过载。

## 配置说明

### 邮件通知配置

要使用邮件通知功能，需要在 `.env` 文件中设置以下变量：

- `SENDER_EMAIL`: 发送者邮箱地址
- `SENDER_PASSWORD`: 发送者邮箱密码或应用专用密码
- `RECEIVER_EMAIL`: 接收者邮箱地址（可以设置为手机号对应的邮箱，如13800000000@sms.service.com）
- `EMAIL_HOST`: SMTP服务器地址（默认为smtp.qq.com）
- `EMAIL_PORT`: SMTP端口号（默认为587）

### DeepSeek API配置

可以在 `.env` 文件中设置 `DEEPSEEK_API_KEY` 环境变量来避免每次运行时手动输入API密钥。

## 编码设置

本项目全面使用UTF-8编码处理所有文本操作，确保对中文及其他Unicode字符的良好支持。详细信息请参阅[ENCODING_GUIDE.md](file:///C:/Users/Administrator/PY_NEWS_AI/ENCODING_GUIDE.md)文件。

## 数据精简策略

为避免数据过多导致的问题，系统采用了以下精简策略：

1. **爬虫阶段**：每个网站默认最多获取5条新闻
2. **分析阶段**：每个文件默认只分析5条记录
3. **通知阶段**：发送到手机的结果默认显示5条

这些数值可以在代码中轻松调整：
- 爬虫中的[max_items](file:///C:/Users/Administrator/PY_NEWS_AI/web_scraper.py#L78-L78)参数
- 分析器中的[max_rows](file:///C:/Users/Administrator/PY_NEWS_AI/text_analyse.py#L71-L71)参数
- 通知服务中的[max_items](file:///C:/Users/Administrator/PY_NEWS_AI/notification_service.py#L43-L43)参数

## 技术架构

本项目采用模块化设计，主要包含以下组件：

1. **数据采集层**：使用`web_scraper.py`实现新闻网站的自动化爬取，支持登录验证和CSS选择器提取
2. **数据分析层**：通过`text_analyse.py`集成DeepSeek大模型API，实现新闻内容的智能分析
3. **通知服务层**：在`notification_service.py`中实现邮件通知系统，支持扩展短信通知功能
4. **配置管理层**：使用`.env`文件集中管理敏感配置信息

项目遵循清晰的分层架构，各模块之间通过标准数据格式进行通信，具有良好的可扩展性和维护性。

## 注意事项

1. 使用前请确保已安装所有依赖
2. 遵守网站的robots.txt规则和使用条款
3. 控制API调用频率，避免对目标网站造成过大压力
4. 妥善保管API密钥等敏感信息
5. 不要将包含真实信息的 `.env` 文件提交到版本控制系统中