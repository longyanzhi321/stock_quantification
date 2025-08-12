# 邮箱配置说明

本项目使用环境变量来配置邮箱服务，以便将新闻分析结果通过邮件发送到指定邮箱。

## 需要配置的环境变量

以下环境变量需要配置以启用邮件通知功能：

- `SENDER_EMAIL`: 发送者邮箱地址
- `SENDER_PASSWORD`: 发送者邮箱密码或应用专用密码
- `RECEIVER_EMAIL`: 接收者邮箱地址
- `EMAIL_HOST`: SMTP服务器地址（可选，默认为smtp.qq.com）
- `EMAIL_PORT`: SMTP端口号（可选，默认为587）

## 配置方法

### Windows系统配置方法

1. 打开命令提示符（CMD）或PowerShell
2. 使用以下命令设置环境变量：
   ```cmd
   setx SENDER_EMAIL "your_email@gmail.com"
   setx SENDER_PASSWORD "your_password"
   setx RECEIVER_EMAIL "receiver@example.com"
   ```

### Linux/macOS系统配置方法

1. 打开终端
2. 编辑 `~/.bashrc` 或 `~/.zshrc` 文件：
   ```bash
   export SENDER_EMAIL="your_email@gmail.com"
   export SENDER_PASSWORD="your_password"
   export RECEIVER_EMAIL="receiver@example.com"
   ```
3. 重新加载配置文件：
   ```bash
   source ~/.bashrc
   ```

### 使用 .env 文件（推荐）

您也可以创建一个 `.env` 文件来配置这些变量：

1. 在项目根目录创建 `.env` 文件
2. 添加以下内容：
   ```
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_password
   RECEIVER_EMAIL=receiver@example.com
   EMAIL_HOST=smtp.qq.com
   EMAIL_PORT=587
   ```

## 常见邮箱服务商SMTP配置

### Gmail
- SMTP服务器: smtp.gmail.com
- 端口: 587 (TLS) 或 465 (SSL)
- 需要开启"两步验证"并使用"应用专用密码"

### QQ邮箱
- SMTP服务器: smtp.qq.com
- 端口: 587 (TLS) 或 465 (SSL)
- 密码为授权码，不是邮箱密码

### 163/126邮箱
- SMTP服务器: smtp.163.com 或 smtp.126.com
- 端口: 25 或 465 (SSL)
- 密码为授权码，不是邮箱密码

### Outlook/Hotmail
- SMTP服务器: smtp-mail.outlook.com
- 端口: 587 (TLS)

## 安全提示

1. 不要在代码中硬编码邮箱密码
2. 使用应用专用密码而不是账户密码
3. 妥善保管环境变量，避免泄露敏感信息
4. 定期更换密码和应用专用密码

## 测试配置

配置完成后，可以运行以下命令测试邮箱配置是否正确：

```bash
python notification_service.py
```

系统会自动寻找最新的分析结果文件并通过邮件发送。

## 故障排除

如果邮件发送失败，请按以下步骤排查：

1. 检查环境变量是否正确设置
2. 验证邮箱账号和密码是否正确
3. 确认SMTP服务器地址和端口是否正确
4. 检查网络连接是否正常
5. 确认邮箱是否开启了SMTP服务
6. 查看控制台输出的错误信息

对于QQ邮箱，需要特别注意：
- 使用授权码而非邮箱密码
- 确保已开启SMTP服务
- 可能需要在QQ邮箱设置中添加发送方到白名单