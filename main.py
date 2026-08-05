import asyncio
import os
import edge_tts
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

# Android Native Integration (Pyjnius)
try:
  from jnius import autoclass

  PythonActivity = autoclass("org.kivy.android.PythonActivity")
  Context = autoclass("android.content.Context")
  PowerManager = autoclass("android.os.PowerManager")
  KeyguardManager = autoclass("android.app.KeyguardManager")
  Intent = autoclass("android.content.Intent")
  Uri = autoclass("android.net.Uri")
  ANDROID_ENV = True
except Exception:
  ANDROID_ENV = False

VOICE = "ur-PK-AsadNeural"  # Movie-style Urdu Voice


class JarvisUltimateApp(MDApp):

  def build(self):
    self.theme_cls.theme_style = "Dark"
    self.theme_cls.primary_palette = "Cyan"

    screen = MDScreen()

    # Title
    self.title_label = MDLabel(
        text="[ J.A.R.V.I.S :: STARK OS ]",
        halign="center",
        pos_hint={"center_y": 0.82},
        font_style="H4",
        theme_text_color="Custom",
        text_color=(0, 0.9, 1, 1),
    )
    screen.add_widget(self.title_label)

    # Status
    self.status_label = MDLabel(
        text="STATUS: FULL SYSTEM ACCESS ACTIVE, BOSS",
        halign="center",
        pos_hint={"center_y": 0.52},
        font_style="Subtitle1",
        theme_text_color="Custom",
        text_color=(0, 1, 0.4, 1),
    )
    screen.add_widget(self.status_label)

    # Trigger Button
    self.btn = MDFillRoundFlatButton(
        text="COMMUNICATE WITH JARVIS",
        pos_hint={"center_x": 0.5, "center_y": 0.28},
        on_release=self.start_command_flow,
    )
    screen.add_widget(self.btn)

    # Welcome Speech
    Clock.schedule_once(
        lambda dt: self.speak(
            "Ji Boss, Stark OS online hai. Aapke paas poora system control"
            " hai."
        ),
        1,
    )

    return screen

  # --- SCREEN UNLOCK & WAKEUP LOGIC ---
  def unlock_device_screen(self):
    if ANDROID_ENV:
      try:
        activity = PythonActivity.mActivity
        power_manager = activity.getSystemService(Context.POWER_SERVICE)
        keyguard_manager = activity.getSystemService(Context.KEYGUARD_SERVICE)

        # Screen light ON
        wake_lock = power_manager.newWakeLock(
            PowerManager.SCREEN_BRIGHT_WAKE_LOCK
            | PowerManager.ACQUIRE_CAUSES_WAKEUP,
            "Jarvis:FullAccessWakeLock",
        )
        wake_lock.acquire(4000)

        # Unlock Keyguard Lock Screen
        keyguard_lock = keyguard_manager.newKeyguardLock("Jarvis:Keyguard")
        keyguard_lock.disableKeyguard()
      except Exception as e:
        print(f"Unlock Error: {e}")

  # --- PHONE AUTOMATION (SEND MESSAGE / OPEN APPS) ---
  def execute_phone_action(self, action_type, detail=""):
    self.unlock_device_screen()

    if ANDROID_ENV:
      activity = PythonActivity.mActivity
      if action_type == "whatsapp":
        # Direct WhatsApp Message Intent
        intent = Intent(Intent.ACTION_VIEW)
        intent.setData(Uri.parse("https://api.whatsapp.com/send?text=Hello"))
        activity.startActivity(intent)
      elif action_type == "sms":
        # Direct SMS Intent
        intent = Intent(Intent.ACTION_VIEW, Uri.parse("sms:"))
        intent.putExtra("sms_body", detail)
        activity.startActivity(intent)

  # --- SPEECH ENGINE ---
  def speak(self, text):
    asyncio.run(self.generate_speech(text))

  async def generate_speech(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save("jarvis_exec.mp3")
    sound = SoundLoader.load("jarvis_exec.mp3")
    if sound:
      sound.play()

  def start_command_flow(self, instance):
    self.status_label.text = "STATUS: LISTENING TO COMMAND, BOSS..."
    # Simulated execution check for demo
    Clock.schedule_once(self.simulate_action, 2)

  def simulate_action(self, dt):
    self.status_label.text = "STATUS: EXECUTING TASK, BOSS"
    self.speak("Hukm sar aankhon par Boss, message bheja ja raha hai.")
    # Example trigger
    self.execute_phone_action("sms", "Hello Boss, Jarvis is online.")


if __name__ == "__main__":
  JarvisUltimateApp().run()