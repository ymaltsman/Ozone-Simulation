GlowScript 2.7 VPython
import random
"""
http://www.glowscript.org/#/user/jmaltsman/folder/MyPrograms/program/ozonesim/edit
Description: CFCs threaten to destroy the atmosphere. If you watch the game without doing anything, you'll see that when 
the multicolored molecule enters a cloud, it binds to the cloud and dichlorine 
breaks off. If dichlorine (two green spheres) gets hit by an ultraviolet ray,
it will break up into two chlorine radicals, which eat up Ozone (yellow spheres) that 
prevents Ultraviolet radiation from reaching the earth and heating it up. The 
one solution that scientists could come up with: lasers. Move the laser with the 
up and down keys and fire it with j to incinerate the CFC before it reaches the stratosphere!
"""


scene.bind('keydown', keydown_fun)     # Function for key presses
#scene.bind('click', click_fun)         # Function for mouse clicks
scene.background = 0.8*vector(1, 1, 1)
scene.width=680
scene.height=550
sky = box(size = vector(30, 1, 40), pos = vector(0, -1, 0), color = vector(0,.2,.8))

sun=sphere(pos=vector(0,1,-22), color=color.yellow, radius=1)

box1base=box(size=vector(2,1,1), color=color.white, pos=vector(-8,1,-1))
sphere11=sphere(radius=2,pos=vector(-8.5,1,-1), color=color.white)
sphere12=sphere(radius=2,pos=vector(-7.5,1,-1),color=color.white)
cloudA=compound([box1base,sphere11,sphere12])
cloudA.vel=vector(10,0,0)
cloudA.pos.z +=4

box2base=box(size=vector(2,1,1), color=color.white, pos=vector(8,1,0))
sphere21=sphere(radius=2,pos=vector(8.5,1,0), color=color.white)
sphere22=sphere(radius=2,pos=vector(7.5,1,0),color=color.white)
cloudB=compound([box2base,sphere21,sphere22])
cloudB.vel=vector(-10,0,0)
cloudB.pos.z+=4

Cl=sphere(radius=.4,pos=vector(1,1,14), color=color.green)
F=sphere(radius=.4, pos=vector(.6,1,14),color=color.yellow)
C=sphere(radius=.4,pos=vector(.2,1,14),color=color.red)
CFC=compound([Cl,F,C])
print(len(CFC))
CFC.vel=vector(0,0,-10)

ship=box(size=vector(2,1,1),color=color.black,pos=vector(15,1,16))

Ozonelayer=[]
for i in range(40):
    O1=sphere(radius=.4,pos=vector(0,1,0), color=color.yellow)
    O2=sphere(radius=.4, pos=vector(-.6,1,0),color=color.yellow)
    O3=sphere(radius=.4,pos=vector(-.8,1,0),color=color.yellow)
    ozone=compound([O1,O2,O3])
    ozone.pos.x=random.uniform(-14,14)
    ozone.pos.z=random.uniform(-6,-10)
    Ozonelayer.append(ozone)
    ozone.pos.z+=4

solution=cylinder(pos=ship.pos, axis=vector(2,0,0), radius=.2, color=color.red)
solution.pos.x = ship.pos.x - 2
solution.vel= vector(0,0,0)
solution.angle=0

#UVrays: cylinders with random directions
UVray=cylinder(pos=sun.pos, axis=vector(0,0,2), radius=.2)
UVray.pos.x=sun.pos.x+3
UVray.vel=vector(10,0,5)
#small sphere at the end of the UVray to detect for collisions with the molecules
UVraycollider=sphere(pos=UVray.pos, radius=.3)
UVraycollider.pos.z=UVray.pos.z+2
UVraycollider.vel=UVray.vel


def twoCl(xpos, zpos):
    """accepts the position of a cloud and makes
    a dichlorine object with a radius and random velocity"""
    cluno=sphere(radius=.4, pos=vector(xpos,1,zpos),color=color.green)
    cldos= sphere(radius=.4, pos=vector(xpos+.4,1,zpos),color=color.green)
    diCl=compound([cluno,cldos])
    diCl.vel=vector(0,0,0)
    diCl.vel.x = random.uniform(-5,5)
    diCl.vel.z = random.uniform(-5,0)
    return diCl

def Clradical(xpos,zpos,xvel,zvel):
    """Two Cl radicals will be added to the list. If its the one whose side has been hit by the UVray collider,
    it will undergo the collide function and have that velocity.Also, position will 
    be determined by the side where the ray hits"""
    clradical=sphere(pos=vector(xpos,1,zpos), radius=.4, color=color.green)
    clradical.vel=vector(0,0,0)
    clradical.vel.x=xvel
    clradical.vel.z=zvel
    
    clradical.nummoves=0
    #in the while loop, check if collider hits, run collide and run append
    #have one of the clrads have an opposite x velocity
    #utilize sunrays velocity in cl's velocity
    return clradical

