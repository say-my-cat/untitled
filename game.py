from button import *
from states import *
from vrag import *
from ob import *
from effects import *
#from images import *
import images as img
from parameters import *
from save import *
from high_score import *


class Game:
    def __init__(self):
        pygame.display.set_caption('Runner')
        pygame.display.set_icon(icon)

        pygame.mixer.music.load('song/background.mp3')
        pygame.mixer.music.set_volume(0.8)

        self.jump_sound = pygame.mixer.Sound('song/Rrr.wav')
        self.fall_sound = pygame.mixer.Sound('song/Bdish.wav')
        self.loss_sound = pygame.mixer.Sound('song/loss.wav')
        self.heart_plus_sound = pygame.mixer.Sound('song/hp+.wav')
        self.button_sound = pygame.mixer.Sound('song/button.wav')
        self.bullet_sound = pygame.mixer.Sound('song/shot.wav')

        self.lv = 1
        self.cactus_opions = [40, 465, 14, 420, 40, 434]  # ширина, высота дисплея(600)-100-высота какткса
        self.img_counter = 0 # dino
        self.health = 2 # кол-во жизней
        self.make_jump = False
        self.jump_counter = 30 # счетчик прыжков
        self.scores = 0
        self.max_scores = 0
        self.max_above = 0
        self.cooldown = 0
        self.game_state = GameState()
        
        self.save_data = Save()
        self.high_scores = HighScore(self.save_data.get('hs'))
        # self.save_data.add('hs', {})

    def start(self):
        while True:
            if self.game_state.check(State.MENU):
                self.show_menu()
            elif self.game_state.check(State.START):
                self.choose_theme()
                self.choose_hero()
                self.start_game()
            elif self.game_state.check(State.CONTINUE):
                #self.choose_them = self.save_data.get('theme')
                self.max_scores = self.save_data.get('max')
                self.start_game()
            elif self.game_state.check(State.LEVEL_2):
                self.levl_2()
            elif self.game_state.check(State.QUIT):
                self.save_data.save()
                self.save_data.add('max', self.max_scores)
                self.save_data.add('hs', self.high_scores.hs_table)
                break

    def show_menu(self):
        pygame.mixer.music.load('Big_Slinker.mp3')
        pygame.mixer.music.set_volume(0.3)  # 30% громкости
        pygame.mixer.music.play(-1)

        start_btn = Button(288, 70)
        cont_btn = Button(222, 70)
        lvl2_btn = Button(170, 70)
        quit_btn = Button(120, 70)
        show = True

        while show:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            display.blit(menu_bckgr, (0, 0))
            
            if start_btn.draw(270, 200, 'Start game', font_size=50):
                self.game_state.change(State.START)
                return
            if lvl2_btn.draw(320, 300, 'Level 2', font_size=50):
                self.game_state.change(State.LEVEL_2)
                return
            if cont_btn.draw(300, 400, 'Continue', font_size=50):
                self.game_state.change(State.CONTINUE)
                return
            if quit_btn.draw(345, 500, 'Quit', font_size=50):
                self.game_state.change(State.QUIT)
                return

            pygame.display.update()
            clock.tick(60)

    def start_game(self):
        pygame.mixer.music.load('background.mp3')
        pygame.mixer.music.set_volume(0.3)  # 30% громкости
        pygame.mixer.music.play(-1)  # пока не проиграешь

        while self.game_cycle():
            self.scores = 0
            self.make_jump = False
            self.jump_counter = 30
            p.usr_y = p.display_height - p.usr_height - 90  # начальное значение
            self.health = 2
            self.cooldown = 0

    def choose_theme(self):
        theme1 = Button(250, 70)
        theme2 = Button(300, 70)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            display.fill((45, 64, 106))

            if theme1.draw(270, 200, 'Day theme', font_size=50):
                set_theme(1)
                return
            if theme2.draw(270, 300, 'Night theme', font_size=50):
                set_theme(2)
                return

            pygame.display.update()
            clock.tick(60)

    def choose_hero(self):
        hero1 = Button(200, 70)
        hero2 = Button(200, 70)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            display.fill((45, 64, 106))

            if hero1.draw(270, 200, '1theme', font_size=50):
                set_hero(1)
                return
            if hero2.draw(270, 300, '2theme', font_size=50):
                set_hero(2)
                return

            pygame.display.update()
            clock.tick(60)

    def choose_lv(self):
        lvl1 = Button(200, 70)
        lvl2 = Button(200, 70)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            display.fill((255, 255, 255))

            if lvl1.draw(270, 200, '1level', font_size=50):
                self.lv = 1
                return
            if lvl2.draw(270, 300, '2level', font_size=50):
                self.lv = 2
                return

            pygame.display.update()
            clock.tick(60)

    def levl_2(self):
        game = True

        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:  # пробел
                self.make_jump = True

            if self.make_jump:
                self.jump()

            display.blit(img.lvl2_bckgr, (0, 0))  # фон, координаты

            self.draw_dino()

            if keys[pygame.K_ESCAPE]:
                self.pause()

            self.show_health()

            pygame.display.update()
            clock.tick(80)  # кол-во обновлений дисплея
        return self.game_over()

    def game_cycle(self):  # функция создания игры
        game = True
        cactus_arr = []
        self.create_cactus_arr(cactus_arr)

        stone, cloud = self.open_random_objects()
        heart = Object(display_width, 280, 30, health_img, 4)

        all_bnt_bullets = []
        all_ms_bullets = []

        vrag1 = Vrag(-80)
        vrag2 = Vrag(-49)

        all_vrags = [vrag1, vrag2]

        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            keys = pygame.key.get_pressed()  # программирование клавишь
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if keys[pygame.K_SPACE]:  # пробел
                self.make_jump = True

            if self.make_jump:
                self.jump()

            self.count_scores(cactus_arr)

            display.blit(img.land, (0, 0))  # фон, координаты
            
            if keys[pygame.K_q]: #при нажатии Q открывается окошка для ввода имени и выхода в таблицу "рейтинга"
                game = False
                
            print_text('Scores: ' + str(self.scores), 600, 10)
            self.draw_array(cactus_arr)
            self.move_object(stone, cloud)

            self.draw_dino()

            if keys[pygame.K_ESCAPE]:
                self.pause()

            if not self.cooldown:
                if keys[pygame.K_x]:
                    pygame.mixer.Sound.play(bullet_sound)
                    all_bnt_bullets.append(Bullet(p.usr_x + p.usr__width, p.usr_y + 28))  # добавляет в конец нашего массива новый элемент, указанный в скобках
                    self.cooldown = 50
                elif click[0]:
                    pygame.mixer.Sound.play(bullet_sound)
                    add_bullet = Bullet(p.usr_x + p.usr__width, p.usr_y + 28)
                    add_bullet.find_path(mouse[0], mouse[1])

                    all_ms_bullets.append(add_bullet)
                    self.cooldown = 50
            else:
                print_text('Cooldown time: ' + str(self.cooldown // 10), 482, 40)
                self.cooldown -= 1

            for bullet in all_bnt_bullets:
                if not bullet.move():
                    all_bnt_bullets.remove(bullet)

            for bullet in all_ms_bullets:
                if not bullet.move_to():
                    all_ms_bullets.remove(bullet)

            heart.move()
            self.heart_plus(heart)

            if self.check_collision(cactus_arr):  # проверка столкновения
                game = False

            self.show_health()

            # vrag1.draw()
            # vrag2.draw()

            self.draw_vrag(all_vrags)
            self.chec_vrag_dmg(all_ms_bullets, all_vrags)

            pygame.display.update()
            clock.tick(80)  # кол-во обновлений дисплея
        return self.game_over()

    def game_over(self):
        if self.scores > self.max_scores:
            self.max_scores = self.scores

        stopped = True
        got_name = False
        while stopped:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
            display.blit(img.land, (0, 0))

            print_text('Game over/ Press Enter to play again, Esc to exit. ', 40, 50)  # (сообщение, координата х, координата у)
            print_text('Max scores: ' + str(self.max_scores), 300, 100)
            
            if not got_name:
                print_text("Enter your name: ", 40, 150)
                name = get_input(40, 200)
                if name:
                    got_name = True
                    print(name)
                    self.high_scores.update(name, self.scores)
            else:
                print_text('Name', 40, 150)
                print_text('Scores', 290, 150)
                self.high_scores.print(40, 200)

            keys = pygame.key.get_pressed()  # программирование клавиш
            if keys[pygame.K_RETURN]:  # enter
                return True
            if keys[pygame.K_ESCAPE]:
                self.game_state.change(State.QUIT)
                return False

            pygame.display.update()
            #clock.tick(15)

    @staticmethod
    def pause():  # функция паузы
        paused = True
        pygame.mixer.music.pause()

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            print_text('Paused. Press enter to continue ', 160, 300)  # (сообщение, координата х, координата у)

            keys = pygame.key.get_pressed()  # программирование клавишь
            if keys[pygame.K_RETURN]:  # enter
                paused = False

            pygame.display.update()
            clock.tick(15)

        pygame.mixer.music.unpause()

    def draw_dino(self):  # функция рисовки dino
        if self.img_counter == 25:
            self.img_counter = 0

        display.blit(img.dino_img[self.img_counter // 5], (p.usr_x, p.usr_y+10))
        self.img_counter += 1

    def create_cactus_arr(self, array):  # создание каактуса
        choice = random.randrange(0, 3)
        img = cactus_img[choice]
        width = self.cactus_opions[choice * 2]
        height = self.cactus_opions[choice * 2 + 1]
        array.append(Object(display_width + 20, height, width, img, 4))  # (координата х, высота, ширина 20, высота 70б скорость 4)

        choice = random.randrange(0, 3)  # выбор случайного числа
        img = cactus_img[choice]  # выбор случайной картинки
        width = self.cactus_opions[choice * 2]
        height = self.cactus_opions[choice * 2 + 1]
        array.append(Object(display_width + 20, height, width, img, 4))

        choice = random.randrange(0, 3)
        img = cactus_img[choice]
        width = self.cactus_opions[choice * 2]
        height = self.cactus_opions[choice * 2 + 1]
        array.append(Object(display_width + 20, height, width, img, 4))

    def draw_array(self, array):  # рисовка кактуса
        for cactus in array:
            check = cactus.move()
            if not check:
                self.object_return(array, cactus)

    def check_collision(self, barriers):  # функция сталкновения для каждого кактуса своя #234
        for barrier in barriers:
            if barrier.y == 449:  # little cac
                if not self.make_jump:
                    if barrier.x <= p.usr_x + p.usr__width - 35 <= barrier.x + barrier.width:  # v3let
                        if self.check_health():
                            self.object_return(barriers, barrier)
                            return False
                        else:
                            return True
                elif self.jump_counter >= 0:
                    if p.usr_y + p.usr_height - 5 >= barrier.y:  # polet
                        if barrier.x <= p.usr_x + p.usr__width - 30 <= barrier.x + barrier.width:  # nozhki
                            if self.check_health():
                                self.object_return(barriers, barrier)
                                return False
                            else:
                                return True
                else:
                    if p.usr_y + p.usr_height - 10 >= barrier.y:  # padenie
                        if barrier.x <= p.usr_x <= barrier.x + barrier.width:
                            if self.check_health():
                                self.object_return(barriers, barrier)
                                return False
                            else:
                                return True
            else:
                if not self.make_jump:
                    if barrier.x <= p.usr_x + p.usr__width - 5 <= barrier.x + barrier.width:
                        if self.check_health():
                            self.object_return(barriers, barrier)
                            return False
                        else:
                            return True
                elif self.jump_counter == 10:
                    if p.usr_y + p.usr_height - 5 >= barrier.y:
                        if barrier.x <= p.usr_x + p.usr__width - 5 <= barrier.x + barrier.width:
                            if self.check_health():
                                self.object_return(barriers, barrier)
                                return False
                            else:
                                return True
                elif self.jump_counter >= -1:
                    if p.usr_y + p.usr_height - 5 >= barrier.y:
                        if barrier.x <= p.usr_x + p.usr__width - 35 <= barrier.x + barrier.width:
                            if self.check_health():
                                self.object_return(barriers, barrier)
                                return False
                            else:
                                return True
                    else:
                        if p.usr_y + p.usr_height - 10 >= barrier.y:
                            if barrier.x <= p.usr_x + 5 <= barrier.x + barrier.width:
                                if self.check_health():
                                    self.object_return(barriers, barrier)
                                    return False
                                else:
                                    return True
        return False

    def object_return(self, objects, obj):
        radius = self.find_radius(objects)

        choice = random.randrange(0, 3)
        img = cactus_img[choice]
        width = self.cactus_opions[choice * 2]
        height = self.cactus_opions[choice * 2 + 1]

        obj.return_self(radius, height, width, img)

    @staticmethod
    def find_radius(array):  # функция
        maximum = max(array[0].x, array[1].x, array[2].x)

        if maximum < display_width:
            radius = display_width
            if radius - maximum < 50:
                radius += 280
        else:
            radius = maximum

        choice = random.randrange(0, 5)  # последнее число не включительно
        if choice == 0:
            radius += random.randrange(10, 15)
        else:
            radius += random.randrange(250, 400)

        return radius

    @staticmethod
    def open_random_objects():  # функция рисовки камень, облако
        choice = random.randrange(0, 2)
        img_of_stone = stone_img[choice]

        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]

        stone = Object(display_width, display_height - 80, 10, img_of_stone, 4)  # позиция по х, позиция по у, ширина(картинки), ..., скорость(как у кактуса)
        cloud = Object(display_width, 80, 70, img_of_cloud, 2)

        return stone, cloud

    def jump(self):  # прыжок
        if self.jump_counter >= -30:
            if self.jump_counter == 30:
                pygame.mixer.Sound.play(jump_sound)
            if self.jump_sound == -26:
                pygame.mixer.Sound.play(fall_sound)

            p.usr_y -= self.jump_counter / 2.5
            self.jump_counter -= 1
        else:
            self.jump_counter = 30
            self.make_jump = False

    @staticmethod
    def move_object(stone, cloud):  # функция камень, облако
        check = stone.move()
        if not check:
            choice = random.randrange(0, 2)
            img_of_stone = stone_img[choice]
            stone.return_self(p.display_width, 500 + random.randrange(10, 80), stone.width, img_of_stone)  # ..., случайноя высота

        check = cloud.move()
        if not check:
            choice = random.randrange(0, 2)
            img_of_cloud = cloud_img[choice]
            cloud.return_self(p.display_width, random.randrange(10, 200), cloud.width, img_of_cloud)

    @staticmethod
    def draw_vrag(vrags):
        for vrag in vrags:
            action = vrag.draw()
            if action == 1:
                vrag.show()
            elif action == 2:
                vrag.hide()
            else:
                vrag.shoot()

    @staticmethod
    def chec_vrag_dmg(bullets, vrags):
        for vrag in vrags:
            for bullet in bullets:
                vrag.chec_dmg(bullet)

    def count_scores(self, barriers):
        above_cactus = 0

        if - 20 <= self.jump_counter <= 25:
            for barrier in barriers:
                if p.usr_y + p.usr_height - 5 <= barrier.y:
                    if barrier.x <= p.usr_x <= barrier.x + barrier.width:
                        above_cactus += 1
                    elif barrier.x <= p.usr_x + p.usr__width <= barrier.x + barrier.width:
                        above_cactus += 1

            self.max_above = max(self.max_above, above_cactus)
        else:
            if self.jump_counter == -30:
                self.scores += self.max_above
                self.max_above = 0

    def check_health(self):  # проверка кол-ва жизней после прыжка
        self.health -= 1
        if self.health == 0:
            pygame.mixer.Sound.play(loss_sound)
            return False
        else:
            pygame.mixer.Sound.play(fall_sound)
            return True

    def show_health(self):  # жизни
        show = 0
        x = 20
        while show != self.health:
            display.blit(health_img, (x, 20))
            x += 40
            show += 1

    def heart_plus(self, heart):
        if heart.x <= -heart.width:
            radius = p.display_width + random.randrange(500, 1700)
            heart.return_self(radius, heart.y, heart.width, heart.image)

        if p.usr_x <= heart.x <= p.usr_x + p.usr__width:
            if p.usr_y <= heart.y <= p.usr_y + p.usr_height:
                pygame.mixer.Sound.play(heart_plus_sound)
                if self.health < 5:
                    self.health += 1

                radius = p.display_width + random.randrange(500, 1700)
                heart.return_self(radius, heart.y, heart.width, heart.image)
