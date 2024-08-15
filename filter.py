import re

def clean_comment(comment):
    # Remove symbols
    cleaned_comment = re.sub(r'[^\w\sㄱ-ㅎㅏ-ㅣ가-힣]', '', comment)

    return cleaned_comment
