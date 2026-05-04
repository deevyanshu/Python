prompt_template="""
You are an expert in creating questions based on coding materials and documentation. Your goal is to prepare a coder or programmer for their exam and coding tests.
You do this by asking questions about the text below:

----------
{text}
----------

create 5 questions that will prepare the coders or programmers for their tests.
Make sure not to lose any important information. Give only questions and no answers

QUESTIONS:
"""

template="""Answer the question based ONLY on the following context:
{context}

Question: {question}
"""