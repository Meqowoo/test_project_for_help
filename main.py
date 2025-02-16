import g4f
import tkinter as tk
from tkinter import scrolledtext
import threading
import pyttsx3
import speech_recognition as sr
import numpy as np

# Настройки голосового синтеза речи
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)


# def speak(text):
#     """Озвучивает текст"""
#     engine.say(text)
#     engine.runAndWait()


# Распознавание речи с учетом громкости



def recognize_speech():
    """Распознаёт речь с микрофона и проверяет уровень громкости"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "\nНейро-ника: Слушаю...\n")
        chat_area.yview(tk.END)
        chat_area.config(state=tk.DISABLED)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

            # Преобразуем аудиоданные в массив
            audio_data = np.frombuffer(audio.frame_data, dtype=np.int16)

            # Вычисляем среднюю громкость (абсолютное значение)
            avg_volume = np.mean(np.abs(audio_data))

            # Устанавливаем порог для громкости
            if avg_volume < 500:  # Порог громкости, значение можно корректировать
                return "Речь слишком тихая, попробуйте снова."

            # Распознавание текста
            text = recognizer.recognize_google(audio, language="ru-RU")
            return text
        except sr.UnknownValueError:
            return "Не удалось распознать речь."
        except sr.RequestError as e:
            return f"Ошибка сервиса: {e}"


# Обработка сообщения через g4f
def fetch_response(user_input):
    """Получает ответ от модели через g4f"""
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )
        ai_response = response if isinstance(response, str) else response['choices'][0]['message']['content']

        # Убираем все символы '*'
        ai_response_cleaned = ai_response.replace('*', '')

        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "\nНейро-ника: " + ai_response_cleaned.strip() + "\n")
        chat_area.config(state=tk.DISABLED)
        chat_area.yview(tk.END)
        # speak(ai_response_cleaned)  # Озвучиваем очищенный текст
    except Exception:
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "\nНейро-ника: Произошла ошибка. Попробуйте позже.\n")
        chat_area.config(state=tk.DISABLED)
        chat_area.yview(tk.END)


# Отправка текста
def send_message():
    """Отправка текстового сообщения"""
    user_input = user_entry.get()
    if user_input.strip():
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "Вы: " + user_input + "\n")
        chat_area.yview(tk.END)
        chat_area.insert(tk.END, "Нейро-ника: Готовлю ответ...\n")
        chat_area.yview(tk.END)
        chat_area.config(state=tk.DISABLED)
        user_entry.delete(0, tk.END)
        threading.Thread(target=fetch_response, args=(user_input,)).start()


# Обработка голосового ввода
def voice_input():
    """Обрабатывает голосовой ввод и отправляет его"""
    user_input = recognize_speech()
    if user_input:
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "Вы (голос): " + user_input + "\n")
        chat_area.insert(tk.END, "Нейро-ника: Готовлю ответ...\n")
        chat_area.config(state=tk.DISABLED)
        threading.Thread(target=fetch_response, args=(user_input,)).start()


# Интерфейс Tkinter
root = tk.Tk()
root.title("Чат с умным братаном")
root.geometry("600x500")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, state=tk.DISABLED, font=("Arial", 10))
chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

user_entry = tk.Entry(root, width=50, font=("Arial", 12))
user_entry.grid(row=1, column=0, padx=10, pady=10)
user_entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(root, text="Отправить", width=10, command=send_message, bg="#4CAF50", fg="white")
send_button.grid(row=1, column=1, padx=10, pady=10)

voice_button = tk.Button(root, text="Голосовой ввод", width=15, command=voice_input, bg="#2196F3", fg="white")
voice_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()