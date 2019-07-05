#coding:utf-8
import random,pygame,math,numpy,time
from pygame.locals import *

pygame.init()
tex,tey=1000,800
fenetre=pygame.display.set_mode([tex,tey])
pygame.display.set_caption("MAD")
font=pygame.font.SysFont("Arial",25)

dim="images/"

tc=100

debug=True

emape=[["sol1 herbe","sol1.png",True],["sol2 gravier","sol2.png",True],["mur1 briques","mur1.png",False],["fin1 herbe","fin1.png",True]]
for em in emape:
    em[1]=pygame.transform.scale(pygame.image.load(dim+em[1]),[tc,tc])
#0=nom , 1=img , 2=pmd

sols=[0,1]
murs=[2]
fins=[3]

class Missil:
    def __init__(self,x,y,tx,ty,agl,dg,vitx,vity,pos):
        self.px=x
        self.py=y
        self.tx=x
        self.ty=y
        self.agl=agl
        self.dg=dg
        self.vitx=vitx
        self.vity=vity
        self.img=pygame.transform.rotate(pygame.image.load(dim+"mis.png"),self.agl)
        self.pos=pos
        self.delet=False
    def update(self,perso,enemis,mape):
        if not self.delet:
            self.px+=self.vitx
            self.py+=self.vity
            srect=pygame.Rect(self.px,self.py,self.tx,self.ty)
            for o in [perso]+enemis:
                if self.pos!=o:
                    if srect.colliderect(pygame.Rect(o.px,o.py,o.tx,o.ty)):
                        o.vie-=s.dg
                        self.delet=True
                        break
            for x in range(mape.shape[0]):
                for y in range(mape.shape[1]):
                    em=emape[mape[x,y]]
                    if not self.delet and not em[2] and srect.colliderect(x*tc,y*tc,tc,tc):
                        self.delet=True
                        break
                

class Perso:
    def __init__(self):
        self.px=500
        self.py=400
        self.tx=50
        self.ty=50
        self.vie_tot=1000
        self.vie=self.vie_tot
        self.img_base=pygame.transform.scale(pygame.image.load(dim+"perso.png"),[self.tx,self.ty])
        self.img=pygame.transform.scale(pygame.image.load(dim+"perso.png"),[self.tx,self.ty])
        self.agl=0
        self.vit_max=5
        self.vitx=0
        self.vity=0
        self.acc=5
        self.dg=10
        self.dbg=time.time()
        self.tbg=0.01
        self.agl=0
    def update(self,cam,mape):  
        if time.time()-self.dbg>=self.tbg:
            pos=pygame.mouse.get_pos()
            opp=self.px-pos[0]
            adj=self.py-pos[1]
            if adj!=0: self.agl=math.atan(opp/adj)
            else: agl=0
            self.img=pygame.transform.rotate(self.img_base,90+math.degrees(self.agl))
            self.dbg=time.time()
            self.px+=self.vitx
            self.py+=self.vity
            bc=True
            srect=pygame.draw.rect(fenetre,(50,50,0),(cam[0]+self.px,cam[1]+self.py,self.tx,self.ty),2)
            for x in range(int((self.px)/tc-1),int((self.px)/tc+2)):
                for y in range(int((self.py)/tc-1),int((self.py)/tc+2)):
                    if x>=0 and y>=0 and x < mape.shape[0] and y < mape.shape[1] and not emape[mape[x,y]][2]: 
                        mrect=pygame.draw.rect(fenetre,(0,0,0),(cam[0]+x*tc,cam[1]+y*tc,tc,tc),2)
                        if srect.colliderect(mrect):
                            bc=True
                            self.px-=self.vitx
                            self.py-=self.vity
                            self.vitx,self.vity=0,0
                            bc=False
            if debug: pygame.display.update()
            if self.px<0: self.px,self.vitx,self.vity=1,0,0
            if self.px>mape.shape[0]*tc: self.px,self.vitx,self.vity=mape.shape[0]*tc-1,0,0
            if self.py<0: self.py,self.vitx,self.vity=1,0,0
            if self.py>mape.shape[1]*tc: self.py,self.vitx,self.vity=mape.shape[1]*tc-1,0,0
            if bc:
                cam[0]-=self.vitx
                cam[1]-=self.vity
            if self.vitx < 0: self.vitx+=1
            if self.vitx > 0: self.vitx-=1
            if self.vity < 0: self.vity+=1
            if self.vity > 0: self.vity-=1
        return cam


def aff_jeu(perso,enemis,cam,mape,mis):
    fenetre.fill((0,0,0))
    for x in range(int((-cam[0])/tc),int((-cam[0]+tex)/tc+1)):
        for y in range(int((-cam[1])/tc),int((-cam[1]+tey)/tc+1)):
            if x>=0 and x < mape.shape[0] and y >= 0 and y < mape.shape[1]:
                fenetre.blit(emape[mape[x,y]][1],[cam[0]+x*tc,cam[1]+y*tc])
    for e in enemis:
        if e.px+cam[0]-e.tx > 0 and e.px+cam[0] < tex and e.py+cam[1]-e.ty > 0 and e.py+cam[1] < tey:
            fenetre.blit(e.img,[cam[0]+e.px,cam[1]+e.py])
            pygame.draw.rect(fenetre,(0,200,0),(cam[0]+e.px,cam[1]+e.py-20,int(float(e.vie)/float(e.vie_tot)*float(e.tx)),15),0)
            pygame.draw.rect(fenetre,(0,0,0),(cam[0]+e.px,cam[1]+e.py-20,e.tx,15),1)
    for m in mis:
        if m.px+cam[0]-m.tx > 0 and m.px+cam[0] < tex and m.py+cam[1]-m.ty > 0 and m.py+cam[1] < tey:
            fenetre.blit(m.img,[cam[0]+m.px,cam[1]+m.py])
    fenetre.blit(perso.img,[cam[0]+perso.px,cam[1]+perso.py])
    if debug: pygame.draw.arc(fenetre,(200,200,0),(cam[0]+perso.px,cam[1]+perso.py,perso.tx,perso.ty), 0, math.degrees(perso.agl), 1)
    pygame.draw.rect(fenetre,(250,0,0),(50,50,int(float(perso.vie)/float(perso.vie_tot)*float(200)),25),0)
    pygame.draw.rect(fenetre,(0,0,0),(50,50,200,25),2)
    pos=pygame.mouse.get_pos()
    pygame.draw.line(fenetre,(0,0,50),(cam[0]+perso.px+perso.tx/2,cam[1]+perso.py+perso.ty/2),pos,2)
    pygame.display.update()