def hitswall(a):
    if a.pos.x>sky.size.x/2:
        a.pos.x=sky.size.x/2
        a.vel.x *= -1
    if a.pos.x<-sky.size.x/2:
        a.pos.x=-sky.size.x/2
        a.vel.x *= -1
    if a.pos.z<-sky.size.z/2:
        a.pos.z=-sky.size.z/2
        a.vel.z *= -1
        


RATE = 30                # The number of times the while loop runs each second
dt = 1.0/(1.0*RATE)      # The time step each time through the while loop
scene.autoscale = False  # Avoids changing the view automatically
scene.forward = vector(0, -3, -2)  # Ask for a bird's-eye view of the scene...

#list of dichlorines
Clmol=[]
#list of cl radicals
clrad=[]

def collide(a, b, r):
    """Checks if two balls collide if their radii are overlapping"""
    diff = a.pos - b.pos
    if mag(diff) < r:
        diff = a.pos - b.pos
        dtan = rotate(diff, radians(90), vector(0, 1, 0))
         # get the two velocities
        vi = a.vel
        vj = b.vel
        #undo last time step
        a.pos -= a.vel * dt
        b.pos -= b.vel * dt
        
         # find the radial and tangent parts
        vi_rad = proj(vi, diff)
        vi_tan = proj(vi, dtan)
        vj_rad = proj(vj, -diff)
        vj_tan = proj(vj, dtan)
        
        # swap the radials and keep the tangents
        a.vel =  vj_rad + vi_tan
        b.vel =  vi_rad + vj_tan
