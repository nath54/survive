#coding:utf-8
import random,pygame,math,numpy,time,sys
from pygame.locals import *

pygame.init()
tex,tey=1000,800
fenetre=pygame.display.set_mode([tex,tey])
pygame.display.set_caption("MAD")
font=pygame.font.SysFont("Arial",25)
font2=pygame.font.SysFont("Arial",17)

strings=(
    "                ",
    "       X        ",
    "      X.X       ",
    "     X . X      ",
    "    X  .  X     ",
    "   X   X   X    ",
    "  X   X.X   X   ",
    " X   X . X   X  ",
    "X...X..X..X...X ",
    " X   X . X   X  ",
    "  X   X.X   X   ",
    "   X   X   X    ",
    "    X  .  X     ",
    "     X . X      ",
    "      X.X       ",
    "       X        ")

cursor,mask=pygame.cursors.compile(strings, black='X', white='.', xor='o')
cursor_sizer=((16,16),(8,8),cursor,mask)

pygame.mouse.set_cursor(*cursor_sizer)


dim="images/"

tc=100

debug=False

armes=[]
armes.append( ["pistolet",10,0.5,2.1,6,50,3,(20,20,20),3,(250,0,0),"perso1.png",52,38] )
armes.append( ["mitraillette",2,0.01,2.5,100,500,1,(20,20,20),1,(255,0,0),"perso.png",50,29] )
#0=nom 1=degats 2=vitesse attaque 3=vitesse rechargement 4=taille chargeur 5=nombre munition niv 1 6=taille missile 7=couleur missile
#8=taille explosion 9=couleur explosion 10=image 11=tx 12=ty
 
enms=[["zombie",50,50,50,[0,50],3,1.,750,60,"en1.png",1]]
#0=nom 1=vie 2=tx 3=ty 4=att 5=vit max 6=acc 7=dist reperage 8=portee 9=img

emape=[]
emape.append( ["sol1","sol1.png",True,True] )      #0
emape.append( ["sol2","sol2.png",True,True] )      #1
emape.append( ["mur1","mur1.png",False,False] )    #2
emape.append( ["fin1","fin1.png",True,True] )      #3
emape.append( ["sol3","sol3.png",True,True] )      #4
emape.append( ["sol4","sol4.png",True,True] )      #5
emape.append( ["sol5","sol5.png",True,True] )      #6
emape.append( ["mur2","mur2.png",False,False] )    #7
emape.append( ["eau1","eau1.png",False,True] )     #8
emape.append( ["eau2","eau2.png",False,True] )     #9

for em in emape:
    em[1]=pygame.transform.scale(pygame.image.load(dim+em[1]),[tc,tc])
#0=nom , 1=img , 2=pmd , 3=mpad

emaps=[ [0,2],[1,2],[4,2],[5,2],[6,2] ]
fins=[3]

def dist(p1,p2): return int(math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[0])**2))

class Missil:
    def __init__(self,x,y,t,cl,dg,vitx,vity,pos,texpl,clexpl):
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
        self.tbg=0.0001
        self.texpl=texpl
        self.clexpl=clexpl
    def update(self,perso,enemis,mape,cam):
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
                                cr=pygame.draw.circle(fenetre,self.clexpl,(int(cam[0]+self.px),int(cam[1]+self.py)),self.texpl,0)
                                pygame.display.update()
                                #if self.texpl>10: time.sleep(0.1)
                                for oo in [perso]+enemis:
                                    if oo!=o and cr.colliderect(pygame.Rect(cam[0]+oo.px,cam[1]+oo.py,oo.tx,oo.ty)):
                                        oo.vie-=self.dg
                                break
                if not self.delet:
                    for x in range(int(self.px/tc-2),int(self.px/tc+2)):
                        for y in range(int(self.py/tc-2),int(self.py/tc+2)):
                            if x >= 0 and y >= 0 and x < mape.shape[0] and y < mape.shape[1]:
                                em=emape[mape[x,y]]
                                if not self.delet and not em[3] and srect.colliderect(x*tc,y*tc,tc,tc):
                                    self.delet=True
                                    cr=pygame.draw.circle(fenetre,self.clexpl,(int(cam[0]+self.px),int(cam[1]+self.py)),self.texpl,0)
                                    pygame.display.update()
                                    for oo in [perso]+enemis:
                                        if cr.colliderect(pygame.Rect(cam[0]+oo.px,cam[1]+oo.py,oo.tx,oo.ty)):
                                            oo.vie-=self.dg
                                    break

