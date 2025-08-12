#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PY_NEWS_AI 主程序入口
该脚本将依次运行所有模块：网页爬虫、文本分析、通知服务
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

def run_module(module_name, module_file):
    """
    运行指定的模块
    :param module_name: 模块名称
    :param module_file: 模块文件名
    """
    print(f"\n{'='*50}")
    print(f"正在运行 {module_name}...")
    print(f"{'='*50}")
    
    if not os.path.exists(module_file):
        print(f"错误: 找不到 {module_file} 文件")
        return False
    
    try:
        # 使用subprocess运行模块
        result = subprocess.run([sys.executable, module_file], 
                              capture_output=True, 
                              text=True, 
                              timeout=300)  # 5分钟超时
        
        if result.returncode == 0:
            print(f"{module_name} 运行成功")
            if result.stdout:
                print(f"{module_name} 输出:")
                print(result.stdout)
            return True
        else:
            print(f"{module_name} 运行失败")
            if result.stderr:
                print(f"错误信息:")
                print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"{module_name} 运行超时")
        return False
    except Exception as e:
        print(f"{module_name} 运行时发生异常: {e}")
        return False

def main():
    """
    主函数：依次运行所有模块
    """
    print("PY_NEWS_AI 一体化运行程序")
    print("该程序将依次执行：网页爬虫 -> 文本分析 -> 通知服务")
    
    # 检查必要文件是否存在
    required_files = ['web_scraper.py', 'text_analyse.py', 'notification_service.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"错误: 缺少以下必要文件: {', '.join(missing_files)}")
        sys.exit(1)
    
    # 依次运行各模块
    modules = [
        ("网页爬虫模块", "web_scraper.py"),
        ("文本分析模块", "text_analyse.py"),
        ("通知服务模块", "notification_service.py")
    ]
    
    success_count = 0
    for module_name, module_file in modules:
        if run_module(module_name, module_file):
            success_count += 1
        else:
            print(f"警告: {module_name} 运行失败，将继续执行后续模块")
    
    # 输出总结
    print(f"\n{'='*50}")
    print("执行总结")
    print(f"{'='*50}")
    print(f"成功运行 {success_count}/{len(modules)} 个模块")
    
    if success_count == len(modules):
        print("所有模块均已成功运行！")
    else:
        print("部分模块运行失败，请查看上方错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main()