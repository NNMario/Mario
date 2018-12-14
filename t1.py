import pygame
pygame.init()

w_height=300
w_length=700
win=pygame.display.set_mode((w_length,w_height))
pygame.display.set_caption("marIo")
x=0
y=100
width=16
height=16
vel=5
tru_vel=5

run = True
isjumping = False

jmp_count=2
cta=0
ctb=0
while run:

    vel=tru_vel+cta/10+ctb/10
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys_list=pygame.key.get_pressed()
    if not keys_list[pygame.K_a]:
        cta=0
    if not keys_list[pygame.K_d]:
        ctb=0
    if keys_list[pygame.K_a] and not x<0+width-1:
        x -= vel
        if cta/10<5:
            cta+=1
    if keys_list[pygame.K_d]and not x>w_length-height:
        x += vel
        if ctb/10<5:
            ctb+=1
    if not isjumping:
        # if keys_list[pygame.K_w]:
        #     y -= vel
        # if keys_list[pygame.K_s]:
        #     y += vel
        if keys_list[pygame.K_SPACE] :
            isjumping=True

    else:
        if jmp_count >= -6:
            neg=1
            if jmp_count<0:
                neg=-1

            y -= (jmp_count**2)/2*neg
            jmp_count-=1
        else:
            isjumping = False
            jmp_count = 6

    print (x,y,cta,ctb)

    pygame.draw.rect(win,(255,0,0),(x,y,width,height))
    pygame.display.update()
    win.fill((0,0,0))
pygame.quit()
