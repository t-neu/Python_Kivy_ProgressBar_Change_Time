from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, AliasProperty, ObjectProperty
import datetime
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.animation import Animation

timeInSecondsGlobal = 90
 
class LargeGrid(GridLayout):
    cols = 8
    rows = 8
 
    def __init__(self,**kwargs):
        super(LargeGrid,self).__init__(**kwargs)
        for i in range(64):
            self.add_widget(Button(text=str(i)))

class MyPBtext(Label):
    pass

class MypbSlider(Slider):
    pass
 
class MyPB(ProgressBar):
    global timeInSecondsGlobal

    value = NumericProperty(0.)

    def __init__(self,**kwargs):
        super(ProgressBar,self).__init__(**kwargs)
        self.barValue = 0
        self.timeInSeconds = 0
        self.increment = 0.25

    def start(self,obj):
        self.variables()
        self.updateProgressBar = Clock.schedule_interval(self.update, self.increment)

    def variables(self):
        self.barValue = 0
        self.timeInSeconds = self.mypb_slider.value
        self.increment = 0.25

    def update(self,obj):
        self.barValue = self.barValue + self.increment
        self.set_norm_value(value=self.barValue / self.timeInSeconds)
        if(self.barValue > self.timeInSeconds):

            Clock.unschedule(self.updateProgressBar)
            self.barValue = 0
            self.timeInSeconds = self.mypb_slider.value
            self.increment = 0.25

    def get_norm_value(self):
        d = self.max
        if d == 0:
            return 0
        return self.value / float(d)

    def set_norm_value(self, value):
        self.value = value * self.max
    
    value_normalized = AliasProperty(get_norm_value, set_norm_value,
                                     bind=('value', 'max'))

    max = NumericProperty(100.)
 
root = Builder.load_string('''

BoxLayout:
    orientation: 'vertical'
    MyPB:
        mypb_slider: mypb_slider
        orientation: 'horizontal'
        id: mypb
    BoxLayout:
        orientation: 'vertical'
        FloatLayout:
            id: float_mypb
            MyPBtext:
                size_hint: None, None
                size: 60, 60
                pos: (mypb_slider.value_pos[0] - 30, mypb_slider.value_pos[1] + 60)
                text: str(int(mypb_slider.value))
                id: mypb_text
                color: 0.3833, 1.0, 0.0, 0.0
                font_size: 24
        MypbSlider:
            min: 10
            max: 240
            value: 40
            step: 5
            id: mypb_slider
            on_touch_up: mypb_text.color = (1.0, 0.7, 0.0, 0.0)
            on_touch_down: mypb_text.color = (1.0, 0.7, 0.0, 1.0)
    Button:
        text: "Start"
        size_hint: (1, 1)
        id: start_btn
        on_press: app.root.ids.mypb.start(self)
 ''')
 
 
class MyApp(App):
 
    def build(self):
        return root
 
MyApp().run()