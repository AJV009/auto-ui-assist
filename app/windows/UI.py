# Auto UI Assist
# This application provides an automated UI assistance tool using PyQt5 for the GUI and various APIs for task processing.

# 1. Imports and Setup
import sys
import os
import requests
import uuid
import json
import importlib
from datetime import datetime
import traceback
import warnings
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2  # Set COM threading model

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QMessageBox,
                             QDesktopWidget)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
import pyautogui
import psutil
import comtypes

# Custom utility imports
from utils.apps import app_list, office_app_list
from utils.user import get_userid
from utils.common import get_temp_path, get_temp_session_path, encode_image
from utils.api import retry_api_call
from action.screenshot import capture_screenshot

# API endpoint
API_URL = "http://44.209.219.172:8000"
# API_URL = "http://localhost:8585"

# 2. APIThread Class
class APIThread(QThread):
    """
    A custom QThread subclass for handling API calls asynchronously.
    This prevents the GUI from freezing during API operations.
    """
    log_signal = pyqtSignal(str, str)
    result_signal = pyqtSignal(dict)
    reset_signal = pyqtSignal()

    def __init__(self, main_window, method_name, **kwargs):
        super().__init__()
        self.main_window = main_window
        self.method_name = method_name
        self.kwargs = kwargs
        sys.excepthook = self.handle_uncaught_exception
        self.reset_signal.connect(self.main_window.reset_app_state)

    def run(self):
        """Execute the specified method with given arguments."""
        method = getattr(self.main_window, self.method_name)
        result = method(**self.kwargs)
        if result:
            self.result_signal.emit(result)

    def handle_uncaught_exception(self, exctype, value, traceback_obj):
        """Handle any uncaught exceptions in the thread."""
        traceback_text = ''.join(traceback.format_exception(exctype, value, traceback_obj))
        error_message = f"Uncaught exception: {exctype.__name__}: {str(value)}\n\n{traceback_text}"
        self.log_signal.emit(error_message, "Error")
        self.reset_signal.emit()

