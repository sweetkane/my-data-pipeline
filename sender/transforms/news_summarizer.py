import json
from enum import Enum

from langchain.output_parsers.enum import EnumOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from transforms._transform import ITransform


class NewsSummarizer(ITransform):

    def __init__(self) -> None:
        self.model = ChatOpenAI()

    def apply(self, data: list) -> str:
        synthesized = self._summarize(data)
        return synthesized

    def _summarize(self, data: list) -> dict:
        prompt = PromptTemplate(
            template="""
            You are an award winning journalist.
            Attached are bunch of recent news headlines for the topic of Artificial Intelligence.
            Your job is to take these headlines and summarize them.
            Create the perfect summary that combines and synthesizes as much relevant information as possible
            DO NOT just list the headlines. You must craft an elegant, well-written summary.

            HEADLINES: {data}
            """,
            input_variables=["data"],
        )
        chain = prompt | self.model | StrOutputParser()

        return chain.invoke({"data": data})
