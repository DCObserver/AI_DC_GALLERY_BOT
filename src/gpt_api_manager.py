import google.generativeai as genai
import logging
from google.generativeai.types import GenerationConfig

class GptApiManager:
    def __init__(self, api_key, model_name, generation_config=None):
        """
        GptApiManager를 초기화합니다.
        
        :param api_key: Google API 키
        :param model_name: 사용할 모델 이름
        :param generation_config: 생성 설정 (선택적)
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.generation_config = generation_config if generation_config else GenerationConfig()

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
            # 비동기 호출
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            content = response.text.strip() if hasattr(response, 'text') else ''
            logging.info("콘텐츠가 성공적으로 생성되었습니다.")
            return content
        
        except Exception as e:
            logging.error(f"콘텐츠 생성에 실패했습니다: {e}")
            return None
