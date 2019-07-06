#coding:utf-8
import random,pygame,math,numpy,time
from pygame.locals import *

pygame.init()
tex,tey=1000,800
fenetre=pygame.display.set_mode([tex,tey])
pygame.display.set_caption("MAD")
font=pygame.font.SysFont("Arial",25)
font2=pygame.font.SysFont("Arial",17)

dim="images/"

tc=100

debug=False

enms=[["zombie",50,50,50,[0,50],3,1.,750,60,"en1.png",1]]
#0=nom 1=vie 2=tx 3=ty 4=att 5=vit max 6=acc 7=dist reperage 8=portee 9=img

emape=[["sol1 herbe","sol1.png",True],["sol2 gravier","sol2.png",True],["mur1 briques","mur1.png",False],["fin1 herbe","fin1.png",True]]
for em in emape:
    em[1]=pygame.transform.scale(pygame.image.load(dim+em[1]),[tc,tc])
#0=nom , 1=img , 2=pmd

sols=[0,1]
murs=[2]
fins=[3]

class Missil:
    def __init__(self,x,y,t,cl,dg,vitx,vity,pos):
        self.px=x
        self.py=y
        self.t=t
        self.cl=cl
        self.dg=dg
        self.vitx=vitx
        self.vity=vity
        self.pos=pos
        self.delet=False
        self.dbg=time.time()
        self.tbg=0.01
    def update(self,perso,enemis,mape):
        if time.time()-self.dbg >= self.tbg:
            self.dbg=time.time()
            if not self.delet:
                self.px+=self.vitx
                self.py+=self.vity
                srect=pygame.Rect(self.px-self.t/2,self.py-self.t/2,self.t,self.t)
                if self.px <= 0: self.delet=True
                if self.py <= 0: self.delet=True
                if self.px >= mape.shape[0]*tc: self.delet=True
                if self.py >= mape.shape[1]*tc: self.delet=True
                if not self.delet:
                    for o in [perso]+enemis:
                        if self.pos!=o:
                            if srect.colliderect(pygame.Rect(o.px,o.py,o.tx,o.ty)):
                                o.vie-=self.dg
                                self.delet=True
                                break
                if not self.delet:
                    for x in range(int(self.px/tc-2),int(self.px/tc+2)):
                        for y in range(int(self.py/tc-2),int(self.py/tc+2)):
                            if x >= 0 and y >= 0 and x < mape.shape[0] and y < mape.shape[1]:
                                em=emape[mape[x,y]]
                                if not self.delet and not em[2] and srect.colliderect(x*tc,y*tc,tc,tc):
                                    self.delet=True
                                    break

class Perso:
    def __init__(self,niv):
        self.px=500
        self.py=400
        self.tx=50
        self.ty=50
        self.vie_tot=1000
        self.vie=self.vie_tot
        self.img_base=pygame.transform.scale(pygame.image.load(dim+"perso.png"),[self.tx,self.ty])
        self.img=pygame.transform.scale(pygame.image.load(dim+"perso.png"),[self.tx,self.ty])
        self.agl=0
        self.vit_max=5.5
        self.vitx=0.
        self.vity=0.
        self.acc=1.4
        self.dg=10
        self.dbg=time.time()
        self.tbg=0.001
        self.agl=0
        self.dat=time.time()
        self.tat=0.1
        self.nbmun=50*niv
        self.nbcharg=10
        self.dchrg=time.time()
        self.tchrg=1
        self.taillechargeur=6
    def update(self,cam,mape):  
        if time.time()-self.dbg>=self.tbg:
            pos=pygame.mouse.get_pos()
            opp=cam[0]+self.px-pos[0]
            adj=cam[1]+self.py-pos[1]
            hyp=math.sqrt((self.px-pos[0])**2+(self.py-pos[1])**2)
            if hyp!=0:
                self.agl1=math.acos(adj/hyp)
                self.agl2=math.asin(opp/hyp)
            if adj!=0:
                self.agl3=math.tan(opp/adj)
            self.agl=math.degrees(self.agl3)
            self.img=pygame.transform.rotate(self.img_base,self.agl)
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
                            #self.vitx,self.vity=0,0
                            bc=False
            if debug: pygame.display.update()
            if self.px<0: self.px,self.vitx,self.vity=1,0,0
            if self.px+self.tx>mape.shape[0]*tc: self.px,self.vitx,self.vity=mape.shape[0]*tc-self.tx-1,0,0
            if self.py<0: self.py,self.vitx,self.vity=1,0,0
            if self.py+self.ty>mape.shape[1]*tc: self.py,self.vitx,self.vity=mape.shape[1]*tc-self.ty-1,0,0
            if bc:
                cam[0]-=self.vitx
                cam[1]-=self.vity
            if self.vitx < 0: self.vitx+=0.5
            if self.vitx > 0: self.vitx-=0.5
            if self.vity < 0: self.vity+=0.5
            if self.vity > 0: self.vity-=0.5
        return cam

