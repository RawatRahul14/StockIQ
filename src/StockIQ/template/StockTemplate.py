from langchain.prompts import StringPromptTemplate
from typing import List
from langchain.agents import Tool

class StockAnalysisPromptTemplate(StringPromptTemplate):
    template: str
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""

        for action, observation in intermediate_steps:
            thoughts += f"Actions: {action.log}\nObservation: {observation}\n"

        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        kwargs["thoughts"] = thoughts

        return self.template.format(**kwargs)