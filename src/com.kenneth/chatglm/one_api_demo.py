import time

from openai import OpenAI


class OneAPIDemo:

    @staticmethod
    def completion(mode_name, messages=[]):
        """
            完成一次对话
        :param mode_name:
        :param messages:
        :return:
        """
        completion = client.chat.completions.create(
            model=model_name,
            messages=messages
        )
        return completion

    @staticmethod
    def completion_stream(model_name, message=[]):
        """
            流式对话
        :param model_name:
        :param message:
        :return:
        """
        completion = client.chat.completions.create(
            model=model_name,
            messages=message,
            stream=True
        )
        return completion


if __name__ == '__main__':
    base_url = "http://192.168.48.10:3999/v1/"
    api_key = "sk-YruGgxkuGedtm2YF5fA41c352c3c4dD18fA713A9Bd83A79e"

    client = OpenAI(api_key=api_key,
                    base_url=base_url)
    """
    model_name | api | stream
    chatglm3-6b | ok | ok
    chatglm_turbo | ok | ok
    gpt-3.5-turbo | ok | ok
    gpt-4 | ok | ok
    """
    model_name = "chatglm3-6b"
    # model_name = "chatglm_turbo"
    # model_name = "gpt-3.5-turbo"
    messages = [
        {"role": "user", "content": "1+1=?"}
    ]
    start_time = time.time()

    # 是否流式输出
    stream = True
    if stream:
        completion_text = ""
        response = OneAPIDemo.completion_stream(model_name, messages)
        for chunk in response:
            if chunk.choices[0].finish_reason == "stop":
                # 完成
                break

            chunk_text = chunk.choices[0].delta.content
            if chunk_text is not None:
                completion_text += chunk_text
                print(f"接收到: {chunk_text}")

        print(f"回复:{completion_text}\n本次耗时: {time.time() - start_time:.2f}s")

    else:
        response = OneAPIDemo.completion(model_name, messages)
        res_text = response.choices[0].message.content
        print(f"回复: {res_text}\n本次耗时: {time.time() - start_time:.2f}s")


