import google.generativeai as genai
import logging
from google.generativeai.types import GenerationConfig, HarmCategory, HarmBlockThreshold

class GptApiManager:
    def __init__(self, api_key, model_name, generation_config=None):
        """
        GptApiManager 클래스를 초기화합니다.

        :param api_key: Google API 키
        :param model_name: 사용할 모델 이름
        :param generation_config: 생성 설정 (선택적, 기본값: GenerationConfig())
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.generation_config = generation_config or GenerationConfig()

    async def generate_content(self, prompt, stream=False):
        """
        주어진 프롬프트를 사용하여 콘텐츠를 생성합니다.

        :param prompt: 콘텐츠 생성을 위한 프롬프트
        :param stream: 스트리밍 모드 사용 여부 (현재 지원되지 않음)
        :return: 생성된 콘텐츠 문자열, 실패 시 None
        """
        if stream:
            logging.error("스트리밍 모드는 현재 지원되지 않습니다.")
            return None

        try:
            response = self.model.generate_content(
                [prompt],
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
                },
                generation_config=self.generation_config
            )
            content = response.text.strip() if hasattr(response, 'text') else ''
            return content
        except Exception as e:
            logging.error(f"콘텐츠 생성 실패: {e}")
            return None