class Perso:
    def __init__(self,niv,arm):
        arme=armes[arm]
        self.px=500
        self.py=400
        self.tx=arme[11]
        self.ty=arme[12]
        self.vie_tot=1000
        self.vie=self.vie_tot
        self.img_base=pygame.transform.scale(pygame.image.load(dim+arme[10]),[self.tx,self.ty])
        self.img=pygame.transform.scale(pygame.image.load(dim+"perso.png"),[self.tx,self.ty])
        self.agl=0
        self.vit_max=5.5
        self.vitx=0.
        self.vity=0.
        self.acc=1.4
        self.dbg=time.time()
        self.tbg=0.001
        self.agl=0
        self.dg=arme[1]
        self.tat=arme[2]
        self.tchrg=arme[3]
        self.taillechargeur=arme[4]
        self.nbmun=arme[5]*niv-self.taillechargeur
        self.texpl=arme[8]
        self.clexpl=arme[9]
        self.nbcharg=self.taillechargeur
        self.tmis=arme[6]
        self.clmis=arme[7]
        self.dat=time.time()-self.tat
        self.dchrg=time.time()-self.tchrg
        self.istirer=False
    def update(self,cam,mape,mis):  
        if time.time()-self.dbg>=self.tbg:
            pos=pygame.mouse.get_pos()
            x1,y1=cam[0]+self.px,cam[1]+self.py
            x2,y2=pos[0],pos[1]
            alpha=0
            if x2 >= x1 and y2 < y1:
                adj=y2-y1
                opp=x2-x1
                alpha=math.degrees( math.atan(opp/adj) )+90
            elif x2 > x1 and y2 >= y1:
                adj=x1-x2
                opp=y1-y2
                alpha=-math.degrees( math.atan(opp/adj) )+360
            elif x2 < x1 and y2 >= y1:
                adj=x1-x2
                opp=y2-y1
                alpha=math.degrees( math.atan(opp/adj) )+180
            elif x2 < x1 and y2 <= y1:
                adj=x1-x2
                opp=y1-y2
                alpha=-math.degrees( math.atan(opp/adj) )+180
            self.agl=alpha
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
        if self.istirer:
            if time.time()-self.dchrg>=self.tchrg and time.time()-self.dat >= self.tat and self.nbcharg>0:
                self.nbcharg-=1
                self.dat=time.time()
                pos=pygame.mouse.get_pos()
                vitx=(pos[0]-(cam[0]+self.px))/1000.*100
                vity=(pos[1]-(cam[1]+self.py))/1000.*100
                mis.append( Missil(self.px+self.tx/2.,self.py+self.ty/2.,self.tmis,self.clmis,self.dg,vitx,vity,self,self.texpl,self.clexpl) )
        return cam,mis

