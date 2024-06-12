import sys
import os
import requests
import uuid
import json
import importlib
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTextEdit, QHBoxLayout)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMessageBox
from dotenv import load_dotenv
import pyautogui

from utils.apps import app_list, office_app_list
from utils.user import get_userid
from utils.common import get_temp_path, get_temp_session_path, encode_image
from utils.api import retry_api_call
from action.screenshot import capture_screenshot

load_dotenv()

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

        input_layout.addWidget(self.input_textbox)
        input_layout.addWidget(self.input_button)

        self.layout.addWidget(self.input_section)

    def setup_backend(self):
        self.app_name = "autoUIAssist"
        self.app_temp_path = get_temp_path(self.app_name)
        self.userid = get_userid(self.app_temp_path)
        self.user_session_uuid = str(uuid.uuid4())
        self.temp_session_path = get_temp_session_path(self.app_temp_path, self.user_session_uuid)
        self.api_url = os.getenv("API_URL")
        self.os_apps = app_list(self.user_session_uuid)

    def log_message(self, message):
        self.logs_text.append(message)

    def handle_input(self):
        user_input = self.input_textbox.text()
        if user_input:
            if self.current_stage == "task":
                self.log_message(f"User Task: {user_input}")
                self.user_task = user_input
                response = self.task_corrector()
                self.user_task = response["corrected_task"]
                launch_app_list = response["selected_app_list"]
                self.first_office_app, self.first_office_app_type = office_app_list(os_apps=launch_app_list)
                self.first_office_app_name = self.first_office_app_type[1]
                self.first_office_app_type = self.first_office_app_type[0]
                if response["refinement"]:
                    self.log_message("Refinement requested")
                    self.current_stage = "question"
                    self.show_question_section()
                else:
                    self.current_stage = "action_plan"
                    self.show_action_plan_section()
            elif self.current_stage == "question":
                self.log_message(f"User Answer: {user_input}")
                self.process_user_answer(user_input)
            elif self.current_stage == "action_plan":
                self.log_message(f"User Correction: {user_input}")
                response = self.action_plan_refiner(user_input)
                self.step_list = response["step_list"]
                self.execute_actions()
            self.input_textbox.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter the required information.")

    def show_question_section(self):
        self.refinement_questions = self.task_refiner_stage_1()["refinement_question_list"]
        self.user_answers = []
        self.show_next_question()

    def show_next_question(self):
        if len(self.user_answers) < len(self.refinement_questions):
            current_question = self.refinement_questions[len(self.user_answers)]
            self.log_message(f"Refinement Question: {current_question}")
            self.input_textbox.setPlaceholderText(f"Q: {current_question}\nA: ")
            self.input_textbox.setEnabled(True)
            self.input_button.setEnabled(True)
        else:
            self.input_textbox.setEnabled(False)
            self.input_button.setEnabled(False)
            qna_str = self.compile_user_answers()
            response = self.task_refiner_stage_2(qna_str)
            self.user_task = response["refined_task"]
            self.current_stage = "action_plan"
            self.show_action_plan_section()

    def process_user_answer(self, user_answer):
        self.user_answers.append(user_answer)
        if len(self.user_answers) < len(self.refinement_questions):
            self.show_next_question()
        else:
            qna_str = self.compile_user_answers()
            response = self.task_refiner_stage_2(qna_str)
            self.user_task = response["refined_task"]
            self.current_stage = "action_plan"
            self.show_action_plan_section()

    def compile_user_answers(self):
        qna_str = ""
        for question, answer in zip(self.refinement_questions, self.user_answers):
            qna_str += f"Q: {question}\nA: {answer}\n\n"
        return qna_str

    def show_action_plan_section(self):
        response = self.high_level_action_plan_creation()
        self.step_list = response["step_list"]
        self.verify_action_plan()

    def verify_action_plan(self):
        MAX_ATTEMPTS = 3
        CURRENT_ATTEMPT = 0
        while CURRENT_ATTEMPT < MAX_ATTEMPTS:
            CURRENT_ATTEMPT += 1
            self.log_message(f"Attempt {CURRENT_ATTEMPT} to verify the action plan")
            response = self.action_plan_verifier()
            verified = response["verified"]
            if 'true' == verified.strip().lower():
                self.log_message("Action plan verified")
                self.execute_actions()
                break
            else:
                self.log_message("Action plan not verified")
                self.log_message(f"Scratchpad: {response['scratchpad']}")
                self.input_textbox.setPlaceholderText("Please help correct the action plan (if left empty will use scratchpad to refine it further. Field timesout in 5 sec): ")
                self.input_textbox.setDisabled(False)
                self.start_timer()
        else:
            self.log_message("Action plan not verified after 3 attempts. Exiting...")
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
            self.log_message("Time is up! Using scratchpad.")
            self.handle_input()

    @retry_api_call(max_attempts=3, delay=1)
    def task_corrector(self):
        desktop_image = pyautogui.screenshot()
        desktop_image_encoded = encode_image(IMAGE_object=desktop_image)
        task_corrector_uri = f"{self.api_url}/task_corrector"
        task_corrector_payload = {
            "userid": self.userid,
            "sessionid": self.user_session_uuid,
            "os": "windows",
            "task": self.user_task,
            "app_list": self.os_apps,
            "image_base64": desktop_image_encoded,
        }
        response = requests.post(task_corrector_uri, json=task_corrector_payload)
        response = json.loads(response.text)
        self.log_message(f"Corrected task: {response['corrected_task']}")
        return response

    @retry_api_call(max_attempts=3, delay=1)
    def task_refiner_stage_1(self):
        desktop_image = pyautogui.screenshot()
        desktop_image_encoded = encode_image(IMAGE_object=desktop_image)
        task_refiner_stage_1_uri = f"{self.api_url}/task_refiner_stage_1"
        task_refiner_stage_1_payload = {
            "userid": self.userid,
            "sessionid": self.user_session_uuid,
            "os": "windows",
            "task": self.user_task,
            "image_base64": desktop_image_encoded
        }
        response = requests.post(task_refiner_stage_1_uri, json=task_refiner_stage_1_payload)
        response = json.loads(response.text)
        self.log_message(f"Refinement questions: {response['refinement_question_list']}")
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
        self.log_message(f"Final refined task: {response['refined_task']}")
        return response

    @retry_api_call(max_attempts=3, delay=1)
    def high_level_action_plan_creation(self):
        desktop_image = pyautogui.screenshot()
        desktop_image_encoded = encode_image(IMAGE_object=desktop_image)
        high_level_action_plan_creation_uri = f"{self.api_url}/high_level_action_plan_creation"
        high_level_action_plan_creation_payload = {
            "userid": self.userid,
            "sessionid": self.user_session_uuid,
            "os": "windows",
            "task": self.user_task,
            "app": self.first_office_app_type,
            "image_base64": desktop_image_encoded,
        }
        response = requests.post(high_level_action_plan_creation_uri, json=high_level_action_plan_creation_payload)
        response = json.loads(response.text)
        self.log_message(f"Step planner: {response['step_list']}")
        return response

    @retry_api_call(max_attempts=3, delay=1)
    def action_plan_verifier(self):
        desktop_image = pyautogui.screenshot()
        desktop_image_encoded = encode_image(IMAGE_object=desktop_image)
        action_plan_verifier_uri = f"{self.api_url}/action_plan_verifier"
        action_plan_verifier_payload = {
            "userid": self.userid,
            "sessionid": self.user_session_uuid,
            "os": "windows",
            "task": self.user_task,
            "step_list": json.dumps(self.step_list),
            "image_base64": desktop_image_encoded,
        }
        response = requests.post(action_plan_verifier_uri, json=action_plan_verifier_payload)
        response = json.loads(response.text)
        self.log_message(f"Verified: {response['verified']}\nScratchpad: {response['scratchpad']}")
        return response

    @retry_api_call(max_attempts=3, delay=1)
    def action_plan_refiner(self, feedback):
        desktop_image = pyautogui.screenshot()
        desktop_image_encoded = encode_image(IMAGE_object=desktop_image)
        action_plan_refiner_uri = f"{self.api_url}/action_plan_refiner"
        action_plan_refiner_payload = {
            "userid": self.userid,
            "sessionid": self.user_session_uuid,
            "os": "windows",
            "task": self.user_task,
            "step_list": self.step_list,
            "feedback": feedback,
            "image_base64": desktop_image_encoded,
        }
        response = requests.post(action_plan_refiner_uri, json=action_plan_refiner_payload)
        response = json.loads(response.text)
        self.log_message(f"Refined steps: {response['step_list']}")
        return response

    def execute_actions(self):
        module = importlib.import_module(f"app_tools.{self.first_office_app_type}.function_call_repo")
        TOOLING = module.TOOLING

        step_id = 0
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

            @retry_api_call(max_attempts=3, delay=1)
            def low_level_action_plan_creation():
                low_level_action_plan_creation_uri = f"{self.api_url}/low_level_action_plan_creation"
                low_level_action_plan_creation_payload = {
                    "userid": self.userid,
                    "sessionid": self.user_session_uuid,
                    "os": "windows",
                    "task": self.user_task,
                    "step": step,
                    "app": self.first_office_app_type,
                    "tooling": json.dumps(TOOLING),
                    "image_base64": app_window_ann_screenshot_base64,
                }
                response = requests.post(low_level_action_plan_creation_uri, json=low_level_action_plan_creation_payload)
                response = json.loads(response.text)
                self.log_message(f"Low level action plan: {response}")
                return response

            response = low_level_action_plan_creation()
            low_level_action_plan = response['action_list']

            if len(low_level_action_plan) <= 0:
                step_id += 1
                self.log_message("No action detected")
                continue

            for i, action in enumerate(low_level_action_plan):
                action = action[f'action_{i+1}']
                self.log_message(f"Action: {action}")

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
                if parameters:
                    function_call(**parameters)
                else:
                    function_call()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
