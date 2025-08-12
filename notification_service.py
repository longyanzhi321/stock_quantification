import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
import pandas as pd
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

class NotificationService:
    def __init__(self):
        """
        初始化通知服务
        """
        self.email_host = os.environ.get("EMAIL_HOST", "smtp.qq.com")
        self.email_port = int(os.environ.get("EMAIL_PORT", "587"))
        self.sender_email = os.environ.get("SENDER_EMAIL", "")
        self.sender_password = os.environ.get("SENDER_PASSWORD", "")
        self.receiver_email = os.environ.get("RECEIVER_EMAIL", "")

    def read_analysis_results(self, file_path):
        """
        读取分析结果文件
        :param file_path: 分析结果CSV文件路径
        :return: DataFrame对象
        """
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            return df
        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {e}")
            return None

    def format_analysis_results(self, df, max_items=5):
        """
        格式化分析结果为可读文本
        :param df: 包含分析结果的DataFrame
        :param max_items: 最大显示条目数，默认为5条
        :return: 格式化后的文本
        """
        if df is None or df.empty:
            return "没有分析结果可显示"

        # 限制显示的条目数
        df_limited = df.head(max_items)
        
        formatted_text = "新闻分析报告\n"
        formatted_text += "=" * 50 + "\n"
        formatted_text += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        formatted_text += f"总共分析了 {len(df)} 条新闻，显示其中 {len(df_limited)} 条:\n\n"

        for index, row in df_limited.iterrows():
            formatted_text += f"新闻 #{index + 1}:\n"
            formatted_text += "-" * 30 + "\n"
            formatted_text += f"原文摘要: {str(row['original_text'])[:200]}...\n"
            formatted_text += f"分析结果: {row['analysis']}\n\n"

        return formatted_text

    def send_email_notification(self, subject, content):
        """
        通过邮件发送通知
        :param subject: 邮件主题
        :param content: 邮件内容
        :return: 发送是否成功
        """
        if not self.sender_email or not self.sender_password or not self.receiver_email:
            print("请设置邮件相关环境变量: SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL")
            return False

        try:
            # 创建邮件对象
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = self.receiver_email
            message["Subject"] = subject

            # 添加邮件正文
            message.attach(MIMEText(content, "plain", "utf-8"))

            # 连接SMTP服务器并发送邮件
            server = smtplib.SMTP(self.email_host, self.email_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(message)
            server.quit()

            print("分析结果已通过邮件发送到您的手机")
            return True
        except Exception as e:
            print(f"发送邮件时出错: {e}")
            return False

    def send_digest_notification(self, df):
        """
        发送摘要通知，只包含关键信息
        :param df: 包含分析结果的DataFrame
        :return: 发送是否成功
        """
        if df is None or df.empty:
            content = "没有分析结果可显示"
        else:
            content = "新闻分析摘要报告\n"
            content += "=" * 30 + "\n"
            content += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            content += f"总共分析了 {len(df)} 条新闻\n\n"
            
            # 提取关键信息
            for index, row in df.iterrows():
                analysis = row['analysis']
                # 提取关键信息（简化版）
                content += f"{index+1}. {analysis[:100]}...\n"
            
            content += "\n详情请查看完整报告文件。"

        subject = f"新闻分析摘要 - {datetime.now().strftime('%Y-%m-%d')}"
        return self.send_email_notification(subject, content)


def main():
    # 初始化通知服务
    notification_service = NotificationService()

    # 获取当前目录下的所有分析结果CSV文件
    analysis_files = [f for f in os.listdir('.') if f.endswith('.csv') and 'analysis' in f]

    if not analysis_files:
        print("未找到任何分析结果文件")
        return

    print("找到以下分析结果文件:")
    for i, file in enumerate(analysis_files):
        print(f"{i + 1}. {file}")

    # 选择最新的分析文件
    latest_file = sorted(analysis_files)[-1]
    print(f"\n选择最新的分析文件: {latest_file}")

    # 读取分析结果
    df = notification_service.read_analysis_results(latest_file)
    if df is None:
        print("无法读取分析结果文件")
        return

    # 格式化分析结果（限制显示3条）
    formatted_content = notification_service.format_analysis_results(df, max_items=5)
    print("\n格式化后的分析结果:")
    print(formatted_content)

    # 发送完整版邮件通知
    subject = f"新闻分析报告 - {datetime.now().strftime('%Y-%m-%d')}"
    notification_service.send_email_notification(subject, formatted_content)
    
    # 也可以选择发送摘要版通知
    # notification_service.send_digest_notification(df)


if __name__ == "__main__":
    main()