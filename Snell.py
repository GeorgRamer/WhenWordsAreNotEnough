from manim import *
import numpy as np
from manim_slides import Slide

manim_CAVS1 = rgb_to_color((0,22/255,78/255))
manim_CAVS2 = rgb_to_color((51/255,203/255,156/255))


class Snell(Slide):
    def construct(self):
        inc = ValueTracker(45)
        trans = ValueTracker(0)
        n1 = ValueTracker(1.0)
        n2 = ValueTracker(1.5)
        def update_trans(ang):
            i = inc.get_value()/180*np.pi
            ratio = np.sin(i)*n1.get_value()/n2.get_value()
            if ratio <= 1:
                o = np.arcsin(ratio)
            else:
                o = np.arcsin(1)
            trans.set_value(o/np.pi*180)
        
        update_trans(None)
        trans.add_updater(update_trans)
        
        length = config.frame_height/2
        
        
        def n_to_color(n):
            offset=0.2
            max_n=3
            min_n=1
            val = 1 - ((n-min_n)/(max_n-min_n)*(1-offset)+offset)
            return rgb_to_color((val, val, val))
        
        def get_n_filler(n):
            return lambda p: p.set_fill(color=n_to_color(n.get_value()))
        
        medium1 = Rectangle(height = config.frame_height, width=config.frame_width/2, color=None,fill_color=n_to_color(n1.get_value())).set_fill(opacity=1).shift(LEFT*config.frame_width/4) 
        medium1.add_updater(get_n_filler(n1))
        medium2 = Rectangle(height = config.frame_height, width=config.frame_width/2, color=None,fill_color=n_to_color(n2.get_value())).set_fill(opacity=1).shift(RIGHT*config.frame_width/4) 
        medium2.add_updater(get_n_filler(n2))
        interface = Line([0,config.frame_height/2, 0], [0,-config.frame_height/2, 0]) 
        ray1 = always_redraw(lambda: Line([-length*np.cos(np.pi*inc.get_value()/180),length*np.sin(np.pi*inc.get_value()/180), 0] , [0,0,0] ).add_tip())
        normal = DashedLine([-config.frame_width/2, 0,0],[config.frame_width/2, 0,0] )
        ray2 = always_redraw(lambda: Line([0,0,0] ,[length*np.cos(np.pi*trans.get_value()/180),-length*np.sin(np.pi*trans.get_value()/180), 0] ).add_tip())
        
        ray3 = always_redraw(lambda: Line([0,0,0] , [-length*np.cos(np.pi*inc.get_value()/180),-length*np.sin(np.pi*inc.get_value()/180), 0]).add_tip())
        angle = always_redraw(lambda:Angle(ray1, normal, quadrant=[-1,-1],radius=1.5))
        angle2 = always_redraw(lambda:Angle(ray2, normal, quadrant=[1,1],radius=1.5))
        angle3 = always_redraw(lambda:Angle(normal, ray3,  quadrant=[-1,1],radius=1.4))
        theta1 = always_redraw(lambda: Tex(r"$\theta_1$").next_to(angle, LEFT))
        theta2 = always_redraw(lambda:Tex(r"$\theta_2$").next_to(angle2, RIGHT))
        theta3 = always_redraw(lambda:Tex(r"$\theta_1'$").next_to(angle3, LEFT))
        ortho = Angle(interface, normal, dot=True, quadrant=[-1,-1], color=WHITE, dot_color=WHITE)  
        
        text_n1 = always_redraw(lambda: Tex(r"$n_1={:.2f}$".format(n1.get_value())).to_corner(UL))
        text_n2 = always_redraw(lambda: Tex(r"$n_2={:.2f}$".format(n2.get_value())).to_corner(UR))
        self.add(trans)
        self.play(Create(medium1),Create(medium2), Create(interface), Create(text_n1), Create(text_n2))
        self.wait()
        self.next_slide()
        self.play(Create(normal), Create(ortho))
        self.wait()
        self.next_slide() 
        self.play(FadeOut(ortho))
        self.play(Create(ray1), Create(angle), Create(theta1))
        self.play(Create(ray3), Create(angle3), Create(theta3))
        self.play(Create(ray2), Create(angle2), Create(theta2))
        self.wait()
        self.next_slide()
        self.play(inc.animate.set_value(85))
        self.wait()
        self.next_slide()
        self.play(inc.animate.set_value(30))
        self.wait()

        self.next_slide()
        self.play(n2.animate.set_value(1.1))
        self.wait()
        self.next_slide()
        self.play(n2.animate.set_value(1.0))
        ray4 = Line([-length*np.cos(np.pi*inc.get_value()/180),length*np.sin(np.pi*inc.get_value()/180), 0] , [length*np.cos(np.pi*trans.get_value()/180),-length*np.sin(np.pi*trans.get_value()/180), 0], color=manim_CAVS2)
        self.play(FadeIn(ray4))
        self.wait()
        self.next_slide()
        self.play(FadeOut(ray4))
        self.play(n2.animate.set_value(2))
        self.wait()
        self.next_slide()
        self.play(n1.animate.set_value(1.5),n2.animate.set_value(1) )
        self.wait()
        self.next_slide()
        self.play(inc.animate.set_value(60))
        self.wait()


