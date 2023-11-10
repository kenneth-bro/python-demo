import json
import time
import requests

from openai import OpenAI

client = OpenAI()
client.api_key = "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"


def get_weather(location, unit="摄氏度"):
    # 这是一个假设的天气 API，实际使用时需要替换为真实的天气 API
    api_url = f"https://restapi.amap.com/v3/weather/weatherInfo?key=cc599260c84349669c5ebf99b8cb67bc&city={location}&extensions=base&output=json"
    return requests.request("GET", api_url).json()


assistant = client.beta.assistants.create(
    name="天气助手",
    instructions="您是一个天气助手，获取当前天气信息后，合理分析温度、降雨及风力，输出天气状况并给出合理的穿衣和出现建议。不要重复输出",
    # model="gpt-4-1106-preview",
    model="gpt-3.5-turbo-1106",
    tools=[{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "地点"
                    },
                    "unit": {
                        "type": "string",
                        "description": "单位",
                        "enum": ["摄氏度", "华氏度"]
                    }
                },
                "required": ["location"]
            }
        }
    }]
)

# 创建线程
thread = client.beta.threads.create()


while True:
    # 获取输入
    input_text = input("请输入您的问题(退出请输入exit): ")
    if input_text == "exit":
        break

    # 输入消息
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=input_text
    )

    # 运行
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    # 结果
    result = None
    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        # 完成
        if run.status == "completed":
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            result = messages.data[0].content[0].text.value;
            break

        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []

            for tool_call in tool_calls:
                call_function = tool_call.function
                function_args = json.loads(call_function.arguments)
                if call_function.name == 'get_weather':
                    res = get_weather(function_args.get("location"), function_args.get("unit"))
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps(res)
                    })

            # 提交函数调用结果
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
            print(f"action 执行完成. {tool_outputs}")

        if run.status == "failed":
            print(run.status)
            break

        # 继续请求
        time.sleep(1)
        print(f"status: {run.status}")

    print(f"\nAI Assistant: {result}\n")





