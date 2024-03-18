import core as c

c.pygame.init()
font = c.Font(None, 30)

def debug(info, x=10, y=10):

    surface = c.get_surface()
    debug_surface = font.render(str(info), True, "white")
    debug_rectangle = debug_surface.get_rect(topleft=(x, y))
    c.rect(surface, "black", debug_rectangle)
    surface.blit(debug_surface, debug_rectangle)
