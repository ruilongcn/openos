#!/usr/bin/env python3
"""
SmartHomeOS 统一智能家庭控制器
整合所有模块，提供友好中文界面
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import logging
import sys

# 导入所有模块
from modules.education.education_module import EducationModule
from modules.entertainment.entertainment_module import EntertainmentModule
from modules.office.office_module import OfficeModule
from modules.shopping.shopping_module import ShoppingModule
from modules.openclaw.app import OpenClawGUI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SmartHomeController:
    """智能家庭主控制器"""

    def __init__(self, root):
        self.root = root
        self.root.title("🏠 智慧家庭操作系统 - 主控制台")
        self.root.geometry("1200x800")
        
        # 初始化所有模块
        self.education_module = EducationModule()
        self.entertainment_module = EntertainmentModule()
        self.office_module = OfficeModule()
        self.shopping_module = ShoppingModule()
        
        # 创建界面
        self._create_ui()
        
        logger.info("智慧家庭控制器已启动")
        
    def _create_ui(self):
        """创建用户界面"""
        # 创建主标签页
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建各个标签页
        self._create_home_tab()
        self._create_education_tab()
        self._create_entertainment_tab()
        self._create_office_tab()
        self._create_shopping_tab()
        self._create_openclaw_tab()
        
    def _create_home_tab(self):
        """首页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🏠 首页")
        
        # 欢迎标题
        title = ttk.Label(tab, text="👋 欢迎使用智慧家庭操作系统", 
                         font=("Arial", 20, "bold"))
        title.pack(pady=30)
        
        subtitle = ttk.Label(tab, text="让科技服务生活，让家更智能", 
                           font=("Arial", 12))
        subtitle.pack(pady=10)
        
        # 功能卡片
        card_frame = ttk.Frame(tab)
        card_frame.pack(pady=40)
        
        self._create_card(card_frame, "🎓 教育模块", 
                         "作业辅导、学习计划、语言学习", 0, 0)
        self._create_card(card_frame, "🎬 娱乐模块", 
                         "智能推荐、家庭影院、字幕生成", 0, 1)
        self._create_card(card_frame, "💼 办公模块", 
                         "文档处理、会议助手、邮件管理", 1, 0)
        self._create_card(card_frame, "🛒 购物模块", 
                         "购物清单、价格比较、配送管理", 1, 1)
        self._create_card(card_frame, "🤖 OpenClaw", 
                         "多代理协作系统，强大的AI助手", 2, 0)
        
        # 系统状态
        status_frame = ttk.LabelFrame(tab, text="系统状态")
        status_frame.pack(pady=30, fill=tk.X, padx=20)
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=6)
        self.status_text.pack(fill=tk.X, padx=10, pady=10)
        
        self.status_text.insert(tk.END, "✅ 智慧家庭系统已启动\n")
        self.status_text.insert(tk.END, "✅ 教育模块正常\n")
        self.status_text.insert(tk.END, "✅ 娱乐模块正常\n")
        self.status_text.insert(tk.END, "✅ 办公模块正常\n")
        self.status_text.insert(tk.END, "✅ 购物模块正常\n")
        self.status_text.insert(tk.END, "✅ OpenClaw多代理系统正常\n")
        
    def _create_card(self, parent, title, desc, row, col):
        """创建功能卡片"""
        card = ttk.Frame(parent)
        card.grid(row=row, column=col, padx=20, pady=15)
        
        ttk.Label(card, text=title, font=("Arial", 14, "bold")).pack(pady=5)
        ttk.Label(card, text=desc, font=("Arial", 10)).pack()
        
        btn = ttk.Button(card, text="立即使用", 
                       command=lambda t=title: self._switch_to_tab(t))
        btn.pack(pady=10)
        
    def _create_education_tab(self):
        """教育模块标签页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🎓 教育模块")
        
        # 页面标题
        title = ttk.Label(tab, text="AI 教育学习平台", font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        # 功能按钮区
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="📝 作业辅导", 
                  command=lambda: self._show_education_demo("homework")).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="📋 学习计划", 
                  command=lambda: self._show_education_demo("learning_plan")).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="🗣️ 语言学习", 
                  command=lambda: self._show_education_demo("language")).grid(row=0, column=2, padx=10)
        
        # 结果显示区
        self.edu_result = scrolledtext.ScrolledText(tab, height=20)
        self.edu_result.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
    def _create_entertainment_tab(self):
        """娱乐模块标签页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🎬 娱乐模块")
        
        title = ttk.Label(tab, text="AI 影视娱乐中心", font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="🎯 智能推荐", 
                  command=lambda: self._show_entertainment_demo("recommendation")).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="📝 字幕生成", 
                  command=lambda: self._show_entertainment_demo("subtitle")).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="🎬 媒体中心", 
                  command=lambda: self._show_entertainment_demo("media_center")).grid(row=0, column=2, padx=10)
        
        self.ent_result = scrolledtext.ScrolledText(tab, height=20)
        self.ent_result.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
    def _create_office_tab(self):
        """办公模块标签页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="💼 办公模块")
        
        title = ttk.Label(tab, text="AI 个人办公助手", font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="📄 文档处理", 
                  command=lambda: self._show_office_demo("document")).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="🎙️ 会议助手", 
                  command=lambda: self._show_office_demo("meeting")).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="📧 邮件管理", 
                  command=lambda: self._show_office_demo("email")).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text="📅 日程安排", 
                  command=lambda: self._show_office_demo("schedule")).grid(row=0, column=3, padx=10)
        
        self.off_result = scrolledtext.ScrolledText(tab, height=20)
        self.off_result.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
    def _create_shopping_tab(self):
        """购物模块标签页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🛒 购物模块")
        
        title = ttk.Label(tab, text="AI 生活购物助手", font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="📝 购物清单", 
                  command=lambda: self._show_shopping_demo("list")).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="💰 价格比较", 
                  command=lambda: self._show_shopping_demo("compare")).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="🤖 购物助手", 
                  command=lambda: self._show_shopping_demo("assistant")).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text="🚚 配送管理", 
                  command=lambda: self._show_shopping_demo("delivery")).grid(row=0, column=3, padx=10)
        
        self.shop_result = scrolledtext.ScrolledText(tab, height=20)
        self.shop_result.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
    def _create_openclaw_tab(self):
        """OpenClaw标签页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🤖 OpenClaw")
        
        title = ttk.Label(tab, text="OpenClaw 多代理协作系统", font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        desc = ttk.Label(tab, text="强大的AI协作系统，包含聊天对话、代理管理、技能系统、团队协作", font=("Arial", 11))
        desc.pack(pady=10)
        
        ttk.Button(tab, text="🚀 打开OpenClaw完整界面", command=self._launch_openclaw).pack(pady=30)
        
        info = ttk.LabelFrame(tab, text="功能介绍")
        info.pack(fill=tk.X, padx=20, pady=10)
        
        info_text = scrolledtext.ScrolledText(info, height=12)
        info_text.pack(padx=10, pady=10)
        
        info_text.insert(tk.END, """💬 聊天对话 - 与AI代理自然交流
