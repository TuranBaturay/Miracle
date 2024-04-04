import batFramework as bf
import pygame
def style(e:bf.Button):
    if type(e)==bf.Button:
        e.set_color(bf.color.GOLD)
        e.set_shadow_color(bf.color.GOLD_SHADE)
        e.set_text_color(bf.color.ORANGE_SHADE)
        e.set_outline_color(bf.color.GOLD_SHADE)
        e.set_outline_width(2)
        e.set_relief(5)
        e.disable_effect()
        e.set_padding((10,8))
        #e.set_border_radius(20)

class TitleScene(bf.Scene):
    def __init__(self):
        super().__init__("title")
    def do_when_added(self):
        
        self.set_clear_color((200,240,210))
        self.add_hud_entity(bf.BasicDebugger())
        self.actions.add_actions(*bf.DirectionalKeyControls())
        for a in self.actions: a.set_instantaneous()
        

        title = bf.Label("MIRACLE").add_constraints(bf.constraints.CenterX()).set_y(20)

        b_play = bf.Button("PLAY",lambda : self.manager.transition_to_scene("main",bf.transition.CircleIn(1)))
        b_quit = bf.Button("QUIT",self.manager.stop)
        
        main_container = bf.Container(bf.layout.Row(gap=10)).set_y(100)

        main_container.add_constraints(bf.constraints.CenterX(),)
        
        main_container.add_child(b_play,b_quit)
        self.root.add_child(title,main_container)
        
        self.root.propagate_function(style)

        title.set_text_size(16).set_draw_mode(bf.drawMode.TEXTURED)
        title.set_texture(pygame.transform.scale_by(bf.ResourceManager().get_image("assets/shapes/shape1.png",True),2))
        title.set_padding(10)


        bf.AudioManager().load_music("test","midi/test.mid")

