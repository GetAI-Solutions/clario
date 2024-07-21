def generate_chat_prompt(query, content):
    template = f"""

    You are a friendly AI assistant to help users know more about a product. The details of the product are provided in the <content> tag below.
    You are to scan the details of the product in the <content> tag below, and use information in the document to answer the question.
    Ensure to not mention the <content> tag or your source and reasoning in your answer.

    RULE TO FOLLOW:
    1. Scan the details in the <content> section and find the best way content can be used to answer query 
    2. Ensure NOT to say something like Based on the information provided in the <content> tag.

    <content>{content}</content>

    The user has askd the following question
    
    USER_QUESTION: {query}

    Answer the question as best as you can using the provided information and general knowledge.

    Again, Make no refrence to <content> tag in your final answer

    """

    return template

response = ""
"""for event in replicate.stream("snowflake/snowflake-arctic-instruct",
                input={"prompt": prompt,
                        "temperature": 0.2
                        }):
    response += str(event)"""