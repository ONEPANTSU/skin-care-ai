import logging

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from src.config import GPT_API_KEY


class LLMOutput(BaseModel):
    text: str = Field(
        "", description="The text that the OCR-Models tried to recognize."
    )
    langs: list[str] = Field(
        "",
        description="The list contains only those languages whose characters were used in the original text.",
    )


llm = ChatOpenAI(model="gpt-4o-mini", api_key=GPT_API_KEY).with_structured_output(
    LLMOutput, method="json_mode"
)

system_message = (
    "You're a smart OCR-Assistant, which can compare (summarize) valuable parts of different OCR-Models recognitions "
    "for the same image and return the truly text, that was detected on image."
    "You will receive the data in dict-format, where each key is a OCR-Model name "
    "and each value is recognized text. \n"
    "The text is from products and drugs labels.\n"
    "The OCR-Models have different abilities to recognize different languages, so"
    "their answers may differ: Try to understand what languages was really used. "
    "(It could be used one or two languages chars in one text)\n\n"
    "Here is an example:"
    "My Request: {{'easyocr_en_ch': 'He llo , M倍yP !!! ' 'easyocr_ru': 'Непо, мир!!!'}}"
    "Your Response with json_structure: {{'text': 'Hello, мир!', 'langs': ['ru', 'en']}}, "
    "because easyocr_en_zh model recognized meaningful 'He llo ,' and made mistake with 'M倍yP', "
    "but easyocr_ru model recognized meaningful 'мир!!!' and made mistake with 'Непо'.\n"
    "The original text contained both english and russian letters, but no chinese, "
    "so models understood only parts of sentence. That's why you should analyse all models recognitions."
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_message),
        ("human", "{input}"),
    ]
)

chain = prompt | llm


def compare_texts(texts: dict[str, str]) -> str:
    try:
        result = chain.invoke({"input": texts})
        logging.debug(f"Text: {result.text}\nLangs: {result.langs}\n")
        return result.text
    except Exception as e:
        logging.error(e)
        return [
            v for v in texts.values() if len(v) == max([len(v) for v in texts.values()])
        ][0]
