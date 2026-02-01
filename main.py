from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
import random

class StepCounterApp(App):
    def build(self):
        self.store = JsonStore('user_profile.json')
        self.steps = 0
        
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        # Header
        layout.add_widget(Label(text="🏃 STEP TRACKER PRO", font_size=28, color=(0, 1, 0.8, 1)))

        # Profile Inputs
        self.name_in = TextInput(hint_text="Apna Naam", multiline=False, size_hint_y=None, height=100)
        self.age_in = TextInput(hint_text="Apni Age", input_filter='int', multiline=False, size_hint_y=None, height=100)
        self.goal_in = TextInput(hint_text="Daily Step Goal (e.g. 5000)", input_filter='int', multiline=False, size_hint_y=None, height=100)

        layout.add_widget(self.name_in)
        layout.add_widget(self.age_in)
        layout.add_widget(self.goal_in)

        # Save Button
        btn_save = Button(text="Save & Start", background_color=(0, 0.7, 0, 1), size_hint_y=None, height=120)
        btn_save.bind(on_press=self.save_data)
        layout.add_widget(btn_save)

        # Step Display
        self.status = Label(text="Steps: 0 | Goal: 0", font_size=22)
        layout.add_widget(self.status)

        self.load_data()
        
        # Simulating steps (Since Termux lacks direct sensor access)
        Clock.schedule_interval(self.update_steps, 2)
        
        return layout

    def save_data(self, instance):
        name, age, goal = self.name_in.text, self.age_in.text, self.goal_in.text
        if name and age and goal:
            self.store.put('user', name=name, age=age, goal=int(goal), steps=self.steps)
            self.status.text = f"Hi {name}! Goal: {goal}"
        else:
            self.status.text = "Error: Fill all details!"

    def load_data(self):
        if self.store.exists('user'):
            user = self.store.get('user')
            self.name_in.text = user['name']
            self.age_in.text = str(user['age'])
            self.goal_in.text = str(user['goal'])
            self.steps = user['steps']
            self.status.text = f"Welcome back! Goal: {user['goal']}"

    def update_steps(self, dt):
        if self.store.exists('user'):
            # In a real APK, this would use the Accelerometer sensor
            self.steps += random.randint(0, 10) 
            user = self.store.get('user')
            self.status.text = f"Steps: {self.steps} / Goal: {user['goal']}"

if __name__ == '__main__':
    StepCounterApp().run()
