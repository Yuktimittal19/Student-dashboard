import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import json
import os

class StudentDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Shubhankar's Life Dashboard")
        self.root.geometry("700x600")
        self.root.attributes('-alpha', 0.92) 
        
        self.tasks_file = "tasks.json"
        self.finance_file = "finance.json"
        self.tasks = []
        self.expenses = []
        
        self.study_fund_goal = 1120000.0
        self.current_saved = 15000.0

        self.load_data()

        self.notebook = ttk.Notebook(root, bootstyle="info")
        self.notebook.pack(fill='both', expand=True, padx=15, pady=15)

        self.tab_tasks = ttk.Frame(self.notebook)
        self.tab_finances = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_tasks, text="📝 Task Manager")
        self.notebook.add(self.tab_finances, text="💰 Finance Tracker")

        self.setup_tasks_tab()
        self.setup_finances_tab()

    def load_data(self):
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as f:
                self.tasks = json.load(f)
        if os.path.exists(self.finance_file):
            with open(self.finance_file, 'r') as f:
                self.expenses = json.load(f)

    def save_data(self):
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=4)
        with open(self.finance_file, 'w') as f:
            json.dump(self.expenses, f, indent=4)

    def setup_tasks_tab(self):
        input_frame = ttk.LabelFrame(self.tab_tasks, text=" Add a New Task ", padding=15, bootstyle="info")
        input_frame.pack(fill='x', pady=15, padx=15)

        ttk.Label(input_frame, text="Description:").grid(row=0, column=0, padx=5, pady=5)
        self.task_desc = ttk.Entry(input_frame, width=35)
        self.task_desc.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Priority:").grid(row=0, column=2, padx=5, pady=5)
        self.task_prio = ttk.Combobox(input_frame, values=["1 (High)", "2 (Med)", "3 (Low)"], width=10, state="readonly")
        self.task_prio.current(2)
        self.task_prio.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(input_frame, text="Add Task", bootstyle="success", command=self.add_task).grid(row=0, column=4, padx=15)

        self.task_tree = ttk.Treeview(self.tab_tasks, columns=("Status", "Priority", "Description"), show="headings", height=12, bootstyle="info")
        self.task_tree.heading("Status", text="Status")
        self.task_tree.heading("Priority", text="Priority")
        self.task_tree.heading("Description", text="Description")
        self.task_tree.column("Status", width=100, anchor="center")
        self.task_tree.column("Priority", width=100, anchor="center")
        self.task_tree.column("Description", width=400)
        self.task_tree.pack(fill='both', expand=True, padx=15, pady=5)

        btn_frame = ttk.Frame(self.tab_tasks)
        btn_frame.pack(fill='x', padx=15, pady=10)
        
        ttk.Button(btn_frame, text="Mark Complete", bootstyle="primary", command=self.complete_task).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete Task", bootstyle="danger", command=self.delete_task).pack(side='left', padx=5)

        self.refresh_task_list()

    def add_task(self):
        desc = self.task_desc.get().strip()
        prio_str = self.task_prio.get()
        if not desc:
            messagebox.showwarning("Empty Field", "Task description cannot be empty!")
            return
        
        priority = int(prio_str.split()[0])
        self.tasks.append({"desc": desc, "prio": priority, "completed": False})
        self.save_data()
        self.task_desc.delete(0, ttk.END)
        self.refresh_task_list()

    def refresh_task_list(self):
        self.tasks.sort(key=lambda x: x['prio'])
        
        for row in self.task_tree.get_children():
            self.task_tree.delete(row)
            
        for index, task in enumerate(self.tasks):
            status = "✅ Done" if task['completed'] else "❌ Pending"
            prio_label = {1: "High", 2: "Med", 3: "Low"}[task['prio']]
            self.task_tree.insert("", "end", iid=index, values=(status, prio_label, task['desc']))

    def complete_task(self):
        selected = self.task_tree.selection()
        if not selected:
            return
        index = int(selected[0])
        if self.tasks[index]['completed']:
            messagebox.showinfo("Already Done", "This task is already completed!")
            return
        self.tasks[index]['completed'] = True
        self.save_data()
        self.refresh_task_list()

    def delete_task(self):
        selected = self.task_tree.selection()
        if not selected:
            return
        index = int(selected[0])
        del self.tasks[index]
        self.save_data()
        self.refresh_task_list()

    def setup_finances_tab(self):
        input_frame = ttk.LabelFrame(self.tab_finances, text=" Log an Expense ", padding=15, bootstyle="info")
        input_frame.pack(fill='x', pady=15, padx=15)

        ttk.Label(input_frame, text="Amount (INR):").grid(row=0, column=0, padx=5, pady=5)
        self.exp_amt = ttk.Entry(input_frame, width=15)
        self.exp_amt.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5)
        self.exp_cat = ttk.Entry(input_frame, width=25)
        self.exp_cat.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(input_frame, text="Add Expense", bootstyle="success", command=self.add_expense).grid(row=0, column=4, padx=15)

        stats_frame = ttk.Frame(self.tab_finances)
        stats_frame.pack(fill='x', padx=15, pady=10)
        
        self.lbl_total = ttk.Label(stats_frame, text="Total Spent: INR 0.00", font=("Helvetica", 14, "bold"), bootstyle="warning")
        self.lbl_total.pack(anchor='w')
        
        self.lbl_fund = ttk.Label(stats_frame, text=f"Master's Fund Progress: INR {self.current_saved} / {self.study_fund_goal}", font=("Helvetica", 11), bootstyle="secondary")
        self.lbl_fund.pack(anchor='w', pady=5)

        self.exp_tree = ttk.Treeview(self.tab_finances, columns=("Amount", "Category"), show="headings", height=10, bootstyle="info")
        self.exp_tree.heading("Amount", text="Amount (INR)")
        self.exp_tree.heading("Category", text="Category")
        self.exp_tree.column("Amount", width=150, anchor="center")
        self.exp_tree.column("Category", width=450)
        self.exp_tree.pack(fill='both', expand=True, padx=15, pady=10)

        self.refresh_finance_list()

    def add_expense(self):
        try:
            amt = float(self.exp_amt.get())
            cat = self.exp_cat.get().strip()
            if not cat:
                raise ValueError
            self.expenses.append({"amt": amt, "cat": cat})
            self.save_data()
            self.exp_amt.delete(0, ttk.END)
            self.exp_cat.delete(0, ttk.END)
            self.refresh_finance_list()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for amount and text for category.")

    def refresh_finance_list(self):
        total_spent = 0.0
        for row in self.exp_tree.get_children():
            self.exp_tree.delete(row)
            
        for exp in self.expenses:
            total_spent += exp['amt']
            self.exp_tree.insert("", "end", values=(f"{exp['amt']:.2f}", exp['cat']))
            
        self.lbl_total.config(text=f"Total Spent: INR {total_spent:.2f}")

if __name__ == "__main__":
    root = ttk.Window(themename="darkly") 
    app = StudentDashboard(root)
    root.mainloop()