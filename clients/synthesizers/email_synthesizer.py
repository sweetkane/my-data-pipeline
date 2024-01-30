from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.enum import EnumOutputParser
from langchain_core.output_parsers import StrOutputParser
from enum import Enum
import json

class Topic(Enum):
    WORLD = "World"
    NATIONAL = "National Politics"
    ENTERTAINMENT = "Entertainment"
    SCIENCE_AND_TECH = "Science & Technology"
    FINANCE = "Finance"
    SPORTS = "Sports"


class EmailSynthesizer:

    def categorize(data: dict) -> dict:
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

                    ONLY USE ONE OF THE PREOVIDED TOPIC CATEGORIES!
                    DO NOT CREATE A NEW CATEGORY!

                    Instructions: {instructions}
                    """,
                    input_variables=["headline"],
                    partial_variables={
                        "instructions": parser.get_format_instructions()
                    }
                )
                chain = prompt | ChatOpenAI() | parser
                topic = chain.invoke({"headline": json.dumps(headline)})
                sorted_headlines[topic].append(headline)
            except:
                continue
        return sorted_headlines

    def synthesize(data: dict) -> dict:
        result = {}
        for topic in Topic:
            headlines = data[topic]
            prompt = PromptTemplate(
            template="""
            Attached: a json file which contains a lot of recent news headlines for the topic of {topic}
            You are a Harvard alum journalist working for a digital news startup.
            Your job is to take these headlines and summarize them.
            Create the perfect 3-5 sentence summary that combines and synthesizes as much relevant information as postible

            {headlines}
            """,
            input_variables=["headlines"],
            partial_variables={
                "topic": topic.value
            }
            )
            model = ChatOpenAI()
            chain = prompt | model | StrOutputParser()

            result[topic.value] = chain.invoke({"headlines": headlines})
        return result