class Enemi:
    def __init__(self,x,y,tp):
        etp=enms[tp]
        self.nom=etp[0]
        self.px=x
        self.py=y
        self.tx=etp[2]
        self.ty=etp[3]
        self.img_base=pygame.transform.scale(pygame.image.load(dim+etp[9]),[self.tx,self.ty])
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
            dis=dist([cam[0]+perso.px+perso.tx/2,cam[1]+perso.py+perso.ty/2],[cam[0]+self.px+self.tx/2,cam[1]+self.py+self.ty/2])
            if dis <= self.distrep:
                if perso.px < self.px: self.vitx-=self.acc
                if perso.px > self.px: self.vitx+=self.acc
                if perso.py < self.py: self.vity-=self.acc
                if perso.py > self.py: self.vity+=self.acc
                x1,y1=cam[0]+self.px,cam[1]+self.py
                x2,y2=cam[0]+perso.px,cam[1]+perso.py
                alpha=0
                if x2 >= x1 and y2 < y1:
                    adj=y2-y1
                    opp=x2-x1
                    alpha=math.degrees( math.atan(opp/adj) )+90
                elif x2 > x1 and y2 >= y1:
                    adj=x1-x2
                    opp=y1-y2
                    alpha=-math.degrees( math.atan(opp/adj) )+360
                elif x2 < x1 and y2 >= y1:
                    adj=x1-x2
                    opp=y2-y1
                    alpha=math.degrees( math.atan(opp/adj) )+180
                elif x2 < x1 and y2 <= y1:
                    adj=x1-x2
                    opp=y1-y2
                    alpha=-math.degrees( math.atan(opp/adj) )+180
                self.agl=alpha
                self.img=pygame.transform.rotate(self.img_base,self.agl)
                if dis <= self.portee:
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
            srhaut=pygame.Rect(cam[0]+self.px,cam[1]+self.py,self.tx,self.ty*15/100)
            srbas=pygame.Rect(cam[0]+self.px,cam[1]+self.py+self.ty*75/100,self.tx,self.ty*15/100)
            srgauche=pygame.Rect(cam[0]+self.px,cam[1]+self.py,self.tx*15/100,self.ty)
            srdroit=pygame.Rect(cam[0]+self.px*75/100,cam[1]+self.py,self.tx*15/100,self.ty)
            for x in range(int((self.px)/tc-1),int((self.px)/tc+2)):
                for y in range(int((self.py)/tc-1),int((self.py)/tc+2)):
                    if x>=0 and y>=0 and x < mape.shape[0] and y < mape.shape[1] and not emape[mape[x,y]][2]: 
                        mrect=pygame.Rect(cam[0]+x*tc,cam[1]+y*tc,tc,tc)
                        if srect.colliderect(mrect):
                            if srhaut.colliderect(mrect): self.py-=self.vity-1
                            elif srbas.colliderect(mrect): self.py+=self.vity+1
                            if srgauche.colliderect(mrect): self.px-=self.vitx-1
                            elif srdroit.colliderect(mrect): self.px+=self.vitx+1
                            else:
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
            if self.vitx<0 and self.vitx > -2: self.vitx=0
            if self.vitx>0 and self.vitx < 2: self.vitx=0
            if self.vity<0 and self.vity > -2: self.vity=0
            if self.vity>0 and self.vity < 2: self.vity=0
        return mis
        




def create_mape(niv,arm):
    mps=[]
    tmx,tmy=random.randint(50*niv,100*niv),random.randint(50*niv,100*niv)
    im=random.choice(emaps)
    isol=im[0]
    imur=im[1]
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
    perso=Perso(niv,arm)
    perso.px=dex*tc+tc/2
    perso.py=dey*tc+tc/2
    return mape,perso,[deb[0],deb[1]],mps
        
def deb_level(niv,arm):
    enemis=[]
    mape,perso,cfin,mps=create_mape(niv,arm)
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

def ecran_gagne(niv,points):
    fenetre.fill((75,90,20))
    fenetre.blit(font.render("Vous avez terminé le niveau "+str(niv),20,(255,255,255)),[250,300])
    fenetre.blit(font.render("Vous avez "+str(points)+" points",20,(255,255,255)),[250,350])
    fenetre.blit(font.render("Appuyez sur 'ESPACE' pour continuer",20,(255,255,255)),[250,400])
    pygame.display.update()
    encor=True
    while encor:
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN and event.key in [K_SPACE,K_ESCAPE]: encor=False

def ecran_perdu(niv,points):
    fenetre.fill((75,90,20))
    fenetre.blit(font.render("Vous êtes mort. Vous étiez au niveau "+str(niv),20,(255,0,0)),[250,300])
    fenetre.blit(font.render("Vous avez "+str(points)+" points",20,(255,255,255)),[250,350])
    fenetre.blit(font.render("Appuyez sur 'ESPACE' pour continuer",20,(255,0,0)),[250,400])
    pygame.display.update()
    encor=True
    while encor:
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN and event.key in [K_SPACE,K_ESCAPE]: encor=False


