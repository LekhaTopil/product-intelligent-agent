import os 
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from .tools import get_product_info, compare_products 

    
load_dotenv()
model_name = os.getenv("MODEL")

root_agent = LlmAgent(
    name="product_assistant_logic", 
    model=model_name,  
    description= "It retrieves detailed specifications for a single product or provides clear comparisons between two products.",
    instruction="""   
    You are a smart product assistant specializing in mobile phones.

    Your responsibilities:

    1. Understand the user's query clearly.
    2. If the user asks about a single product:
       - Use the get_product_info tool.
       - Return all variants with price and key specifications.

    3. If the user asks to compare two products:
       - Use the compare_products tool.
       - Compare based on:
         - price
         - battery
         - performance (chip)
         - camera
         - display
       - Clearly mention:
         - number of variants for each product
         - key differences
         - which product is better for different use cases

    4. Always present information in a structured and easy-to-read format.

    5. If multiple variants exist:
       - Group them properly
       - Highlight storage and price differences

    6. Keep responses concise but informative.

    7. Do NOT make up information.
       Only use the data returned from tools.

    8. If the query is unclear:
       - Ask a clarification question.
    """,

    tools=[get_product_info, compare_products]

)  


async def run_terminal_test():
    import asyncio
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService 
    print("\n🚀 Starting Agent Terminal Test...")
    
    # 1. Initialize the Memory Service 
    session_service = InMemorySessionService()
    
    # 2. Initialize the Runner
    runner = Runner(
        agent=root_agent, 
        session_service=session_service,
        app_name="product_test_app" 
    )

    test_query = "Compare iphone 17 and samsung galaxy s26?"
    print(f"📝 Query: {test_query}\n")
    
    try:
        await runner.run_debug(
            test_query,
            session_id="debug_session_99",
            user_id="lekha_dev"
        )
    except Exception as e:
        print(f"\n❌ Execution Error: {e}")

if __name__ == "__main__":
    asyncio.run(run_terminal_test())





