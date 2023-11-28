import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトの画面内外を判定し、真理値タプルを返す関数
    引数rct：こうかとんor爆弾SurfaseのRect
    戻り値：横方向、縦方向はみ出し判定結果
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = [900, 400]
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5
    accs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    i = 0

    kk_roto = {
        (0, -5): pg.transform.rotozoom(kk_img, -90, 1.0),
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 1.0),
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 1.0),
        (0, +5): pg.transform.rotozoom(kk_img, 90, 1.0),
        (+5, +5): pg.transform.rotozoom(kk_img, 45, 1.0),
        (+5, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
        (+5, -5): pg.transform.rotozoom(kk_img, -45, 1.0)
    }

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rct.colliderect(bb_rct):
            print("Game Over!")
            return
        
        if (tmr%100 == 0):
            if i < 10:
                i += 1
            
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
            if (tuple(sum_mv) in kk_roto):
                kk_img = kk_roto[tuple(sum_mv)]
            if sum_mv[0] > 0:
                kk_img = pg.transform.flip(kk_img, True, False)

        for k, muki in kk_roto.items():
            if sum_mv == k:
                kk_img = muki

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx*accs[i], vy*accs[i])
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()