class Enemi:
    def __init__(self,x,y,tp):
        etp=enms[tp]
        self.nom=etp[0]
        self.px=x
        self.py=y
        self.tx=etp[2]
        self.ty=etp[3]
        self.img=pygame.transform.scale(pygame.image.load(dim+etp[9]),[self.tx,self.ty])
        self.vie_tot=etp[1]
        self.vie=self.vie_tot
        self.vitx=0.
        self.vity=0.
        self.att=etp[4]
        self.dbg=time.time()
        self.tbg=0.01
        self.vitmax=etp[5]
        self.acc=etp[6]
        self.distrep=etp[7]
        self.portee=etp[8]
        self.dat=time.time()
        self.tat=etp[10]
    def update(self,mape,perso,mis,cam):
        if time.time()-self.dbg>=self.tbg:
            self.dbg=time.time()
            dist=math.sqrt((self.px-perso.px)**2+(self.py-perso.py)**2)
            if dist <= self.distrep:
                if self.px+self.tx/2 < perso.px+perso.tx: self.vitx+=self.acc
                if self.px+self.tx/2 > perso.px+perso.tx: self.vitx-=self.acc
                if self.py+self.ty/2 < perso.py+perso.ty: self.vity+=self.acc
                if self.py+self.ty/2 > perso.py+perso.ty: self.vity-=self.acc
                if dist <= self.portee:
                    if self.att[0]==0:
                        if time.time()-self.dat >= self.tat:
                            self.dat=time.time()
                            perso.vie-=self.att[1]
                    else: pass
            else:
                self.vitx+=random.choice([-self.acc,self.acc])
                self.vity+=random.choice([-self.acc,self.acc])
            if self.vitx < -self.vitmax: self.vitx=-self.vitmax
            if self.vitx > self.vitmax: self.vitx=self.vitmax
            if self.vity < -self.vitmax: self.vity=-self.vitmax
            if self.vity > self.vitmax: self.vity=self.vitmax
            self.px+=self.vitx
            self.py+=self.vity
            srect=pygame.Rect(cam[0]+self.px,cam[1]+self.py,self.tx,self.ty)
            for x in range(int((self.px)/tc-1),int((self.px)/tc+2)):
                for y in range(int((self.py)/tc-1),int((self.py)/tc+2)):
                    if x>=0 and y>=0 and x < mape.shape[0] and y < mape.shape[1] and not emape[mape[x,y]][2]: 
                        mrect=pygame.Rect(cam[0]+x*tc,cam[1]+y*tc,tc,tc)
                        if srect.colliderect(mrect):
                            self.px-=self.vitx
                            self.py-=self.vity
                            #self.vitx,self.vity=0,0
            if self.px<0: self.px=1
            if self.py<0: self.py=1
            if self.px+self.tx>mape.shape[0]*tc: self.px=mape.shape[0]*tc-self.tx-1
            if self.py+self.ty>mape.shape[1]*tc: self.py=mape.shape[1]*tc-self.ty-1
            if self.vitx<0: self.vitx+=0.1
            if self.vitx>0: self.vitx-=0.1
            if self.vity<0: self.vity+=0.1
            if self.vity>0: self.vity-=0.1
        return mis
        


