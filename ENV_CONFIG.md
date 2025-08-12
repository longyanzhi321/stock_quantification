# 环境变量配置说明

本项目使用 `.env` 文件来管理敏感信息和配置参数，以提高安全性并方便配置。

## 配置步骤

1. 项目根目录下有一个 `.env` 文件模板
2. 复制 `.env` 文件并根据您的实际信息修改其中的值
3. 运行项目时，程序会自动加载这些环境变量

## 支持的环境变量

### 邮件相关配置
- `SENDER_EMAIL`: 发送者邮箱地址
- `SENDER_PASSWORD`: 发送者邮箱密码或应用专用密码
- `RECEIVER_EMAIL`: 接收者邮箱地址
- `EMAIL_HOST`: SMTP服务器地址（可选，默认为smtp.qq.com）
- `EMAIL_PORT`: SMTP端口号（可选，默认为587）

### DeepSeek API相关配置
- `DEEPSEEK_API_KEY`: DeepSeek API密钥

### 其他配置
- `BASE_URL`: API基础URL（可选，默认为https://api.deepseek.com/v1）

## 使用方法

1. 编辑 `.env` 文件，填入您的实际信息：
   ```
   SENDER_EMAIL=your_real_email@example.com
   SENDER_PASSWORD=your_real_password
   RECEIVER_EMAIL=receiver_email@example.com
   DEEPSEEK_API_KEY=your_actual_api_key
   ```

2. 保存文件后，运行项目中的Python脚本，它们会自动读取这些配置。

## 安全提示

- 不要将包含真实信息的 `.env` 文件提交到版本控制系统中
- 项目中已包含 `.env` 到 `.gitignore`（如果项目使用Git）
- 定期更换密码和API密钥以确保安全
- 对于生产环境，请使用更安全的密钥管理方案

## 故障排除

如果配置后仍然无法正常工作，请检查：

1. 确保 `.env` 文件位于项目根目录
2. 确保变量名称拼写正确
3. 确保值没有多余的引号或空格
4. 检查网络连接是否正常
5. 验证邮箱和API密钥是否有效