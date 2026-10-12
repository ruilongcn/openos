#!/usr/bin/env python3
"""
SmartHomeOS OpenClaw - GUI界面应用程序
"""

import os
import sys
import logging
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog, messagebox
from typing import Dict, Optional

# 添加项目根目录到Python路径
current_file = os.path.abspath(__file__)
core_dir = os.path.dirname(current_file)
root_dir = os.path.dirname(core_dir)
sys.path.insert(0, root_dir)

from .core import OpenClawCore, AgentConfig, AgentState, AgentRole
from .skills import SkillRegistry
from .collaboration import (
    MultiAgentOrchestrator, CollaborationMode,
    AgentTeamCoordinator, AgentToAgentProtocol, Task
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenClawGUI:
    """OpenClaw主GUI界面"""

    def __init__(self, root):
        self.root = root
        self.root.title("智慧家庭OS - OpenClaw多代理协作系统")
        self.root.geometry("1200x800")

        # 初始化核心
        self.core = OpenClawCore()
        self.skill_registry = SkillRegistry()
        self.orchestrator = MultiAgentOrchestrator(self.core)

        # 注册技能到核心
        for name, skill in self.skill_registry.skills.items():
            self.core.register_skill(skill)

        # 当前选中的Agent
        self.current_agent = None

        # 创建界面
        self._create_menu()
        self._create_main_layout()

        # 刷新状态
        self._refresh_agents_list()

        logger.info("OpenClawGUI initialized")

    def _create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="新建代理", command=self._show_new_agent_dialog)
        file_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=file_menu)

        # 视图菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="刷新代理列表", command=self._refresh_agents_list)
        menubar.add_cascade(label="视图", menu=view_menu)

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self._show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)

        self.root.config(menu=menubar)

    def _create_main_layout(self):
        """创建主布局"""
        # 主框架
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 左侧 - Agent面板
        left_frame = ttk.Frame(main_paned, width=300)
        main_paned.add(left_frame)

        ttk.Label(left_frame, text="代理列表", font=('Arial', 12, 'bold')).pack(pady=5)

        # Agent列表
        self.agent_listbox = tk.Listbox(left_frame, height=15)
        self.agent_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.agent_listbox.bind('<<ListboxSelect>>', self._on_agent_select)

        # Agent操作按钮
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(btn_frame, text="新建", command=self._show_new_agent_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="启动", command=self._start_selected_agent).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="停止", command=self._stop_selected_agent).pack(side=tk.LEFT, padx=2)

        # 右侧 - 主内容区
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame)

        # 标签页
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # 聊天标签页
        self.chat_frame = self._create_chat_tab()
        self.notebook.add(self.chat_frame, text="聊天对话")

        # Agent管理标签页
        self.agent_mgmt_frame = self._create_agent_mgmt_tab()
        self.notebook.add(self.agent_mgmt_frame, text="代理管理")

        # 技能标签页
        self.skills_frame = self._create_skills_tab()
        self.notebook.add(self.skills_frame, text="技能系统")

        # 团队协作标签页
        self.team_frame = self._create_team_tab()
        self.notebook.add(self.team_frame, text="团队协作")

    def _create_chat_tab(self) -> ttk.Frame:
        """创建聊天标签页"""
        frame = ttk.Frame()

        # 对话历史
        ttk.Label(frame, text="对话历史", font=('Arial', 10, 'bold')).pack(anchor='w', padx=5, pady=5)

        self.chat_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=20)
        self.chat_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.chat_text.config(state=tk.DISABLED)

        # 输入区
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(input_frame, text="消息:").pack(side=tk.LEFT)

        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.input_entry.bind('<Return>', lambda e: self._send_message())

        ttk.Button(input_frame, text="发送", command=self._send_message).pack(side=tk.LEFT)

        # 快捷按钮
        quick_frame = ttk.Frame(frame)
        quick_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(quick_frame, text="你好！", command=lambda: self._quick_message("你好！")).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_frame, text="查询天气", command=lambda: self._quick_message("查询今天的天气怎么样？")).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_frame, text="智能家居控制", command=lambda: self._quick_message("请帮我控制家里的智能设备。")).pack(side=tk.LEFT, padx=2)

        return frame

    def _create_agent_mgmt_tab(self) -> ttk.Frame:
        """创建Agent管理标签页"""
        frame = ttk.Frame()

        # 信息面板
        info_frame = ttk.LabelFrame(frame, text="代理信息")
        info_frame.pack(fill=tk.X, padx=5, pady=5)

        self.agent_info_text = scrolledtext.ScrolledText(info_frame, height=10, wrap=tk.WORD)
        self.agent_info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 操作按钮
        btn_frame = ttk.Frame(info_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(btn_frame, text="启动", command=self._start_selected_agent).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="停止", command=self._stop_selected_agent).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="暂停", command=self._pause_selected_agent).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="恢复", command=self._resume_selected_agent).pack(side=tk.LEFT, padx=2)

        return frame

    def _create_skills_tab(self) -> ttk.Frame:
        """创建技能标签页"""
        frame = ttk.Frame()

        # 技能列表
        ttk.Label(frame, text="可用技能", font=('Arial', 10, 'bold')).pack(anchor='w', padx=5, pady=5)

        self.skills_listbox = tk.Listbox(frame, height=10)
        self.skills_listbox.pack(fill=tk.X, padx=5, pady=5)

        # 技能说明
        skill_desc_frame = ttk.LabelFrame(frame, text="技能说明")
        skill_desc_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.skill_desc_text = scrolledtext.ScrolledText(skill_desc_frame, height=8, wrap=tk.WORD)
        self.skill_desc_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 刷新技能列表
        self._refresh_skills_list()
        self.skills_listbox.bind('<<ListboxSelect>>', self._on_skill_select)

        return frame

    def _create_team_tab(self) -> ttk.Frame:
        """创建团队协作标签页"""
        frame = ttk.Frame()

        # 顶部按钮
        top_frame = ttk.Frame(frame)
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(top_frame, text="创建团队", command=self._show_create_team_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(top_frame, text="启动任务编排", command=self._show_orchestrate_dialog).pack(side=tk.LEFT, padx=2)

        # 团队列表
        ttk.Label(frame, text="团队列表", font=('Arial', 10, 'bold')).pack(anchor='w', padx=5, pady=5)

        self.team_listbox = tk.Listbox(frame, height=8)
        self.team_listbox.pack(fill=tk.X, padx=5, pady=5)

        # 协作日志
        ttk.Label(frame, text="协作日志", font=('Arial', 10, 'bold')).pack(anchor='w', padx=5, pady=5)

        self.collab_log = scrolledtext.ScrolledText(frame, height=10, wrap=tk.WORD)
        self.collab_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        return frame

    def _refresh_agents_list(self):
        """刷新Agent列表"""
        self.agent_listbox.delete(0, tk.END)

        # 角色名称翻译
        role_translation = {
            'GENERIC': '通用助手',
            'MANAGER': '管理员',
            'WORKER': '工作者',
            'RESEARCHER': '研究员',
            'ANALYST': '分析师',
            'COORDINATOR': '协调员'
        }

        for agent in self.core.list_agents():
            state_emoji = "🟢" if agent['state'] == 'RUNNING' else "🔴" if agent['state'] == 'STOPPED' else "🟡"
            role_display = role_translation.get(agent['role'], agent['role'])
            display_text = f"{state_emoji} {agent['name']} ({role_display}) - {agent['total_messages']} 条消息"
            self.agent_listbox.insert(tk.END, display_text)
            self.agent_listbox.itemconfig(tk.END, tags=(agent['agent_id'],))

    def _refresh_skills_list(self):
        """刷新技能列表"""
        self.skills_listbox.delete(0, tk.END)

        # 技能名称和描述翻译
        skill_translation = {
            'calculator': ('计算器', '执行基本数学计算'),
            'web_search': ('网页搜索', '搜索互联网获取信息'),
            'file_system': ('文件系统', '读写和管理本地文件'),
            'weather': ('天气查询', '查询天气信息'),
            'home_control': ('智能家居控制', '控制家庭智能设备'),
            'news': ('新闻查询', '获取最新新闻资讯'),
            'reminder': ('提醒功能', '管理提醒事项')
        }

        for skill in self.skill_registry.list_skills():
            name, desc = skill_translation.get(skill['name'], (skill['name'], skill['description']))
            display_text = f"⚙️ {name} - {desc}"
            self.skills_listbox.insert(tk.END, display_text)

    def _on_agent_select(self, event):
        """选中Agent事件"""
        selection = self.agent_listbox.curselection()
        if not selection:
            return

        idx = selection[0]
        agents = self.core.list_agents()
        if idx < len(agents):
            self.current_agent = agents[idx]['agent_id']
            self._update_agent_info()

    def _on_skill_select(self, event):
        """选中技能事件"""
        selection = self.skills_listbox.curselection()
        if not selection:
            return

        idx = selection[0]
        skills = self.skill_registry.list_skills()
        if idx < len(skills):
            skill = skills[idx]
            
            # 翻译
            skill_translation = {
                'calculator': ('计算器', '执行基本数学计算'),
                'web_search': ('网页搜索', '搜索互联网获取信息'),
                'file_system': ('文件系统', '读写和管理本地文件'),
                'weather': ('天气查询', '查询天气信息'),
                'home_control': ('智能家居控制', '控制家庭智能设备'),
                'news': ('新闻查询', '获取最新新闻资讯'),
                'reminder': ('提醒功能', '管理提醒事项')
            }
            
            name, desc = skill_translation.get(skill['name'], (skill['name'], skill['description']))
            
            self.skill_desc_text.delete(1.0, tk.END)
            self.skill_desc_text.insert(tk.END, f"技能名称: {name}\n")
            self.skill_desc_text.insert(tk.END, f"功能描述: {desc}\n")
            self.skill_desc_text.insert(tk.END, f"版本: {skill.get('version', '1.0')}\n")

    def _update_agent_info(self):
        """更新Agent信息"""
        if not self.current_agent:
            return

        agent = self.core.get_agent(self.current_agent)
        if not agent:
            return

        # 翻译
        role_translation = {
            'GENERIC': '通用助手',
            'MANAGER': '管理员',
            'WORKER': '工作者',
            'RESEARCHER': '研究员',
            'ANALYST': '分析师',
            'COORDINATOR': '协调员'
        }
        
        state_translation = {
            'CREATED': '已创建',
            'INITIALIZING': '初始化中',
            'RUNNING': '运行中',
            'PAUSED': '已暂停',
            'STOPPED': '已停止',
            'ERROR': '错误'
        }

        role_display = role_translation.get(agent.config.role.name, agent.config.role.name)
        state_display = state_translation.get(agent.state.name, agent.state.name)

        self.agent_info_text.delete(1.0, tk.END)
        self.agent_info_text.insert(tk.END, f"代理ID: {agent.config.agent_id}\n")
        self.agent_info_text.insert(tk.END, f"名称: {agent.config.name}\n")
        self.agent_info_text.insert(tk.END, f"角色: {role_display}\n")
        self.agent_info_text.insert(tk.END, f"状态: {state_display}\n")
        self.agent_info_text.insert(tk.END, f"模型: {agent.config.model}\n")
        self.agent_info_text.insert(tk.END, f"总消息数: {agent.total_messages}\n")
        if agent.start_time:
            self.agent_info_text.insert(tk.END, f"启动时间: {agent.start_time}\n")

    def _show_new_agent_dialog(self):
        """显示新建Agent对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("创建新代理")
        dialog.geometry("500x400")

        # 表单
        ttk.Label(dialog, text="代理名称:").pack(anchor='w', padx=10, pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.pack(fill=tk.X, padx=10, pady=2)

        ttk.Label(dialog, text="角色:").pack(anchor='w', padx=10, pady=5)
        role_combo = ttk.Combobox(dialog, values=[
            'GENERIC (通用助手)', 
            'MANAGER (管理员)', 
            'WORKER (工作者)',
            'RESEARCHER (研究员)',
            'ANALYST (分析师)',
            'COORDINATOR (协调员)'
        ])
        role_combo.current(0)
        role_combo.pack(fill=tk.X, padx=10, pady=2)

        ttk.Label(dialog, text="系统提示词:").pack(anchor='w', padx=10, pady=5)
        prompt_text = scrolledtext.ScrolledText(dialog, height=10)
        prompt_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=2)
        prompt_text.insert(tk.END, "你是一个乐于助人的助手。")

        def create_agent():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("错误", "请输入代理名称")
                return

            role_str = role_combo.get().split(' ')[0]
            role = AgentRole[role_str]
            prompt = prompt_text.get(1.0, tk.END).strip()

            config = AgentConfig(
                agent_id=f"agent_{len(self.core.agents) + 1}",
                name=name,
                role=role,
                system_prompt=prompt,
                skills=[s['name'] for s in self.skill_registry.list_skills()]
            )

            agent = self.core.create_agent(config)
            if agent:
                self._refresh_agents_list()
                dialog.destroy()
                messagebox.showinfo("成功", f"代理 {name} 创建成功！")

        ttk.Button(dialog, text="创建", command=create_agent).pack(pady=10)

    def _start_selected_agent(self):
        """启动选中的Agent"""
        if not self.current_agent:
            messagebox.showwarning("警告", "请先选择一个代理")
            return

        if self.core.start_agent(self.current_agent):
            self._refresh_agents_list()
            self._update_agent_info()
            self._append_chat_text("系统", f"代理 {self.current_agent} 已启动！")

    def _stop_selected_agent(self):
        """停止选中的Agent"""
        if not self.current_agent:
            messagebox.showwarning("警告", "请先选择一个代理")
            return

        if self.core.stop_agent(self.current_agent):
            self._refresh_agents_list()
            self._update_agent_info()
            self._append_chat_text("系统", f"代理 {self.current_agent} 已停止")

    def _pause_selected_agent(self):
        """暂停选中的Agent"""
        if not self.current_agent:
            return

        if self.core.pause_agent(self.current_agent):
            self._refresh_agents_list()
            self._update_agent_info()

    def _resume_selected_agent(self):
        """恢复选中的Agent"""
        if not self.current_agent:
            return

        if self.core.resume_agent(self.current_agent):
            self._refresh_agents_list()
            self._update_agent_info()

    def _send_message(self):
        """发送消息"""
        if not self.current_agent:
            messagebox.showwarning("警告", "请先选择一个代理！")
            return

        message = self.input_entry.get().strip()
        if not message:
            return

        # 显示用户消息
        self._append_chat_text("你", message)
        self.input_entry.delete(0, tk.END)

        # 发送给Agent
        response = self.core.send_message_to_agent(self.current_agent, message)

        # 显示响应
        if response:
            self._append_chat_text(self.current_agent, response)
        else:
            self._append_chat_text("系统", "未收到响应")

    def _quick_message(self, message: str):
        """快速消息"""
        if not self.current_agent:
            messagebox.showwarning("警告", "请先选择一个代理！")
            return
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, message)

    def _append_chat_text(self, sender: str, text: str):
        """追加聊天文本"""
        sender_translation = {
            'You': '你',
            'System': '系统'
        }
        display_sender = sender_translation.get(sender, sender)
        
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, f"\n{display_sender}:\n{text}\n")
        self.chat_text.see(tk.END)
        self.chat_text.config(state=tk.DISABLED)

    def _show_create_team_dialog(self):
        """显示创建团队对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("创建团队")
        dialog.geometry("400x300")

        ttk.Label(dialog, text="团队名称:").pack(padx=10, pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.pack(padx=10, pady=5)

        ttk.Label(dialog, text="选择代理成员:").pack(anchor='w', padx=10, pady=5)

        agents_listbox = tk.Listbox(dialog, selectmode=tk.MULTIPLE, height=10)
        agents_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        for agent in self.core.list_agents():
            agents_listbox.insert(tk.END, agent['agent_id'])

        def create_team():
            team_name = name_entry.get().strip()
            if not team_name:
                return

            selection = agents_listbox.curselection()
            members = [agents_listbox.get(i) for i in selection]

            team = self.orchestrator.team_coordinator.create_team(
                f"team_{len(self.orchestrator.team_coordinator.teams) + 1}",
                team_name
            )

            for member in members:
                self.orchestrator.team_coordinator.add_member(team.team_id, member)

            if members:
                self.orchestrator.team_coordinator.set_leader(team.team_id, members[0])

            self.collab_log.insert(tk.END, f"已创建团队 {team_name}，共 {len(members)} 名成员\n")
            self.team_listbox.insert(tk.END, f"👥 {team_name} - {len(members)} 名成员")

            dialog.destroy()

        ttk.Button(dialog, text="创建", command=create_team).pack(pady=10)

    def _show_orchestrate_dialog(self):
        """显示编排对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("多代理任务编排")
        dialog.geometry("600x400")

        ttk.Label(dialog, text="任务描述:").pack(anchor='w', padx=10, pady=5)
        task_text = scrolledtext.ScrolledText(dialog, height=5)
        task_text.pack(fill=tk.X, padx=10, pady=5)
        task_text.insert(tk.END, "构建一个综合智能家居自动化系统")

        ttk.Label(dialog, text="协作模式:").pack(anchor='w', padx=10, pady=5)
        mode_combo = ttk.Combobox(dialog, values=[
            'SUBAGENT (子代理模式)',
            'TEAM (团队协作模式)',
            'AGENT_TO_AGENT (代理间通信模式)'
        ])
        mode_combo.current(0)
        mode_combo.pack(fill=tk.X, padx=10, pady=5)

        def start_orchestration():
            task_desc = task_text.get(1.0, tk.END).strip()
            mode_str = mode_combo.get().split(' ')[0]
            mode = CollaborationMode[mode_str]

            self.collab_log.insert(tk.END, f"\n=== 开始任务编排 ===\n")
            self.collab_log.insert(tk.END, f"任务: {task_desc[:50]}...\n")
            self.collab_log.insert(tk.END, f"模式: {mode_str}\n")

            result = self.orchestrator.orchestrate_complex_task(task_desc, mode)
            self.collab_log.insert(tk.END, f"状态: {result['status']}\n")
            self.collab_log.insert(tk.END, f"子任务数: {len(result['subtasks'])}\n")
            self.collab_log.see(tk.END)

        ttk.Button(dialog, text="开始！", command=start_orchestration).pack(pady=20)

    def _show_about(self):
        """显示关于"""
        messagebox.showinfo(
            "关于", 
            "智慧家庭OS - OpenClaw多代理协作平台\n"
            "基于多代理的智能协作系统\n"
            "版本 1.0"
        )


def main():
    """主函数"""
    root = tk.Tk()
    app = OpenClawGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