def create_mape():
    tmx,tmy=random.randint(50,100),random.randint(50,100)
    isol=random.choice(sols)
    imur=random.choice(murs)
    ifin=random.choice(fins)
    import copy
    mape=numpy.zeros([tmx,tmy],dtype=int)
    for x in range(tmx):
        for y in range(tmy):
            mape[x,y]=imur
    dex,dey=random.randint(1,tmx-1),random.randint(1,tmy-1)
    deb=[copy.deepcopy(dex),copy.deepcopy(dey)]
    for z in range(random.randint(50,1000)):
        mape[deb[0],deb[1]]=isol
        if random.choice([True,False]): deb[0]+=random.randint(-1,1)
        else: deb[1]+=random.randint(-1,1)
        if deb[0]<0: deb[0]=0
        if deb[0]>tmx-1: deb[0]=tmx-1
        if deb[1]<0: deb[1]=0
        if deb[1]>tmy-1: deb[1]=tmy-1
    mape[deb[0],deb[1]]=ifin
    perso=Perso()
    perso.px=dex*tc+tc/2
    perso.py=dey*tc+tc/2
    return mape,perso,[deb[0],deb[1]]
        



def verif_keys(perso,cam):
    keys=pygame.key.get_pressed()
    if keys[K_UP]:
        perso.vity-=perso.acc
        if perso.vity<-perso.vit_max: perso.vity=-perso.vit_max
    if keys[K_DOWN]:
        perso.vity+=perso.acc
        if perso.vity>perso.vit_max: perso.vity=perso.vit_max
    if keys[K_LEFT]:
        perso.vitx-=perso.acc
        if perso.vitx<-perso.vit_max: perso.vitx=-perso.vit_max
    if keys[K_RIGHT]:
        perso.vitx+=perso.acc
        if perso.vitx>perso.vit_max: perso.vitx=perso.vit_max
    if keys[K_KP8]: cam[1]-=30
    if keys[K_KP2]: cam[1]+=30
    if keys[K_KP4]: cam[0]-=30
    if keys[K_KP6]: cam[0]+=30
    return perso,cam

def deb_level(niv):
    enemis=[]
    mape,perso,cfin=create_mape()
    cam=[-perso.px+tex/2,-perso.py+tey/2]
    mis=[]
    gagne=False
    return enemis,mape,perso,cfin,cam,mis,gagne

def ecran_gagne(niv):
    fenetre.fill((75,90,20))
    fenetre.blit(font.render("Vous avez terminé le niveau "+str(niv),20,(255,255,255)),[250,300])
    fenetre.blit(font.render("Appuyez sur 'ESPACE' pour continuer",20,(255,255,255)),[250,350])
    pygame.display.update()
    encor=True
    while encor:
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN and event.key in [K_SPACE,K_ESCAPE]: encor=False

def ecran_perdu(niv):
    fenetre.fill((75,90,20))
    fenetre.blit(font.render("Vous êtes mort. Vous étiez au niveau "+str(niv),20,(255,0,0)),[250,300])
    fenetre.blit(font.render("Appuyez sur 'ESPACE' pour continuer",20,(255,0,0)),[250,350])
    pygame.display.update()
    encor=True
    while encor:
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN and event.key in [K_SPACE,K_ESCAPE]: encor=False

def main_jeu():
    niv=1
    enemis,mape,perso,cfin,cam,mis,gagne=deb_level(niv)
    encour=True
    while encour:
        aff_jeu(perso,enemis,cam,mape,mis)
        cam=perso.update(cam,mape)
        for e in enemis: e.update()
        for m in mis:
            m.update(perso,enemis,mape)
            if m.delet:
                if m in mis: del(mis[mis.index(m)])
        perso,cam=verif_keys(perso,cam)
        if pygame.Rect(perso.px,perso.py,perso.tx,perso.ty).colliderect(pygame.Rect(cfin[0]*tc,cfin[1]*tc,tc,tc)):
            enemis,mape,perso,cfin,cam,mis,gagne=deb_level(niv)
            ecran_gagne(niv)
            niv+=1
        if perso.vie<=0:
            encour=False
            ecran_perdu(niv)
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN and event.key==K_ESCAPE: encour=False
            elif event.type==MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                alpha=math.degrees(perso.agl)
                vitx=math.sin(alpha)*10.
                vity=math.cos(alpha)*10.
                mis.append( Missil(perso.px+perso.tx/2,perso.py+perso.ty/2,5,2,alpha,perso.dg,vitx,vity,perso) )


main_jeu()









