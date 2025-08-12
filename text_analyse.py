import pandas as pd
import os
from openai import OpenAI
import csv
from datetime import datetime
import sys
from typing import List, Dict, Any, Optional
import subprocess
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()


def api_key():
    # 从环境变量获取API密钥，如果不存在则要求用户输入
    api = os.getenv("DEEPSEEK_API_KEY")
    if not api:
        api = input("请输入您的DeepSeek API密钥：")
    return api


class TextAnalyzer:
    def __init__(self, api_key, base_url="https://api.deepseek.com/v1"):
        """
        初始化文本分析器
        :param api_key: DeepSeek API密钥
        :param base_url: DeepSeek API基础URL
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

    def read_csv_file(self, file_path):
        """
        读取CSV文件
        :param file_path: CSV文件路径
        :return: DataFrame对象
        """
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            return df
        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {e}")
            return None

    def analyze_text_with_deepseek(self, text: str, prompt_template: Optional[str] = None) -> Optional[str]:
        """
        使用DeepSeek大模型分析文本
        :param text: 要分析的文本
        :param prompt_template: 提示模板
        :return: 分析结果
        """
        if not prompt_template:
            prompt_template = """
            请分析以下新闻文本内容，提供以下信息：
            1. 主要事件或主题
            2. 涉及的公司或机构
            3. 情感倾向（正面、负面或中性）
            4. 重要日期或时间信息
            5. 关键数字或数据
            
            新闻内容：
            {text}
            
            请以简洁明了的中文总结。
            """

        prompt = prompt_template.format(text=text)

        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的新闻分析助手，能够准确提取和分析新闻中的关键信息。"},
                    {"role": "user", "content": prompt}
                ],
                stream=False)
            return response.choices[0].message.content
        except Exception as e:
            print(f"调用DeepSeek API时出错: {e}")
            return None

    def analyze_csv_file(self, file_path, prompt_template=None, max_rows=5):
        """
        分析CSV文件中的文本内容
        :param file_path: CSV文件路径
        :param prompt_template: 提示模板
        :param max_rows: 最大分析行数，避免API调用过多，默认为5条
        :return: 分析结果列表
        """
        df = self.read_csv_file(file_path)
        if df is None:
            return None

        results = []
        # 限制分析的行数，避免产生过多数据
        for index, row in df.head(max_rows).iterrows():
            print(f"正在分析第 {index + 1} 条新闻...")
            text = row['text']
            if text and isinstance(text, str) and len(text.strip()) > 0:
                analysis = self.analyze_text_with_deepseek(text, prompt_template)
                if analysis:
                    results.append({
                        'original_text': text,
                        'analysis': analysis
                    })
                else:
                    results.append({
                        'original_text': text,
                        'analysis': '分析失败'
                    })
            else:
                results.append({
                    'original_text': text,
                    'analysis': '原文为空或无效'
                })

        return results

    def save_analysis_to_csv(self, results, origin_filename):
        """
        将分析结果保存到CSV文件
        :param results: 分析结果列表
        :param origin_filename: 原始文件名
        :return: 保存的文件名
        """
        if not results:
            return None

        # 生成新文件名
        base_name = os.path.splitext(origin_filename)[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{base_name}_analysis_{timestamp}.csv"

        with open(new_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['original_text', 'analysis']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for result in results:
                # 确保文本内容不会太长导致CSV写入问题
                result['original_text'] = str(result['original_text'])[:32767] if result['original_text'] else ""
                result['analysis'] = str(result['analysis'])[:32767] if result['analysis'] else ""
                writer.writerow(result)

        return new_filename

    def notify_analysis_completion(self, analysis_file):
        """
        通知分析完成
        :param analysis_file: 分析结果文件名
        """
        try:
            # 检查notification_service.py文件是否存在
            if os.path.exists('notification_service.py'):
                # 调用通知服务发送分析结果到手机
                subprocess.run([sys.executable, 'notification_service.py'], check=True)
                print("已尝试发送分析结果到您的手机")
            else:
                print("未找到通知服务，跳过发送到手机的步骤")
        except Exception as e:
            print(f"通知服务执行出错: {e}")


def main():
    # 使用示例
    API_KEY = os.environ.get("DEEPSEEK_API_KEY") or f"{api_key()}"
    if API_KEY == "your_deepseek_api_key_here":
        print("请设置DEEPSEEK_API_KEY环境变量或在代码中直接设置API_KEY")
        sys.exit(1)

    # 初始化分析器
    analyzer = TextAnalyzer(API_KEY)

    # 获取当前目录下的所有CSV文件
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and 'analysis' not in f]

    if not csv_files:
        print("未找到任何CSV文件")
        return None

    print("找到以下CSV文件:")
    for i, file in enumerate(csv_files):
        print(f"{i + 1}. {file}")

    # 分析每个CSV文件
    for file in csv_files:
        print(f"\n正在分析文件: {file}")
        # 进一步减少分析条目数到3条，以减少数据量
        results = analyzer.analyze_csv_file(file, max_rows=5)

        if results:
            output_file = analyzer.save_analysis_to_csv(results, file)
            if output_file:
                print(f"分析完成，结果已保存到: {output_file}")
                # 添加通知功能
                analyzer.notify_analysis_completion(output_file)
            else:
                print("保存分析结果时出错")
        else:
            print("分析过程中出现错误")


if __name__ == "__main__":
    main()
