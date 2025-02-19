from langchain.agents import Tool
from langchain.agents import AgentOutputParser
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from StockIQ.utils.data import get_stock_data
from StockIQ.utils.news import get_stock_news
from StockIQ.utils.stock_finance import get_stock_financials
from StockIQ.template.StockTemplate import StockAnalysisPromptTemplate
from typing import Union
import re

def create_stock_agent(llm):
    tools = [
        Tool(
            name = "get_stock_info()",
            func = get_stock_data,
            description = "Get basic information about a stock. Input should be a stock ticker symbol."
        ),
        Tool(
            name = "get_stock_news",
            func = get_stock_news,
            description = "Get recent news articles about a stock. Input should be a stock ticker symbol."
        ),
        Tool(
            name = "get_stock_financials",
            func = get_stock_financials,
            description = "Get key financial metrics for a stock. Input should be a stock ticker symbol."
        )
    ]

    template = """
                You are a helpful AI stock analysis assistant. Your goal is to help users analyze stocks based on their questions.

                You have access to the following tools:
                {tools}

                Use the following format:
                Question: the input question you must answer
                Thought: you should always think about what to do
                Action: the action to take, should be one of [{tool_names}]
                Action Input: the input to the action
                Observation: the result of the action
                ... (this Thought/Action/Action Input/Observation can repeat N times)
                Thought: I now know the final answer
                Final Answer: the final answer to the original input question

                Previous conversation:
                {thoughts}

                Question: {input}
                """
    
    prompt = StockAnalysisPromptTemplate(
        template = template,
        tools = tools,
        input_variables = ["input", "intermediate_steps"]
    )

    def extract_ticker(text):
        # Look for common stock ticker patterns
        matches = re.findall(r"\b[A-Z]{1, 5}\b", text)
        return matches[0] if matches else None

    class StockAgentOutputParser(AgentOutputParser):
        def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
            if "Final Answer:" in llm_output:
                return AgentFinish(
                    return_values = {"output": llm_output.split("Final Answer: ")[-1].strip()},
                    log = llm_output
                )

            regex = r"Action: (.*?)[\n]*Action Input: (.*)"
            match = re.search(regex, llm_output, re.DOTALL)

            if not match:
                return AgentFinish(
                    return_values = {"output": "I cannot determine what action to take. Please try rephrasing your question."},
                    log = llm_output
                )

            action = match.group(1).strip()
            action_input = match.group(2).strip()

            return AgentAction(tool = action,
                               tool_input = action_input,
                               log = llm_output)

    outputparser = StockAgentOutputParser()

    agent = LLMSingleActionAgent(
        llm_chain = LLMChain(llm = llm, prompt = prompt),
        output_parser = outputparser,
        stop = ["\nObservation:"],
        allowed_tools = [tool.name for tool in tools]
    )

    memory = ConversationBufferMemory(memory_key = "thoughts")

    return AgentExecutor.from_agent_and_tools(
        agent = agent,
        tools = tools,
        memory = memory,
        verbose = True
    )