def aff_jeu(perso,enemis,cam,mape,mis,fps):
    fenetre.fill((0,0,0))
    for x in range(int((-cam[0])/tc),int((-cam[0]+tex)/tc+1)):
        for y in range(int((-cam[1])/tc),int((-cam[1]+tey)/tc+1)):
            if x>=0 and x < mape.shape[0] and y >= 0 and y < mape.shape[1]:
                fenetre.blit(emape[mape[x,y]][1],[cam[0]+x*tc,cam[1]+y*tc])
    for e in enemis:
        if True or e.px+cam[0]-e.tx > 0 and e.px+cam[0] < tex and e.py+cam[1]-e.ty > 0 and e.py+cam[1] < tey:
            fenetre.blit(e.img,[cam[0]+e.px,cam[1]+e.py])
            pygame.draw.rect(fenetre,(150,0,0),(cam[0]+e.px,cam[1]+e.py-15,int(float(e.vie)/float(e.vie_tot)*float(e.tx)),8),0)
            pygame.draw.rect(fenetre,(0,0,0),(cam[0]+e.px,cam[1]+e.py-15,e.tx,7),1)
            if debug : pygame.draw.line(fenetre,(250,0,0),(cam[0]+perso.px,cam[1]+perso.py),(cam[0]+e.px,cam[1]+e.py),1)
    for m in mis:
        if m.px+cam[0]-m.t > 0 and m.px+cam[0] < tex and m.py+cam[1]-m.t > 0 and m.py+cam[1] < tey:
            pygame.draw.circle(fenetre,m.cl,(int(cam[0]+m.px),int(cam[1]+m.py)),m.t,0)
    fenetre.blit(perso.img,[cam[0]+perso.px,cam[1]+perso.py])
    pygame.draw.rect(fenetre,(250,0,0),(50,50,int(float(perso.vie)/float(perso.vie_tot)*float(200)),25),0)
    pygame.draw.rect(fenetre,(0,0,0),(50,50,200,25),2)
    pos=pygame.mouse.get_pos()
    pygame.draw.line(fenetre,(0,0,100),(cam[0]+perso.px+int(float(perso.tx)/2.),cam[1]+perso.py+int(float(perso.ty)/2.)),(pos[0]+(pos[0]-(cam[0]+perso.px))*10,pos[1]+(pos[1]-(cam[1]+perso.py))*10),1)
    fenetre.blit(font2.render("fps : "+str(int(fps)),20,(255,255,255)),[15,15])
    pygame.display.update()


def create_mape(niv):
    mps=[]
    tmx,tmy=random.randint(50*niv,100*niv),random.randint(50*niv,100*niv)
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
    for z in range(random.randint(50*niv,1000*niv)):
        mps.append( copy.deepcopy(deb) )
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
    return mape,perso,[deb[0],deb[1]],mps
        



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
    mape,perso,cfin,mps=create_mape(niv)
    cam=[-perso.px+tex/2,-perso.py+tey/2]
    mis=[]
    nbenms=random.randint(2*niv,5*niv)
    ne=niv
    if niv >= len(enms):
        while ne > len(enms)-1: ne-=1
    for x in range(nbenms):
        mm=random.choice( mps )
        enemis.append( Enemi(mm[0]*tc+20,mm[1]*tc+20,ne) )
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
    fps=0
    while encour:
        t1=time.time()
        aff_jeu(perso,enemis,cam,mape,mis,fps)
        cam=perso.update(cam,mape)
        for e in enemis:
            mis=e.update(mape,perso,mis,cam)
            if e.vie<=0:
                if e in enemis: del(enemis[enemis.index(e)])
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
                if event.button==1:
                    if time.time()-perso.dchrg>=perso.tchrg and time.time()-perso.dat >= perso.tat and perso.nbcharg>0:
                        perso.nbmun-=1
                        perso.dat=time.time()
                        pos=pygame.mouse.get_pos()
                        vitx=(pos[0]-(cam[0]+perso.px))/1000.*100
                        vity=(pos[1]-(cam[1]+perso.py))/1000.*100
                        mis.append( Missil(perso.px+perso.tx/2.,perso.py+perso.ty/2.,3,(20,20,20),perso.dg,vitx,vity,perso) )
                elif event.button==2:
                    if perso.nbmun>0:
                        if perso.nbmun<perso.taillechargeur:
                            perso.nbcharg=perso.nbmun
                        else:
                            perso.nbcharg=perso.taillechargeur
                            perso.nbmun-=perso.taillechargeur
                        perso.dchrg=time.time()
        t2=time.time()
        tt=(t2-t1)
        if tt!=0: fps=1.0/tt
                        

main_jeu()










