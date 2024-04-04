import batFramework as bf
import pygame
import math
import random
from .utils import *


def rotate(surface:pygame.SurfaceType, angle, origin, pivot):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    surface_rect = surface.get_rect(topleft = (origin[0] - pivot[0], origin[1]-pivot[1]))
    offset_center_to_pivot = pygame.math.Vector2(origin) - surface_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(surface, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    return rotated_image,rotated_image_rect

class Egg(bf.Sprite):
    def __init__(self):
        super().__init__(bf.ResourceManager().get_image("assets/sprites/egg_full.png",True), (32,32), True)
        self.shaking = 0
        self.hot_surf = self.surface.copy()
        self.cold_surf = self.surface.copy()

        self.hot_surf.fill("red")
        self.cold_surf.fill("cyan")


        self.temp = 0

    def do_update(self, dt: float) -> None:
        if self.shaking>0:
            self.shaking -= dt
            #self.surface = pygame.transform.rotate(self.original_surface,50*self.shaking * math.cos(0.02*pygame.time.get_ticks()))
            self.rect.x = 20*self.shaking * math.cos(0.09*pygame.time.get_ticks())
            self.rect = self.surface.get_frect(center=self.rect.center)
        if self.shaking <=0:
            self.shaking = 0
            self.rect.x = 0
            #self.surface = self.original_surface
            self.rect = self.surface.get_frect(center=self.rect.center)

        
    def shake(self):
        self.shaking = 0.5

    def draw(self, camera: bf.Camera) -> int:
        tmp = self.surface.copy()
        self.hot_surf.set_alpha(20)
        self.surface.blit(self.hot_surf,(0,0),special_flags=pygame.BLEND_RGBA_MULT)
        i = super().draw(camera)
        self.surface = tmp
        return i
class Ball(bf.Sprite):

    def __init__(self,surf):
        super().__init__(surf,(16,16),True)
    def set_speed(self,speed)->"Ball":
        self.speed = speed
        self.velocity.y = self.speed
        return self

    def set_centery(self,y:float)->"Ball":
        self.rect.centery = y
        return self

    def do_update(self, dt: float) -> None:
        self.move_by_velocity(dt)
        if self.rect.top > bf.const.RESOLUTION[1]:
            self.parent_scene.remove_hud_entity(self)


class MainScene(bf.Scene):
    def __init__(self  ):
        super().__init__("main")
    def do_when_added(self):
        self.set_clear_color((200,210,240))
        self.add_hud_entity(bf.BasicDebugger())
        self.egg = Egg()
        self.table = bf.Sprite(bf.ResourceManager().get_image("assets/sprites/table.png",True),(64,64),True)
        self.add_world_entity(self.table,self.egg)
        self.table.set_center(*self.egg.rect.move(0,30).center)
        self.camera.set_center(*self.egg.rect.move(-40,0).center)
        self.root.add_child(bf.Shape((0,0)).add_constraints(bf.constraints.Center()))
        self.music_time = -3000

        self.actions.add_actions(bf.Action("click").add_mouse_control(1))
        ball1 = pygame.Surface((16,16)).convert_alpha()
        ball1.fill((0,0,0,0))
        pygame.draw.circle(ball1,bf.color.RED_SHADE,ball1.get_rect().center,8)

        ball2 = pygame.Surface((16,16)).convert_alpha()
        ball2.fill((0,0,0,0))
        
        pygame.draw.circle(ball2,bf.color.BLUE,ball1.get_rect().center,8)



        self.time = bf.Label("00:00:00").set_draw_mode(bf.drawMode.TEXTURED).set_texture(bf.ResourceManager().get_image("assets/shapes/shape1.png",True))
        self.root.add_child(self.time.add_constraints(bf.constraints.AnchorTopRight()))


        balls = [ball1,ball2]
        self.notes = midi_to_note_events(bf.ResourceManager().get_path("midi/test.mid"))

        self.ball_speed = 70

        self.hitbox_height = bf.const.RESOLUTION[1]-20

        for note in self.notes:
            left = 10
            gap = 16
            lane = [48,50,52,55].index(note[0])
            self.add_hud_entity(Ball(ball1).set_x((left+lane*gap) - 8).set_speed(self.ball_speed).set_centery(self.hitbox_height - self.ball_speed*(note[1]-self.music_time/1000)))
            self.add_hud_entity(Ball(ball2).set_x((left+(3-lane)*gap) - 8).set_speed(self.ball_speed).set_centery(self.hitbox_height - self.ball_speed*(note[1]-self.music_time/1000)))
    

    


    def do_post_world_draw(self, surface: pygame.Surface):
        #surface.fill("red")
        color = (200,180,180)
        color2 = (180,170,170)

        left = 10
        gap = 16
        pygame.draw.line(surface,color2,(left, self.hitbox_height),(left+3*gap, self.hitbox_height),3)
        for i in range(4):
            pygame.draw.line(surface,color,(left+i * gap,0),(left+i * gap,bf.const.RESOLUTION[1]),3)
            #pygame.draw.line(surface,"red",(left+i * 
            # 16,0),(left+i * 16,bf.const.RESOLUTION[1]),2)


    def do_update(self, dt):
        self.music_time = int(self.music_time+dt*1000)
        if self.music_time >= 0 and bf.AudioManager().get_current_music()==None:
            bf.AudioManager().play_music("test")
        self.time.set_text(ms_to_min_sec_centi(self.music_time))
        if self.actions.is_active("click"):
            if self.camera.transpose(self.egg.rect).collidepoint(pygame.mouse.get_pos()): self.egg.shake()