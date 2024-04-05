from manim import *
import numpy as np
from manim_slides import Slide

from matplotlib.colors import Normalize, LinearSegmentedColormap
from matplotlib.cm import coolwarm, ScalarMappable


manim_CAVS1 = rgb_to_color((0,22/255,78/255))
manim_CAVS2 = rgb_to_color((51/255,203/255,156/255))


cm_div_dark = LinearSegmentedColormap.from_list("dark_diverging", [[0.0,  np.array([255,223,232])/255],[0.1,  (0.40392156862745099,  0.0                ,  0.12156862745098039)], [0.5, (0,0,0)], [0.9,(0.0196078431372549 ,  0.18823529411764706,  0.38039215686274508)], [1,np.array([199,224,251])/255]
])
cm_dark_white = LinearSegmentedColormap.from_list("black_white", [(0.0,  (0.,0.,0.,1.)),(0.99, (1.,1.,1., 1.)), (1.0, (1.,1.,1., 1.))])





class grating(Slide):

   start_x =  -config.frame_width/2 +1
   
   spacing = 1
   
   def wave_intersect(self, v1, v2, r1, r2):
   
       v1 = np.array(v1)
       v2 = np.array(v2)
       d = np.sqrt( np.sum( (v1-v2)**2))
       print(d, r1,r2)
       if (r1+r2)<d or np.abs(r1-r2)>d:
           return np.nan, np.nan
       a = (r1**2-r2**2+d**2)/(2*d)
       h = np.sqrt(r1**2-a**2)   
       
       v3 = v1+a/d*(v2-v1)
       v4 = v3 + h*np.array([1,-1])/d*(v2-v1)[::-1]
       print(v3,v4)
       if v3[0]>self.start_x:
           return v3
       return v4
            
   def construct(self):
        wl = ValueTracker(.5)
        phase = ValueTracker(0)
        f = ValueTracker(1)
        cur_spacing = ValueTracker(0)
        self.last_spacing = cur_spacing.get_value()
        
        
        def get_base_field(spacing):
                x = np.linspace(-config.frame_width/2-self.start_x,config.frame_width/2-self.start_x,int(config.frame_width*100))    
                y = np.linspace(-config.frame_height/2,config.frame_height/2,int(config.frame_height*100))
                Y,X = np.meshgrid(y,x)
                img = np.zeros_like(X, dtype=complex)
                left_side = X<0
                right_side = X>=0
                img[left_side] = np.exp(2j*np.pi/wl.get_value()*X[left_side])
                for start_y in [spacing/2,-spacing/2]:
                    r = np.sqrt((X[right_side])**2 + (Y[right_side]-start_y)**2)
                    img[right_side] = img[right_side]+ np.exp(2j*np.pi/wl.get_value()*r)/r
                return img
                
        self.field = get_base_field(cur_spacing.get_value())
        
        def get_field_at_phase(cur_phase, f):
            multiplier = np.exp(-2j*np.pi*cur_phase)
            return np.real(self.field*multiplier)
            
            
        

        scm = ScalarMappable(norm=Normalize(-1,1), cmap=cm_div_dark)
        
        def get_color_pixels(imga):
            colored = np.uint8(scm.to_rgba(imga.T)*255)
            return colored
        
        print(np.amax(self.field))

        def get_mimg(redo_field=False):
                if redo_field:
                    self.field = get_base_field(cur_spacing.get_value())
                colored = get_color_pixels(get_field_at_phase(phase.get_value(), f.get_value()))
                mimg = ImageMobject(colored)
                mimg.height=config.frame_height
                mimg.width=config.frame_width 
                return mimg
        
        mimg = get_mimg()
        
        def diffraction_angle(wl, d, m):
           return np.arcsin(wl*m/d)
        
        def create_slits(spacing):
                slit_size = 0.2
                width=4
                grating = VMobject(z_index=10, color=manim_CAVS2,stroke_width=width)
                grating.append_vectorized_mobject(Line([self.start_x,config.frame_height/2,0],[self.start_x, spacing/2+slit_size/2,0],stroke_width=width))
                if spacing > slit_size:
                       grating.append_vectorized_mobject(Line([self.start_x, spacing/2-slit_size/2,0],[self.start_x, -spacing/2+slit_size/2,0],stroke_width=width))
                grating.append_vectorized_mobject(Line([self.start_x, -spacing/2-slit_size/2,0],[self.start_x,-config.frame_height/2,0],stroke_width=width))
                return grating
        grating = create_slits(cur_spacing.get_value())
        
        waves_0 = [Arc(idx*wl.get_value(), -np.pi/2, np.pi, arc_center=([self.start_x,-cur_spacing.get_value()/2,0]),color=WHITE) for idx in range(30)]
        waves_1 = [Arc(idx*wl.get_value(), -np.pi/2, np.pi, arc_center=([self.start_x,cur_spacing.get_value()/2,0]),color=WHITE) for idx in range(30)]
        
        self.t =  0
        
        
        def update_grating(m):
            grating.become(create_slits(cur_spacing.get_value()))
             
        
        def update_mimg(m):
            redo =  True
                
            mimg.become(get_mimg(redo))
            self.last_spacing = cur_spacing.get_value()
        
        mimg.add_updater(update_mimg)
        grating.add_updater(update_grating)
        
        def update_waves(m):
            for idx, g  in enumerate(waves_0):
                g.set_radius(idx*wl.get_value()+np.mod(phase.get_value(),1)*wl.get_value())
                g.set_arc_center([self.start_x,-cur_spacing.get_value()/2,0])
                g.generate_points()
            for idx, g  in enumerate(waves_1):
                g.set_radius(idx*wl.get_value()+np.mod(phase.get_value(),1)*wl.get_value())
                g.set_arc_center([self.start_x,cur_spacing.get_value()/2,0])
                g.generate_points()
                        
        waves_0[0].add_updater(update_waves)
                
       

        self.play(Create(grating))
        self.play(FadeIn(mimg))
        self.bring_to_front(grating)
        
        
        self.next_slide(loop=True) 
        
        self.play(phase.animate.increment_value(1), rate_func=rate_functions.linear, run_time=1)
        self.next_slide()
        self.play(cur_spacing.animate.set_value(self.spacing))
        #self.play(phase.animate.increment_value(4), rate_func=rate_functions.linear, run_time=4)
        self.next_slide()
        
        for w1, w2 in zip(waves_0, waves_1):
            self.play(FadeIn(w1), FadeIn(w2),run_time=0.05)
        self.wait()
        self.next_slide(loop=True)
        #self.play(Create(first_order), Create(m_first_order))
        
        self.play(phase.animate.increment_value(1), rate_func=rate_functions.linear, run_time=1)
        self.next_slide()
        
        
        d1 = [  Dot(list(self.wave_intersect([self.start_x,-cur_spacing.get_value()/2], 
        [self.start_x,+cur_spacing.get_value()/2], idx*wl.get_value(), (1+idx)*wl.get_value()))+[0])
        for idx in range(1,30)]
        d2 = [  Dot(list(self.wave_intersect([self.start_x,-cur_spacing.get_value()/2], 
        [self.start_x,+cur_spacing.get_value()/2], (1+idx)*wl.get_value(), (idx)*wl.get_value()))+[0])
        for idx in range(1,30)]
        dc = [  Dot(list(self.wave_intersect([self.start_x,-cur_spacing.get_value()/2], 
        [self.start_x,+cur_spacing.get_value()/2], (idx)*wl.get_value(), (idx)*wl.get_value()))+[0])
        for idx in range(2,30)]
        for d in [dc[0], d1[0], d1[1]]:
             l1 = Line([self.start_x,-cur_spacing.get_value()/2,0], d.arc_center, color=manim_CAVS2)
             l2 = Line(d.arc_center, [self.start_x,+cur_spacing.get_value()/2,0], color=manim_CAVS2)
             self.play(FadeIn(d), subcaption=r"The waves show positive interference along lines that are  $N \lambda$ from both slits.", subcation_duration=3)
             self.play(Create(l1))
             self.play(Create(l2))
             self.play(FadeOut(l1), FadeOut(l2))
        self.next_slide()
        for d in d1[1:]+d2[1:]+dc[1:]:
            self.play(Create(d,run_time=0.05))
        
        def get_diffraction(order):
             a1 = diffraction_angle(wl.get_value(), cur_spacing.get_value(), order)
             
             return Line([self.start_x,0,0], 
                                np.array([self.start_x,0,0])+ 20 * np.array([np.cos(a1),
                                 np.sin(a1), 0]))
                                 
        zeroth_order = get_diffraction(0)
        first_order = get_diffraction(1)
        
        ang = Angle(zeroth_order, first_order, radius=3)
        
        ang_label = Tex(r"$d \sin(\theta_m) = m \lambda$").next_to(ang, RIGHT)
        
        self.play(Create(zeroth_order))
        self.play(Create(first_order))
        self.play(*[FadeOut(d) for d in d1+d2+dc])
        self.play(*[FadeOut(w) for w in waves_0+waves_1])
        self.play(Create(ang))
        self.play(Create(ang_label))
        self.next_slide()
        def order_updater(m):
            first_order.become(get_diffraction(1))
        def ang_updater(m):
           ang.become(Angle(zeroth_order, first_order, radius=6))
           ang_label.next_to(ang, RIGHT)
        ang.add_updater(ang_updater)
        first_order.add_updater(order_updater)
        self.play(wl.animate.set_value(0.75), subcaption="Larger wavelengths are diffracted to larger angles.", run_time=3)
        self.wait()
        self.next_slide()
        self.play(wl.animate.set_value(0.25), subcaption="Shorter wavelengths are diffracted to smaller angles.",run_time=3)
        self.next_slide()
        self.play(cur_spacing.animate.set_value(0.5), subcaption="Lower spacing leads to larger angles.")
        self.next_slide()
        self.play(cur_spacing.animate.set_value(2), subcaption="Higher spacing leads to larger angles.")
        
        self.play(ang_label.animate.become(Tex(r"$d \sin(\theta_m) = \mathbf{1} \lambda$").next_to(ang, RIGHT)))
        
        second_order = get_diffraction(2)
        ang2 = Angle(zeroth_order, second_order, radius=4)
        ang2_label = Tex(r"$d \sin(\theta_m) = \mathbf{2} \lambda$").next_to(ang2, UP+RIGHT)
        
        self.play(Create(second_order), 
           subcaption="There are multiple diffraction orders.", subcaption_duration=2)
        self.play(Create(ang2), Create(ang2_label))
        
        
        third_order = get_diffraction(3)
        ang3 = Angle(zeroth_order, third_order, radius=2)
        ang3_label = Tex(r"$d \sin(\theta_m) = \mathbf{3} \lambda$").next_to(ang3, UP)
        
        self.play(Create(third_order))
        self.play(Create(ang3), Create(ang3_label))
        self.wait()
        self.next_slide()
        
        """
        self.play(first_order.animate.become(second_order), 
                ang.animate.become(ang2), ang_label.animate.become(ang2_label))
        self.end_fragment(fragment_type=manim_revealjs.NORMAL, t=0)
        self.remove(ang)
        self.remove(ang_label)
        self.remove(second_order)
        def order_updater(m):
            first_order.become(get_diffraction(1))
        first_order.add_updater(order_updater)
        """
        
        
        

