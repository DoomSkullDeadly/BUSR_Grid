import sys
import pygame

pygame.init()

display_info = pygame.display.Info()
display_size = display_info.current_w / 2, display_info.current_h / 2

display = pygame.display.set_mode(display_size, pygame.RESIZABLE | pygame.HWACCEL)
c_black = (0, 0, 0)
c_white = (255, 255, 255)

fps_font = pygame.font.SysFont("Arial", 18)

clock = pygame.time.Clock()


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = fps_font.render(fps, True, c_white)
    return fps_text


class Button:
    def __init__(self, size, pos_c=None, pos_tl=None, text="button", action="yes", font_size=18, colour=(0, 0, 0),
                 show=True):
        self.size = size
        self.text = text
        self.action = action
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect()
        self.colour = colour
        if pos_c:
            self.rect.center = pos_c
        elif pos_tl:
            self.rect.topleft = pos_tl
        self.font_size = font_size
        self.show = show

    def click(self, mouse_pos):
        if not self.rect.collidepoint(mouse_pos) or not self.show:
            return
        if self.action == "yes":
            yes()
        if self.action == "render":
            render()

    def render(self):
        if not self.show:
            return
        pygame.draw.rect(self.surface, self.colour, self.surface.get_rect())
        font = pygame.font.SysFont("Arial", self.font_size)
        pos = (self.surface.get_size()[0]/2 - font.size(self.text)[0]/2,
               self.surface.get_size()[1]/2 - font.size(self.text)[1]/2)
        self.surface.blit(font.render(self.text, True, (255, 255, 255)), pos)
        display.blit(self.surface, self.rect.topleft)


class Scroll:
    def __init__(self, size, pos_c=None, pos_tl=None, content=None):
        self.size = size
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect()
        if pos_c:
            self.rect.center = pos_c
        elif pos_tl:
            self.rect.topleft = pos_tl
        if not content:
            self.content = []
        else:
            self.content = content


def yes():
    print("yes")


def render():
    print("render")


def main(x: int = 60):
    # if sys.argv[1]:
    #     x = int(sys.argv[1])
    running = 1
    buttons = []
    test_button = Button((100, 100), (200, 200), "button", "yes", colour=(210, 40, 21), font_size=60, show=True)
    buttons.append(test_button)
    render_button = Button(size=(200, 60), pos_c=(display_size[0]/2, display_size[1]-60), text="Render",
                           action="render", font_size=40, colour=(69, 169, 90))
    buttons.append(render_button)
    while running:
        display.fill(color=c_black)
        display.blit(update_fps(), (3, 3))
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.click(mouse_pos)

            if event.type == pygame.MOUSEBUTTONUP:
                pass

        for button in buttons:
            button.render()

        clock.tick(x)
        pygame.display.flip()


if __name__ == '__main__':
    main()