def aff_jeu(perso,enemis,cam,mape,mis,fps,points):
    fenetre.fill((0,0,0))
    for x in range(int((-cam[0])/tc),int((-cam[0]+tex)/tc+1)):
        for y in range(int((-cam[1])/tc),int((-cam[1]+tey)/tc+1)):
            if x>=0 and x < mape.shape[0] and y >= 0 and y < mape.shape[1]:
                fenetre.blit(emape[mape[x,y]][1],[cam[0]+x*tc,cam[1]+y*tc])
    for e in enemis:
        if True or e.px+cam[0]-e.tx > 0 and e.px+cam[0] < tex and e.py+cam[1]-e.ty > 0 and e.py+cam[1] < tey:
            fenetre.blit(e.img,[cam[0]+e.px,cam[1]+e.py])
            if e.vie>=0:
                pygame.draw.rect(fenetre,(150,0,0),(cam[0]+e.px,cam[1]+e.py-15,int(float(e.vie)/float(e.vie_tot)*float(e.tx)),8),0)
                pygame.draw.rect(fenetre,(0,0,0),(cam[0]+e.px,cam[1]+e.py-15,e.tx,7),1)
            if debug : pygame.draw.line(fenetre,(250,0,0),(cam[0]+perso.px,cam[1]+perso.py),(cam[0]+e.px,cam[1]+e.py),1)
    for m in mis:
        if m.px+cam[0]-m.t > 0 and m.px+cam[0] < tex and m.py+cam[1]-m.t > 0 and m.py+cam[1] < tey:
            pygame.draw.circle(fenetre,m.cl,(int(cam[0]+m.px),int(cam[1]+m.py)),m.t,0)
    fenetre.blit(perso.img,[cam[0]+perso.px,cam[1]+perso.py])
    if perso.vie>=0:
        pygame.draw.rect(fenetre,(250,0,0),(50,50,int(float(perso.vie)/float(perso.vie_tot)*float(200)),25),0)
        pygame.draw.rect(fenetre,(0,0,0),(50,50,200,25),2)
    fenetre.blit(font2.render("score : "+str(points),20,(255,255,255)),[tex-200,10])
    fenetre.blit(font2.render("munitions : "+str(perso.nbcharg)+"/"+str(perso.nbmun),20,(255,255,255)),[tex-200,40])
    if time.time()-perso.dchrg<=perso.tchrg:
        pygame.draw.rect(fenetre,(0,0,120),(tex-200,65,int((time.time()-perso.dchrg)/perso.tchrg*100),5),0)
        pygame.draw.rect(fenetre,(0,0,0),(tex-200,65,100,5),1)
    if time.time()-perso.dat<=perso.tat:
        pygame.draw.rect(fenetre,(200,0,0),(tex-200,75,int((time.time()-perso.dat)/perso.tat*100),5),0)
        pygame.draw.rect(fenetre,(0,0,0),(tex-200,75,100,5),1)
    if perso.nbcharg==0 and perso.nbmun>0: fenetre.blit( font.render("click droit pour recharger",20,(255,50,50)),[tex/2,50])
    fenetre.blit(font2.render("nb enemis restants: "+str(len(enemis)),20,(255,255,255)),[tex-200,80])
    pos=pygame.mouse.get_pos()
    pygame.draw.line(fenetre,(0,0,100),(cam[0]+perso.px+int(float(perso.tx)/2.),cam[1]+perso.py+int(float(perso.ty)/2.)),(pos[0]+(pos[0]-(cam[0]+perso.px))*10,pos[1]+(pos[1]-(cam[1]+perso.py))*10),1)
    fenetre.blit(font2.render("fps : "+str(int(fps)),20,(255,255,255)),[15,15])
    pygame.display.update()

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
    
