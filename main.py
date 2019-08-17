#coding:utf-8
#!/bin/python3
import random,pygame,math,numpy,time,sys
from pygame.locals import *
dim="images/"
pygame.init()
btex,btey=1000,800
io = pygame.display.Info()
tex,tey=io.current_w,io.current_h
fenetre=pygame.display.set_mode([tex,tey],pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
iconimage=pygame.image.load(dim+"icon.png")
pygame.display.set_icon(iconimage)
pygame.display.set_caption("Survive")

def rx(x): return int(x/btex*tex)
def ry(y): return int(y/btey*tey)

font=pygame.font.SysFont("Arial",ry(25))
font2=pygame.font.SysFont("Arial",ry(17))


strings1=(
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


cursor1,mask1=pygame.cursors.compile(strings1, black='X', white='.', xor='o')
cursor_sizer1=((16,16),(9,8),cursor1,mask1)

strings2=(
    "                ",
    "                ",
    "       X        ",
    "      X.X       ",
    "     X . X      ",
    "    X  .  X     ",
    "   X   X   X    ",
    "  X   X.X   X   ",
    " X...X.X.X...X  ",
    "  X   X.X   X   ",
    "   X   X   X    ",
    "    X  .  X     ",
    "     X . X      ",
    "      X.X       ",
    "       X        ",
    "                ")


cursor2,mask2=pygame.cursors.compile(strings2, black='X', white='.', xor='o')
cursor_sizer2=((16,16),(9,8),cursor2,mask2)

pygame.mouse.set_cursor(*cursor_sizer1)


tc=rx(100)

debug=False

armes=[]
p11=["perso1-1-1.png","perso1-1-2.png","perso1-1-3.png","perso1-1-4.png","perso1-1-5.png","perso1-1-6.png","perso1-1-7.png","perso1-1-8.png","perso1-1-9.png","perso1-1-10.png","perso1-1-11.png","perso1-1-12.png","perso1-1-13.png","perso1-1-14.png","perso1-1-15.png","perso1-1-16.png","perso1-1-17.png","perso1-1-18.png","perso1-1-19.png","perso1-1-20.png"]
p12=["perso1-2-1.png","perso1-2-2.png","perso1-2-3.png"]
p21=["perso.png"]
p22=["perso2-2-1.png","perso2-2-2.png","perso2-2-3.png"]
p31=["perso3.png"]
p32=["perso3-2-1.png","perso3-2-2.png","perso3-2-3.png","perso3-2-4.png","perso3-2-5.png","perso3-2-6.png","perso3-2-7.png","perso3-2-8.png","perso3-2-9.png","perso3-2-10.png","perso3-2-11.png","perso3-2-12.png","perso3-2-13.png","perso3-2-14.png"]
armes.append( ["pistolet",10,0.5,2.1,10,60,3,(20,20,20),3,(250,0,0),p11,rx(38),ry(52),0,0,p12,rx(38),ry(52)] )
armes.append( ["mitraillette",2,0.01,2.5,100,500,1,(20,20,20),1,(255,0,0),p21,rx(29),ry(50),0,0,p22,rx(206/5),ry(312/5)] )
armes.append( ["couteau",40,0.4,0,0,0,0,0,0,0,p31,rx(219/4),ry(279/4),1,90,p32,rx(300/3.5),ry(329/3.5)] )
#0=nom 1=degats 2=vitesse attaque 3=vitesse rechargement 4=taille chargeur 5=nombre munition niv 1 6=taille missile 7=couleur missile
#8=taille explosion 9=couleur explosion 10=images 11=tx 12=ty 13=type arme(0=distance 1=melee) 14=portee ( si type == 1 ) , sinon mettre 0 15=images tir
#16=tx tir , 17=ty tir

#
 
enms=[]
enms.append( ["zombie",50,rx(50),ry(50),[0,50],3,1.,750,60,"en1.png",1] )
enms.append( ["zombie2",60,rx(50),ry(50),[0,60],4.5,1.5,500,60,"en1.png",1] )
#0=nom 1=vie 2=tx 3=ty 4=att 5=vit max 6=acc 7=dist reperage 8=portee 9=img 10=?

imgtrs=[pygame.image.load(dim+"tr1.png"),pygame.image.load(dim+"tr2.png"),pygame.image.load(dim+"tr3.png"),pygame.image.load(dim+"tr4.png")]

emape=[]
emape.append( ["sol1","sol1.png",True,True,0.4] )      #0
emape.append( ["sol2","sol2.png",True,True,0.4] )      #1
emape.append( ["mur1","mur1.png",False,False] )    #2
emape.append( ["fin1","fin1.png",True,True] )      #3
emape.append( ["sol3","sol3.png",True,True,0.4] )      #4
emape.append( ["sol4","sol4.png",True,True,0.3] )      #5
emape.append( ["sol5","sol5.png",True,True,0.4] )      #6
emape.append( ["mur2","mur2.png",False,False] )    #7
emape.append( ["eau1","eau1.png",False,True] )     #8
emape.append( ["eau2","eau2.png",False,True] )     #9
emape.append( ["sol6","sol6.png",True,True,0.2] )      #10 neige
emape.append( ["sol7","sol7.png",True,True,0.1] )      #11 neige

for em in emape:
    em[1]=pygame.transform.scale(pygame.image.load(dim+em[1]),[tc,tc])
#0=nom , 1=img , 2=pmd , 3=mpad , 4=glisse

emaps=[ [0,2],[1,2],[4,2],[5,2],[6,2] , [10,2] , [11,2] ]
fins=[3]

def dist(p1,p2): return int(math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2))

class Missil:
    def __init__(self,x,y,t,cl,dg,vitx,vity,pos,texpl,clexpl):
        self.px=x
        self.py=y
        self.t=rx(t)
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
                self.rect=pygame.Rect(self.px-self.t/2,self.py-self.t/2,self.t,self.t)
                if self.px <= 0: self.delet=True
                if self.py <= 0: self.delet=True
                if self.px >= mape.shape[0]*tc: self.delet=True
                if self.py >= mape.shape[1]*tc: self.delet=True
                if not self.delet:
                    for o in [perso]+enemis:
                        if self.pos!=o:
                            if self.rect.colliderect(pygame.Rect(o.px,o.py,o.tx,o.ty)):
                                o.vie-=self.dg
                                self.delet=True
                                cr=pygame.draw.circle(fenetre,self.clexpl,(int(cam[0]+self.px),int(cam[1]+self.py)),self.texpl,0)
                                pygame.display.update()
                                #if self.texpl>10: time.sleep(0.1)
                                if self.texpl>5:
                                    for oo in [perso]+enemis:
                                        if oo!=o and cr.colliderect(pygame.Rect(cam[0]+oo.px,cam[1]+oo.py,oo.tx,oo.ty)):
                                            oo.vie-=self.dg
                                break
                if not self.delet:
                    for x in range(int(self.px/tc-2),int(self.px/tc+2)):
                        for y in range(int(self.py/tc-2),int(self.py/tc+2)):
                            if x >= 0 and y >= 0 and x < mape.shape[0] and y < mape.shape[1]:
                                em=emape[mape[x,y]]
                                if not self.delet and not em[3] and self.rect.colliderect(x*tc,y*tc,tc,tc):
                                    self.delet=True
                                    if self.texpl>5:
                                        cr=pygame.draw.circle(fenetre,self.clexpl,(int(cam[0]+self.px),int(cam[1]+self.py)),self.texpl,0)
                                        pygame.display.update()
                                        for oo in [perso]+enemis:
                                            if cr.colliderect(pygame.Rect(cam[0]+oo.px,cam[1]+oo.py,oo.tx,oo.ty)):
                                                oo.vie-=self.dg
                                    break

class Perso:
    def __init__(self,niv,arm,glisse):
        arme=armes[arm]
        self.px=500
        self.py=400
        self.tx=arme[11]
        self.ty=arme[12]
        self.txtir=arme[16]
        self.tytir=arme[17]
        self.vie_tot=1000
        self.vie=self.vie_tot
        self.imgs=[]
        for ii in arme[10]:
            self.imgs.append( pygame.transform.scale( pygame.image.load(dim+ii), [self.tx,self.ty] ) )
        self.imgs_tir=[]
        for ii in arme[15]:
            self.imgs_tir.append( pygame.transform.scale( pygame.image.load(dim+ii), [self.txtir,self.tytir] ) )
        self.anim=self.imgs
        self.an=0
        self.img=self.anim[0]
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
        self.energy_tot=5000
        self.energy=self.energy_tot
        self.issprint=False
        self.tparme=arme[13]
        self.portee=arme[14]
        self.dan=time.time()
        self.tan=0.03
        self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
        self.re=glisse
        self.isral=False
    def update(self,cam,mape,mis,trs,points,enemis,debug):  
        if time.time()-self.dbg>=self.tbg:
            pos=pygame.mouse.get_pos()
            x1,y1=cam[0]+self.px,cam[1]+self.py
            x2,y2=pos[0],pos[1]
            alpha=0
            if x2 >= x1 and y2 < y1:
                adj=y1-y2
                opp=x2-x1
                alpha=math.degrees( math.atan(opp/adj) )
            elif x2 > x1 and y2 >= y1:
                adj=x2-x1
                opp=y2-y1
                alpha=math.degrees( math.atan(opp/adj) )+90
            elif x2 <= x1 and y2 > y1:
                adj=y2-y1
                opp=x1-x2
                alpha=math.degrees( math.atan(opp/adj) )+180
            elif x2 < x1 and y2 <= y1:
                adj=x1-x2
                opp=y1-y2
                alpha=math.degrees( math.atan(opp/adj) )+270
            self.agl=alpha
            if time.time()-self.dan>=self.tan:
                self.dan=time.time()
                if self.anim==self.imgs_tir: self.an+=1
                else:
                    if (abs(self.vitx)+abs(self.vity))/2 >= 0.5: self.an+=1
                if self.an>=len(self.anim):
                    self.an=0
                    if self.anim==self.imgs_tir: self.anim=self.imgs
            self.img=pygame.transform.rotate(self.anim[self.an],-self.agl)
            self.dbg=time.time()
            vitx,vity=self.vitx,self.vity
            if self.issprint and self.energy>=5:
                self.energy-=5
                vitx*=2
                vity*=2
            if self.isral:
                vitx/=2
                vity/=2
            if not self.issprint:
                self.energy+=1
                if self.isral:
                    self.energy+=4
            if self.energy>self.energy_tot: self.energy=self.energy_tot
            self.px+=vitx
            self.py+=vity
            bc=True
            self.rect=pygame.Rect( cam[0]+self.px               , cam[1]+self.py                , self.tx      , self.ty      )
            srhaut=pygame.Rect   ( cam[0]+self.px+self.tx*0.425 , cam[1]+self.py+self.ty*0.000  , self.tx*0.15 , self.ty*0.10 )
            srbas=pygame.Rect    ( cam[0]+self.px+self.tx*0.425 , cam[1]+self.py+self.ty*0.900  , self.tx*0.15 , self.ty*0.10 )
            srgauche=pygame.Rect ( cam[0]+self.px+self.tx*0.000 , cam[1]+self.py+self.ty*0.425  , self.tx*0.10 , self.ty*0.15 )
            srdroit=pygame.Rect  ( cam[0]+self.px+self.tx*0.900 , cam[1]+self.py+self.ty*0.425  , self.tx*0.10 , self.ty*0.15 )
            if debug: pygame.draw.rect(fenetre,(0,50,100),self.rect,2)
            if debug: pygame.draw.rect(fenetre,(100,50,0),srhaut,2)
            if debug: pygame.draw.rect(fenetre,(100,50,0),srbas,2)
            if debug: pygame.draw.rect(fenetre,(100,50,0),srgauche,2)
            if debug: pygame.draw.rect(fenetre,(100,50,0),srdroit,2)
            for x in range(int((self.px)/tc-1),int((self.px)/tc+2)):
                for y in range(int((self.py)/tc-1),int((self.py)/tc+2)):
                    if x>=0 and y>=0 and x < mape.shape[0] and y < mape.shape[1] and not emape[mape[x,y]][2]: 
                        mrect=pygame.draw.rect(fenetre,(0,0,0),(cam[0]+x*tc,cam[1]+y*tc,tc,tc),2)
                        if self.rect.colliderect(mrect):
                            if srhaut.colliderect(mrect): self.py+=abs(vity)+1
                            elif srbas.colliderect(mrect): self.py-=abs(vity)+1
                            if srgauche.colliderect(mrect): self.px+=abs(vitx)+1
                            elif srdroit.colliderect(mrect): self.px-=abs(vitx)+1
                            if False:
                                self.px-=vitx
                                self.py-=vity
                            #self.vitx,self.vity=0,0
            if debug: pygame.display.update()
            for t in trs:
                if not t.pris and self.rect.colliderect(pygame.Rect(cam[0]+t.px,cam[1]+t.py,t.tx,t.ty)):
                    t.pris=True
                    points+=30
            if self.px<0: self.px,self.vitx,self.vity=1,0,0
            if self.px+self.tx>mape.shape[0]*tc: self.px,self.vitx,self.vity=mape.shape[0]*tc-self.tx-1,0,0
            if self.py<0: self.py,self.vitx,self.vity=1,0,0
            if self.py+self.ty>mape.shape[1]*tc: self.py,self.vitx,self.vity=mape.shape[1]*tc-self.ty-1,0,0
            if self.vitx <= -self.re: self.vitx+=self.re
            if self.vitx >= self.re: self.vitx-=self.re
            if self.vity <= -self.re: self.vity+=self.re
            if self.vity >= self.re: self.vity-=self.re
            if self.vitx<0 and self.vitx > -self.re: self.vitx=0
            if self.vitx>0 and self.vitx < self.re: self.vitx=0
            if self.vity<0 and self.vity > -self.re: self.vity=0
            if self.vity>0 and self.vity < self.re: self.vity=0
        if self.istirer:
            if time.time()-self.dat >= self.tat:
                self.dat=time.time()
                self.anim=self.imgs_tir
                self.an=0
                if self.tparme==0 and time.time()-self.dchrg>=self.tchrg and self.nbcharg>0:
                    self.nbcharg-=1
                    pos=pygame.mouse.get_pos()
                    vitx,vity=50,0
                    if self.agl <= 90 and self.agl > 0:
                        vitx=math.sin(math.radians(self.agl))*50
                        vity=-math.cos(math.radians(self.agl))*50
                    elif self.agl <= 180 and self.agl > 90:
                        vitx=math.cos(math.radians(self.agl-90))*50
                        vity=math.sin(math.radians(self.agl-90))*50
                    elif self.agl <= 270 and self.agl > 180:
                        vitx=-math.sin(math.radians(self.agl-180))*50
                        vity=math.cos(math.radians(self.agl-180))*50
                    elif self.agl <= 360 and self.agl > 270:
                        vitx=-math.cos(math.radians(self.agl-270))*50
                        vity=-math.sin(math.radians(self.agl-270))*50
                    mis.append( Missil(self.px+self.tx/2.,self.py+self.ty/2.,self.tmis,self.clmis,self.dg,vitx,vity,self,self.texpl,self.clexpl) )
                elif self.tparme==1:
                    for e in enemis:
                        if dist([self.px,self.py],[e.px,e.py]) <= self.portee:
                            e.vie-=self.dg
        return cam,mis,trs,points,enemis

class Enemi:
    def __init__(self,x,y,tp,glisse):
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
        self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
        self.glisse=glisse
    def update(self,mape,perso,mis,cam,debug,enemis):
        if time.time()-self.dbg>=self.tbg:
            self.dbg=time.time()
            self.rect=pygame.Rect( cam[0]+self.px               , cam[1]+self.py                , self.tx      , self.ty      )
            srhaut=pygame.Rect   ( cam[0]+self.px+self.tx*0.425 , cam[1]+self.py+self.ty*0.000  , self.tx*0.15 , self.ty*0.10 )
            srbas=pygame.Rect    ( cam[0]+self.px+self.tx*0.425 , cam[1]+self.py+self.ty*0.900  , self.tx*0.15 , self.ty*0.10 )
            srgauche=pygame.Rect ( cam[0]+self.px+self.tx*0.000 , cam[1]+self.py+self.ty*0.425  , self.tx*0.10 , self.ty*0.15 )
            srdroit=pygame.Rect  ( cam[0]+self.px+self.tx*0.900 , cam[1]+self.py+self.ty*0.425  , self.tx*0.10 , self.ty*0.15 )
            if debug: pygame.draw.rect(fenetre,(0,50,100),self.rect,2)
            if debug: pygame.draw.rect(fenetre,(100,50,0),srhaut,2)
            if debug: pygame.draw.rect(fenetre,(100,50,0),srbas,2)
            if debug: pygame.draw.rect(fenetre,(100,50,0),srgauche,2)
            if debug: pygame.draw.rect(fenetre,(100,50,0),srdroit,2)
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
                self.agl=alpha-90
                self.img=pygame.transform.rotate(self.img_base,self.agl)
                if dis <= self.portee or self.rect.colliderect(pygame.Rect(cam[0]+perso.px,cam[1]+perso.py,perso.tx,perso.ty)):
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
            for e in enemis:
                if self != e and self.rect.colliderect(e.rect):
                    if srhaut.colliderect(e.rect): self.py+=abs(self.vity)+1
                    elif srbas.colliderect(e.rect): self.py-=abs(self.vity)+1
                    if srgauche.colliderect(e.rect): self.px+=abs(self.vitx)+1
                    elif srdroit.colliderect(e.rect): self.px-=abs(self.vitx)+1
            self.rect=pygame.Rect( cam[0]+self.px               , cam[1]+self.py                , self.tx      , self.ty      )
            srhaut=pygame.Rect   ( cam[0]+self.px+self.tx*0.425 , cam[1]+self.py+self.ty*0.000  , self.tx*0.15 , self.ty*0.10 )
            srbas=pygame.Rect    ( cam[0]+self.px+self.tx*0.425 , cam[1]+self.py+self.ty*0.900  , self.tx*0.15 , self.ty*0.10 )
            srgauche=pygame.Rect ( cam[0]+self.px+self.tx*0.000 , cam[1]+self.py+self.ty*0.425  , self.tx*0.10 , self.ty*0.15 )
            srdroit=pygame.Rect  ( cam[0]+self.px+self.tx*0.900 , cam[1]+self.py+self.ty*0.425  , self.tx*0.10 , self.ty*0.15 )
            for x in range(int((self.px)/tc-1),int((self.px)/tc+2)):
                for y in range(int((self.py)/tc-1),int((self.py)/tc+2)):
                    if x>=0 and y>=0 and x < mape.shape[0] and y < mape.shape[1] and not emape[mape[x,y]][2]: 
                        mrect=pygame.draw.rect(fenetre,(0,0,0),(cam[0]+x*tc,cam[1]+y*tc,tc,tc),2)
                        if self.rect.colliderect(mrect):
                            if srhaut.colliderect(mrect): self.py+=abs(self.vity)+1
                            elif srbas.colliderect(mrect): self.py-=abs(self.vity)+1
                            if srgauche.colliderect(mrect): self.px+=abs(self.vitx)+1
                            elif srdroit.colliderect(mrect): self.px-=abs(self.vitx)+1
                            if False:
                                self.px-=self.vitx
                                self.py-=self.vity
                            #self.vitx,self.vity=0,0
            if debug: pygame.display.update()
            if self.px<0: self.px=1
            if self.py<0: self.py=1
            if self.px+self.tx>mape.shape[0]*tc: self.px=mape.shape[0]*tc-self.tx-1
            if self.py+self.ty>mape.shape[1]*tc: self.py=mape.shape[1]*tc-self.ty-1
            if self.vitx<0: self.vitx+=self.glisse
            if self.vitx>0: self.vitx-=self.glisse
            if self.vity<0: self.vity+=self.glisse
            if self.vity>0: self.vity-=self.glisse
            if self.vitx<0 and self.vitx > -self.glisse: self.vitx=0
            if self.vitx>0 and self.vitx < self.glisse: self.vitx=0
            if self.vity<0 and self.vity > -self.glisse: self.vity=0
            if self.vity>0 and self.vity < self.glisse: self.vity=0
        return mis
        
class Tresor:
    def __init__(self,x,y,i):
        self.px=x
        self.py=y
        self.tx=rx(40)
        self.ty=ry(40)
        self.img=pygame.transform.scale( imgtrs[i] , [self.tx,self.ty])
        self.pris=False



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
    perso=Perso(niv,arm,emape[isol][4])
    perso.px=dex*tc+rx(20)
    perso.py=dey*tc+ry(20)
    return mape,perso,[deb[0],deb[1]],mps,isol,imur
        
def deb_level(niv,arm):
    enemis=[]
    mape,perso,cfin,mps,isol,imur=create_mape(niv,arm)
    cam=[-perso.px+tex/2,-perso.py+tey/2]
    mis=[]
    nbenms=random.randint(2*niv,5*niv)
    ne=niv
    if niv >= len(enms):
        while ne > len(enms)-1: ne-=1
    for x in range(nbenms):
        mm=random.choice( mps[int(len(mps)*10/100):] )
        enemis.append( Enemi(mm[0]*tc+rx(20),mm[1]*tc+ry(20),ne,emape[isol][4]) )
    gagne=False
    trs=[]
    rr=[0,1,2,3]
    for x in range(3):
        mm=random.choice( mps[int(len(mps)*10/100):-1] )
        r=random.choice(rr)
        if r in rr: del(rr[rr.index(r)])
        trs.append( Tresor(mm[0]*tc+rx(20),mm[1]*tc+ry(20),r) )
    return enemis,mape,perso,cfin,cam,mis,gagne,trs

def ecran_gagne(niv,points):
    fenetre.fill((75,90,20))
    fenetre.blit(font.render("Vous avez terminé le niveau "+str(niv),20,(255,255,255)),[rx(250),ry(300)])
    fenetre.blit(font.render("Vous avez "+str(points)+" points",20,(255,255,255)),[rx(250),ry(350)])
    fenetre.blit(font.render("Appuyez sur 'ESPACE' pour continuer",20,(255,255,255)),[rx(250),ry(400)])
    pygame.display.update()
    encor=True
    while encor:
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN and event.key in [K_SPACE,K_ESCAPE]: encor=False

def ecran_perdu(niv,points):
    fenetre.fill((75,90,20))
    fenetre.blit(font.render("Vous êtes mort. Vous étiez au niveau "+str(niv),20,(255,0,0)),[rx(250),ry(300)])
    fenetre.blit(font.render("Vous avez "+str(points)+" points",20,(255,255,255)),[rx(250),ry(350)])
    fenetre.blit(font.render("Appuyez sur 'ESPACE' pour continuer",20,(255,0,0)),[rx(250),ry(400)])
    pygame.display.update()
    encor=True
    while encor:
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN and event.key in [K_SPACE,K_ESCAPE]: encor=False

def ecran_chargement():
    fenetre.fill((75,90,20))
    fenetre.blit(font.render("Chargement...",20,(255,255,255)),[rx(400),ry(400)])
    pygame.display.update()

def aff_jeu(perso,enemis,cam,mape,mis,fps,points,trs,debug):
    fenetre.fill((0,0,0))
    for x in range(int((-cam[0])/tc),int((-cam[0]+tex)/tc+1)):
        for y in range(int((-cam[1])/tc),int((-cam[1]+tey)/tc+1)):
            if x>=0 and x < mape.shape[0] and y >= 0 and y < mape.shape[1]:
                fenetre.blit(emape[mape[x,y]][1],[cam[0]+x*tc,cam[1]+y*tc])
            
    for e in enemis:
        if e.px+cam[0]+e.tx > 0 and e.px+cam[0] < tex and e.py+cam[1]+e.ty > 0 and e.py+cam[1] < tey:
            e.rect=fenetre.blit(e.img,[cam[0]+e.px,cam[1]+e.py])
            if e.vie>=0:
                pygame.draw.rect(fenetre,(150,0,0),(cam[0]+e.px,cam[1]+e.py-15,int(float(e.vie)/float(e.vie_tot)*float(e.tx)),7),0)
                pygame.draw.rect(fenetre,(0,0,0),(cam[0]+e.px,cam[1]+e.py-15,e.tx,7),1)
        else: e.rect=pygame.Rect(cam[0]+e.px,cam[1]+e.py,e.tx,e.ty)
    for t in trs:
        if not t.pris and t.px+cam[0]+t.tx > 0 and t.px+cam[0] < tex and t.py+cam[1]+t.ty > 0 and t.py+cam[1] < tey:
            fenetre.blit(t.img,[cam[0]+t.px,cam[1]+t.py])
    for m in mis:
        if m.px+cam[0]-m.t > 0 and m.px+cam[0] < tex and m.py+cam[1]-m.t > 0 and m.py+cam[1] < tey:
            pygame.draw.circle(fenetre,m.cl,(int(cam[0]+m.px),int(cam[1]+m.py)),m.t,0)
    perso.rect=fenetre.blit(perso.img,[cam[0]+perso.px,cam[1]+perso.py])
    if debug : fenetre.blit(font2.render(str(perso.agl)+"°",20,(10,10,10)),[cam[0]+perso.px+50,cam[1]+perso.py-50])
    if perso.vie>=0:
        pygame.draw.rect(fenetre,(250,0,0),(rx(50),ry(50),int(float(perso.vie)/float(perso.vie_tot)*float(rx(200))),ry(25)),0)
        pygame.draw.rect(fenetre,(0,0,0),(rx(50),ry(50),rx(200),ry(25)),2)
    if perso.energy>=0:
        pygame.draw.rect(fenetre,(0,250,200),(rx(50),ry(80),int(float(perso.energy)/float(perso.energy_tot)*float(rx(200))),ry(8)),0)
        pygame.draw.rect(fenetre,(0,0,0),(rx(50),ry(80),rx(200),ry(8)),2)
    fenetre.blit(font2.render("score : "+str(points),20,(10,10,10)),[tex-rx(200),ry(10)])
    fenetre.blit(font2.render("munitions : "+str(perso.nbcharg)+"/"+str(perso.nbmun),20,(10,10,10)),[tex-rx(200),ry(40)])
    if time.time()-perso.dchrg<=perso.tchrg:
        pygame.draw.rect(fenetre,(0,0,120),(tex-rx(200),ry(65),int((time.time()-perso.dchrg)/perso.tchrg*rx(100)),ry(5)),0)
        pygame.draw.rect(fenetre,(0,0,0),(tex-rx(200),ry(65),rx(100),ry(5)),1)
    if time.time()-perso.dat<=perso.tat:
        pygame.draw.rect(fenetre,(200,0,0),(tex-rx(200),ry(75),int((time.time()-perso.dat)/perso.tat*rx(100)),ry(5)),0)
        pygame.draw.rect(fenetre,(0,0,0),(tex-rx(200),ry(75),rx(100),ry(5)),1)
    if perso.nbcharg==0 and perso.nbmun>0: fenetre.blit( font.render("click droit pour recharger",20,(255,50,50)),[tex/2,50])
    fenetre.blit(font2.render("nb enemis restants: "+str(len(enemis)),20,(10,10,10)),[tex-rx(200),ry(80)])
    pos=pygame.mouse.get_pos()
    if debug: pygame.draw.line(fenetre,(0,0,100),(cam[0]+perso.px+int(float(perso.tx)/2.),cam[1]+perso.py+int(float(perso.ty)/2.)),(pos[0]+(pos[0]-(cam[0]+perso.px))*10,pos[1]+(pos[1]-(cam[1]+perso.py))*10),1)
    fenetre.blit(font2.render("fps : "+str(int(fps)),20,(0,0,0)),[rx(15),ry(15)])
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
    ecran_chargement()
    niv=1
    enemis,mape,perso,cfin,cam,mis,gagne,trs=deb_level(niv,arm)
    encour=True
    fps=0
    points=0
    debug=False
    while encour:
        t1=time.time()
        aff_jeu(perso,enemis,cam,mape,mis,fps,points,trs,debug)
        for m in mis:
            m.update(perso,enemis,mape,cam)
            if m.delet:
                if m in mis: del(mis[mis.index(m)])
        cam,mis,trs,points,enemis=perso.update(cam,mape,mis,trs,points,enemis,debug)
        for e in enemis:
            mis=e.update(mape,perso,mis,cam,debug,enemis)
            if e.vie<=0:
                points+=10
                if e in enemis: del(enemis[enemis.index(e)])
        perso,cam=verif_keys(perso,cam)
        cam=[-perso.px+tex/2,-perso.py+tey/2]
        if pygame.Rect(perso.px,perso.py,perso.tx,perso.ty).colliderect(pygame.Rect(cfin[0]*tc,cfin[1]*tc,tc,tc)):
            points+=100
            ecran_gagne(niv,points)
            ecran_chargement()
            enemis,mape,perso,cfin,cam,mis,gagne,trs=deb_level(niv,arm)
            niv+=1
        if perso.vie<=0:
            encour=False
            ecran_perdu(niv,points)
            ecran_chargement()
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE: encour=False
                elif event.key==K_d: debug=not debug
                elif event.key in [K_LSHIFT,K_RSHIFT]: perso.issprint=True
                elif event.key in [K_LCTRL,K_RCTRL]: perso.isral=True
            elif event.type==KEYUP:
                if event.key in [K_LSHIFT,K_RSHIFT]: perso.issprint=False
                elif event.key in [K_LCTRL,K_RCTRL]: perso.isral=False
            elif event.type==MOUSEBUTTONDOWN:
                pygame.mouse.set_cursor(*cursor_sizer2)
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
                pygame.mouse.set_cursor(*cursor_sizer1)
                if event.button==1: perso.istirer=False
        t2=time.time()
        tt=(t2-t1)
        if tt!=0: fps=1.0/tt
                        
###########################################################################################

imb1=pygame.transform.scale(pygame.image.load(dim+"button1.png"),[rx(200),ry(100)])
imb2=pygame.transform.scale(pygame.image.load(dim+"button2.png"),[rx(200),ry(100)])
imb3=pygame.transform.scale(pygame.image.load(dim+"button3.png"),[rx(200),ry(100)])

def aff_menu(men,btsel,arm,an,dan,tan):
    fenetre.fill((0,0,0))
    bst=[]
    for x in range(20): bst.append(None)
    #button 1
    if men==0: ib=imb3
    elif btsel==0: ib=imb2
    else: ib=imb1
    fenetre.blit( ib , [rx(50),ry(50)] )
    fenetre.blit( font.render("jouer",20,(100,150,35)) , [rx(80),ry(70)] )
    #button 2
    if men==1: ib=imb3
    elif btsel==1: ib=imb2
    else: ib=imb1
    fenetre.blit( ib , [rx(50),ry(200)] )
    fenetre.blit( font.render("personnage",20,(100,150,35)) , [rx(80),ry(220)] )
    #button 3
    if men==2: ib=imb3
    elif btsel==2: ib=imb2
    else: ib=imb1
    fenetre.blit( ib , [rx(50),ry(350)] )
    fenetre.blit( font.render("stats",20,(100,150,35)) , [rx(80),ry(370)] )
    #button 4
    if men==3: ib=imb3
    elif btsel==3: ib=imb2
    else: ib=imb1
    fenetre.blit( ib , [rx(50),ry(500)] )
    fenetre.blit( font.render("parametres",20,(100,150,35)) , [rx(80),ry(520)] )
    #button 5
    if men==4: ib=imb3
    elif btsel==4: ib=imb2
    else: ib=imb1
    fenetre.blit( ib , [rx(50),ry(650)] )
    fenetre.blit( font.render("quitter",20,(100,150,35)) , [rx(80),ry(670)] )
    if men==1:
        if arm==0: ib=imb3
        else: ib=imb1
        bst[0]=fenetre.blit( ib , [rx(740),ry(10)] )
        fenetre.blit( font.render("pistolet",20,(100,150,35)) , [rx(770),ry(30)] )
        if arm==1: ib=imb3
        else: ib=imb1
        bst[1]=fenetre.blit( ib , [rx(740),ry(120)] )
        fenetre.blit( font.render("mitraillette",20,(100,150,35)) , [rx(770),ry(140)] )
        if arm==2: ib=imb3
        else: ib=imb1
        bst[2]=fenetre.blit( ib , [rx(740),ry(230)] )
        fenetre.blit( font.render("couteau",20,(100,150,35)) , [rx(770),ry(250)] )
        if time.time()-dan>=tan:
            dan=time.time()
            an+=1
            if an >= len(armes[arm][15]): an=0
        fenetre.blit( pygame.transform.scale(pygame.image.load(dim+armes[arm][15][an]),[armes[arm][11]*4,armes[arm][12]*4]) , [rx(400),ry(400)] )
    pygame.display.update()
    return bst,an,dan

def main():
    an=0
    dan=time.time()
    tan=0.05
    btsel=0
    men=None
    bts=[pygame.Rect(rx(50),ry(50),rx(200),ry(100)),pygame.Rect(rx(50),ry(200),rx(200),ry(100)),pygame.Rect(rx(50),ry(350),rx(200),ry(100)),pygame.Rect(rx(50),ry(500),rx(200),ry(100)),pygame.Rect(rx(50),ry(650),rx(200),ry(100))]
    #0=jouer 1=personnage 2=stats 3=parametres 4=credits 5=quitter
    arm=0
    encoure=True
    while encoure:
        pos=pygame.mouse.get_pos()
        btsel=None
        for b in bts:
            if b.collidepoint(pos): btsel=bts.index(b)
        bst,an,dan=aff_menu(men,btsel,arm,an,dan,tan)
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE: encoure=False
            elif event.type==MOUSEBUTTONUP:
                for b in bts:
                    if b.collidepoint(pos): men=bts.index(b)
                if men==0:
                    #try:
                    if True:
                        men=None
                        main_jeu(arm)
                    else:
                    #except Exception as error:
                        print("error : ",error)
                elif men==4: exit()
                for bb in bst:
                    if bb!=None and bb.collidepoint(pos):
                        i=bst.index(bb)
                        if i==0: arm,an=0,0
                        elif i==1: arm,an=1,0
                        elif i==2: arm,an=2,0
                
                






main()



