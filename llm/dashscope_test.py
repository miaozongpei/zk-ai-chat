from http import HTTPStatus
import dashscope
dashscope.api_key = "sk-97d523aa76184c338c80b32954643e40"



def call_with_prompt():

    response = dashscope.Generation.call(
        model=dashscope.Generation.Models.qwen_max,
        prompt='你是谁？'
    )
    # The response status_code is HTTPStatus.OK indicate success,
    # otherwise indicate request is failed, you can get error code
    # and message from code and message.
    if response.status_code == HTTPStatus.OK:
        print(response.output)  # The output text
        print(response.usage)  # The usage information
    else:
        print(response.code)  # The error code.
        print(response.message)  # The error message.

if __name__ == '__main__':
    call_with_prompt()

