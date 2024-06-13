import sys
import os
import requests
import uuid
import json
import importlib
from datetime import datetime

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from dotenv import load_dotenv
import pyautogui

from utils.apps import app_list, office_app_list
from utils.user import get_userid
from utils.common import get_temp_path, get_temp_session_path, encode_image
from utils.api import retry_api_call
from action.screenshot import capture_screenshot

load_dotenv()

class APIThread(QThread):
    log_signal = pyqtSignal(str)
    result_signal = pyqtSignal(dict)

    def __init__(self, main_window, method_name, **kwargs):
        super().__init__()
        self.main_window = main_window
        self.method_name = method_name
        self.kwargs = kwargs

    def run(self):
        method = getattr(self.main_window, self.method_name)
        result = method(**self.kwargs)
        self.result_signal.emit(result)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Auto UI Assist")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.init_logs_section()
        self.init_input_section()

        self.current_stage = "task"

        self.setStyleSheet(self.load_styles())

        self.setup_backend()

        self.api_thread = None

    def load_styles(self):
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
        logs_layout = QVBoxLayout()

        logs_label = QLabel("Logs:")
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)

        logs_layout.addWidget(logs_label)
        logs_layout.addWidget(self.logs_text)

        self.layout.addLayout(logs_layout)

    def init_input_section(self):
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

    def setup_backend(self):
        self.app_name = "autoUIAssist"
        self.app_temp_path = get_temp_path(self.app_name)
        self.userid = get_userid(self.app_temp_path)
        self.user_session_uuid = str(uuid.uuid4())
        self.temp_session_path = get_temp_session_path(self.app_temp_path, self.user_session_uuid)
        self.api_url = os.getenv("API_URL")
        self.os_apps = app_list(self.user_session_uuid)

    def log_message(self, message, log_type="Info"):
        message = message.strip()  # Remove whitespace and newline characters from both ends

        log_colors_emojis = {
            "Warning": ("⚠️", "#ff9800"),  # Orange
            "Info": ("ℹ️", "#ffffff"),  # White
            "Debug": ("🐞", "#00ffff"),  # Cyan
            "User Input": ("📢", "#00ff00"),  # Bright Green
            "Error": ("❌", "#ff0000")  # Bright Red
        }

        emoji, color = log_colors_emojis.get(log_type, ("", "black"))  # Get the emoji and color based on the log_type, default to empty string and black if not found

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current timestamp

        formatted_message = f'<font color="{color}">{emoji} [{log_type}] [{current_time}] {message}</font>'
        self.logs_text.append(formatted_message)

    def handle_input(self):
        user_input = self.input_textbox.text()
        if user_input.lower() in ["exit", "quit"]:
            self.log_message("Application terminated by the user.", log_type="Info")
            QApplication.quit()
            return

        if self.current_stage == "question":
            self.log_message(f"User Answer: {user_input}", log_type="User Input")
            self.process_user_answer(user_input)
        else:
            if user_input:
                if self.current_stage == "task":
                    self.log_message(f"User Task: {user_input}", log_type="User Input")
                    self.user_task = user_input
                    self.api_thread = APIThread(self, "task_corrector", user_task=self.user_task)
                    self.api_thread.log_signal.connect(self.log_message)
                    self.api_thread.result_signal.connect(self.process_task_corrector_result)
                    self.api_thread.start()
                    self.input_textbox.setEnabled(False)  # Disable the text box
                    self.input_button.setEnabled(False)  # Disable the button
                elif self.current_stage == "action_plan":
                    self.log_message(f"User Correction: {user_input}", log_type="User Input")
                    self.api_thread = APIThread(self, "action_plan_refiner", feedback=user_input, step_list=self.step_list)
                    self.api_thread.log_signal.connect(self.log_message)
                    self.api_thread.result_signal.connect(self.process_action_plan_refiner_result)
                    self.api_thread.start()
                    self.input_textbox.setEnabled(False)  # Disable the text box
                    self.input_button.setEnabled(False)  # Disable the button
            else:
                if self.current_stage != "question":
                    QMessageBox.warning(self, "Input Error", "Please enter the required information.")

        self.input_textbox.clear()

    def show_question_section(self):
        self.api_thread = APIThread(self, "task_refiner_stage_1", user_task=self.user_task)
        self.api_thread.log_signal.connect(self.log_message)
        self.api_thread.result_signal.connect(self.process_task_refiner_stage_1_result)
        self.api_thread.start()
        self.input_textbox.setEnabled(False)  # Disable the text box
        self.input_button.setEnabled(False)  # Disable the button

    def show_next_question(self):
        if len(self.user_answers) < len(self.refinement_questions):
            current_question = self.refinement_questions[len(self.user_answers)]
            self.log_message(f"Refinement Question: {current_question}", log_type="Debug")
            self.input_textbox.setPlaceholderText(f"Q: {current_question}")
            self.input_textbox.setEnabled(True)  # Enable the text box
            self.input_button.setEnabled(True)  # Enable the button
        else:
            self.input_textbox.setEnabled(False)  # Disable the text box
            self.input_button.setEnabled(False)  # Disable the button
            qna_str = self.compile_user_answers()
            self.api_thread = APIThread(self, "task_refiner_stage_2", refinement_data=qna_str)
            self.api_thread.log_signal.connect(self.log_message)
            self.api_thread.result_signal.connect(self.process_task_refiner_stage_2_result)
            self.api_thread.start()

    def process_user_answer(self, user_answer):
        self.user_answers.append(user_answer)
        if len(self.user_answers) < len(self.refinement_questions):
            self.show_next_question()
        else:
            self.input_textbox.setEnabled(False)  # Disable the text box
            self.input_button.setEnabled(False)  # Disable the button
            qna_str = self.compile_user_answers()
            self.api_thread = APIThread(self, "task_refiner_stage_2", refinement_data=qna_str)
            self.api_thread.log_signal.connect(self.log_message)
            self.api_thread.result_signal.connect(self.process_task_refiner_stage_2_result)
            self.api_thread.start()

    def compile_user_answers(self):
        qna_str = ""
        for question, answer in zip(self.refinement_questions, self.user_answers):
            qna_str += f"Q: {question}\nA: {answer}\n\n"
        return qna_str

    def show_action_plan_section(self):
        self.api_thread = APIThread(self, "high_level_action_plan_creation", user_task=self.user_task, first_office_app_type=self.first_office_app_type)
        self.api_thread.log_signal.connect(self.log_message)
        self.api_thread.result_signal.connect(self.process_high_level_action_plan_creation_result)
        self.api_thread.start()
        self.input_textbox.setEnabled(False)  # Disable the text box
        self.input_button.setEnabled(False)  # Disable the button

    def verify_action_plan(self):
        MAX_ATTEMPTS = 3
        CURRENT_ATTEMPT = 0
        while CURRENT_ATTEMPT < MAX_ATTEMPTS:
            CURRENT_ATTEMPT += 1
            self.log_message(f"Attempt {CURRENT_ATTEMPT} to verify the action plan", log_type="Debug")
            self.api_thread = APIThread(self, "action_plan_verifier", user_task=self.user_task, step_list=json.dumps(self.step_list))
            self.api_thread.log_signal.connect(self.log_message)
            self.api_thread.result_signal.connect(self.process_action_plan_verifier_result)
            self.api_thread.start()
            break
        else:
            self.log_message("Action plan not verified after 3 attempts. Exiting...", log_type="Error")
            sys.exit()

    def start_timer(self):
        self.time_left = 5
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        self.timer_label = QLabel(f"Time remaining: {self.time_left} seconds")
        self.layout.addWidget(self.timer_label)

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"Time remaining: {self.time_left} seconds")
        if self.time_left == 0:
            self.timer.stop()
            self.log_message("Time is up! Using scratchpad.", log_type="Warning")
            self.handle_input()

    @retry_api_call(max_attempts=3, delay=1)
    def task_corrector(self, user_task):
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
        response = requests.post(task_corrector_uri, json=task_corrector_payload)
        response = json.loads(response.text)
        self.api_thread.log_signal.emit(f"Corrected task: {response['corrected_task']}")
        return response

    @retry_api_call(max_attempts=3, delay=1)
    def task_refiner_stage_1(self, user_task):
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
        response = requests.post(task_refiner_stage_1_uri, json=task_refiner_stage_1_payload)
        response = json.loads(response.text)
        self.api_thread.log_signal.emit(f"Refinement questions: {response['refinement_question_list']}")
        return response

    @retry_api_call(max_attempts=3, delay=1)
    def task_refiner_stage_2(self, refinement_data):
        task_refiner_stage_2_uri = f"{self.api_url}/task_refiner_stage_2"
        task_refiner_stage_2_payload = {
            "userid": self.userid,
            "sessionid": self.user_session_uuid,
            "os": "windows",
            "task": self.user_task,
            "refinement_data": refinement_data,
        }
        response = requests.post(task_refiner_stage_2_uri, json=task_refiner_stage_2_payload)
        response = json.loads(response.text)
        self.api_thread.log_signal.emit(f"Final refined task: {response['refined_task']}")
        return response

    @retry_api_call(max_attempts=3, delay=1)
    def high_level_action_plan_creation(self, user_task, first_office_app_type):
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
        response = requests.post(high_level_action_plan_creation_uri, json=high_level_action_plan_creation_payload)
        response = json.loads(response.text)
        self.api_thread.log_signal.emit(f"Step planner: {response['step_list']}")
        return response

    @retry_api_call(max_attempts=3, delay=1)
    def action_plan_verifier(self, user_task, step_list):
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
        response = requests.post(action_plan_verifier_uri, json=action_plan_verifier_payload)
        response = json.loads(response.text)
        self.api_thread.log_signal.emit(f"Verified: {response['verified']}\nScratchpad: {response['scratchpad']}")
        return response

    @retry_api_call(max_attempts=3, delay=1)
    def action_plan_refiner(self, feedback, step_list):
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
        response = requests.post(action_plan_refiner_uri, json=action_plan_refiner_payload)
        response = json.loads(response.text)
        self.api_thread.log_signal.emit(f"Refined steps: {response['step_list']}")
        return response

    def execute_actions(self):
        module = importlib.import_module(f"app_tools.{self.first_office_app_type}.function_call_repo")
        TOOLING = module.TOOLING

        for i, step in enumerate(self.step_list):
            step = step[f"step_{i+1}"]
            self.log_message(f"Step: {step}")

            temp_session_step_path = os.path.join(self.temp_session_path, f"step_{i+1}")
            app_window_ann_screenshot_path, app_window_coordinate_dict = capture_screenshot(
                screenshot_type="app_window",
                app_title=self.first_office_app_name,
                temp_session_step_path=temp_session_step_path
            )
            app_window_ann_screenshot_base64 = encode_image(app_window_ann_screenshot_path)

            self.api_thread = APIThread(self, "low_level_action_plan_creation", user_task=self.user_task, step=step, first_office_app_type=self.first_office_app_type, app_window_ann_screenshot_base64=app_window_ann_screenshot_base64, TOOLING=TOOLING)
            self.api_thread.log_signal.connect(self.log_message)
            self.api_thread.result_signal.connect(lambda result: self.process_low_level_action_plan_creation_result(result, TOOLING))
            self.api_thread.start()
        
        self.log_message("Task execution completed.", log_type="Info")
        self.reset_app_state()

    @retry_api_call(max_attempts=3, delay=1)
    def low_level_action_plan_creation(self, user_task, step, first_office_app_type, app_window_ann_screenshot_base64, TOOLING):
        low_level_action_plan_creation_uri = f"{self.api_url}/low_level_action_plan_creation"
        low_level_action_plan_creation_payload = {
            "userid": self.userid,
            "sessionid": self.user_session_uuid,
            "os": "windows",
            "task": user_task,
            "step": step,
            "app": first_office_app_type,
            "tooling": json.dumps(TOOLING),
            "image_base64": app_window_ann_screenshot_base64,
        }
        response = requests.post(low_level_action_plan_creation_uri, json=low_level_action_plan_creation_payload)
        response = json.loads(response.text)
        self.api_thread.log_signal.emit(f"Low level action plan: {response}")
        return response
    
    def process_task_corrector_result(self, result):
        self.user_task = result["corrected_task"]
        launch_app_list = result["selected_app_list"]
        self.first_office_app, self.first_office_app_type = office_app_list(os_apps=launch_app_list)
        self.first_office_app_name = self.first_office_app_type[1]
        self.first_office_app_type = self.first_office_app_type[0]
        if result["refinement"]:
            self.log_message("Refinement requested", log_type="Warning")
            self.current_stage = "question"
            self.show_question_section()
        else:
            self.current_stage = "action_plan"
            self.show_action_plan_section()

    def process_task_refiner_stage_1_result(self, result):
        self.refinement_questions = result["refinement_question_list"]
        self.user_answers = []
        self.show_next_question()

    def process_task_refiner_stage_2_result(self, result):
        self.user_task = result["refined_task"]
        self.current_stage = "action_plan"
        self.show_action_plan_section()

    def process_high_level_action_plan_creation_result(self, result):
        self.step_list = result["step_list"]
        self.verify_action_plan()

    def process_action_plan_verifier_result(self, result):
        verified = result["verified"]
        if 'true' == verified.strip().lower():
            self.log_message("Action plan verified", log_type="Debug")
            self.execute_actions()
        else:
            self.log_message("Action plan not verified", log_type="Warning")
            self.log_message(f"Scratchpad: {result['scratchpad']}", log_type="Warning")
            self.input_textbox.setPlaceholderText("Please help correct the action plan (if left empty will use scratchpad to refine it further. Field timesout in 5 sec): ")
            self.input_textbox.setEnabled(True)  # Enable the text box
            self.input_button.setEnabled(True)  # Enable the button
            self.start_timer()

    def process_action_plan_refiner_result(self, result):
        self.step_list = result["step_list"]
        self.execute_actions()

    def process_low_level_action_plan_creation_result(self, result, TOOLING):
        low_level_action_plan = result['action_list']
        if not low_level_action_plan:
            self.log_message("No action detected", log_type="Warning")
            return

        for i, action in enumerate(low_level_action_plan):
            if not isinstance(action, list):
                continue
            if len(action) <= 0:
                continue
            action = action[f'action_{i+1}']
            self.log_message(f"Action: {action}", log_type="Debug")
            function_name = action['action_function_call']
            if "parameters" in action:
                parameters = action['parameters']
            else:
                parameters = None

            for tool in TOOLING:
                if tool['name'] == function_name:
                    function_path = tool['function_path']
                    break
            module = importlib.import_module(function_path)
            function_call = getattr(module, function_name)
            try:
                if parameters:
                    function_call(**parameters)
                else:
                    function_call()
            except Exception as e:
                self.log_message(f"Error executing function '{function_name}': {str(e)}", log_type="Error")
                
    def reset_app_state(self):
        self.current_stage = "task"
        self.user_task = ""
        self.user_answers = []
        self.refinement_questions = []
        self.step_list = []
        self.input_textbox.setEnabled(True)
        self.input_button.setEnabled(True)
        self.cancel_button.setEnabled(True)
        self.input_textbox.setPlaceholderText("Enter your task")
        self.input_textbox.clear()
        self.log_message("Application reset. You can start a new task now.", log_type="Info")

    def cancel_process(self):
        if self.api_thread and self.api_thread.isRunning():
            self.api_thread.terminate()
            self.log_message("Process cancelled by the user.", log_type="Warning")
        self.reset_app_state()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
