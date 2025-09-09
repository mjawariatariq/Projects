from agents.task_allocator import TaskAllocatorAgent
from agents.deadline_monitor import DeadlineMonitorAgent
from agents.progress_reporter import ProgressReporterAgent
import streamlit as st

class ProjectManagerAgent:
    def __init__(self):
        self.task_allocator = TaskAllocatorAgent()
        self.deadline_monitor = None
        self.progress_reporter = None
    
    def run(self):
        # Task Allocation
        self.task_allocator.load_sample_data()
        assignments = self.task_allocator.allocate_tasks()
        
        # Deadline Monitoring
        self.deadline_monitor = DeadlineMonitorAgent(self.task_allocator.tasks)
        self.deadline_monitor.train_delay_model()
        delays = self.deadline_monitor.predict_delays()
        
        # Progress Reporting
        self.progress_reporter = ProgressReporterAgent(self.task_allocator.tasks)
        
        # Streamlit UI
        st.title("Multi-Agent Project Managemnet")
        self.progress_reporter.generate_dashboard()
        
        with st.expander("Task Assignments"):
            for task in self.task_allocator.tasks:
                st.write(f"{task.description} -> {next(e.name for e in self.task_allocator.employees if e.id in [a[1] for a in assignments if a[0] == task.id])}")
        
        with st.expander("AI Progress Report"):
            st.write(self.progress_reporter.generate_ai_report())

if __name__ == "__main__":
    agent = ProjectManagerAgent()
    agent.run()