def main_jeu(arm):
    niv=1
    enemis,mape,perso,cfin,cam,mis,gagne=deb_level(niv,arm)
    encour=True
    fps=0
    points=0
    while encour:
        t1=time.time()
        aff_jeu(perso,enemis,cam,mape,mis,fps,points)
        for m in mis:
            m.update(perso,enemis,mape,cam)
            if m.delet:
                if m in mis: del(mis[mis.index(m)])
        cam,mis=perso.update(cam,mape,mis)
        for e in enemis:
            mis=e.update(mape,perso,mis,cam)
            if e.vie<=0:
                points+=10
                if e in enemis: del(enemis[enemis.index(e)])
        perso,cam=verif_keys(perso,cam)
        cam=[-perso.px+tex/2,-perso.py+tey/2]
        if pygame.Rect(perso.px,perso.py,perso.tx,perso.ty).colliderect(pygame.Rect(cfin[0]*tc,cfin[1]*tc,tc,tc)):
            enemis,mape,perso,cfin,cam,mis,gagne=deb_level(niv,arm)
            points+=100
            ecran_gagne(niv,points)
            niv+=1
        if perso.vie<=0:
            encour=False
            ecran_perdu(niv,points)
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN and event.key==K_ESCAPE: encour=False
            elif event.type==MOUSEBUTTONDOWN:
                if event.button==1: perso.istirer=True
                elif event.button==3:
                    if time.time()-perso.dchrg >= perso.tchrg and perso.nbmun>0:
                        if perso.nbmun<perso.taillechargeur:
                            perso.nbcharg=perso.nbmun
                            perso.nbmun=0
                        else:
                            perso.nbcharg=perso.taillechargeur
                            perso.nbmun-=perso.taillechargeur
                        perso.dchrg=time.time()
            elif event.type==MOUSEBUTTONUP:
                if event.button==1: perso.istirer=False
        t2=time.time()
        tt=(t2-t1)
        if tt!=0: fps=1.0/tt
                        
###########################################################################################

imb1=pygame.image.load(dim+"button1.png")
imb2=pygame.image.load(dim+"button2.png")
imb3=pygame.image.load(dim+"button3.png")

def aff_menu(men,btsel,arm):
    fenetre.fill((0,0,0))
    bst=[]
    for x in range(20): bst.append(None)
    #button 1
    if men==0: ib=imb3
    elif btsel==0: ib=imb2
    else: ib=imb1
    fenetre.blit( ib , [50,50] )
    fenetre.blit( font.render("jouer",20,(100,150,35)) , [80,70] )
    #button 2
    if men==1: ib=imb3
    elif btsel==1: ib=imb2
    else: ib=imb1
    fenetre.blit( ib , [50,200] )
    fenetre.blit( font.render("personnage",20,(100,150,35)) , [80,220] )
    #button 3
    if men==2: ib=imb3
    elif btsel==2: ib=imb2
    else: ib=imb1
    fenetre.blit( ib , [50,350] )
    fenetre.blit( font.render("stats",20,(100,150,35)) , [80,370] )
    #button 4
    if men==3: ib=imb3
    elif btsel==3: ib=imb2
    else: ib=imb1
    fenetre.blit( ib , [50,500] )
    fenetre.blit( font.render("parametres",20,(100,150,35)) , [80,520] )
    #button 5
    if men==4: ib=imb3
    elif btsel==4: ib=imb2
    else: ib=imb1
    fenetre.blit( ib , [50,650] )
    fenetre.blit( font.render("quitter",20,(100,150,35)) , [80,670] )
    if men==1:
        if arm==0: ib=imb3
        else: ib=imb1
        bst[0]=fenetre.blit( ib , [740,10] )
        fenetre.blit( font.render("pistolet",20,(100,150,35)) , [770,30] )
        if arm==1: ib=imb3
        else: ib=imb1
        bst[1]=fenetre.blit( ib , [740,120] )
        fenetre.blit( font.render("mitraillette",20,(100,150,35)) , [770,140] )
        fenetre.blit( pygame.image.load(dim+armes[arm][10]) , [400,400] )
    pygame.display.update()
    return bst

def main_menu():
    btsel=0
    men=None
    bts=[pygame.Rect(50,50,200,100),pygame.Rect(50,200,200,100),pygame.Rect(50,350,200,100),pygame.Rect(50,500,200,100),pygame.Rect(50,650,200,100)]
    #0=jouer 1=personnage 2=stats 3=parametres 4=credits 5=quitter
    arm=0
    encoure=True
    while encoure:
        pos=pygame.mouse.get_pos()
        btsel=None
        for b in bts:
            if b.collidepoint(pos): btsel=bts.index(b)
        bst=aff_menu(men,btsel,arm)
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE: encoure=False
            elif event.type==MOUSEBUTTONUP:
                for b in bts:
                    if b.collidepoint(pos): men=bts.index(b)
                if men==0:
                    try:
                        main_jeu(arm)
                    except Exception as error:
                        print("error : ",error)
                for bb in bst:
                    if bb!=None and bb.collidepoint(pos):
                        i=bst.index(bb)
                        if i==0: arm=0
                        elif i==1: arm=1
                
                








main_menu()











