"""
streaming

"""

import asyncio


app = 

INPUT = {"ticket": "Payment failed twice", "category": None, "reply": None}

 
async def stream_tokens():
    print("\n=== astream_events: tokens as they're generated, inside 'reply' ===")
    async for event in app.astream_events(INPUT, version="v2"):
        if event["event"] == "on_chat_model_stream" and event["metadata"].get("langgraph_node") == "reply":
            print(event["data"]["chunk"].content, end="", flush=True)
    print()


asyncio.run(stream_tokens())