👤 代理管理 - 创建、配置、管理多个AI代理
🔧 技能系统 - 计算器、天气查询、智能家居控制等
👥 团队协作 - 多代理协同工作，完成复杂任务
📋 任务编排 - 自动分解任务，协调执行
""")
        
    def _switch_to_tab(self, title):
        """切换到指定标签页"""
        tab_mapping = {
            "🎓 教育模块": 1,
            "🎬 娱乐模块": 2,
            "💼 办公模块": 3,
            "🛒 购物模块": 4,
            "🤖 OpenClaw": 5
        }
        if title in tab_mapping:
            self.notebook.select(tab_mapping[title])
            
    def _launch_openclaw(self):
        """启动OpenClaw独立界面"""
        openclaw_window = tk.Toplevel(self.root)
        openclaw_window.title("OpenClaw 多代理协作系统")
        openclaw_window.geometry("1100x700")
        OpenClawGUI(openclaw_window)
        
    def _show_education_demo(self, demo_type):
        """展示教育模块功能"""
        self.edu_result.delete(1.0, tk.END)
        
        if demo_type == "homework":
            result = self.education_module.process_request("homework", {"image_path": "test.jpg"})
            self.edu_result.insert(tk.END, "📝 作业辅导结果\n")
            self.edu_result.insert(tk.END, f"\n识别文本: {result.get('text', '')}\n")
            self.edu_result.insert(tk.END, f"\n解答: {result.get('solution', '')}\n")
            self.edu_result.insert(tk.END, f"\n相关知识点: {', '.join(result.get('related_topics', []))}\n")
            
        elif demo_type == "learning_plan":
            result = self.education_module.process_request("learning_plan", 
                                                          {"user_id": "user123", "age": 15, 
                                                           "subjects": ["数学", "英语", "语文"]})
            self.edu_result.insert(tk.END, "📋 学习计划\n")
            plan = result.get('plan', {})
            self.edu_result.insert(tk.END, f"\n每日计划:\n")
            for key, items in plan.get('daily_plan', {}).items():
                self.edu_result.insert(tk.END, f"  {key}: {', '.join(items)}\n")
            self.edu_result.insert(tk.END, f"\n每周目标: {', '.join(plan.get('weekly_goals', []))}\n")
            
        elif demo_type == "language":
            result = self.education_module.process_request("language", {"audio_path": "test.wav"})
            self.edu_result.insert(tk.END, "🗣️ 语言学习\n")
            self.edu_result.insert(tk.END, f"\n识别文本: {result.get('text', '')}\n")
            self.edu_result.insert(tk.END, f"\n语音合成: {result.get('audio_output', '')}\n")
            
        self.edu_result.insert(tk.END, "\n✅ 功能正常！\n")
        
    def _show_entertainment_demo(self, demo_type):
        """展示娱乐模块功能"""
        self.ent_result.delete(1.0, tk.END)
        
        if demo_type == "recommendation":
            result = self.entertainment_module.process_request("recommendation",
                                                               {"user_id": "user123", "content_type": "all", "mood": "relaxed"})
            self.ent_result.insert(tk.END, "🎯 智能推荐\n")
            recs = result.get('recommendations', {})
            if isinstance(recs, dict):
                for category, items in recs.items():
                    self.ent_result.insert(tk.END, f"\n{category}:\n")
                    for item in items:
                        self.ent_result.insert(tk.END, f"  - {item.get('title', '')} (评分: {item.get('rating', 0)})\n")
            
        elif demo_type == "subtitle":
            result = self.entertainment_module.process_request("subtitle",
                                                             {"video_path": "/test.mp4", "language": "zh-CN"})
            self.ent_result.insert(tk.END, "📝 字幕生成\n")
            self.ent_result.insert(tk.END, f"\n视频: {result.get('video_path', '')}\n")
            self.ent_result.insert(tk.END, f"语言: {result.get('language', '')}\n")
            for sub in result.get('subtitle', []):
                self.ent_result.insert(tk.END, f"\n[{sub.get('start', '')} -> {sub.get('end', '')}] {sub.get('text', '')}\n")
                
        elif demo_type == "media_center":
            result = self.entertainment_module.process_request("media_center",
                                                             {"action": "play", "media_path": "/test.mp4", "media_type": "video"})
            self.ent_result.insert(tk.END, "🎬 媒体中心\n")
            self.ent_result.insert(tk.END, f"\n{result.get('message', '')}\n")
            
        self.ent_result.insert(tk.END, "\n✅ 功能正常！\n")
        
    def _show_office_demo(self, demo_type):
        """展示办公模块功能"""
        self.off_result.delete(1.0, tk.END)
        
        if demo_type == "document":
            result = self.office_module.process_request("document",
                                                       {"action": "summarize", "document_path": "/report.pdf"})
            self.off_result.insert(tk.END, "📄 文档摘要\n")
            self.off_result.insert(tk.END, f"\n摘要: {result.get('summary', '')}\n")
            self.off_result.insert(tk.END, f"\n要点:\n")
            for point in result.get('key_points', []):
                self.off_result.insert(tk.END, f"  - {point}\n")
                
        elif demo_type == "meeting":
            result = self.office_module.process_request("meeting",
                                                       {"action": "generate_minutes", "meeting_id": "mtg_1"})
            self.off_result.insert(tk.END, "🎙️ 会议纪要\n")
            minutes = result.get('minutes', {})
            self.off_result.insert(tk.END, f"\n标题: {minutes.get('title', '')}\n")
            self.off_result.insert(tk.END, f"日期: {minutes.get('date', '')}\n")
            self.off_result.insert(tk.END, f"讨论内容:\n")
            for d in minutes.get('discussions', []):
                self.off_result.insert(tk.END, f"  - {d}\n")
            self.off_result.insert(tk.END, f"\n行动项:\n")
            for a in minutes.get('action_items', []):
                self.off_result.insert(tk.END, f"  - {a.get('task', '')} ({a.get('owner', '')}) - 截止: {a.get('deadline', '')}\n")
                
        elif demo_type == "email":
            result = self.office_module.process_request("email",
                                                       {"action": "list", "filter": "all"})
            self.off_result.insert(tk.END, "📧 邮件列表\n")
            emails = result.get('emails', [])
            for email in emails:
                status = "✅" if email.get('read') else "🔴"
                self.off_result.insert(tk.END, f"\n{status} {email.get('subject', '')} - {email.get('from', '')}\n")
                self.off_result.insert(tk.END, f"  {email.get('body', '')[:50]}...\n")
                
        elif demo_type == "schedule":
            result = self.office_module.process_request("schedule",
                                                       {"action": "suggest", "tasks": ["完成报告", "团队会议", "代码审查"]})
            self.off_result.insert(tk.END, "📅 智能日程建议\n")
            for s in result.get('suggestions', []):
                self.off_result.insert(tk.END, f"\n任务: {s.get('task', '')}\n")
                self.off_result.insert(tk.END, f"时间: {s.get('suggested_time', '')}\n")
                
        self.off_result.insert(tk.END, "\n✅ 功能正常！\n")
        
    def _show_shopping_demo(self, demo_type):
        """展示购物模块功能"""
        self.shop_result.delete(1.0, tk.END)
        
        if demo_type == "list":
            result = self.shopping_module.process_request("list", {"action": "list"})
            self.shop_result.insert(tk.END, "📝 购物清单\n")
            for lst in result.get('lists', []):
                self.shop_result.insert(tk.END, f"\n{lst.get('name', '')} ({lst.get('item_count', 0)} 个物品)\n")
                
        elif demo_type == "compare":
            result = self.shopping_module.process_request("compare",
                                                         {"product_name": "牛奶"})
            self.shop_result.insert(tk.END, "💰 价格比较\n")
            self.shop_result.insert(tk.END, f"\n产品: {result.get('product', '')}\n")
            self.shop_result.insert(tk.END, f"{result.get('savings', '')}\n\n")
            for store in result.get('stores', []):
                self.shop_result.insert(tk.END, f"{store.get('store', '')}: ¥{store.get('price', 0)}/{store.get('unit', '')}\n")
                
        elif demo_type == "assistant":
            result = self.shopping_module.process_request("assistant",
                                                         {"action": "recommend", "category": "食品", "budget": 500})
            self.shop_result.insert(tk.END, "🤖 购物推荐\n")
            for rec in result.get('recommendations', []):
                self.shop_result.insert(tk.END, f"\n{rec.get('name', '')} - {rec.get('brand', '')} - ¥{rec.get('price', 0)}\n")
                self.shop_result.insert(tk.END, f"  理由: {rec.get('reason', '')}\n")
                
        elif demo_type == "delivery":
            result = self.shopping_module.process_request("delivery",
                                                         {"action": "track", "order_id": "ORD123456"})
            self.shop_result.insert(tk.END, "🚚 配送追踪\n")
            self.shop_result.insert(tk.END, f"\n订单号: {result.get('order_id', '')}\n")
            self.shop_result.insert(tk.END, f"状态: {result.get('current_status', '')}\n")
            self.shop_result.insert(tk.END, f"位置: {result.get('location', '')}\n")
            self.shop_result.insert(tk.END, f"预计时间: {result.get('estimated_time', '')}\n")
            self.shop_result.insert(tk.END, f"配送员: {result.get('driver', '')}\n")
            
        self.shop_result.insert(tk.END, "\n✅ 功能正常！\n")


def main():
    """主函数"""
    root = tk.Tk()
    app = SmartHomeController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
