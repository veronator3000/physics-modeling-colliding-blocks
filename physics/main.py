import pygame

pygame.init()

HEIGHT = 280
WIDTH = 1800
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font('beer-money12.ttf', 30)


class Cube:
    def __init__(self, x, w, color, v, m):
        self.w = w
        self.x = x
        self.y = HEIGHT - self.w
        self.color = color
        self.v = v
        self.m = m


cube0 = Cube(1000, 15, (200, 230, 50), 0, 1)
cube1 = Cube(1300, 30, (200, 0, 100), -300, 10)


class InputBox:
    __text_margin = 20
    __input_box_margin = 60

    def __init__(self, input_text, text):
        self.margin = InputBox.__text_margin
        InputBox.__text_margin += 80
        self.input_text = input_text
        self.input_box = pygame.Rect(20, InputBox.__input_box_margin, 140, 32)
        InputBox.__input_box_margin += 80
        self.is_active = False
        self.text = text
        self.color = COLOR_INACTIVE

    def draw(self):
        surface = font.render(self.text, True, self.color)
        self.input_box.w = max(200, surface.get_width() + 10)
        screen.blit(surface, (self.input_box.x + 5, self.input_box.y - 5))
        screen.blit(self.input_text, (20, self.margin))
        pygame.draw.rect(screen, self.color, self.input_box, 2)

    def click(self):
        self.is_active = self.input_box.collidepoint(event.pos)
        self.color = COLOR_ACTIVE if self.is_active else COLOR_INACTIVE

    def print(self):
        if self.is_active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():
                self.text += event.unicode


mass_input = InputBox(font.render('Масса красного объекта:', True, (180, 0, 0)), '10')
speed_input = InputBox(font.render('Скорость красного объекта:', True, (180, 0, 0)), '300')

start = False
while not start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mass_input.click()
            speed_input.click()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                cube1.m = int(mass_input.text)
                cube1.v = -int(speed_input.text)
                start = True
            mass_input.print()
            speed_input.print()

    screen.fill((30, 30, 30))

    mass_input.draw()
    speed_input.draw()

    pygame.display.update()
    pygame.time.Clock().tick(60)

hits_counter_text = font.render('Количество ударов:', True, (0, 0, 0))

running = True
cnt = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)

    screen.fill((153, 139, 158))
    if cube0.x <= 0:
        cnt += 1
        cube0.v = -cube0.v
    if cube0.x + cube0.w >= cube1.x:
        cnt += 1
        new_v0 = (((cube0.m - cube1.m) * cube0.v) + 2 * cube1.m * cube1.v) / (cube0.m + cube1.m)
        new_v1 = (((cube1.m - cube0.m) * cube1.v) + 2 * cube0.m * cube0.v) / (cube0.m + cube1.m)
        cube0.v = new_v0
        cube1.v = new_v1
    # x = x0 + v * t
    cube0.x = cube0.x + cube0.v * 0.016
    cube1.x = cube1.x + cube1.v * 0.016

    if cube1.x <= cube0.w:
        pygame.draw.rect(screen, cube0.color, (0, cube0.y, cube0.w, cube0.w))
        pygame.draw.rect(screen, cube1.color, (cube0.w, cube1.y, cube1.w, cube1.w))
    else:
        pygame.draw.rect(screen, cube0.color, (cube0.x, cube0.y, cube0.w, cube0.w))
        pygame.draw.rect(screen, cube1.color, (cube1.x, cube1.y, cube1.w, cube1.w))

    screen.blit(hits_counter_text, (750, 20))
    hits_count_text = font.render(str(cnt), True, (0, 0, 0))
    screen.blit(hits_count_text, (980, 20))

    pygame.display.update()
    pygame.time.Clock().tick(60)

pygame.quit()

print(cnt)
