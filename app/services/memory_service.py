conversation_history = []


def add_message(role: str, content: str):

    conversation_history.append({
        "role": role,
        "content": content
    })


def get_conversation_context():

    history = ""

    for msg in conversation_history[-6:]:

        history += f"{msg['role']}: {msg['content']}\n"

    return history