# 3. MainWindow Class
class MainWindow(QMainWindow):
    """
    The main application window class.
    Handles the GUI and core functionality of the Auto UI Assist tool.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto UI Assist")
        self.setup_window_geometry()
        self.setup_ui()
        self.setup_backend()
        self.api_thread = None

    # 3.1 UI Setup Methods
    def setup_window_geometry(self):
        """Set up the window size and position."""
        screen_geometry = QDesktopWidget().screenGeometry()
        window_width, window_height = 550, 400
        x = screen_geometry.width() - window_width - 10
        y = screen_geometry.height() - window_height - 70
        self.setGeometry(x, y, window_width, window_height)

    def setup_ui(self):
        """Set up the user interface components."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.init_logs_section()
        self.init_input_section()
        self.setStyleSheet(self.load_styles())

    def load_styles(self):
        """Load and return CSS styles for the UI."""
        return """
            QMainWindow {
                background-color: #333333;
            }
            QLabel {
                color: #f5f5f5;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                font-size: 14px;
                color: #f5f5f5;
                background-color: #555555;
            }
            QPushButton {
                background-color: #0066ff;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0080ff;
            }
            QTextEdit {
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                font-size: 14px;
                color: #f5f5f5;
                background-color: #555555;
            }
        """

    def init_logs_section(self):
        """Initialize the logs section of the UI."""
        logs_layout = QVBoxLayout()
        logs_label = QLabel("Logs:")
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        logs_layout.addWidget(logs_label)
        logs_layout.addWidget(self.logs_text)
        self.layout.addLayout(logs_layout)

    def init_input_section(self):
        """Initialize the input section of the UI."""
        self.input_section = QWidget()
        input_layout = QHBoxLayout(self.input_section)
        self.input_textbox = QLineEdit()
        self.input_textbox.setPlaceholderText("Enter your task")
        self.input_button = QPushButton("Submit")
        self.input_button.clicked.connect(self.handle_input)
        self.input_textbox.returnPressed.connect(self.input_button.click)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_process)
        input_layout.addWidget(self.input_textbox)
        input_layout.addWidget(self.input_button)
        input_layout.addWidget(self.cancel_button)
        self.layout.addWidget(self.input_section)

    # 3.2 Backend Setup Method
    def setup_backend(self):
        """Set up backend-related attributes and configurations."""
        self.app_name = "autoUIAssist"
        self.app_pid = os.getpid()
        self.work_app_pid = None
        self.app_temp_path = get_temp_path(self.app_name)
        self.userid = get_userid(self.app_temp_path)
        self.user_session_uuid = str(uuid.uuid4())
        self.temp_session_path = get_temp_session_path(self.app_temp_path, self.user_session_uuid)
        self.api_url = API_URL
        self.os_apps = app_list(self.user_session_uuid)
        self.action_history = []
        self.current_stage = "task"

    # 3.3 Logging Method
    def log_message(self, message, log_type="Info"):
        """Log a message with a specified type and format."""
        message = message.strip()
        log_colors_emojis = {
            "Warning": ("⚠️", "#ff9800"),
            "Info": ("ℹ️", "#ffffff"),
            "Debug": ("🐞", "#00ffff"),
            "User Input": ("📢", "#00ff00"),
            "Error": ("❌", "#ff0000")
        }
        emoji, color = log_colors_emojis.get(log_type, ("", "black"))
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f'<font color="{color}">{emoji} [{log_type}] [{current_time}] {message}</font>'
        self.logs_text.append(formatted_message)

        # Write logs to a file
        log_file_path = os.path.join(self.temp_session_path, "session_log.txt")
        with open(log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"{emoji} [{log_type}] [{current_time}] {message}\n")

        if log_type == "Error":
            error_message = f"An error occurred.<br>Error Message: {message}<br>Please check the log file at: <br>{log_file_path}<br><br>Maybe close the app and start again if the error persists."
            QMessageBox.critical(self, "Error", f'<font color="black">{error_message}</font>')

    # 3.4 Input Handling Method
    def handle_input(self):
        """Handle user input based on the current stage of the application."""
        user_input = self.input_textbox.text()
        if user_input.lower() in ["exit", "quit"]:
            self.log_message("Application terminated by the user.", "Info")
            QApplication.quit()
            return

        if self.current_stage == "question":
            self.log_message(f"User Answer: {user_input}", "User Input")
            self.process_user_answer(user_input)
        else:
            if user_input:
                if self.current_stage == "task":
                    self.log_message(f"User Task: {user_input}", "User Input")
                    self.user_task = user_input
                    self.start_api_thread("task_corrector", user_task=self.user_task)
                elif self.current_stage == "action_plan":
                    self.log_message(f"User Correction: {user_input}", "User Input")
                    self.start_api_thread("action_plan_refiner", feedback=user_input, step_list=self.step_list)
            else:
                if self.current_stage != "question":
                    QMessageBox.warning(self, "Input Error", "Please enter the required information.")

        self.input_textbox.clear()

    # 3.5 API Thread Management Methods
    def start_api_thread(self, method_name, **kwargs):
        """Start an API thread for a given method with specified arguments."""
        self.api_thread = APIThread(self, method_name, **kwargs)
        self.api_thread.log_signal.connect(self.log_message)
        self.api_thread.result_signal.connect(getattr(self, f"process_{method_name}_result"))
        self.api_thread.start()
        self.input_textbox.setEnabled(False)
        self.input_button.setEnabled(False)

    # 3.6 Question Handling Methods
    def show_question_section(self):
        """Initiate the question refinement process."""
        self.start_api_thread("task_refiner_stage_1", user_task=self.user_task)

    def show_next_question(self):
        """Display the next question or proceed to task refinement."""
        if len(self.user_answers) < len(self.refinement_questions):
            current_question = self.refinement_questions[len(self.user_answers)]
            self.log_message(f"Refinement Question: {current_question}", "Debug")
            self.input_textbox.setPlaceholderText(f"Q: {current_question}")
            self.input_textbox.setEnabled(True)
            self.input_button.setEnabled(True)
        else:
            self.input_textbox.setEnabled(False)
            self.input_button.setEnabled(False)
            qna_str = self.compile_user_answers()
            self.start_api_thread("task_refiner_stage_2", refinement_data=qna_str)

    def process_user_answer(self, user_answer):
        """Process the user's answer and move to the next question or stage."""
        self.user_answers.append(user_answer)
        if len(self.user_answers) < len(self.refinement_questions):
            self.show_next_question()
        else:
            self.input_textbox.setEnabled(False)
            self.input_button.setEnabled(False)
            qna_str = self.compile_user_answers()
            self.start_api_thread("task_refiner_stage_2", refinement_data=qna_str)

    def compile_user_answers(self):
        """Compile user answers into a formatted string."""
        return "\n\n".join([f"Q: {q}\nA: {a}" for q, a in zip(self.refinement_questions, self.user_answers)])

    # 3.7 Action Plan Methods
    def show_action_plan_section(self):
        """Initiate the creation of a high-level action plan."""
        self.start_api_thread("high_level_action_plan_creation", user_task=self.user_task, first_office_app_type=self.first_office_app_type)

    def verify_action_plan(self):
        """Verify the created action plan."""
        MAX_ATTEMPTS = 3
        CURRENT_ATTEMPT = 0
        while CURRENT_ATTEMPT < MAX_ATTEMPTS:
            CURRENT_ATTEMPT += 1
            self.log_message(f"Attempt {CURRENT_ATTEMPT} to verify the action plan", "Debug")
            self.start_api_thread("action_plan_verifier", user_task=self.user_task, step_list=json.dumps(self.step_list))
            break
        else:
            self.log_message("Action plan not verified after 3 attempts. Exiting...", "Error")
            sys.exit()

    # 3.8 Timer Methods
    def start_timer(self):
        """Start a timer for user input."""
        self.time_left = 5
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        self.timer_label = QLabel(f"Time remaining: {self.time_left} seconds")
        self.layout.addWidget(self.timer_label)

    def update_timer(self):
        """Update the timer and handle timeout."""
        self.time_left -= 1
        self.timer_label.setText(f"Time remaining: {self.time_left} seconds")
        if self.time_left == 0:
            self.timer.stop()
            self.log_message("Time is up! Using scratchpad.", "Warning")
            self.handle_input()

    # 3.9 API Call Methods (continued)
    @retry_api_call(max_attempts=3, delay=1)
    def task_corrector(self, user_task):
        """
        Call the task corrector API to refine and correct the user's task.
        
        Args:
            user_task (str): The original task input by the user.
        
        Returns:
            dict: The API response containing the corrected task and other details.
        """
        self.api_thread.log_signal.emit(f"Correcting task: {user_task}", "Debug")
        desktop_image = pyautogui.screenshot()
        desktop_image_encoded = encode_image(IMAGE_object=desktop_image)
        task_corrector_uri = f"{self.api_url}/task_corrector"
        task_corrector_payload = {
            "userid": self.userid,
            "sessionid": self.user_session_uuid,
            "os": "windows",
            "task": user_task,
            "app_list": self.os_apps,
            "image_base64": desktop_image_encoded,
        }
        try:
            response = requests.post(task_corrector_uri, json=task_corrector_payload)
            response.raise_for_status()
            response = json.loads(response.text)
        except Exception as e:
            self.api_thread.log_signal.emit(f"Error: {str(e)}\n\n{traceback.format_exc()}", "Error")
            raise e
        print_response = response['corrected_task']
        self.api_thread.log_signal.emit(f"Corrected task: {print_response}", "Debug")
        return response
    
    def process_task_corrector_result(self, result):
        """
        Process the result from the task corrector API and determine the next step.
        
        Args:
            result (dict): The API response from the task corrector.
        """
        self.user_task = result["corrected_task"]
        launch_app_list = result["selected_app_list"]
        try:
            self.first_office_app, self.first_office_app_type = office_app_list(os_apps=launch_app_list)
            self.first_office_app_name = self.first_office_app_type[1]
            self.first_office_app_type = self.first_office_app_type[0]
        except Exception as e:
            self.log_message(f"Error getting office application: {str(e)}", "Error")
            self.reset_app_state()
            return
        if result["refinement"]:
            self.log_message("Refinement requested", "Warning")
            self.current_stage = "question"
            self.show_question_section()
        else:
            self.current_stage = "action_plan"
            self.show_action_plan_section()

    @retry_api_call(max_attempts=3, delay=1)
    def task_refiner_stage_1(self, user_task):
        """
        Call the task refiner stage 1 API to generate refinement questions.
        
        Args:
            user_task (str): The corrected user task.
        
        Returns:
            dict: The API response containing refinement questions.
        """
        self.api_thread.log_signal.emit(f"Refining task: {user_task}", "Debug")
        desktop_image = pyautogui.screenshot()
        desktop_image_encoded = encode_image(IMAGE_object=desktop_image)
        task_refiner_stage_1_uri = f"{self.api_url}/task_refiner_stage_1"
        task_refiner_stage_1_payload = {
            "userid": self.userid,
            "sessionid": self.user_session_uuid,
            "os": "windows",
            "task": user_task,
            "image_base64": desktop_image_encoded
        }
        try:
            response = requests.post(task_refiner_stage_1_uri, json=task_refiner_stage_1_payload)
            response.raise_for_status()
            response = json.loads(response.text)
        except Exception as e:
            self.api_thread.log_signal.emit(f"Error: {str(e)}\n\n{traceback.format_exc()}", "Error")
            raise e
        print_response = response['refinement_question_list']
        self.api_thread.log_signal.emit(f"Refinement questions: {print_response}", "Debug")
        return response

    def process_task_refiner_stage_1_result(self, result):
        """
        Process the result from the task refiner stage 1 API and initiate the questioning process.
        
        Args:
            result (dict): The API response containing refinement questions.
        """
        self.refinement_questions = result["refinement_question_list"]
        self.user_answers = []
        self.show_next_question()

    @retry_api_call(max_attempts=3, delay=1)
    def task_refiner_stage_2(self, refinement_data):
        """
        Call the task refiner stage 2 API to generate the final refined task.
        
        Args:
            refinement_data (str): Compiled questions and answers from the refinement process.
        
        Returns:
            dict: The API response containing the final refined task.
        """
        self.api_thread.log_signal.emit(f"Refining task with answers: {refinement_data}", "Debug")
        task_refiner_stage_2_uri = f"{self.api_url}/task_refiner_stage_2"
        task_refiner_stage_2_payload = {
            "userid": self.userid,
            "sessionid": self.user_session_uuid,
            "os": "windows",
            "task": self.user_task,
            "refinement_data": refinement_data,
        }
        try:
            response = requests.post(task_refiner_stage_2_uri, json=task_refiner_stage_2_payload)
            response.raise_for_status()
            response = json.loads(response.text)
        except Exception as e:
            self.api_thread.log_signal.emit(f"Error: {str(e)}\n\n{traceback.format_exc()}", "Error")
            raise e
        print_response = response['refined_task']
        self.api_thread.log_signal.emit(f"Final refined task: {print_response}", "Debug")
        return response

    def process_task_refiner_stage_2_result(self, result):
        """
        Process the result from the task refiner stage 2 API and move to action plan creation.
        
        Args:
            result (dict): The API response containing the final refined task.
        """
        self.user_task = result["refined_task"]
        self.current_stage = "action_plan"
        self.show_action_plan_section()

    @retry_api_call(max_attempts=3, delay=1)
    def high_level_action_plan_creation(self, user_task, first_office_app_type):
        """
        Call the high-level action plan creation API to generate a series of steps for the task.
        
        Args:
            user_task (str): The refined user task.
            first_office_app_type (str): The type of office application to be used.
        
        Returns:
            dict: The API response containing the high-level action plan steps.
        """
        self.api_thread.log_signal.emit(f"Creating high level action plan for task: {user_task}", "Debug")
        desktop_image = pyautogui.screenshot()
        desktop_image_encoded = encode_image(IMAGE_object=desktop_image)
        high_level_action_plan_creation_uri = f"{self.api_url}/high_level_action_plan_creation"
        high_level_action_plan_creation_payload = {
            "userid": self.userid,
            "sessionid": self.user_session_uuid,
            "os": "windows",
            "task": user_task,
            "app": first_office_app_type,
            "image_base64": desktop_image_encoded,
        }
        try:
            response = requests.post(high_level_action_plan_creation_uri, json=high_level_action_plan_creation_payload)
            response.raise_for_status()
            response = json.loads(response.text)
        except Exception as e:
            self.api_thread.log_signal.emit(f"Error: {str(e)}\n\n{traceback.format_exc()}", "Error")
            raise e
        print_response = response['step_list']
        self.api_thread.log_signal.emit(f"Step planner: {print_response}", "Debug")
        return response
    
    def process_high_level_action_plan_creation_result(self, result):
        """
        Process the result from the high-level action plan creation API and initiate plan verification.
        
        Args:
            result (dict): The API response containing the high-level action plan.
        """
        self.step_list = result["step_list"]
        self.verify_action_plan()

    @retry_api_call(max_attempts=3, delay=1)
    def action_plan_verifier(self, user_task, step_list):
        """
        Call the action plan verifier API to check if the generated plan is valid.
        
        Args:
            user_task (str): The refined user task.
            step_list (str): JSON string of the high-level action plan steps.
        
        Returns:
            dict: The API response containing verification results.
        """
        self.api_thread.log_signal.emit(f"Verifying action plan for task: {user_task}", "Debug")
        desktop_image = pyautogui.screenshot()
        desktop_image_encoded = encode_image(IMAGE_object=desktop_image)
        action_plan_verifier_uri = f"{self.api_url}/action_plan_verifier"
        action_plan_verifier_payload = {
            "userid": self.userid,
            "sessionid": self.user_session_uuid,
            "os": "windows",
            "task": user_task,
            "step_list": step_list,
            "image_base64": desktop_image_encoded,
        }
        try:
            response = requests.post(action_plan_verifier_uri, json=action_plan_verifier_payload)
            response.raise_for_status()
            response = json.loads(response.text)
        except Exception as e:
            self.api_thread.log_signal.emit(f"Error: {str(e)}\n\n{traceback.format_exc()}", "Error")
            raise e
        print_response_verified = response['verified']
        print_response_scratchpad = response['scratchpad']
        self.api_thread.log_signal.emit(f"Verified: {print_response_verified} | Scratchpad: {print_response_scratchpad}", "Debug")
        return response

    def process_action_plan_verifier_result(self, result):
        """
        Process the result from the action plan verifier API and determine the next step.
        
        Args:
            result (dict): The API response containing verification results.
        """
        verified = result["verified"]
        if 'true' == verified.strip().lower():
            self.log_message("Action plan verified", "Debug")
            self.execute_actions()
        else:
            self.log_message("Action plan not verified", "Warning")
            self.log_message(f"Scratchpad: {result['scratchpad']}", "Warning")
            self.input_textbox.setPlaceholderText("Please help correct the action plan (if left empty will use scratchpad to refine it further. Field timesout in 5 sec): ")
            self.input_textbox.setEnabled(True)
            self.input_button.setEnabled(True)
            self.start_timer()

    @retry_api_call(max_attempts=3, delay=1)
    def action_plan_refiner(self, feedback, step_list):
        """
        Call the action plan refiner API to improve the action plan based on feedback.
        
        Args:
            feedback (str): User feedback on the action plan.
            step_list (str): The current action plan steps.
        
        Returns:
            dict: The API response containing the refined action plan.
        """
        self.api_thread.log_signal.emit(f"Refining action plan with feedback: {feedback}", "Debug")
        desktop_image = pyautogui.screenshot()
        desktop_image_encoded = encode_image(IMAGE_object=desktop_image)
        action_plan_refiner_uri = f"{self.api_url}/action_plan_refiner"
        action_plan_refiner_payload = {
            "userid": self.userid,
            "sessionid": self.user_session_uuid,
            "os": "windows",
            "task": self.user_task,
            "step_list": step_list,
            "feedback": feedback,
            "image_base64": desktop_image_encoded,
        }
        try:
            response = requests.post(action_plan_refiner_uri, json=action_plan_refiner_payload)
            response.raise_for_status()
            response = json.loads(response.text)
        except Exception as e:
            self.api_thread.log_signal.emit(f"Error: {str(e)}\n\n{traceback.format_exc()}", "Error")
            raise e
        print_response = response['step_list']
        self.api_thread.log_signal.emit(f"Refined steps: {print_response}", "Debug")
        return response

    def process_action_plan_refiner_result(self, result):
        """
        Process the result from the action plan refiner API and start executing the refined plan.
        
        Args:
            result (dict): The API response containing the refined action plan.
        """
        self.step_list = result["step_list"]
        self.execute_actions()

    # 3.10 Action Execution Methods
    def execute_actions(self):
        """
        Start the execution of the action plan by loading the appropriate module and executing the first action.
        """
        module = importlib.import_module(f"app_tools.{self.first_office_app_type}.function_call_repo")
        self.TOOLING = module.TOOLING

        self.current_action_index = 0
        self.execute_next_action()
    
    def execute_next_action(self):
        """
        Execute the next action in the action plan or finish the task if all actions are completed.
        """
        if self.current_action_index < len(self.step_list):
            step = self.step_list[self.current_action_index][f"step_{self.current_action_index+1}"]
            self.log_message(f"Step: {step}", "Debug")

            temp_session_step_path = os.path.join(self.temp_session_path, f"step_{self.current_action_index+1}")
            app_window_ann_screenshot_path, app_window_coordinate_dict = capture_screenshot(
                screenshot_type="app_window",
                app_title=self.first_office_app_name,
                temp_session_step_path=temp_session_step_path
            )
            app_window_ann_screenshot_base64 = encode_image(app_window_ann_screenshot_path)

            self.start_api_thread("low_level_action_plan_creation", 
                                  user_task=self.user_task, 
                                  step=step, 
                                  first_office_app_type=self.first_office_app_type, 
                                  app_window_ann_screenshot_base64=app_window_ann_screenshot_base64, 
                                  TOOLING=self.TOOLING)
        else:
            self.log_message("Task execution completed.", "Info")
            self.reset_app_state()

    @retry_api_call(max_attempts=3, delay=1)
    def low_level_action_plan_creation(self, user_task, step, first_office_app_type, app_window_ann_screenshot_base64, TOOLING):
        """
        Call the low-level action plan creation API to generate specific actions for a step.
        
        Args:
            user_task (str): The refined user task.
            step (str): The current high-level step to be broken down.
            first_office_app_type (str): The type of office application being used.
            app_window_ann_screenshot_base64 (str): Base64 encoded screenshot of the application window.
            TOOLING (dict): Available tools and functions for the specific application.
        
        Returns:
            dict: The API response containing the low-level action plan.
        """
        self.api_thread.log_signal.emit(f"Creating low level action plan for step: {step}", "Debug")
        low_level_action_plan_creation_uri = f"{self.api_url}/low_level_action_plan_creation"
        low_level_action_plan_creation_payload = {
            "userid": self.userid,
            "sessionid": self.user_session_uuid,
            "os": "windows",
            "task": user_task,
            "step": step,
            "app": first_office_app_type,
            "previous_execution_data": "\n".join(self.action_history),
            "tooling": json.dumps(TOOLING),
            "image_base64": app_window_ann_screenshot_base64,
        }
        try:
            response = requests.post(low_level_action_plan_creation_uri, json=low_level_action_plan_creation_payload)
            response.raise_for_status()
            response = json.loads(response.text)
            self.api_thread.log_signal.emit(f"Response: {response}", "Debug")
        except Exception as e:
            self.api_thread.log_signal.emit(f"Error: {str(e)}\n\n{traceback.format_exc()}", "Error")
            raise e
        try:
            print_response = response['action_list']
            self.api_thread.log_signal.emit(f"Low level action plan: {print_response}", "Debug")
        except Exception as e:
            self.api_thread.log_signal.emit("No action detected", "Warning")
            response = {"action_list": None}
        return response

    def process_low_level_action_plan_creation_result(self, result):
        """
        Process the result from the low-level action plan creation API and execute the actions.
        
        Args:
            result (dict): The API response containing the low-level action plan.
        """
        self.log_message("Processing low level action plan", "Debug")
        self.log_message(f"Action list: {result}", "Debug")
        low_level_action_plan = result['action_list']

        if low_level_action_plan:
            for i, action in enumerate(low_level_action_plan):
                self.log_message(f"Action {i}: {action}", "Debug")
                if ((not isinstance(action, list)) or (not isinstance(action, dict))) and len(action) <= 0:
                    continue
                self.log_message(f"Action running: {action[f'action_{i+1}']}", "Debug")
                action = action[f'action_{i+1}']
                if 'action_function_call' in action:
                    self.log_message(f"Action: {action}", "Debug")
                    function_name = action['action_function_call']
                    if "action_scratchpad" in action:
                        action_scratchpad = action["action_scratchpad"]
                        history_note = f"""
            Function Called: {function_name}
            Action Scratchpad: {action_scratchpad}
                        """
                    else:
                        history_note = f"""
            Function Called: {function_name}
                        """
                    self.action_history.append(history_note)
                    if "parameters" in action:
                        parameters = action['parameters']
                        parameters["extra_args"] = {"temp_session_step_path": self.temp_session_path}
                    else:
                        parameters = {"extra_args": {"temp_session_step_path": self.temp_session_path}}

                    for tool in self.TOOLING:
                        if tool['name'] == function_name:
                            function_path = tool['function_path']
                            break
                    module = importlib.import_module(function_path)
                    function_call = getattr(module, function_name)
                    
                    # Switch to app before executing the function
                    switch_app_function = getattr(module, "switch_to_app")
                    switch_app_function(extra_args={"temp_session_step_path": self.temp_session_path})
                    
                    # Execute the function
                    try:
                        self.log_message(f"Executing function '{function_name}'", "Debug")
                        function_call(**parameters)
                    except Exception as e:
                        self.log_message(f"Error executing function '{function_name}': {str(e)}", "Error")
        else:
            self.log_message("No actions detected, skipping execution", "Warning")
        self.current_action_index += 1
        self.execute_next_action()

    # 3.12 Utility Methods
    def reset_app_state(self):
        """
        Reset the application state to its initial condition, ready for a new task.
        """
        self.current_stage = "task"
        self.user_task = ""
        self.user_answers = []
        self.refinement_questions = []
        self.step_list = []
        self.action_history = []
        self.input_textbox.setEnabled(True)
        self.input_button.setEnabled(True)
        self.cancel_button.setEnabled(True)
        self.input_textbox.setPlaceholderText("Enter your task")
        self.input_textbox.clear()
        self.log_message("Application reset. You can start with a new task now.", "Info")

    def cancel_process(self):
        """
        Cancel the current process and reset the application state.
        """
        if self.api_thread and self.api_thread.isRunning():
            self.api_thread.terminate()
            self.log_message("Process cancelled by the user.", "Warning")
        self.reset_app_state()

# 4. Main Execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

# 5. Code Structure Overview
# The Auto UI Assist application is structured as follows:
# 
# 5.1. Imports and Setup:
#   - Import necessary libraries and modules
#   - Set up system configurations
# 
# 5.2. APIThread Class:
#   - Handles asynchronous API calls
#   - Manages exceptions and signals results back to the main thread
# 
# 5.3. MainWindow Class:
#   - The core of the application, handling the GUI and logic
#   - Divided into several sections:
#     5.3.1. Initialization and UI Setup
#     5.3.2. Backend Setup
#     5.3.3. Logging
#     5.3.4. Input Handling
#     5.3.5. API Thread Management
#     5.3.6. Question Handling
#     5.3.7. Action Plan Methods
#     5.3.8. Timer Methods
#     5.3.9. API Call Methods
#     5.3.10. Action Execution Methods
#     5.3.11. Result Processing Methods
#     5.3.12. Utility Methods
# 
# 5.4. Main Execution:
#   - Creates the QApplication instance
#   - Initializes and shows the MainWindow
#   - Starts the event loop
# 
# This structure allows for a modular and organized approach to handling
# the complex task of UI automation, from user input to task execution.
