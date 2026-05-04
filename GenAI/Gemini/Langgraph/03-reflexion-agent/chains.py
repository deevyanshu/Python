from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from schema import AnswerQuestion, ReviseAnswer
from langchain_core.output_parsers import JsonOutputToolsParser
from langchain_core.messages import HumanMessage

load_dotenv()

#instead of Jsonparser we could have used with_structured_output

#parser=JsonOutputKeyToolsParser(key_name="AnswerQuestion", first_tool_only=True)

#parser=JsonOutputToolsParser()

#parser1=JsonOutputKeyToolsParser(key_name="ReviseAnswer")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

#Actor Agent prompt
actor_prompt_template=ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """you are expert AI researcher.
            Current time:{time}

            1. {first_instruction}
            2. Reflect and critique your answer. Be severe to maximize improvement.
            3. After the reflection, **list 1-3 search queries seperately** for researching improvements. Do not include them inside the reflection.
            """
        ),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system", "Answer the user's question above using the required format."
        )
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat()
)

first_responder_prompt_template=actor_prompt_template.partial(
    first_instruction="provide a detailed 250 words answer."
)

llm= ChatGoogleGenerativeAI(model="gemini-3-flash-preview",
    max_retries=6
)


first_responder_chain= first_responder_prompt_template | llm.bind_tools(tools=[AnswerQuestion])

revise_instruction="""Revise your previous instruction using new information.
    -You should use the previous critique to add important information to your answer.
    -You must include numerical citations in your revised answer to ensure it can be verified.
    -add a "references" section to the bottom of your answer (which does not count towards the word limit). In form of:
        -[1] https://example.com
        -[2] https://example.com
    -you should use previous crititque to remove superfluous information from your answer and make sure it is not more than 250 words.
"""

revisor_chain=actor_prompt_template.partial(
    first_instruction=revise_instruction
) | llm.bind_tools(tools=[ReviseAnswer])

# response=first_responder_chain.invoke({
#     "messages":[HumanMessage(content="write a blog post on how samll business can leverage AI to grow")]
# })

# print("response: ",response)