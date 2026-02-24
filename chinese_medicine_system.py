import sqlite3
from collections import Counter

# 尝试导入matplotlib，如果失败则跳过可视化
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("警告：matplotlib库未安装，将跳过可视化功能")

# 设置中文字体，避免可视化时中文乱码
if MATPLOTLIB_AVAILABLE:
    plt.rcParams["font.family"] = ["SimHei", "Arial Unicode MS", "DejaVu Sans"]
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    plt.rcParams["font.size"] = 12  # 设置默认字体大小
    plt.rcParams["axes.titleweight"] = "bold"  # 标题加粗
    plt.rcParams["axes.labelweight"] = "medium"  # 标签中等粗细
    plt.rcParams["axes.facecolor"] = "#f8f9fa"  # 背景色
    plt.rcParams["figure.facecolor"] = "#ffffff"  # 画布色

class ChineseMedicineSystem:
    def __init__(self, db_name="chinese_medicine.db"):
        """初始化数据库连接并创建表"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._connect_db()
        self._create_table()

    def _connect_db(self):
        """建立数据库连接"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"成功连接到数据库: {self.db_name}")
        except sqlite3.Error as e:
            print(f"数据库连接失败: {e}")

    def _create_table(self):
        """创建中药信息表"""
        create_sql = """
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,          -- 中药名称
            property TEXT NOT NULL,             -- 性味（如：甘温）
            channel TEXT NOT NULL,              -- 归经（如：脾、胃经）
            efficacy TEXT NOT NULL,             -- 功效（如：补气健脾）
            usage TEXT,                         -- 用法用量
            source TEXT                         -- 药材来源
        );
        """
        try:
            self.cursor.execute(create_sql)
            self.conn.commit()
            print("中药信息表创建/检查完成")
        except sqlite3.Error as e:
            print(f"创建表失败: {e}")



    def search_medicine(self, name=None, property_keyword=None, efficacy_keyword=None):
        """
        多条件检索中药信息
        :param name: 中药名称（精确/模糊）
        :param property_keyword: 性味关键词（如：温、甘）
        :param efficacy_keyword: 功效关键词（如：补气、清热解毒）
        :return: 检索结果列表（字典格式）
        """
        try:
            # 先获取所有数据
            self.cursor.execute("SELECT * FROM medicines")
            columns = [desc[0] for desc in self.cursor.description]
            all_medicines = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            
            # 在Python中进行过滤
            filtered_medicines = []
            for med in all_medicines:
                match = True
                if name and name not in med['name']:
                    match = False
                if property_keyword and property_keyword not in med['property']:
                    match = False
                if efficacy_keyword and efficacy_keyword not in med['efficacy']:
                    match = False
                if match:
                    filtered_medicines.append(med)
            
            print(f"检索到 {len(filtered_medicines)} 条符合条件的中药信息")
            return filtered_medicines
        except sqlite3.Error as e:
            print(f"检索失败: {e}")
            return []

    def visualize_property_distribution(self, data=None):
        """可视化中药性味分布（统计“温/寒/平”等属性）"""
        if not MATPLOTLIB_AVAILABLE:
            print("matplotlib库未安装，跳过可视化功能")
            return
            
        if not data:
            data = self.search_medicine()  # 无数据时查询全部

        # 提取性味中的核心属性（温/寒/凉/热/平）
        properties = []
        for item in data:
            prop = item["property"]
            if "温" in prop:
                properties.append("温")
            elif "寒" in prop:
                properties.append("寒")
            elif "凉" in prop:
                properties.append("凉")
            elif "热" in prop:
                properties.append("热")
            elif "平" in prop:
                properties.append("平")

        # 统计频次
        prop_count = Counter(properties)
        if not prop_count:
            print("暂无可用的性味数据用于可视化")
            return

        # 绘制饼图
        plt.figure(figsize=(8, 6))
        plt.pie(prop_count.values(), labels=prop_count.keys(), autopct='%1.1f%%', startangle=90)
        plt.title("中药性味分布")
        plt.axis('equal')  # 保证饼图是正圆形
        plt.tight_layout()
        plt.show(block=True)
        plt.close()

    def visualize_efficacy_tags(self, data=None):
        """可视化中药功效关键词分布（所有关键词）"""
        if not MATPLOTLIB_AVAILABLE:
            print("matplotlib库未安装，跳过可视化功能")
            return
            
        if not data:
            data = self.search_medicine()

        # 提取功效关键词（拆分常见功效词）
        efficacy_words = []
        common_efficacies = ["补气", "清热解毒", "补血", "健脾", "养肝", "明目", "安神", "活血", "止咳", "化痰"]
        for item in data:
            efficacy = item["efficacy"]
            for word in common_efficacies:
                if word in efficacy:
                    efficacy_words.append(word)

        if not efficacy_words:
            print("暂无可用的功效数据用于可视化")
            return

        # 统计所有关键词
        efficacy_count = Counter(efficacy_words).most_common()
        words = [item[0] for item in efficacy_count]
        counts = [item[1] for item in efficacy_count]

        # 绘制柱状图
        plt.figure(figsize=(12, 6))
        bars = plt.bar(words, counts, color='#66b3ff')
        plt.title("中药功效关键词分布（所有关键词）")
        plt.xlabel("功效关键词")
        plt.ylabel("出现次数")
        plt.xticks(rotation=45)
        # 添加数据标签
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height}', ha='center', va='bottom')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show(block=True)
        plt.close()

    def visualize_property_distribution(self, data=None):
        """可视化中药性味分布（统计“温/寒/平”等属性）"""
        if not MATPLOTLIB_AVAILABLE:
            print("matplotlib库未安装，跳过可视化功能")
            return
            
        if not data:
            data = self.search_medicine()  # 无数据时查询全部

        # 提取性味中的核心属性（温/寒/凉/热/平）
        properties = []
        for item in data:
            prop = item["property"]
            if "温" in prop:
                properties.append("温")
            elif "寒" in prop:
                properties.append("寒")
            elif "凉" in prop:
                properties.append("凉")
            elif "热" in prop:
                properties.append("热")
            elif "平" in prop:
                properties.append("平")

        # 统计频次
        prop_count = Counter(properties)
        if not prop_count:
            print("暂无可用的性味数据用于可视化")
            return

        # 绘制饼图
        plt.figure(figsize=(8, 6))
        wedges, texts, autotexts = plt.pie(
            prop_count.values(), 
            labels=prop_count.keys(), 
            autopct='%1.1f%%', 
            startangle=90
        )
        # 设置文本样式
        for text in texts:
            text.set_fontsize(12)
            text.set_fontweight('medium')
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
            autotext.set_color('white')
        plt.title("中药性味分布")
        plt.axis('equal')  # 保证饼图是正圆形
        plt.tight_layout()
        plt.show(block=True)
        plt.close()

    def visualize_medicine_table(self, data=None):
        """以表格式图表显示中药数据（支持翻页）"""
        try:
            import tkinter as tk
            from tkinter import ttk
        except ImportError:
            print("tkinter库未可用，跳过可视化功能")
            return
            
        if not data:
            data = self.search_medicine()

        if not data:
            print("暂无可用的中药数据用于可视化")
            return

        total_records = len(data)
        page_size = 20  # 每页显示20条
        total_pages = (total_records + page_size - 1) // page_size

        # 创建主窗口
        root = tk.Tk()
        root.title("中药数据表格")
        root.geometry("1200x600")
        root.resizable(True, True)

        # 设置字体
        style = ttk.Style()
        style.configure("Treeview", font=("SimHei", 11))
        style.configure("Treeview.Heading", font=("SimHei", 12, "bold"))

        # 创建框架
        frame = ttk.Frame(root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # 创建表格
        columns = ('ID', '名称', '性味', '归经', '功效')
        tree = ttk.Treeview(frame, columns=columns, show='headings')

        # 设置列标题
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor=tk.CENTER)

        # 设置列宽
        tree.column('ID', width=50)
        tree.column('名称', width=120)
        tree.column('性味', width=100)
        tree.column('归经', width=150)
        tree.column('功效', width=400)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # 分页信息标签
        page_info_var = tk.StringVar()
        page_info_label = ttk.Label(frame, textvariable=page_info_var, font=("SimHei", 10))
        page_info_label.pack(pady=10)

        # 当前页码
        current_page = [1]  # 使用列表存储，以便在函数中修改

        def update_table():
            """更新表格数据"""
            # 清空表格
            for item in tree.get_children():
                tree.delete(item)

            # 计算当前页的数据范围
            start_idx = (current_page[0] - 1) * page_size
            end_idx = min(start_idx + page_size, total_records)
            display_data = data[start_idx:end_idx]

            # 添加数据到表格
            for item in display_data:
                tree.insert('', tk.END, values=(
                    item['id'],
                    item['name'],
                    item['property'],
                    item['channel'],
                    item['efficacy']
                ))

            # 更新分页信息
            page_info_var.set(f"第 {current_page[0]}/{total_pages} 页，共 {total_records} 条记录")

            # 更新按钮状态
            btn_previous['state'] = 'normal' if current_page[0] > 1 else 'disabled'
            btn_next['state'] = 'normal' if current_page[0] < total_pages else 'disabled'
            btn_first['state'] = 'normal' if current_page[0] > 1 else 'disabled'
            btn_last['state'] = 'normal' if current_page[0] < total_pages else 'disabled'

        def go_previous():
            """上一页"""
            if current_page[0] > 1:
                current_page[0] -= 1
                update_table()

        def go_next():
            """下一页"""
            if current_page[0] < total_pages:
                current_page[0] += 1
                update_table()

        def go_first():
            """首页"""
            current_page[0] = 1
            update_table()

        def go_last():
            """末页"""
            current_page[0] = total_pages
            update_table()

        # 创建分页按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        btn_first = ttk.Button(btn_frame, text="首页", command=go_first)
        btn_first.pack(side=tk.LEFT, padx=5)

        btn_previous = ttk.Button(btn_frame, text="上一页", command=go_previous)
        btn_previous.pack(side=tk.LEFT, padx=5)

        btn_next = ttk.Button(btn_frame, text="下一页", command=go_next)
        btn_next.pack(side=tk.LEFT, padx=5)

        btn_last = ttk.Button(btn_frame, text="末页", command=go_last)
        btn_last.pack(side=tk.LEFT, padx=5)

        # 退出按钮
        btn_exit = ttk.Button(btn_frame, text="退出", command=root.destroy)
        btn_exit.pack(side=tk.LEFT, padx=5)

        # 初始更新表格
        update_table()

        # 运行主循环
        root.mainloop()

    def show_interactive_menu(self):
        """显示交互式菜单，让用户选择要查看的图表"""
        print("\n=== 中药信息管理系统 ===")
        print("1. 查看中药数据表格")
        print("2. 查看中药性味分布")
        print("3. 查看中药功效关键词分布")
        print("4. 搜索特定中药")
        print("5. 退出系统")
        
        while True:
            try:
                choice = input("\n请输入您的选择（1-5）: ")
                
                if choice == '1':
                    print("\n=== 中药数据表格 ===")
                    self.visualize_medicine_table()
                elif choice == '2':
                    print("\n=== 中药性味分布 ===")
                    self.visualize_property_distribution()
                elif choice == '3':
                    print("\n=== 中药功效关键词分布 ===")
                    self.visualize_efficacy_tags()
                elif choice == '4':
                    print("\n=== 搜索特定中药 ===")
                    keyword = input("请输入搜索关键词: ")
                    results = self.search_medicine(efficacy_keyword=keyword)
                    if results:
                        print("\n搜索结果:")
                        for med in results[:10]:  # 只显示前10条
                            print(f"名称：{med['name']} | 性味：{med['property']} | 功效：{med['efficacy'][:30]}...")
                    else:
                        print("未找到符合条件的中药")
                elif choice == '5':
                    print("\n退出系统...")
                    break
                else:
                    print("输入错误，请重新输入")
            except Exception as e:
                print(f"发生错误: {e}")
                continue

    def close_db(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            print("数据库连接已关闭")

# ------------------------------
# 系统使用示例
# ------------------------------
if __name__ == "__main__":
    # 初始化系统
    sys = ChineseMedicineSystem()

    # 显示交互式菜单
    sys.show_interactive_menu()

    # 关闭数据库
    sys.close_db()