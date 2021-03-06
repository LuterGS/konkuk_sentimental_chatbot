import os

import google.cloud.logging_v2
import requests
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from dotenv import load_dotenv

from dto.rest_dtos import Message
from utils.python_logger import TraceLogger


class MainFastAPI:

    def __init__(self):

        # setup logging
        # client = google.cloud.logging_v2.Client()
        # client.setup_logging()

        # test
        load_dotenv(dotenv_path="envs")
        self._ai_server_url = f'http://{os.getenv("AI_SERVER_URL")}'

        self._url = '0.0.0.0'
        self._logger = TraceLogger()
        self._app = FastAPI(
            title='web service for sentimental chatbot',
            version='0.0.1',
            root_path='/'
        )
        # set static files
        self._app.mount("/static", StaticFiles(directory="static"), name="static")
        # set Jinja 2 HTML template
        self._templates = Jinja2Templates(directory="templates")
        self._app.add_api_route(
            **self._request_conversation_property,
            endpoint=self.request_conversation,
            methods=["POST"]
        )
        self._app.add_api_route(
            **self._main_page_property,
            endpoint=self.main_page,
            methods=["GET"]
        )

    @property
    def _main_page_property(self):
        return {
            "path": "/"
        }

    def main_page(self, request: Request):
        return self._templates.TemplateResponse("main_page.html", {"request": request})


    @property
    def _request_conversation_property(self):
        return {
            "path": "/conversation",
            "name": '챗봇한테 대화를 보내는 API',
            "description": "챗봇한테 입력받은 message 를 보내고, 챗봇의 응답을 반환합니다.",
            "response_class": JSONResponse,
            "responses": {
                200: {
                    "description": "챗봇이 반환한 값을 string 으로 반환",
                    "content": {
                        "application/json": {
                            "example": {
                                "resposne": "많이 힘드시겠어요."
                            }
                        }
                    }
                }
            }
        }

    async def request_conversation(self, message: Message):
        response = requests.post(self._ai_server_url, json={"userMessage": message.userInput}).json()
        ai_response: str = response["response"].replace("<usr>", "").lstrip(" ")
        if ai_response == "":
            ai_response = "AI 추론 실패!"
        self._logger.info(f"get {ai_response}")
        return {"response": ai_response}

    def start_app(self):
        uvicorn.run(self._app, host=self._url, port=int(os.getenv('PORT') or 8080))


