from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OpenAI_API_KEY"))

def ChatGPT(systemPrompt, userMessage, Completion_model="gpt-4o-mini") :
    completion = client.chat.completions.create(
        model=Completion_model,
        messages=[
            {
                "role": "system", 
                "content": systemPrompt
            },
            {
                "role": "user",
                "content": userMessage
            }
        ]
    )
    print(completion.choices[0].message)


if __name__ == "__main__":
    System_Prompt= input("設定一個和你對話的身分:")
    User_Message = input("你想對這個身分說的話:")
    ChatGPT(systemPrompt=System_Prompt, userMessage=User_Message)
