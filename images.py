import pygame

pygame.init()

icon = pygame.image.load('fon/icon.png')
menu_bckgr = pygame.image.load('fon/Menu.jpg')

land = pygame.image.load('fon/Land.jpg')

cactus_img = [pygame.image.load('ob/Cactus0.png'), pygame.image.load('ob/Cactus1.png'),
              pygame.image.load('ob/Cactus2.png')]

stone_img = [pygame.image.load('ob/Stone0.png'), pygame.image.load('ob/Stone1.png')]
cloud_img = [pygame.image.load('ob/Cloud0.png'), pygame.image.load('ob/Cloud1.png')]
cloud_img[0] = pygame.transform.scale(cloud_img[0], (93, 51))
cloud_img[1] = pygame.transform.scale(cloud_img[1], (93, 51))

dino_img = [pygame.image.load('dind/Dino0.png'), pygame.image.load('dind/Dino1.png'),
            pygame.image.load('dind/Dino2.png'), pygame.image.load('dind/Dino3.png'),
            pygame.image.load('dind/Dino4.png')]

vrag_img = [pygame.image.load('vrag/Bird0.png'), pygame.image.load('vrag/Bird1.png'),
            pygame.image.load('vrag/Bird2.png'), pygame.image.load('vrag/Bird3.png')]

health_img = pygame.image.load('efect/heart.png')
health_img = pygame.transform.scale(health_img, (30, 30))

bullet_img = pygame.image.load('efect/shot.png')
bullet_img = pygame.transform.scale(bullet_img, (30, 9))

light_img = [pygame.image.load('efect/Light0.png'), pygame.image.load('efect/Light1.png'),
             pygame.image.load('efect/Light2.png'), pygame.image.load('efect/Light3.png'),
             pygame.image.load('efect/Light4.png'), pygame.image.load('efect/Light5.png'),
             pygame.image.load('efect/Light6.png'), pygame.image.load('efect/Light7.png'),
             pygame.image.load('efect/Light8.png'), pygame.image.load('efect/Light9.png'),
             pygame.image.load('efect/Light10.png')]