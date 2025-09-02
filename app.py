import streamlit as st
import datetime
from typing import List, Dict
import json

# Page configuration
st.set_page_config(
    page_title="✨ My To-Do List",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 3rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
    }
    
    .task-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        transition: transform 0.2s ease;
    }
    
    .task-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }
    
    .task-completed {
        opacity: 0.6;
        border-left-color: #28a745;
    }
    
    .task-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #2c3e50;
    }
    
    .task-description {
        color: #7f8c8d;
        margin-bottom: 1rem;
        line-height: 1.5;
    }
    
    .task-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.9rem;
        color: #95a5a6;
    }
    
    .priority-high {
        background: linear-gradient(90deg, #ff6b6b, #ee5a52);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .priority-medium {
        background: linear-gradient(90deg, #feca57, #ff9ff3);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .priority-low {
        background: linear-gradient(90deg, #48dbfb, #0abde3);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stats-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .add-task-form {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 2px dashed #dee2e6;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .delete-btn {
        background: linear-gradient(90deg, #ff6b6b, #ee5a52) !important;
    }
    
    .complete-btn {
        background: linear-gradient(90deg, #28a745, #20c997) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'task_id_counter' not in st.session_state:
    st.session_state.task_id_counter = 0

def add_task(title: str, description: str, priority: str, due_date: str) -> None:
    """Add a new task to the list"""
    task = {
        'id': st.session_state.task_id_counter,
        'title': title,
        'description': description,
        'priority': priority,
        'due_date': due_date,
        'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'completed': False
    }
    st.session_state.tasks.append(task)
    st.session_state.task_id_counter += 1
    st.success("✅ Task added successfully!")

def toggle_task_completion(task_id: int) -> None:
    """Toggle task completion status"""
    for task in st.session_state.tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break

def delete_task(task_id: int) -> None:
    """Delete a task from the list"""
    st.session_state.tasks = [task for task in st.session_state.tasks if task['id'] != task_id]
    st.success("🗑️ Task deleted successfully!")

def get_priority_class(priority: str) -> str:
    """Get CSS class for priority styling"""
    priority_classes = {
        'High': 'priority-high',
        'Medium': 'priority-medium',
        'Low': 'priority-low'
    }
    return priority_classes.get(priority, 'priority-low')

def get_task_stats() -> Dict[str, int]:
    """Calculate task statistics"""
    total = len(st.session_state.tasks)
    completed = sum(1 for task in st.session_state.tasks if task['completed'])
    pending = total - completed
    return {'total': total, 'completed': completed, 'pending': pending}

# Main app
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>✨ My To-Do List</h1>
        <p>Stay organized and productive with your personal task manager</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for adding new tasks
    with st.sidebar:
        st.markdown("### 📝 Add New Task")
        
        with st.form("add_task_form"):
            title = st.text_input("Task Title", placeholder="Enter task title...")
            description = st.text_area("Description", placeholder="Enter task description...", height=100)
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            due_date = st.date_input("Due Date", value=datetime.date.today())
            
            submitted = st.form_submit_button("➕ Add Task", use_container_width=True)
            
            if submitted and title:
                add_task(title, description, priority, due_date.strftime("%Y-%m-%d"))
            elif submitted and not title:
                st.error("Please enter a task title!")
    
    # Main content area
    col1, col2, col3 = st.columns(3)
    
    # Statistics
    stats = get_task_stats()
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{stats['total']}</div>
            <div class="stats-label">Total Tasks</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{stats['completed']}</div>
            <div class="stats-label">Completed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{stats['pending']}</div>
            <div class="stats-label">Pending</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Task list
    st.markdown("### 📋 Your Tasks")
    
    if not st.session_state.tasks:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #7f8c8d;">
            <h3>🎉 No tasks yet!</h3>
            <p>Add your first task using the sidebar to get started.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Filter options
        filter_col1, filter_col2 = st.columns([3, 1])
        
        with filter_col1:
            show_completed = st.checkbox("Show completed tasks", value=True)
        
        with filter_col2:
            sort_by = st.selectbox("Sort by", ["Created Date", "Priority", "Due Date"])
        
        # Filter and sort tasks
        filtered_tasks = st.session_state.tasks.copy()
        
        if not show_completed:
            filtered_tasks = [task for task in filtered_tasks if not task['completed']]
        
        if sort_by == "Priority":
            priority_order = {"High": 3, "Medium": 2, "Low": 1}
            filtered_tasks.sort(key=lambda x: priority_order.get(x['priority'], 1), reverse=True)
        elif sort_by == "Due Date":
            filtered_tasks.sort(key=lambda x: x['due_date'])
        else:  # Created Date
            filtered_tasks.sort(key=lambda x: x['created_at'], reverse=True)
        
        # Display tasks
        for task in filtered_tasks:
            task_class = "task-completed" if task['completed'] else ""
            priority_class = get_priority_class(task['priority'])
            
            with st.container():
                st.markdown(f"""
                <div class="task-card {task_class}">
                    <div class="task-title">{'✅ ' if task['completed'] else '📌 '}{task['title']}</div>
                    <div class="task-description">{task['description']}</div>
                    <div class="task-meta">
                        <span class="{priority_class}">{task['priority']} Priority</span>
                        <span>📅 Due: {task['due_date']}</span>
                        <span>🕒 Created: {task['created_at']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Task actions
                action_col1, action_col2, action_col3 = st.columns([1, 1, 1])
                
                with action_col1:
                    if st.button(f"{'↩️ Undo' if task['completed'] else '✅ Complete'}", 
                               key=f"complete_{task['id']}", 
                               help="Toggle completion status"):
                        toggle_task_completion(task['id'])
                        st.rerun()
                
                with action_col2:
                    if st.button("🗑️ Delete", 
                               key=f"delete_{task['id']}", 
                               help="Delete this task"):
                        delete_task(task['id'])
                        st.rerun()
                
                with action_col3:
                    if st.button("📝 Edit", 
                               key=f"edit_{task['id']}", 
                               help="Edit this task"):
                        st.info("Edit functionality coming soon! For now, you can delete and recreate the task.")
                
                st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #7f8c8d;">
        <p>✨ Built with Streamlit • Stay productive and organized! ✨</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
