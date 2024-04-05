from manim import *
import numpy as np
from manim_slides import Slide 

from matplotlib.colors import Normalize, LinearSegmentedColormap, SymLogNorm
from matplotlib.cm import coolwarm, ScalarMappable


manim_CAVS1 = rgb_to_color((0,22/255,78/255))
manim_CAVS2 = rgb_to_color((51/255,203/255,156/255))


cm_div_dark = LinearSegmentedColormap.from_list("dark_diverging", [[0.0,  np.array([255,223,232])/255],[0.1,  (0.40392156862745099,  0.0                ,  0.12156862745098039)], [0.5, (0,0,0)], [0.9,(0.0196078431372549 ,  0.18823529411764706,  0.38039215686274508)], [1,np.array([199,224,251])/255]
])
cm_dark_white = LinearSegmentedColormap.from_list("black_white", [(0.0,  (0.,0.,0.,1.)),(0.99, (1.,1.,1., 1.)), (1.0, (1.,1.,1., 1.))])





class grating_2(Slide):

   start_x =  -config.frame_width/2 +1
   
   spacing = 0.05
   
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
        wl = ValueTracker(.025)
        phase = ValueTracker(0)
        f = ValueTracker(1)
        N_waves=ValueTracker(1)
        cur_spacing = ValueTracker(self.spacing)
        self.last_spacing = cur_spacing.get_value()
        
        
        def get_base_field(spacing,N):
                x = np.linspace(-config.frame_width/2-self.start_x,config.frame_width/2-self.start_x,int(config.frame_width*100))    
                y = np.linspace(-config.frame_height/2,config.frame_height/2,int(config.frame_height*100))
                Y,X = np.meshgrid(y,x)
                img = np.zeros_like(X, dtype=complex)
                left_side = X<0
                right_side = X>=0
                img[left_side] = np.exp(2j*np.pi/wl.get_value()*X[left_side])
                for start_y in [spacing *(N/2-n-0.5)  for n in range(0,N)]:
                    r = np.sqrt((X[right_side])**2 + (Y[right_side]-start_y)**2)
                    img[right_side] = img[right_side]+ np.exp(2j*np.pi/wl.get_value()*r)/r
                    
                return img
                
        self.field = get_base_field(cur_spacing.get_value(),int(N_waves.get_value()))
        
        def get_field_at_phase(cur_phase, f):
            multiplier = np.exp(-2j*np.pi*cur_phase)
            return np.real(self.field*multiplier)
            
            
        

        scm = ScalarMappable(norm=SymLogNorm(linthresh=5/config.frame_width, vmin=-2, vmax=2), cmap=cm_div_dark)
        
        def get_color_pixels(imga):
            mx = np.max(np.abs(imga))
            colored = np.uint8(scm.to_rgba(imga.T)*255)
            return colored
        
        print(np.amax(self.field))

        def get_mimg(redo_field=False):
                if redo_field:
                    self.field = get_base_field(cur_spacing.get_value(),int(N_waves.get_value()) )
                colored = get_color_pixels(get_field_at_phase(phase.get_value(), f.get_value()))
                mimg = ImageMobject(colored)
                mimg.height=config.frame_height
                mimg.width=config.frame_width 
                return mimg
        
        mimg = get_mimg()
        
        def diffraction_angle(wl, d, m):
           return np.arcsin(wl*m/d)
        
        def create_slits(spacing, N):
                slit_size = 0.05
                width=6
                grating = VMobject(z_index=10, color=manim_CAVS2,stroke_width=width)
                grating.append_vectorized_mobject(Line([self.start_x,config.frame_height/2,0],[self.start_x, (N/2 -0.5)*spacing+slit_size/2,0]))
                for n in range(0,N):
                       grating.append_vectorized_mobject(
                          Line([self.start_x, (N/2-n-0.5)*spacing-slit_size/2,0],
                          [self.start_x, (N/2-n-1-0.5)*spacing+slit_size/2,0]))
                grating.append_vectorized_mobject(Line([self.start_x, (-N/2+0.5)*spacing-slit_size/2,0],[self.start_x,-config.frame_height/2,0]))
                return grating
        grating = create_slits(cur_spacing.get_value(), int(N_waves.get_value()))
    
        
        def update_grating(m):
            grating.become(create_slits(cur_spacing.get_value(), int(N_waves.get_value())))
             
        
        def update_mimg(m):
            redo =  True
                
            mimg.become(get_mimg(redo))
            self.last_spacing = cur_spacing.get_value()
        
        mimg.add_updater(update_mimg)
        grating.add_updater(update_grating)


        self.play(Create(grating))
        self.play(FadeIn(mimg))
        self.bring_to_front(grating)
        self.wait()
        self.next_slide() 
        self.play(N_waves.animate.set_value(2))
        self.wait()
        self.next_slide() 
        self.play(N_waves.animate.set_value(20),  rate_func=rate_functions.linear, run_time=2)
        self.wait()
        self.next_slide() 
        def get_diffraction(order):
             a1 = diffraction_angle(wl.get_value(), cur_spacing.get_value(), order)
             
             return Line([self.start_x,0,0], 
                                np.array([self.start_x,0,0])+ 20 * np.array([np.cos(a1),
                                 np.sin(a1), 0]))
        zeroth_order = get_diffraction(0)
        first_order = get_diffraction(1)
        
        ang = Angle(zeroth_order, first_order, radius=3)
        
        ang_label = Tex(r"$d \sin(\theta_m) = m \lambda$").next_to(ang, RIGHT)
        mimg.remove_updater(update_mimg)
        self.play(Create(zeroth_order))
        self.play(Create(first_order))
        self.play(Create(ang))
        self.play(Create(ang_label))
        def order_updater(m):
            first_order.become(get_diffraction(1))
        def ang_updater(m):
           ang.become(Angle(zeroth_order, first_order, radius=6))
           ang_label.next_to(ang, RIGHT)
        ang.add_updater(ang_updater)
        first_order.add_updater(order_updater)
        mimg.add_updater(update_mimg)
        self.wait()
        self.next_slide() 
        self.play(cur_spacing.animate.set_value(self.spacing*1.5), run_time=1)
        self.play(cur_spacing.animate.set_value(self.spacing/1.5),  run_time=1)
        self.play(cur_spacing.animate.set_value(self.spacing),  run_time=1)
        self.wait()
        
