import json
from difflib import get_close_matches
import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button

# Existing functions...
def load_knowledge_base(file_path: str):
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# Save the updated knowledge base to the JSON file
'''def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)'''

# Find the closest matching question
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None
class ChatBotGUI:
    def __init__(self, master, knowledge_base):
        self.master = master
        master.title("ChatBot")

        self.knowledge_base = knowledge_base

        self.chat_display = Text(master, height=20, width=50)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.scrollbar = Scrollbar(master, command=self.chat_display.yview)
        self.scrollbar.grid(row=0, column=2, sticky='nsew')
        self.chat_display['yscrollcommand'] = self.scrollbar.set

        self.user_input = Entry(master, width=50)
        self.user_input.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

    def send_message(self):
        user_message = self.user_input.get()
        self.display_message(f"You: {user_message}")

        best_match = find_best_match(user_message, [q["question"] for q in self.knowledge_base["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, self.knowledge_base)
            self.display_message(f"Bot: {answer}")
        else:
            self.display_message("Bot: I don't know the answer.")
            '''
            new_answer = input("Type the answer or 'skip' to skip: ")

            if new_answer.lower() != 'skip':
                self.knowledge_base["questions"].append({"question": user_message, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', self.knowledge_base)
                self.display_message("Bot: Thank you! I've learned something new.")'''

        self.user_input.delete(0, 'end')  # Clear the input field

    def display_message(self, message):
        self.chat_display.insert(tk.END, message + '\n')
        self.chat_display.see(tk.END)

# Existing functions...

if __name__ == "__main__":
    knowledge_base_data = load_knowledge_base('knowledge_base.json')
    root = tk.Tk()
    chatbot_gui = ChatBotGUI(root, knowledge_base_data)
    root.mainloop()
