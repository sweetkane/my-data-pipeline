from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.enum import EnumOutputParser
from langchain_core.output_parsers import StrOutputParser
from enum import Enum
import json
from transforms._transform import ITransform

class Topic(Enum):
    WORLD = "World"
    US_POLITICS = "US Politics"
    ENTERTAINMENT = "Entertainment"
    SCIENCE_AND_TECH = "Science & Technology"
    FINANCE = "Finance"
    SPORTS = "Sports"


class NewsSynthesizer(ITransform):

    def __init__(self) -> None:
        self.model = ChatOpenAI()

    def transform(self, data: dict) -> dict:
        categorized = self._categorize(data)
        synthesized = self._synthesize(categorized)
        return synthesized

    def _categorize(self, data: dict) -> dict:
        sorted_headlines = {}
        for topic in Topic:
            sorted_headlines[topic] = []

        parser = EnumOutputParser(enum=Topic)
        for headline in data:
            try:
                prompt = PromptTemplate(
                    template="""
                    Categorize the topic of the news headline:

                    {headline}

                    ONLY USE ONE OF THE PROVIDED TOPIC CATEGORIES!
                    DO NOT CREATE A NEW CATEGORY!

                    Instructions: {instructions}
                    """,
                    input_variables=["headline"],
                    partial_variables={
                        "instructions": parser.get_format_instructions()
                    }
                )

                chain = prompt | self.model | parser
                topic = chain.invoke({"headline": json.dumps(headline)})
                sorted_headlines[topic].append(headline)
            except:
                continue
        return sorted_headlines

    def _synthesize(self, data: dict) -> dict:
        result = {}
        for topic in Topic:
            headlines = data[topic]

            prompt = PromptTemplate(
                template="""
                Attached: a bunch of recent news headlines for the topic of {topic}
                Your job is to take these headlines and summarize them.
                Create the perfect 3-5 sentence summary that combines and synthesizes as much relevant information as possible
                DO NOT just list the headlines. You must craft an elegant, well-written summary. Feel free to editorialize a little!

                HEADLINES: {headlines}
                """,
                input_variables=["headlines"],
                partial_variables={
                    "topic": topic.value
                }
            )
            chain = prompt | self.model | StrOutputParser()

            result[topic.value] = chain.invoke({"headlines": headlines})
        return result
