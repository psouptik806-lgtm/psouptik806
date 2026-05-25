# main.py
# Single-file Android-ready AI chatbot app using Kivy
# Run locally:
# pip install kivy requests
#
# Build APK later with Buildozer.

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import StringProperty
import requests
import threading

KV = '''
#:import dp kivy.metrics.dp

<ChatMessage@Label>:
    size_hint_y: None
    text_size: self.width - dp(20), None
    height: self.texture_size[1] + dp(30)
    padding: dp(15), dp(15)
    markup: True
    canvas.before:
        Color:
            rgba: (0.45,0.2,1,1) if self.is_user else (0.15,0.15,0.2,1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20]

BoxLayout:
    orientation: 'vertical'
    spacing: dp(10)
    padding: dp(10)
    canvas.before:
        Color:
            rgba: 0.03,0.04,0.09,1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: dp(70)
        padding: dp(10)

        canvas.before:
            Color:
                rgba: 0.1,0.12,0.2,1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [20]

        Label:
            text: 'SOUPTIK AI'
            bold: True
            font_size: '28sp'
            color: 1,1,1,1

    ScrollView:
        do_scroll_x: False

        BoxLayout:
            id: chat_area
            orientation: 'vertical'
            spacing: dp(10)
            padding: dp(10)
            size_hint_y: None
            height: self.minimum_height

    BoxLayout:
        size_hint_y: None
        height: dp(65)
        spacing: dp(10)

        TextInput:
            id: user_input
            hint_text: 'Ask anything...'
            multiline: False
            background_color: 0.1,0.1,0.15,1
            foreground_color: 1,1,1,1
            cursor_color: 1,1,1,1
            padding: dp(15)
            font_size: '16sp'

        Button:
            text: 'Send'
            bold: True
            background_normal: ''
            background_color: 0.45,0.2,1,1
            on_release: app.send_message()

    BoxLayout:
        size_hint_y: None
        height: dp(120)
        spacing: dp(10)

        Button:
            text: 'Starter\\n₹150'
            bold: True
            background_normal: ''
            background_color: 0.1,0.4,0.8,1

        Button:
            text: 'Pro\\n₹299'
            bold: True
            background_normal: ''
            background_color: 0.5,0.2,1,1

        Button:
            text: 'Ultra\\n₹499'
            bold: True
            background_normal: ''
            background_color: 0.9,0.3,0.5,1
'''

class MainApp(App):

    API_KEY = "YOUR_OPENAI_API_KEY"

    def build(self):
        self.title = "SOUPTIK AI"
        return Builder.load_string(KV)

    def add_message(self, text, is_user=False):

        from kivy.uix.label import Label

        msg = Label(
            text=text,
            markup=True,
            size_hint_y=None,
            halign='left',
            valign='middle',
            padding=(20, 20),
            color=(1,1,1,1)
        )

        msg.bind(
            width=lambda s, w: setattr(
                s, 'text_size', (w - 40, None)
            )
        )

        msg.texture_update()
        msg.height = msg.texture_size[1] + 40

        bg = BoxLayout(
            size_hint_y=None,
            height=msg.height,
            padding=10
        )

        with bg.canvas.before:
            from kivy.graphics import Color, RoundedRectangle

            if is_user:
                Color(0.45,0.2,1,1)
            else:
                Color(0.15,0.15,0.2,1)

            bg.rect = RoundedRectangle(
                pos=bg.pos,
                size=bg.size,
                radius=[20]
            )

        def update_rect(*args):
            bg.rect.pos = bg.pos
            bg.rect.size = bg.size

        bg.bind(pos=update_rect, size=update_rect)

        bg.add_widget(msg)

        self.root.ids.chat_area.add_widget(bg)

    def send_message(self):

        text = self.root.ids.user_input.text.strip()

        if not text:
            return

        self.add_message(
            f'[b]You:[/b] {text}',
            True
        )

        self.root.ids.user_input.text = ''

        threading.Thread(
            target=self.ai_reply,
            args=(text,)
        ).start()

    def ai_reply(self, text):

        try:

            headers = {
                "Authorization": f"Bearer {self.API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "gpt-4.1-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are SOUPTIK AI, a futuristic AI assistant."
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ]
            }

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )

            reply = response.json()['choices'][0]['message']['content']

        except Exception as e:
            reply = f"Error: {e}"

        Clock.schedule_once(
            lambda dt: self.add_message(
                f'[b]SOUPTIK AI:[/b] {reply}',
                False
            )
        )

MainApp().run()