temp=0
while True:

    rate(RATE)
    
    
    def keydown_fun(event):
        """This function is called each time a key is pressed."""
        key = event.key
        print(key)
        if key == 'down' or key in 'wWiI':
            ship.pos.z+=1
            solution.pos.z+=1
        if key == 'up' or key in 'sSkK':
            ship.pos.z-=1
            solution.pos.z-=1
        if key == 'j':
            solution.vel.x=-30
    
    
    cloudA.pos.x += cloudA.vel.x*dt
    cloudB.pos.x += cloudB.vel.x*dt
    CFC.pos.z += CFC.vel.z*dt
    solution.pos.x += solution.vel.x*dt
    UVray.pos.x+=UVray.vel.x*dt
    UVray.pos.z+=UVray.vel.z*dt
    UVraycollider.pos.x +=UVray.vel.x*dt
    UVraycollider.pos.z +=UVray.vel.z*dt
    
    """if diCl:
        diCl.pos.z += diCl.vel.z*dt
        diCl.pos.x += diCl.vel.x*dt
        if diCl.pos.z< -sky.size.z/2:
            diCl.pos.z = sky.size.z/2
            diCl.vel.z *= -1
        if diCl.pos.x>sky.size.x/2:
            diCl.pos.x=sky.size.x/2
            diCl.vel.x *=-1
        if diCl.pos.x<-sky.size.x/2:
            diCl.pos.x=-sky.size.x/2
            diCl.vel.x *= -1"""
        
    
    if cloudA.pos.x>sky.size.x/2:
        cloudA.pos.x=sky.size.x/2
        cloudA.vel.x *=-1
    if cloudA.pos.x<-sky.size.x/2:
        cloudA.pos.x=-sky.size.x/2
        cloudA.vel.x *= -1
        
    if cloudB.pos.x>sky.size.x/2:
        cloudB.pos.x=sky.size.x/2
        cloudB.vel.x *=-1
    if cloudB.pos.x<-sky.size.x/2:
        cloudB.pos.x=-sky.size.x/2
        cloudB.vel.x *= -1
        
    if CFC.pos.z < -sky.size.z/2:
        CFC.pos=vector(0,1,14)
        CFC.pos.x=random.uniform(-10,10)
    
    if abs(CFC.pos.z-solution.pos.z)<.5 and abs(CFC.pos.x-solution.pos.x)<.5:
        CFC.pos=vector(0,1,14)
        CFC.pos.x=random.uniform(-10,10)
    
    if solution.pos.x<-sky.size.x/2:
        solution.pos.x=ship.pos.x-2
        solution.pos.z=ship.pos.z
        solution.vel.x=0

    if UVray.pos.x>sky.size.x/2:
        UVray.pos=sun.pos
        UVraycollider.pos.x=UVray.pos.x
        UVraycollider.pos.z=UVray.pos.z+2
        UVray.vel.z=10
        UVray.vel.x=random.uniform(-6,6)
    
    if UVray.pos.x<-sky.size.x/2:
        UVray.pos=sun.pos
        UVraycollider.pos.x=UVray.pos.x
        UVraycollider.pos.z=UVray.pos.z+2
        UVray.vel.z=10
        UVray.vel.x=random.uniform(-6,6)
        
    if UVray.pos.z>sky.size.z/2:
        UVray.pos=sun.pos
        UVraycollider.pos.x=UVray.pos.x
        UVraycollider.pos.z=UVray.pos.z+2
        UVray.vel.z=10
        UVray.vel.x=random.uniform(-6,6)
        temp +=.5
        print("Temperature:",temp)
        if temp>3:
            print("Game over!")
        
    if abs(CFC.pos.z-cloudA.pos.z)<3 and abs(CFC.pos.x-cloudA.pos.x)<3:
        Clmol.append(twoCl(cloudA.pos.x,cloudA.pos.z+1))
        CFC.pos=vector(0,1,14)
        CFC.pos.x=random.uniform(-10,10)
        
    if abs(CFC.pos.z-cloudB.pos.z)<1 and abs(CFC.pos.x-cloudB.pos.x)<1:
        Clmol.append(twoCl(cloudB.pos.x,cloudB.pos.z+1))
        CFC.pos=vector(0,1,14)
        CFC.pos.x=random.uniform(-10,10)  
        
    
    if Clmol != []:
        for i in range(len(Clmol)):
            Clmol[i].pos.x+=Clmol[i].vel.x*dt
            Clmol[i].pos.z+=Clmol[i].vel.z*dt
            hitswall(Clmol[i])
            if abs(Clmol[i].pos.z-UVraycollider.pos.z)<1 and abs(Clmol[i].pos.x-UVraycollider.pos.x)<1:
                print("collision")
                collide(Clmol[i],UVraycollider,1)
                clrad.append(Clradical(Clmol[i].pos.x+.2,Clmol[i].pos.z,Clmol[i].vel.x,Clmol[i].vel.z))
                clrad.append(Clradical(Clmol[i].pos.x-.2,Clmol[i].pos.z,-Clmol[i].vel.x,Clmol[i].vel.z))#if its zero it'll keep having the same velocity. #it'll have the same velocity, but the collide function will happen so it may move differently
                #Clmol.remove(Clmol[i])
                Clmol[i].pos.x=random.uniform(50,100)
                Clmol[i].pos.z=random.uniform(50,100)
                Clmol[i].vel=vector(0,0,0)
                UVray.pos=sun.pos
                UVraycollider.pos.x=UVray.pos.x
                UVraycollider.pos.z=UVray.pos.z+2
                UVray.vel.z=10
                UVray.vel.x=random.uniform(-6,6)
            for j in range(len(Clmol)):
                if Clmol[i] != Clmol[j]:
                    collide(Clmol[i],Clmol[j],.6)
            
                    
    if clrad != []:
        for i in range(len(clrad)):
            clrad[i].pos.x+=clrad[i].vel.x*dt
            clrad[i].pos.z+=clrad[i].vel.z*dt
            clrad[i].nummoves+=1
            hitswall(clrad[i])
            for j in range(len(clrad)):
                if clrad[i] != clrad[j]:
                    collide(clrad[i],clrad[j],.4)
    
    if Ozonelayer != []:
        for i in range(len(Ozonelayer)):
                if abs(Ozonelayer[i].pos.z-UVraycollider.pos.z)<.3 and abs(Ozonelayer[i].pos.x-UVraycollider.pos.x)<.3: 
                    UVray.pos=sun.pos
                    UVraycollider.pos.x=UVray.pos.x
                    UVraycollider.pos.z=UVray.pos.z+2
                    UVray.vel.z=10
                    UVray.vel.x=random.uniform(-6,6)
                if Clmol != []:
                    for j in range(len(Clmol)):
                        collide(Ozonelayer[i],Clmol[j])
                    
            
    if Ozonelayer != [] and clrad != []:
        for i in range(len(Ozonelayer)):
            for j in range(len(clrad)):
                if abs(Ozonelayer[i].pos.x-clrad[j].pos.x)<3 and abs(Ozonelayer[i].pos.z-clrad[j].pos.z)<3:
                    Ozonelayer[i].pos.x= random.uniform(50,100)
                    Ozonelayer[i].pos.z=random.uniform(50,100)
                    clrad[j].pos.x=random.uniform(50,100)
                    clrad[j].pos.z=random.uniform(50,100)
                    clrad[j].vel=vector(0,0,0)
                    
        
        