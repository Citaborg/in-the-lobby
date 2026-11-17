from pathlib import Path
import bisect, math, subprocess as sp
import numpy as np
from PIL import Image, ImageDraw, ImageFont
root=Path(__file__).resolve().parent
song=root.parent/'src'/'web'/'in-the-lobby.mp3'
out=root.parent/'src'/'web'/'in-the-lobby.mp4'
atlas=Image.open(root/'lobby-film-sheet.png').convert('RGB')
w,h=atlas.size
panels=[atlas.crop((round(i%4*w/4)+4,round(i//4*h/3)+4,round((i%4+1)*w/4)-4,round((i//4+1)*h/3)-4)) for i in range(12)]
audio=np.frombuffer(sp.check_output(['ffmpeg','-loglevel','error','-i',str(song),'-ar','12000','-ac','1','-f','f32le','-']),dtype='<f4')
fps=24
duration=len(audio)/12000
hop=120
frames=np.lib.stride_tricks.sliding_window_view(audio,512)[::hop]
spec=np.log1p(abs(np.fft.rfft(frames*np.hanning(512),axis=1)))
flux=np.maximum(np.diff(spec,axis=0),0).mean(1)
def snap(t):
    a=int((t-.35)*100)
    return (a+np.argmax(flux[a:a+70]))/100
shots=[(0,0),(2.8,3),(8.6,1),(12.2,2),(16,1),(19.8,0),(23.3,3),(27,1),(30.3,3),(34.5,1),(38.7,0),(40.8,6),(42.2,3),(44.3,1),(46.5,0),(48.4,6),(50.1,1),(52.2,0),(55.7,3),(59.5,1),(63.3,3),(67.5,6),(70.5,4),(74.6,5),(78.4,4),(82.9,5),(86.3,0),(88.4,6),(89.8,2),(91.7,3),(93.9,7),(95.6,6),(97.7,3),(99.5,2),(103.5,7),(106.8,6),(108.8,2),(111.9,7),(114.4,6),(116.4,8),(118.2,3),(120.9,8),(124.2,4),(126.8,8),(128.5,6),(130.6,9),(132.5,7),(134.5,8),(136.2,9),(138,10),(139.4,4),(141.3,10),(144.1,9),(146,10),(148.3,0),(152.2,6),(155.3,9),(160.1,3),(162.5,1),(163.7,3),(164.7,8),(168.4,3),(171.8,1),(175.6,5),(179,0),(182.7,3),(186,0),(189.3,11),(190.3,5),(194,0),(197,11)]
starts=[snap(t) if t else 0 for t,_ in shots]+[duration]
W,H=960,540
large=ImageFont.truetype(r'C:\Windows\Fonts\impact.ttf',67)
small=ImageFont.truetype(r'C:\Windows\Fonts\consolab.ttf',17)
proc=sp.Popen(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-i',str(song),'-map','0:v','-map','1:a','-vf','scale=1280:720:flags=bicubic','-c:v','libx264','-preset','veryfast','-crf','21','-maxrate','1750k','-bufsize','3500k','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest',str(out)],stdin=sp.PIPE)
for n in range(math.ceil(duration*fps)):
    t=n/fps
    s=bisect.bisect_right(starts,t)-1
    i=shots[s][1]
    u=(t-starts[s])/(starts[s+1]-starts[s])
    p=panels[i]; pw,ph=p.size
    pulse=min(1,float(flux[min(len(flux)-1,int(t*100))])*19)
    ease=u*u*(3-2*u)
    zoom=1.03+.13*(ease if s%2 else 1-ease)+.014*pulse
    cw=min(pw,ph*W/H)/zoom; ch=cw*H/W
    x=(pw-cw)*(.5+.33*math.sin(s+u*1.4))
    y=(ph-ch)*(.48+.24*math.sin(s*1.6+u))
    frame=p.transform((W,H),Image.Transform.EXTENT,(x,y,x+cw,y+ch),Image.Resampling.BICUBIC)
    d=ImageDraw.Draw(frame,'RGBA')
    if i in (8,9,10):
        for j in range(16 if i==10 else 7):
            z=(j*.371+t*(.105+j%4*.018))%1
            xx=480+math.cos(j*2.399+t*.13)*z*790
            yy=250+math.sin(j*2.399+t*.13)*z*470
            a=1+z*z*24; b=a*(.2+.35*abs(math.sin(t*2+j)))
            d.polygon([(xx-a,yy-b),(xx+a*.6,yy-b*1.3),(xx+a,yy+b),(xx-a*.6,yy+b*1.5)],fill=(225,194,135,int(145*z)))
    if i==2:
        for j in range(3):
            pts=[(W*.28+j*9+math.sin(t*1.5-k*.10+j)*k*.27,H*.63-k*1.5) for k in range(32)]
            d.line(pts,fill=(237,216,173,45),width=2)
    if t<3.8:
        d.rectangle((0,348,508,510),fill=(11,29,31,222))
        d.rectangle((26,371,30,478),fill=(221,115,55,255))
        d.text((45,376),'S K A T T E F U T E N',font=small,fill='#f8cb85')
        d.text((42,396),'IN THE LOBBY',font=large,fill='#ffebc4')
    # Diegetic cutaways: the waiting-room software develops a life of its own.
    inserts=[(3.8,3.6,'admit'),(8.6,2.8,'clock'),(42.2,2.1,'admit'),(71.0,3.3,'staff'),(82.9,2.8,'staff'),(103.5,3.0,'lift'),(108.8,3.0,'clock'),(132.5,1.9,'lift'),(182.7,3.0,'admit')]
    for begin,span,kind in inserts:
        v=t-begin
        if not 0<=v<span: continue
        slide=max(0,1-v*7,(v-span+.16)*6)
        xx=round(32-slide*430); yy=33
        cream='#e9d9af'; ink='#183431'; orange='#ca673d'
        d.rectangle((xx+6,yy+7,xx+400,yy+171),fill=(5,13,13,178))
        d.rectangle((xx,yy,xx+394,yy+165),fill=cream,outline=ink,width=4)
        d.rectangle((xx+4,yy+4,xx+390,yy+31),fill=ink)
        heading={'admit':'CONFERENCE SERVICES','clock':'LOBBY STANDARD TIME','staff':'PERSONNEL RECORD','lift':'DIRECTORY / LIFT 01'}[kind]
        d.text((xx+14,yy+7),heading,font=small,fill=cream)
        if kind=='admit':
            d.text((xx+16,yy+54),'Waiting for the host'+'.'*(1+int(v*3)%3),font=small,fill=ink)
            d.rectangle((xx+17,yy+99,xx+377,yy+121),outline=ink,width=2)
            for k in range(17):
                if (k+int(v*10))%17<8:d.rectangle((xx+20+k*21,yy+102,xx+35+k*21,yy+118),fill=orange)
            d.text((xx+17,yy+132),'PARTICIPANTS   '+('0001' if begin<100 else '0000'),font=small,fill=ink)
        elif kind=='clock':
            cx,cy=xx+68,yy+96
            d.ellipse((cx-48,cy-48,cx+48,cy+48),outline=ink,width=4)
            for j in range(12):
                a=j*math.pi/6
                d.line((cx+39*math.cos(a),cy+39*math.sin(a),cx+44*math.cos(a),cy+44*math.sin(a)),fill=ink,width=2)
            for length,speed,col in [(27,1.7,ink),(37,8,orange)]:
                a=v*speed
                d.line((cx,cy,cx+length*math.sin(a),cy-length*math.cos(a)),fill=col,width=4)
            d.text((xx+140,yy+70),'ESTIMATED WAIT',font=small,fill=ink)
            d.text((xx+140,yy+104),'Recalculating'+'.'*(1+int(v*4)%3),font=small,fill=ink)
        elif kind=='staff':
            thumb=panels[4].resize((114,103))
            frame.paste(thumb,(xx+11,yy+43))
            d.text((xx+145,yy+50),'STEVE',font=large.font_variant(size=42),fill=ink)
            d.text((xx+147,yy+108),'Dept. of Pointing',font=small,fill=ink)
            for k in range(32):
                if k%5!=1:d.line((xx+147+5*k,yy+140,xx+147+5*k,yy+151),fill=ink,width=1+k%3)
        else:
            floor=int((begin-66)*10+v*(12 if begin<100 else 75))
            d.text((xx+16,yy+44),f'{floor:03d}',font=large,fill=ink)
            d.text((xx+159,yy+65),'NEXT STOP',font=small,fill=ink)
            d.text((xx+159,yy+98),'Lobby. Again.',font=small,fill=ink)
            d.polygon([(xx+350,yy+73),(xx+365,yy+53),(xx+380,yy+73)],fill=orange)
    for begin,end,message in [(162.5,163.7,'HOST: YOU'),(164.7,168.0,'Sorry! We forgot you were there.'),(168.4,171.5,'Meeting ended.'),(171.8,175.1,'Same time tomorrow?'),(175.6,179.0,"Next time, please don't join so late."),(189.3,190.3,'Steve?'),(190.3,193,'Welcome home.')]:
        if begin<=t<end:
            width=int(small.getlength(message))+60
            left=(W-width)//2
            d.rectangle((left,444,left+width,491),fill=(11,29,31,234),outline='#dfb77c',width=1)
            d.text((W//2,467),message,font=small,anchor='mm',fill='#ffe2b1')
    if t>duration-1.1:
        frame=Image.blend(frame,Image.new('RGB',frame.size,'#061313'),min(1,(t-duration+1.1)/.8))
    if n==0 or n%1200==0: print(round(t),flush=True)
    proc.stdin.write(frame.tobytes())
proc.stdin.close()
assert proc.wait()==0
print(out,out.stat().st_size,flush=True)


