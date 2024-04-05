from manim import *
import numpy as np
from manim_slides import Slide

manim_CAVS1 = rgb_to_color((0,22/255,78/255))
manim_CAVS2 = rgb_to_color((51/255,203/255,156/255))




class vibrations(Slide):

            
    def construct(self):
        
        radius = 0.3
        bond_dist = 0.05
        
        C = Dot([-4,0,0], radius=radius,z_index=5)
        O1 = Dot([-5,0,0], radius=radius,color=RED,z_index=5)
        O2 = Dot([-3,0,0], radius=radius,color=RED,z_index=5)   
        mole = VGroup(C, O1, O2)
        
        bond1 = always_redraw(lambda: VGroup(*[Line(O1.get_center()+UP*bond_dist, C.get_center()+UP*bond_dist), Line(O1.get_center()+DOWN*bond_dist, C.get_center()+DOWN*bond_dist)])) 
        bond2 = always_redraw(lambda: VGroup(*[Line(O2.get_center()+UP*bond_dist, C.get_center()+UP*bond_dist), Line(O2.get_center()+DOWN*bond_dist, C.get_center()+DOWN*bond_dist)])) 
             
        
        
             
                                                                                                     
        self.add(C, O1, O2, bond1, bond2)
        self.wait()
        self.next_slide()
        coords1 = Tex(r"""$\begin{bmatrix}
           x_1\\
           y_1\\
           z_1
         \end{bmatrix}$""").next_to(O1, UP)
        coords2 = Tex(r"""$\begin{bmatrix}
           x_2\\
           y_2\\
           z_2
         \end{bmatrix}$""").next_to(C, UP)
        coords3 = Tex(r"""$\begin{bmatrix}
           x_3\\
           y_3\\
           z_3
         \end{bmatrix}$""").next_to(O2, UP)
        for c in [coords1, coords2, coords3]:
            self.play(Write(c))
        self.next_slide()
        self.play(coords3.animate.move_to([-2,-3,0]))
        self.play( coords2.animate.next_to(coords3, UP, buff=0.0, ))
        self.play(coords1.animate.next_to(coords2, UP, buff=0.0))
        
        coords_all = Tex(r"""$\begin{bmatrix}
           x_1\\
           y_1\\
           z_1\\
           x_2\\
           y_2\\
           z_2\\
           x_3\\
           y_3\\
           z_3
         \end{bmatrix}$""").move_to(coords2)
        
        self.play(FadeIn(coords_all),*[FadeOut(c) for c in [coords1, coords2, coords3]])
        self.next_slide()
        
        self.play(mole.animate.shift(UP))
        self.play(mole.animate.shift(DOWN+LEFT))
        self.play(mole.animate.shift(RIGHT))
        self.play(mole.animate.scale(1.2))
        coords_change = Tex(r"""$= \bar{x} + \bar{y} + \bar{z}$""").next_to(coords_all, RIGHT)
        
        self.play( mole.animate.scale(1/1.2), Create(coords_change))
        self.wait()
        self.next_slide()
        coords_rotate= Tex(r"""$+ \rho_y + \rho_z$""").next_to(coords_change, RIGHT)
        self.play(Rotate(mole,axis=UP+np.array([0,0,1]), angle=6*PI), Write(coords_rotate), rate_func=linear, duration=4)
        self.wait()
        self.next_slide()
        
        self.t = 0
        def sym_updated(m, dt):
            A = 0.5
            f = 1
            self.t = self.t + dt
            t = self.t
            O1.shift([np.cos(2*np.pi*t)*A/f/2/np.pi,0,0])
            O2.shift([-np.cos(2*np.pi*t)*A/f/2/np.pi,0,0])
        def asym_updated(m, dt):
            A = 0.5
            self.t = self.t + dt
            f = 2
            t = self.t
            O1.shift([np.cos(2*np.pi*t)*A/f/2/np.pi,0,0])
            O2.shift([np.cos(2*np.pi*t)*A/f/2/np.pi,0,0])
            C.shift([-np.cos(2*np.pi*t)*A/2/f/2/np.pi,0,0])
        def def_updated(m, dt):
            A = 0.5
            f = 3
            self.t = self.t + dt
            t = self.t
            O1.shift([0, np.cos(2*np.pi*t)*A/f/2/np.pi,0])
            O2.shift([0, np.cos(2*np.pi*t)*A/f/2/np.pi,0])
        
        O1.add_updater(sym_updated)
        coords_sym = Tex(r"""$+\sigma_{s}$""").next_to(coords_rotate, RIGHT)
        self.play(Write(coords_sym), duration=2)
        self.wait()
        self.next_slide()
        O1.remove_updater(sym_updated)
        O1.add_updater(asym_updated)
        coords_asym = Tex(r"""$ + \sigma_{a}$""").next_to(coords_sym, RIGHT)
        self.play(Write(coords_asym), duration=2)
        O1.remove_updater(asym_updated)
        O1.add_updater(def_updated)
        self.wait()
        self.next_slide()
        coords_def= Tex(r"""$+ \delta$""").next_to(coords_asym, RIGHT)
        
         #Tex(r"""\begin{equation}+  \delta \end{equation}""").next_to(coords_asym, RIGHT)
        self.play(Write(coords_def), duration=2)
        self.wait()
