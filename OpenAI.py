import openai
import json

openai.api_key = "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"

function_descriptions = [
    {
        "name": "get_subject_name",
        "description": "extract  the subject name from the entered text",
        "parameters": {
            "type": "object",
            "properties": {
                "subject": {
                    "type": "string",
                    "description": "The subject from the text e.g. mathematics, science, None",
                },  
            },
            "required": ["subject"],
        },
    }
]


def get_subject_name(topic):
    subject_info = {
        "topic": topic,
    }
    return json.dumps(subject_info)

def check_values_in_dict(dict1, dict2):
    # Extract the values from dict1 and convert to lowercase
    topic_value = dict1["subject"].lower()
    
    # Check if the values are present in the values of either key in dict2 (case-insensitive)
    for valid_values in dict2.values():
        if topic_value in valid_values:
            return True

    return False


if __name__ == "__main__":
    # Sample data with valid topics and operators
    data = {
        "valid_topics": [
            "mathematics", "science",
        ]
    }

    # Start the conversation
    print("Chatbot: Hello! I can help you with some calculations. You can ask me questions like 'What is the volume of a cone?' or 'Calculate sin(90).'")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        about_me_prompt = f'''Please classify this question as Science or Maths or if does not belongs to any one of these two the subject will be None.
        You are presented with a question:
        "{user_input}"
        Please select the appropriate category:
        1. Science
        2. Mathematics
        3. None
        
        {user_input}
        '''
        openai_response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-0613",
            messages = [{'role': 'user', 'content': about_me_prompt}]
        )
        content = openai_response.choices[0].message['content']
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[{"role": "user", "content": content}],
            functions=function_descriptions,
            function_call={"name": "get_subject_name"},
        )
        output = completion.choices[0].message
        params = json.loads(output.function_call.arguments)
        print(params)
        #print(type(params))
        #print(params)
        #print(type(data))
        #print(data)
        result = check_values_in_dict(params, data)

        if result:
            print("Chatbot: You are not authorized to ask this question.")
        else:
            response = completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=[{"role": "user", "content": user_input}],
            )
            print("Chatbot:", response.choices[0].message.content)

        
