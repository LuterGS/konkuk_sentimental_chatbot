import os

import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from utils.python_logger import TraceLogger


class MainFastAPI:

    def __init__(self):
        self._url = '0.0.0.0'
        self._logger = TraceLogger()
        self._app = FastAPI(
            title='web service for sentimental chatbot',
            version='0.0.1',
            root_path='/'
        )
        self._app.add_api_route(
            **self._request_conversation_property,
            endpoint=self.request_conversation,
            methods=["GET"]
        )

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

    async def request_conversation(
        self,
        message: str = Query(
            False,
            title='사용자가 입력한, 챗봇이 입력받을 문장',
            example='오늘 지각해서 밥도 못 먹었어.',
            description='사용자가 입력한 문장입니다. 해당 문장을 챗봇 서버로 보내 결과를 받아옵니다.')
    ):
        self._logger.info(f"get {message}")
        return {"response": message}

    def start_app(self):
        uvicorn.run(self._app, host=self._url, port=int(os.getenv('PORT')))


