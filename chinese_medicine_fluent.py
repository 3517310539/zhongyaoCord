import sys
import sqlite3
import pandas as pd
import numpy as np

# 尝试导入matplotlib，如果失败则跳过可视化
MATPLOTLIB_AVAILABLE = False
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    # 设置Matplotlib中文支持
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    MATPLOTLIB_AVAILABLE = True
except Exception as e:
    print(f"警告：matplotlib库导入失败，将跳过可视化功能: {e}")
    # 定义一个占位符类
    class FigureCanvas:
        pass
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QTableWidget, QTableWidgetItem, 
                           QPushButton, QLineEdit, QLabel, QComboBox, 
                           QMessageBox, QDialog, QFormLayout, QTextEdit)
from PyQt5.QtCore import Qt, QTimer
from qfluentwidgets import (
    NavigationInterface, NavigationItemPosition, 
    FluentWindow, SubtitleLabel, PushButton, 
    LineEdit, ComboBox, TableWidget, 
    CardWidget, InfoBar, InfoBarPosition,
    PrimaryPushButton, 
    Theme, setTheme
)

class ChineseMedicineFluentApp(FluentWindow):
    def __init__(self):
        super().__init__()
        self.db_name = "chinese_medicine.db"
        self.conn = None
        self.cursor = None
        self.current_page = 1
        self.page_size = 20
        self.total_pages = 1
        
        # 设置主题
        setTheme(Theme.LIGHT)
        
        # 确保导航栏折叠后有可见标志
        self.navigationInterface.setCollapsible(True)
        
        # 初始化数据库连接
        self._connect_db()
        self._create_table()
        
        # 设置窗口
        self.resize(1200, 800)
        self.setWindowTitle("中药管理系统")
        
        # 创建页面
        self._init_pages()
        
        # 创建导航栏
        self._init_navigation()
        
        # 加载数据
        self._load_data()
        
        # 确保导航栏可见
        self.navigationInterface.expand(True)
    
    def _connect_db(self):
        """建立数据库连接"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"成功连接到数据库: {self.db_name}")
        except sqlite3.Error as e:
            print(f"数据库连接失败: {e}")
            InfoBar.error(
                title="错误",
                content=f"数据库连接失败: {e}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                parent=self
            )
    
    def _create_table(self):
        """创建数据库表"""
        try:
            # 扩展表结构，添加更多字段
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS medicines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    property TEXT,
                    channel TEXT,
                    efficacy TEXT,
                    usage TEXT,
                    source TEXT,
                    category TEXT,
                    origin TEXT,
                    morphology TEXT,
                    pharmacology TEXT,
                    clinical_application TEXT,
                    modern_research TEXT
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"创建表失败: {e}")
    
    def _init_navigation(self):
        """初始化导航栏"""
        self.addSubInterface(self.data_page, "数据管理", "数据管理")
        self.addSubInterface(self.analysis_page, "数据分析", "数据分析")
        self.addSubInterface(self.edit_page, "数据编辑", "数据编辑")
        self.addSubInterface(self.import_export_page, "导入导出", "导入导出")
        self.addSubInterface(self.about_page, "关于", "关于", NavigationItemPosition.BOTTOM)
    
    def _init_pages(self):
        """初始化页面 """
        # 数据管理页面
        self.data_page = QWidget()
        self.data_page.setObjectName("data_page")
        data_layout = QVBoxLayout(self.data_page)
        
        # 搜索栏
        search_layout = QHBoxLayout()
        self.search_input = LineEdit()
        self.search_input.setPlaceholderText("搜索中药名称...")
        self.search_btn = PrimaryPushButton("搜索")
        self.search_btn.clicked.connect(self._search_data)
        
        # 筛选器
        self.filter_combo = ComboBox()
        self.filter_combo.addItems(["全部", "解表药", "清热药", "泻下药", "祛风湿药", "化湿药", "利水渗湿药", "温里药", "理气药", "消食药", "驱虫药", "止血药", "活血化瘀药", "化痰止咳平喘药", "安神药", "平肝息风药", "开窍药", "补虚药", "收涩药", "涌吐药", "攻毒杀虫止痒药", "拔毒化腐生肌药"])
        self.filter_combo.currentIndexChanged.connect(self._filter_data)
        
        search_layout.addWidget(QLabel("分类筛选:"))
        search_layout.addWidget(self.filter_combo)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        
        # 数据表格
        self.table_widget = TableWidget()
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(["ID", "名称", "性味", "归经", "功效", "用法"])
        
        # 分页控件
        pagination_layout = QHBoxLayout()
        self.page_label = QLabel("第 1 页，共 1 页")
        self.prev_btn = PushButton("上一页")
        self.next_btn = PushButton("下一页")
        self.first_btn = PushButton("首页")
        self.last_btn = PushButton("末页")
        
        self.prev_btn.clicked.connect(self._prev_page)
        self.next_btn.clicked.connect(self._next_page)
        self.first_btn.clicked.connect(self._first_page)
        self.last_btn.clicked.connect(self._last_page)
        
        pagination_layout.addWidget(self.first_btn)
        pagination_layout.addWidget(self.prev_btn)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_btn)
        pagination_layout.addWidget(self.last_btn)
        
        data_layout.addLayout(search_layout)
        data_layout.addWidget(self.table_widget)
        data_layout.addLayout(pagination_layout)
        
        # 数据分析页面
        self.analysis_page = QWidget()
        self.analysis_page.setObjectName("analysis_page")
        analysis_layout = QVBoxLayout(self.analysis_page)
        
        # 分析类型选择
        analysis_type_layout = QHBoxLayout()
        self.analysis_combo = ComboBox()
        self.analysis_combo.addItems(["性味分布", "归经分布", "功效分类", "用药频率"])
        self.analysis_combo.currentIndexChanged.connect(self._update_analysis)
        
        analysis_type_layout.addWidget(QLabel("分析类型:"))
        analysis_type_layout.addWidget(self.analysis_combo)
        analysis_type_layout.addStretch()
        
        # 图表容器
        self.chart_container = QWidget()
        self.chart_layout = QVBoxLayout(self.chart_container)
        
        analysis_layout.addLayout(analysis_type_layout)
        analysis_layout.addWidget(self.chart_container)
        
        # 初始化时触发一次图表更新
        self._update_analysis()
        
        # 数据编辑页面
        self.edit_page = QWidget()
        self.edit_page.setObjectName("edit_page")
        edit_layout = QVBoxLayout(self.edit_page)
        
        # 编辑操作按钮
        edit_buttons_layout = QHBoxLayout()
        self.add_btn = PrimaryPushButton("添加中药")
        self.update_btn = PushButton("修改选中")
        self.delete_btn = PushButton("删除选中")
        
        self.add_btn.clicked.connect(self._add_medicine)
        self.update_btn.clicked.connect(self._update_medicine)
        self.delete_btn.clicked.connect(self._delete_medicine)
        
        edit_buttons_layout.addWidget(self.add_btn)
        edit_buttons_layout.addWidget(self.update_btn)
        edit_buttons_layout.addWidget(self.delete_btn)
        
        # 详细信息展示
        self.detail_card = CardWidget()
        detail_layout = QFormLayout(self.detail_card)
        
        self.detail_id = QLabel("ID:")
        self.detail_name = QLabel("名称:")
        self.detail_property = QLabel("性味:")
        self.detail_channel = QLabel("归经:")
        self.detail_efficacy = QTextEdit()
        self.detail_efficacy.setReadOnly(True)
        self.detail_usage = QTextEdit()
        self.detail_usage.setReadOnly(True)
        self.detail_category = QLabel("分类:")
        self.detail_origin = QLabel("产地:")
        
        detail_layout.addRow("ID:", self.detail_id)
        detail_layout.addRow("名称:", self.detail_name)
        detail_layout.addRow("性味:", self.detail_property)
        detail_layout.addRow("归经:", self.detail_channel)
        detail_layout.addRow("功效:", self.detail_efficacy)
        detail_layout.addRow("用法:", self.detail_usage)
        detail_layout.addRow("分类:", self.detail_category)
        detail_layout.addRow("产地:", self.detail_origin)
        
        edit_layout.addLayout(edit_buttons_layout)
        edit_layout.addWidget(SubtitleLabel("选中中药详情"))
        edit_layout.addWidget(self.detail_card)
        
        # 导入导出页面
        self.import_export_page = QWidget()
        self.import_export_page.setObjectName("import_export_page")
        import_export_layout = QVBoxLayout(self.import_export_page)
        
        # 导入导出按钮
        import_export_buttons_layout = QHBoxLayout()
        self.import_btn = PrimaryPushButton("导入数据")
        self.export_btn = PushButton("导出数据")
        
        # 添加点击事件
        self.import_btn.clicked.connect(self._import_data)
        self.export_btn.clicked.connect(self._export_data)
        
        import_export_buttons_layout.addWidget(self.import_btn)
        import_export_buttons_layout.addWidget(self.export_btn)
        
        # 导入导出说明
        import_export_info = QTextEdit()
        import_export_info.setReadOnly(True)
        import_export_info.setText("导入：支持CSV、Excel格式的数据导入\n导出：可导出为CSV、Excel或SQL格式")
        
        import_export_layout.addLayout(import_export_buttons_layout)
        import_export_layout.addWidget(SubtitleLabel("导入导出说明"))
        import_export_layout.addWidget(import_export_info)
        
        # 关于页面
        self.about_page = QWidget()
        self.about_page.setObjectName("about_page")
        about_layout = QVBoxLayout(self.about_page)
        
        about_info = QTextEdit()
        about_info.setReadOnly(True)
        about_info.setText("中药管理系统 v1.0\n\n使用PyQt-Fluent-Widgets开发的现代化中药管理系统，支持数据管理、分析和可视化功能。\n\n© 2026 中药管理系统")
        
        about_layout.addWidget(SubtitleLabel("关于系统"))
        about_layout.addWidget(about_info)
    
    def _load_data(self, page=1, search="", category="全部"):
        """加载数据"""
        try:
            # 构建查询
            query = "SELECT id, name, property, channel, efficacy, usage FROM medicines WHERE 1=1"
            params = []
            
            if search:
                query += " AND name LIKE ?"
                params.append(f"%{search}%")
            
            # 获取总数
            count_query = query.replace("id, name, property, channel, efficacy, usage", "COUNT(*)")
            self.cursor.execute(count_query, params)
            total_count = self.cursor.fetchone()[0]
            
            # 计算总页数
            self.total_pages = (total_count + self.page_size - 1) // self.page_size
            self.current_page = page
            
            # 分页查询
            offset = (page - 1) * self.page_size
            query += " ORDER BY id LIMIT ? OFFSET ?"
            params.extend([self.page_size, offset])
            
            self.cursor.execute(query, params)
            data = self.cursor.fetchall()
            
            # 更新表格
            self.table_widget.setRowCount(len(data))
            for row_idx, row_data in enumerate(data):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data) if col_data else "")
                    self.table_widget.setItem(row_idx, col_idx, item)
            
            # 更新分页信息
            self.page_label.setText(f"第 {self.current_page} 页，共 {self.total_pages} 页")
            
            # 更新按钮状态
            self.first_btn.setEnabled(self.current_page > 1)
            self.prev_btn.setEnabled(self.current_page > 1)
            self.next_btn.setEnabled(self.current_page < self.total_pages)
            self.last_btn.setEnabled(self.current_page < self.total_pages)
            
        except sqlite3.Error as e:
            print(f"加载数据失败: {e}")
            InfoBar.error(
                title="错误",
                content=f"加载数据失败: {e}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                parent=self
            )
    
    def _search_data(self):
        """搜索数据"""
        search_text = self.search_input.text()
        self._load_data(1, search_text)
    
    def _filter_data(self):
        """筛选数据"""
        search_text = self.search_input.text()
        self._load_data(1, search_text)
    
    def _prev_page(self):
        """上一页"""
        if self.current_page > 1:
            self._load_data(self.current_page - 1, self.search_input.text())
    
    def _next_page(self):
        """下一页"""
        if self.current_page < self.total_pages:
            self._load_data(self.current_page + 1, self.search_input.text())
    
    def _first_page(self):
        """首页"""
        self._load_data(1, self.search_input.text())
    
    def _last_page(self):
        """末页"""
        self._load_data(self.total_pages, self.search_input.text())
    
    def _update_analysis(self):
        """更新分析图表"""
        analysis_type = self.analysis_combo.currentText()
        
        # 清空图表容器
        for i in reversed(range(self.chart_layout.count())):
            widget = self.chart_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # 检查matplotlib是否可用
        if not MATPLOTLIB_AVAILABLE:
            # 创建一个标签提示
            from PyQt5.QtWidgets import QLabel
            error_label = QLabel("matplotlib库未可用，无法显示图表")
            error_label.setAlignment(Qt.AlignCenter)
            error_label.setStyleSheet("font-size: 14px; color: #666;")
            self.chart_layout.addWidget(error_label)
            return
        
        try:
            # 创建图表
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if analysis_type == "性味分布":
                # 性味分布分析
                self.cursor.execute("SELECT property, COUNT(*) FROM medicines GROUP BY property ORDER BY COUNT(*) DESC LIMIT 10")
                data = self.cursor.fetchall()
                if data:
                    labels = [item[0] for item in data]
                    values = [item[1] for item in data]
                    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
                    ax.set_title('中药性味分布')
            
            elif analysis_type == "归经分布":
                # 归经分布分析
                self.cursor.execute("SELECT channel, COUNT(*) FROM medicines GROUP BY channel ORDER BY COUNT(*) DESC LIMIT 10")
                data = self.cursor.fetchall()
                if data:
                    labels = [item[0] for item in data]
                    values = [item[1] for item in data]
                    ax.bar(labels, values)
                    ax.set_title('中药归经分布')
                    ax.set_xticklabels(labels, rotation=45, ha='right')
                    ax.set_ylabel('数量')
            
            elif analysis_type == "功效分类":
                # 功效分类分析 - 使用功效字段的关键词进行分析
                self.cursor.execute("SELECT efficacy FROM medicines")
                data = self.cursor.fetchall()
                if data:
                    # 提取功效关键词
                    keyword_count = {}
                    for item in data:
                        if item[0]:
                            keywords = item[0].split('，')
                            for keyword in keywords:
                                if keyword:
                                    keyword_count[keyword] = keyword_count.get(keyword, 0) + 1
                    
                    # 排序并取前10个
                    sorted_keywords = sorted(keyword_count.items(), key=lambda x: x[1], reverse=True)[:10]
                    labels = [item[0] for item in sorted_keywords]
                    values = [item[1] for item in sorted_keywords]
                    
                    ax.barh(labels, values)
                    ax.set_title('中药功效分类')
                    ax.set_xlabel('数量')
            
            elif analysis_type == "用药频率":
                # 模拟用药频率数据
                labels = ['一月', '二月', '三月', '四月', '五月', '六月']
                values = np.random.randint(50, 200, size=6)
                ax.plot(labels, values, marker='o')
                ax.set_title('中药用药频率趋势')
                ax.set_ylabel('使用频次')
            
            # 创建画布并添加到布局
            canvas = FigureCanvas(fig)
            self.chart_layout.addWidget(canvas)
            
        except Exception as e:
            print(f"分析数据失败: {e}")
            InfoBar.error(
                title="错误",
                content=f"分析数据失败: {e}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                parent=self
            )
    
    def _add_medicine(self):
        """添加中药"""
        dialog = MedicineEditDialog(self, None)
        if dialog.exec_():
            self._load_data()
            InfoBar.success(
                title="成功",
                content="中药添加成功",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                parent=self
            )
    
    def _update_medicine(self):
        """修改选中中药"""
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            InfoBar.warning(
                title="提示",
                content="请先选择要修改的中药",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                parent=self
            )
            return
        
        row = selected_rows[0].row()
        medicine_id = int(self.table_widget.item(row, 0).text())
        dialog = MedicineEditDialog(self, medicine_id)
        if dialog.exec_():
            self._load_data()
            InfoBar.success(
                title="成功",
                content="中药修改成功",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                parent=self
            )
    
    def _delete_medicine(self):
        """删除选中中药"""
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            InfoBar.warning(
                title="提示",
                content="请先选择要删除的中药",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                parent=self
            )
            return
        
        reply = QMessageBox.question(
            self, "确认删除", "确定要删除选中的中药吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                for row in selected_rows:
                    medicine_id = int(self.table_widget.item(row.row(), 0).text())
                    self.cursor.execute("DELETE FROM medicines WHERE id = ?", (medicine_id,))
                self.conn.commit()
                self._load_data()
                InfoBar.success(
                    title="成功",
                    content="中药删除成功",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    parent=self
                )
            except sqlite3.Error as e:
                print(f"删除数据失败: {e}")
                InfoBar.error(
                    title="错误",
                    content=f"删除数据失败: {e}",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    parent=self
                )
    
    def _import_data(self):
        """导入数据"""
        try:
            from PyQt5.QtWidgets import QFileDialog
            
            # 打开文件对话框
            file_path, _ = QFileDialog.getOpenFileName(
                self, "选择导入文件", "", "CSV文件 (*.csv);;Excel文件 (*.xlsx);;所有文件 (*.*)"
            )
            
            if not file_path:
                return
            
            # 读取文件
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                InfoBar.warning(
                    title="提示",
                    content="不支持的文件格式",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    parent=self
                )
                return
            
            # 导入数据
            count = 0
            for _, row in df.iterrows():
                try:
                    self.cursor.execute('''
                        INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage) 
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        row.get('name', ''),
                        row.get('property', ''),
                        row.get('channel', ''),
                        row.get('efficacy', ''),
                        row.get('usage', '')
                    ))
                    count += 1
                except Exception as e:
                    print(f"导入失败: {e}")
            
            self.conn.commit()
            self._load_data()
            
            InfoBar.success(
                title="成功",
                content=f"成功导入 {count} 条数据",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                parent=self
            )
            
        except Exception as e:
            print(f"导入数据失败: {e}")
            InfoBar.error(
                title="错误",
                content=f"导入数据失败: {e}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                parent=self
            )
    
    def _export_data(self):
        """导出数据"""
        try:
            from PyQt5.QtWidgets import QFileDialog
            
            # 打开文件对话框
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存导出文件", "chinese_medicine", "CSV文件 (*.csv);;Excel文件 (*.xlsx)"
            )
            
            if not file_path:
                return
            
            # 读取数据
            self.cursor.execute("SELECT id, name, property, channel, efficacy, usage FROM medicines")
            data = self.cursor.fetchall()
            
            # 转换为DataFrame
            df = pd.DataFrame(
                data, 
                columns=['id', 'name', 'property', 'channel', 'efficacy', 'usage']
            )
            
            # 导出数据
            if file_path.endswith('.csv'):
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
            elif file_path.endswith('.xlsx'):
                df.to_excel(file_path, index=False)
            
            InfoBar.success(
                title="成功",
                content=f"成功导出 {len(data)} 条数据到 {file_path}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                parent=self
            )
            
        except Exception as e:
            print(f"导出数据失败: {e}")
            InfoBar.error(
                title="错误",
                content=f"导出数据失败: {e}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                parent=self
            )

class MedicineEditDialog(QDialog):
    def __init__(self, parent, medicine_id=None):
        super().__init__(parent)
        self.parent = parent
        self.medicine_id = medicine_id
        self.setWindowTitle("添加中药" if medicine_id is None else "修改中药")
        self.resize(600, 500)
        
        layout = QVBoxLayout(self)
        
        # 表单
        form_layout = QFormLayout()
        
        self.name_input = LineEdit()
        self.property_input = LineEdit()
        self.channel_input = LineEdit()
        self.efficacy_input = QTextEdit()
        self.usage_input = QTextEdit()
        self.category_input = ComboBox()
        self.category_input.addItems(["解表药", "清热药", "泻下药", "祛风湿药", "化湿药", "利水渗湿药", "温里药", "理气药", "消食药", "驱虫药", "止血药", "活血化瘀药", "化痰止咳平喘药", "安神药", "平肝息风药", "开窍药", "补虚药", "收涩药", "涌吐药", "攻毒杀虫止痒药", "拔毒化腐生肌药"])
        self.origin_input = LineEdit()
        self.morphology_input = QTextEdit()
        self.pharmacology_input = QTextEdit()
        self.clinical_application_input = QTextEdit()
        self.modern_research_input = QTextEdit()
        
        form_layout.addRow("名称:", self.name_input)
        form_layout.addRow("性味:", self.property_input)
        form_layout.addRow("归经:", self.channel_input)
        form_layout.addRow("功效:", self.efficacy_input)
        form_layout.addRow("用法:", self.usage_input)
        form_layout.addRow("分类:", self.category_input)
        form_layout.addRow("产地:", self.origin_input)
        form_layout.addRow("形态:", self.morphology_input)
        form_layout.addRow("药理作用:", self.pharmacology_input)
        form_layout.addRow("临床应用:", self.clinical_application_input)
        form_layout.addRow("现代研究:", self.modern_research_input)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.save_btn = PrimaryPushButton("保存")
        self.cancel_btn = PushButton("取消")
        
        self.save_btn.clicked.connect(self._save)
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        
        # 加载数据（如果是修改）
        if medicine_id:
            self._load_medicine_data()
    
    def _load_medicine_data(self):
        """加载中药数据"""
        try:
            self.parent.cursor.execute('''
                SELECT name, property, channel, efficacy, usage 
                FROM medicines WHERE id = ?
            ''', (self.medicine_id,))
            data = self.parent.cursor.fetchone()
            if data:
                self.name_input.setText(data[0])
                self.property_input.setText(data[1] if data[1] else "")
                self.channel_input.setText(data[2] if data[2] else "")
                self.efficacy_input.setText(data[3] if data[3] else "")
                self.usage_input.setText(data[4] if data[4] else "")
        except sqlite3.Error as e:
            print(f"加载数据失败: {e}")
    
    def _save(self):
        """保存数据"""
        name = self.name_input.text().strip()
        if not name:
            InfoBar.warning(
                title="提示",
                content="请输入中药名称",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                parent=self
            )
            return
        
        try:
            if self.medicine_id:
                # 修改
                self.parent.cursor.execute('''
                    UPDATE medicines SET 
                        name = ?, property = ?, channel = ?, efficacy = ?, usage = ?
                    WHERE id = ?
                ''', (
                    name, self.property_input.text(), self.channel_input.text(),
                    self.efficacy_input.toPlainText(), self.usage_input.toPlainText(),
                    self.medicine_id
                ))
            else:
                # 添加
                self.parent.cursor.execute('''
                    INSERT OR IGNORE INTO medicines (
                        name, property, channel, efficacy, usage
                    ) VALUES (?, ?, ?, ?, ?)
                ''', (
                    name, self.property_input.text(), self.channel_input.text(),
                    self.efficacy_input.toPlainText(), self.usage_input.toPlainText()
                ))
            self.parent.conn.commit()
            self.accept()
        except sqlite3.Error as e:
            print(f"保存数据失败: {e}")
            InfoBar.error(
                title="错误",
                content=f"保存数据失败: {e}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                parent=self
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChineseMedicineFluentApp()
    window.show()
    sys.exit(app.exec_())
