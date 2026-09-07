"""
manual observability

"""


import time
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    ticket: str
    category: str | None
    reply: str | None


TRACE: list[dict] = []


def traced(name):
    def decorator(fn):
        def wrapper(state: State) -> dict:
            start = time.perf_counter()
            result = fn(state)
            TRACE.append(
                {
                    "node": name,
                    "ms": round((time.perf_counter() - start) * 1000),
                    "input_keys": list(state.keys()),
                    "output": result,
                }
            )
            return result

        return wrapper

    return decorator


def classify(state: State) -> dict:
    time.sleep(0.1)
    return {"category": "billing"}


def reply(state: State) -> dict:
    time.sleep(0.05)
    return {"reply": f"Thank you for reporting. Category: {state['category']}"}


print("=== print()-only version ===")


def classify_v1(state: State) -> dict:
    print("classifying...")
    return classify(state)


def reply_v1(state: State) -> dict:
    print("replying...")
    return reply(state)


g1 = StateGraph(State)
g1.add_node("classify", classify_v1)
g1.add_node("reply", reply_v1)
g1.add_edge(START, "classify")
g1.add_edge("classify", "reply")
g1.add_edge("reply", END)
g1.compile().invoke({"ticket": "Payment failed twice", "category": None, "reply": None})
print(
    "-> useless for answering: which step was slow? what did the model actually see?\n"
)

print("=== structured-trace version ===")


@traced("classify")
def classify_v2(state: State) -> dict:
    return classify(state)


@traced("reply")
def reply_v2(state: State) -> dict:
    return reply(state)


g2 = StateGraph(State)
g2.add_node("classify", classify_v2)
g2.add_node("reply", reply_v2)
g2.add_edge(START, "classify")
g2.add_edge("classify", "reply")
g2.add_edge("reply", END)
g2.compile().invoke(
    {"ticket": "Payment failed twice", "category": None, 
    "reply": None}
    )
for event in TRACE:
    print(
        f"  [{event['node']}] {event['ms']}ms 
         saw={event['input_keys']}  wrote={list(event['output'].keys())}"
    )
print(
    "-> now which step was slow and what it wrote is answerable -- Unit 20 gets this per node, automatically"
)

