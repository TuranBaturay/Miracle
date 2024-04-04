import batFramework as bf
from .constants import Constants as const
from .mainScene import MainScene
from .titleScene import TitleScene
import pygame
bf.init(const.RESOLUTION,const.FLAGS,default_text_size=const.TEXT_SIZE,default_font="fonts/"+const.FONT,resource_path="data",fps_limit=const.FPS)


class MyManager(bf.Manager):    
    def __init__(self) -> None:
        super().__init__(
            TitleScene(),
            MainScene())


    def do_pre_init(self) -> None:
        c = bf.ResourceManager().get_image("assets/cursors/default.png")
        ch = bf.ResourceManager().get_image("assets/cursors/hover.png")
        cc = bf.ResourceManager().get_image("assets/cursors/click.png")

        c = pygame.transform.scale_by (c,    6)
        ch = pygame.transform.scale_by(ch,  6)
        cc = pygame.transform.scale_by(cc,  6)



        c.set_colorkey((255,0,255))
        ch.set_colorkey((255,0,255))
        cc.set_colorkey((255,0,255))


        bf.const.set_default_cursor(pygame.Cursor((0,0),c))
        bf.const.set_default_hover_cursor(pygame.Cursor((0,0),ch))
        bf.const.set_default_click_cursor(pygame.Cursor((10,10),cc))
        pygame.mouse.set_cursor(bf.const.DEFAULT_CURSOR)
        
    

