#altaf
import tkinter as tk
import time
import threading

# Function to generate a response based on user input
def chatbot_response(user_input):
    # Lowercase the user input for easier matching
    user_input = user_input.lower()

    # Rule-based responses
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I assist you today?"
    
    elif "how are you" in user_input:
        return "I'm just a chatbot, but I'm doing great! How about you?"

    elif"im good" in user_input:
        return "That's Great"

    elif "your name" in user_input:
        return "I'm a simple chatbot , but you can call me JARVIS!"
    
    elif "bye" in user_input or "goodbye" in user_input:
        return "Goodbye! It was nice talking to you. Have a great day!"
    
    elif "help" in user_input:
        return "Sure! I'm here to help you. You can ask me about my name, how I am, or just chat!"
    
    elif "weather" in user_input:
        return "I can't check the weather right now, but you can try asking about today's forecast!"
    
    else:
        return "Sorry, I dodn't have informataion about that. is there anything else?"

# Function to simulate typing with a delay
def simulate_typing(response):
    for i in range(len(response)):
        chat_window.insert(tk.END, response[i], 'chatbot_typing')
        chat_window.yview(tk.END)  # Scroll to the bottom to show the new message
        chat_window.update_idletasks()  # Update the window
        time.sleep(0.1)  # Simulate typing delay
    chat_window.insert(tk.END, "\n", 'chatbot_response')  # Add final newline

# Function to handle sending a message
def send_message():
    user_input = entry.get()  # Get user input from the entry box
    if user_input.lower() == "bye" or user_input.lower() == "goodbye":
        chat_window.insert(tk.END, "Chatbot: Goodbye! It was nice talking to you. Have a great day!\n", 'chatbot_response')
        root.after(1000, root.quit)  # Close the window after 1 second
    else:
        chat_window.config(state=tk.NORMAL)  # Enable the chat window to add new text
        # Display user input with decoration (message bubble)
        chat_window.insert(tk.END, f"You: {user_input}\n", 'user_input')
        chat_window.yview(tk.END)  # Scroll to the bottom to show the new message
        entry.delete(0, tk.END)  # Clear the entry box

        # Get the chatbot's response
        response = chatbot_response(user_input)

        # Simulate chatbot typing with a delay for a more interactive experience
        threading.Thread(target=simulate_typing, args=(response,)).start()

# Create the main window
root = tk.Tk()
root.title("Interactive Chatbot")

# Configure the style for the chat window
root.config(bg="#f0f0f0")

# Create a chat window (text box) to display messages
chat_window = tk.Text(root, state=tk.DISABLED, height=20, width=50, wrap=tk.WORD, font=("Helvetica", 12))
chat_window.pack(pady=10)

#  decoration
chat_window.tag_configure('user_input', foreground='blue', font=("Helvetica", 12, "bold"))
chat_window.tag_configure('chatbot_response', foreground='green', font=("Helvetica", 12))
chat_window.tag_configure('chatbot_typing', foreground='green', font=("Helvetica", 12, "italic"))

# Create an entry box to allow the user to type messages
entry = tk.Entry(root, width=50, font=("Helvetica", 12), relief="solid", bd=2)
entry.pack(pady=10)

# Create a button to send the message
send_button = tk.Button(root, text="Send", width=20, command=send_message, font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white")
send_button.pack(pady=5)

root.mainloop() 
