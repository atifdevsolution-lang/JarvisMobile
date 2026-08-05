import os
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

# Android Native Bridge (Pyjnius)
try:
    from jnius import autoclass
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    Context = autoclass("android.content.Context")
    Intent = autoclass("android.content.Intent")
    Uri = autoclass("android.net.Uri")
    TextToSpeech = autoclass("android.speech.tts.TextToSpeech")
    Locale = autoclass("java.util.Locale")
    ANDROID_ENV = True
except Exception as e:
    print(f"Non-Android Environment: {e}")
    ANDROID_ENV = False


class JarvisUltimateApp(MDApp):
    tts_engine = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"

        screen = MDScreen()

        # Title Label
        self.title_label = MDLabel(
            text="[ J.A.R.V.I.S :: STARK OS ]",
            halign="center",
            pos_hint={"center_y": 0.82},
            font_style="H4",
            theme_text_color="Custom",
            text_color=(0, 0.9, 1, 1),
        )
        screen.add_widget(self.title_label)

        # Status Label
        self.status_label = MDLabel(
            text="STATUS: FULL SYSTEM ACCESS ACTIVE, BOSS",
            halign="center",
            pos_hint={"center_y": 0.52},
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=(0, 1, 0.4, 1),
        )
        screen.add_widget(self.status_label)

        # Action Button
        self.btn = MDFillRoundFlatButton(
            text="COMMUNICATE WITH JARVIS",
            pos_hint={"center_x": 0.5, "center_y": 0.28},
            on_release=self.start_command_flow,
        )
        screen.add_widget(self.btn)

        # Initialize Android Speech Engine
        if ANDROID_ENV:
            Clock.schedule_once(self.init_tts, 0.5)

        # Welcome Speech
        Clock.schedule_once(
            lambda dt: self.speak("Ji Boss, Stark OS online hai. Full system access tayar hai."), 2
        )

        return screen

    # --- NATIVE ANDROID TEXT-TO-SPEECH (TTS) ---
    def init_tts(self, dt):
        try:
            activity = PythonActivity.mActivity
            self.tts_engine = TextToSpeech(activity, None)
            # Set language to Hindi/Urdu context
            self.tts_engine.setLanguage(Locale("hi", "IN"))
        except Exception as e:
            print(f"TTS Init Error: {e}")

    def speak(self, text):
        print(f"JARVIS: {text}")
        if ANDROID_ENV and self.tts_engine:
            try:
                # TextToSpeech.QUEUE_FLUSH = 0
                self.tts_engine.speak(text, 0, None, None)
            except Exception as e:
                print(f"Speech Execution Error: {e}")

    # --- SAFE SCREEN & DEVICE ACTION LOGIC ---
    def unlock_device_screen(self):
        if ANDROID_ENV:
            try:
                activity = PythonActivity.mActivity
                # Modern Android safe Wake Lock
                PowerManager = autoclass("android.os.PowerManager")
                power_manager = activity.getSystemService(Context.POWER_SERVICE)
                wake_lock = power_manager.newWakeLock(
                    PowerManager.FULL_WAKE_LOCK | PowerManager.ACQUIRE_CAUSES_WAKEUP,
                    "Jarvis:WakeLock"
                )
                wake_lock.acquire(3000)
            except Exception as e:
                print(f"WakeLock Error: {e}")

    def execute_phone_action(self, action_type, detail=""):
        self.unlock_device_screen()

        if ANDROID_ENV:
            try:
                activity = PythonActivity.mActivity
                if action_type == "whatsapp":
                    intent = Intent(Intent.ACTION_VIEW)
                    intent.setData(Uri.parse("https://api.whatsapp.com/send?text=" + detail))
                    activity.startActivity(intent)
                elif action_type == "sms":
                    intent = Intent(Intent.ACTION_VIEW, Uri.parse("sms:"))
                    intent.putExtra("sms_body", detail)
                    activity.startActivity(intent)
            except Exception as e:
                print(f"Intent Error: {e}")

    def start_command_flow(self, instance):
        self.status_label.text = "STATUS: EXECUTING COMMAND, BOSS..."
        self.speak("Hukm sar aankhon par Boss, message bheja ja raha hai.")
        Clock.schedule_once(self.simulate_action, 2)

    def simulate_action(self, dt):
        self.execute_phone_action("sms", "Hello Boss, Jarvis is online.")
        self.status_label.text = "STATUS: TASK COMPLETED"


if __name__ == "__main__":
    JarvisUltimateApp().run()
