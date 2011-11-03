#Nga-impor library
import pygame #keur GUI na
import random #keur ngocok kartu
import time #keur delay hungkul

def nextturn(last):
  #Ganti giliran pemaen

  #mun pemaen can go'ong  
  if last<3:
    return last+1
  #mun ges go'ong balik ka kordi
  else:
    return 0

def throw(playerno, card, pos):
  #Maenkeun kartu pas giliran na
  drac = card[1]+card[0]

  #lamun eweuh nu bisa dipiceun
  if player[playerno].count(card)==0 and player[playerno].count(drac)==0:
    return "Player%s teu boga kartu %s" % (str(playerno+1),card)
  #mun aya
  else:
    #mun tibalik kartuna dibalikeun
    if player[playerno].count(card)==0:
      #kurangan ti leungeun (itungan)
      c = player[playerno].pop(player[playerno].index(drac))
      #kurangan ti leungen (gambarna)
      d = human[playerno].hands.pop(human[playerno].name.index(drac))
      e = human[playerno].name.pop(human[playerno].name.index(drac))
    #mun teu mah langsung piceun
    else:
      #kurangan ti leungeun (itungan)
      c = player[playerno].pop(player[playerno].index(card))
      #kurangan ti leungen (gambarna)
      d = human[playerno].hands.pop(human[playerno].name.index(card))
      e = human[playerno].name.pop(human[playerno].name.index(card))
    #arah miceun kartu na mun ka ujung kiri
    if pos==0:
      #asupkeun ka meja (itungan na)
      ptable.insert(0,card)
      #asupkeun ka meja (gambar na)
      meja.addCardL(card[0],card[1],0)
    #mun ka kanan
    else:
      #asupkeun ka meja (itungan na)
      ptable.append(card)
      #asupkeun ka meja (gambar na)
      meja.addCardR(card[0],card[1],0)
    return "Player%s ngalung kartu %s" % (str(playerno+1),card)

def valtable(card, auto='-1'):
  #Ngecek kartu nu dipaenkeun
  cl = card[0]
  cr = card[-1]
  ctl = ptable[0][0]
  ctr = ptable[-1][-1]
  #mun lain kartuna
  if cl!=ctl and cl!=ctr and cr!=ctl and cr!=ctr:
    return 'xxx'
  #mun bener kartu na
  else:
    #mun ujung kiri jeung kanan beda
    if ctl!=ctr:
      #mun kartuna bisa ka kiri jeung ka kanan
      if (cl==ctl and cr==ctr and cr!=cl) or (cl==ctr and cr==ctl and cr!=cl):
        #mun ku komputer lsg asupkeun
        if int(auto)>=0:
          where = auto
        #mun jalma nu maen dititah milih
        else:
          where = ''
          sMsg("Rek di %s-%s ato di %s-%s ?" %(ctr,ctr,ctl,ctl))
          #nungguan jalma milik ujung kiri ato kanan
          while where=='':
            #ngecek klik mouse
            for event in pygame.event.get():
              if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                #lamun d klik nu kanan
                if meja.tcards[meja.tctr].pressed(mouse):
                  where = ctr
                #lamun d klik nu kiri
                if meja.tcards[meja.tctl].pressed(mouse):
                  where = ctl
      #mun ngan asup di kiri asupkeun ka kiri
      elif cl==ctl and cl!=ctr:
        where=ctl
      #mun ngan asup di kiri tp kartu kudu dibalikeun
      elif cr==ctl and cr!=ctr:
        where=ctl
      #mun d kanan
      else:
        where=ctr
    #mun d kanan
    else:
      where=ctr
    #lamun asupna ka kanan, kartuna ditandaan jd 'LRx'
    if where==ctr:
      if cl==ctr:
        return ctr+cr+'x'
      #Mun tibalik jd 'RLx'
      else:
        return ctr+cl+'x'
    #mun di kiri jd 'xRL'
    else:
      if cl==ctl:
        return 'x'+cr+ctl
      #mun tibalik jd 'xLR'
      else:
        return 'x'+cl+ctl

def valhands(playerno):
  #Ngecek pemaen nu keur giliran, liwat ato nteu na
  ctl = ptable[0][0]
  ctr = ptable[-1][-1]
  #dianggep liwat hla
  valid = 0
  #trs di tingalian kartu na
  for i in range(len(player[playerno])):
    for j in range(2):
      #lamun boga kartu na teu liwat
      if player[playerno][i][j]==ctl or player[playerno][i][j]==ctr:
        valid=1
  return valid

def gaplehmate():
  #Ngecek bisi ges gapleh

  #ngecek giliran mimiti ato lain
  #mun lain
  if len(ptable)>0:
    ctl = ptable[0][0]
    ctr = ptable[-1][-1]
  #mun mimiti
  else:
    ctl = 9
    ctr = 9
  #di anggep can aya nu bisa jalan
  valid = 0
  #trs di cek 1-1
  for h in range(len(player)):
    for i in range(len(player[h])):
      for j in range(2):
        #lamun aya keneh nu bisa maen, can gapleh
        if player[h][i][j]==ctl or player[h][i][j]==ctr:
          valid=1
  #mun kakara maen can gapleh
  if ctl == 9:
    valid = 1
  return valid

def score():
  #Ngitung skor mun geusan
  small = 1000
  win = 0
  #grafik na di reset
  screen.fill(bg)
  #kartu nu ges maen di tampilkeun deui
  meja.update()
  #nu di leungeun di tingalikeun kabeh
  for i in range(len(human)):
    human[i].update(1)
  #ngagambar kotak skor
  pygame.draw.rect(screen,white,[0,0,200,150],0)
  pygame.draw.rect(screen,red,[0,0,200,150],5)
  #nulis judul skor
  font = pygame.font.Font(None, 14)
  title = font.render('Score Game Na :',True,black)
  screen.blit(title,[60,4])
  #mulai ngitung
  countsix=0
  countzero=0
  sixteteng=5
  zeroteteng=5
  #skor na
  nilai=[]
  #ngecek balak 6 jeung 0 bisi teteng
  for i in range(len(ptable)):
    for j in range(2):
      #mun balak 6 teteng bakal d itung
      if ptable[i][j]=='6':
        countsix+=1
      #mun balak kosong teteng bakal d itung
      elif ptable[i][j]=='0':
        countzero+=1
  #skor na di asupkeun
  for h in range(len(player)):
    total = 0
    #kartu na ditambahkeun
    for i in range(len(player[h])):
      #lamun boga balak 6 nu teteng
      if player[h][i]=='66' and countsix==6:
        total+=50
        sixteteng=h
      #lamun boga balak 0 nu teteng
      elif player[h][i]=='00'and countzero==6:
        total+=25
        zeroteteng=h
      #lamun diitung biasa
      else:
        for j in range(2):
          total+=int(player[h][i][j])
    nilai.append(total)
    #nilai nu pangleutik na meunang
    if total<=small :
      win = h
      small = total
  #lamun nu pangleutik na lewih ti 1
  if nilai.count(small)>1:
    candidate = []
    #asupkeun kana kandidat
    for i in range(len(player)):
      if nilai[i]==small:
        candidate.append(i)
    candidatevalue = []
    maxval = 0
    #di itung aya sbrh kartu di leungeun
    for i in candidate:
      candidatevalue.append(len(player[i]))
    #mun boga balak nilai na dikurangan
    for i in range(len(candidatevalue)):
      for j in range(len(player[candidate[i]])):
        if player[candidate[i]][j][0]==player[candidate[i]][j][1]:
          candidatevalue[i]-=2
      #diteang nilai nu pang gede na
      if maxval<candidatevalue[i]:
        maxval=candidatevalue[i]
        win = candidate[i]
    #lamun beak d leungen lsg jd nu meunang
    for i in candidate:
      if len(player[i])==0:
        win = i
  #lamun kabeh pamaen boga keneh kartu berarti gapleh
  if len(player[win])>0:
    win=4
    wincondition = 'ku gapleh %s !!' % ptable[-1][-1]
    lastgapleh=int(ptable[-1][-1])
    #lamun gapleh balak nu teteng diitung biasa
    if sixteteng<5:
      nilai[sixteteng]-=38
    if zeroteteng<5:
      nilai[zeroteteng]-=25
  else:
    wincondition = 'poldan.'
  for i in range(len(nilai)):
    #nuliskeun nilai masing2 di papan skor
    font = pygame.font.Font(None, 14)
    tscore = font.render("Player %s : %s" % (str(i+1),str(nilai[i])),True,black)
    screen.blit(tscore,[50,30+(i*10)])
  #nuliskeun pemaen nu meunang
  font = pygame.font.Font(None, 14)
  tscore = font.render("Player%s meunang %s" % ((str(win+1)),wincondition),True,black)
  screen.blit(tscore,[50,80])
  #nyieun tombol oke na pake jisong
  but = card()
  but.setlr(0,1)
  but.putinto(100,115,0,0)
  #fps pas nampilkeun skor
  clock.tick(10)
  #ngarepres layar
  pygame.display.flip()
  #jisong can di klik
  ok=0
  while ok==0:
    #ngecek mun jisong ges di klik
    for event in pygame.event.get():
      if event.type==pygame.MOUSEBUTTONDOWN:
        mouse = pygame.mouse.get_pos()
        if but.pressed(mouse):
          ok=1        
  return win+1

def aimove(playerno):
  #mun giliran komputer, komputerna dititah ngitung
  
  #ngasupkeun nilai mimiti ker penilaian kartu
  playable = [0,0,0,0,0,0,0]
  ontable = [0,0,0,0,0,0,0]
  priority = [5,0,1,2,3,4,6]
  balak = [0,0,0,0,0,0,0]
  ctr = '9'
  ctl = '9'
  #ngabaca meja
  if len(ptable)>0:
    for i in range(len(ptable)):
      for j in range(2):
        ontable[int(ptable[i][j])]+=1
    ctr = ptable[-1][-1]
    ctl = ptable[0][0]
  #ngabaca leungeun
  for i in range(len(player[playerno])):
    for j in range(2):
      if player[playerno][i][0]!=player[playerno][i][1]:
        playable[int(player[playerno][i][j])]+=1
      else:
        if j==1:
          playable[int(player[playerno][i][j])]+=1
          balak[int(player[playerno][i][j])]+=1
  #kartu dileungeun diurutkeun menurut kemungkinan na
  maxlimit = 8
  sortedplayable = []
  while maxlimit>0:
    maxval = 0
    maxcard = 9
    #prioritas pang gede na di tunda di hareup
    for i in priority:
      if playable[i]>maxval and playable[i]<=maxlimit and i not in sortedplayable:
        maxval = playable[i]
        maxcard = i
    if maxval>0:
      sortedplayable.append(maxcard)
    if maxcard<9:
      maxlimit = maxval
    else:
      maxlimit = 0

  cardval = []
  #ngitung untung rugi na tiap kartu
  for i in range(len(player[playerno])):
    psv=0
    if player[playerno][i][0]==ctr or player[playerno][i][0]==ctl or player[playerno][i][1]==ctr or player[playerno][i][1]==ctl or ctr=='9':
      psv = 1
    plv = playable[int(player[playerno][i][0])]
    prv = playable[int(player[playerno][i][1])]
    tlv = ontable[int(player[playerno][i][0])]
    trv = ontable[int(player[playerno][i][1])]
    cval = plv+prv+tlv+trv
    if tlv>6 or trv>6:
      cval -= 6
    if (tlv<3 or trv<3) and player[playerno][i][0]==player[playerno][i][1]:
      cval += 6
      if len(ptable)==0 and (player[playerno][i][0]=='0' or player[playerno][i][0]=='6'):
        cval-=20
    fval = cval*psv
    cardval.append(fval)
  choicelist = []
  maxindex = 0
  #nyieun daptar kartu2 nu dipilih
  for i in range(len(cardval)):
    if cardval[i]>=maxindex:
      maxindex = cardval[i]
  for i in range(len(player[playerno])):
    if cardval[i]==maxindex:
      choicelist.append(player[playerno][i])
  #lamun di daptar aya rea, dipilih hiji nu pang untung na
  if len(choicelist)>1:
    choiceval = []
    for i in range(len(choicelist)):
      cval = priority[int(choicelist[i][0])]+priority[int(choicelist[i][1])]
      choiceval.append(cval)
    maxchoice = 0
    for i in range(len(choiceval)):
      if choiceval[i]>=maxchoice:
        maxchoice = choiceval[i]
    for i in range(len(choicelist)):
      if choiceval[i]==maxchoice:
        choice = choicelist[i]
  else:
    choice = choicelist[0]
  #lamun kartu nu dipilih bisa asup ka kiri ato kanan
  putside=''
  if ctl!=ctr:
    if ( choice[0]==ctl and  choice[1]==ctr and  choice[1]!= choice[0]) or ( choice[0]==ctr and  choice[1]==ctl and  choice[1]!= choice[0]):
      lside = playable[int(ctl)]+ontable[int(ctl)]
      rside = playable[int(ctr)]+ontable[int(ctr)]
      #mun cek si komputer ka kiri
      if lside>rside:
        putside = ctl
      #Mun cek si komputer ka kanan
      else:
        putside = ctr
  if putside!='':
    return "%s,%s" % (choice,putside)
  else:
    return choice

def cekbalak():
  #ngecek balak pas kakara ngabagi kartu

  #mimiti can di itung dianggep can boga kabeh  
  balakinplayer = [0,0,0,0]
  #trs ditingalian 1-1
  for i in range(len(player)):
    balakcount = 0
    for j in range(len(player[i])):
      if player[i][j][0]==player[i][j][1]:
        balakcount+=1
    #jumlah balak na trs dicatet
    balakinplayer[i]=balakcount
  save = 0
  for i in range(len(balakinplayer)):
    #mun aya nu boga 5 balak ato lewih
    if balakinplayer[i]>4:
      save=1
      wMsg("Si Player%s boga %s balak, kocok deui." % (str(i+1),str(balakinplayer[i])))
  return save


def shuffle():  
  #Ngocok kartu na
  
  save = 1
  #lamun aya nu rea teung balak ngke dikocok deui
  while save>0:
    #layarna dihideungan
    screen.fill(bg)
    sMsg('Ngocok Kartu...')
    #kartu nu urut saacan na diasupkeun kana kocokan
    for i in range(len(human)):
      for j in range(len(human[i].hands)):
        human[i].hands.pop()
        human[i].name.pop()
    for i in range(7):
      for j in range(7-i):
        deck.append(str(i)+str(j+i))
    for i in range(len(phavebalak)):
      phavebalak[i]=0
      
    #Kartu dikocok trs dibagikeun 7 ewang
    for i in range(28):
      x = int(random.random()*(28-i))
      c = deck.pop(x)
      if c[0]==c[-1]:
        phavebalak[int(c[0])] = (i%4)
      #asupkeun kartu kanan masing2 pamaen (itungan)
      player[i%4].append(c)
      #asupkeun kartu kanan masing2 pamaen (gambar)
      #mun pemaen jalma kartu na katingali
      if isAI[i%4]==0:
        human[i%4].addCard(int(c[0]),int(c[-1]))
      #mun komputer kartu na dibalikeun
      else:
        human[i%4].addHidCard(int(c[0]),int(c[-1]))
    #ngecek bisi rea teung balak
    save = cekbalak()
  
def playtable(first):
  #Mulai maen di meja
  
  #lamun mimiti maen
  if first>5:
    fmovestr = '0'
  #lamun saacan na ges maen
  else:
    fmovestr = str(first)
  fmove = int(fmovestr)
  new=0
  #Lamun anyar maen nu boga balak 1, maen mimiti
  if fmove<1 or fmove>5:
    #nu boga balak 1 meunang giliran
    fmove=phavebalak[1]
    sMsg( "Player%s ngalung balak 1" % str(fmove+1))
    #ngalung balak 1
    proc = throw(fmove,'11',0)
    sMsg( proc)
    #trs giliran pamaen berikutna
    fmove = nextturn(fmove)
  #mun saacan na gapleh
  elif fmove==5:
    #lamun gapleh 0 jd balak 1
    if lastgapleh==0 : lastgapleh=1
    #lamun gapleh 6 jd balak 5
    if lastgapleh==6 : lastgapleh=5
    
    #nu boga balak sesuai gapleh na meunang giliran mimiti
    fmove=phavebalak[lastgapleh]
    sMsg( "Player%s ngalung balak %s" % (str(fmove+1),str(lastgapleh)))
    #balak na dialungkeun 
    proc = throw(fmove,str(lastgapleh)+str(lastgapleh),0)
    sMsg(  proc)
    #giliran pemaen berikutna
    fmove = nextturn(fmove)
  #lamun nu saacan na meunang poldan, jalan mimiti
  else:
    fmove-=1
  #mulai giliran kadua jeung saterusna nepi sa game
  while len(player[0])>0 and len(player[1])>0 and len(player[2])>0 and len(player[3])>0 and gaplehmate()>0:
    #nampilkeun pemaen nu pas giliran
    sMsg( "Player%s eun maen" % str(fmove+1))
    #ngabetem sadetik meh teu gancang teuing
    time.sleep(1)
    #ngitung hela kartu pilihan komputer
    aipick = aimove(fmove)
    #lamun bisa kiri kanan
    if len(aipick)>2:
      aiput = aipick.split(',')[-1]
      aipick = aipick.split(',')[0]
    #mun ngan bisa kiri ato kanan hungkul
    else:
      aiput = '-1'
    #cek bisi masih giliran pertama
    if len(ptable)>0:
      #cek kartu di leungeun aya ato teu nu bisa maen
      pturn = valhands(fmove)
    #mun giliran mimiti pasti bisa maen
    else:
      pturn = 1
    #lamun pas giliran na boga kartu nu bisa dipaenkeun
    if pturn!=0:
      #lamun giliran komputer asupkeun ti pilihan komputer
      if isAI[fmove]>0:
        pcard = aipick
      #lamun giliran jalma, pemaen dititah milih kartu na
      else:
        pcard = ''
      while len(pcard)!=2:
        sMsg("Ngalung nu mana ?")
        #nungguan kartu di leungen aya nu diklik
        for event in pygame.event.get():
          if event.type==pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            for i in range(len(human[fmove].hands)):
              if human[fmove].hands[i].pressed(mouse):
                pcard = human[fmove].name[i]
      #ngecek giliran mimiti, mun lain
      if len(ptable)>0:
        #mun komputer
        if isAI[fmove]>0:
          newcard = valtable(pcard,aiput)
        #mun jalma
        else:
          newcard = valtable(pcard)
      #mun giliran mimiti
      else:
        newcard = pcard+'x'
      #mun kartu bisa dipaenkeun
      if newcard!='xxx':
        pos = (newcard.find('x')/2)*len(ptable)
        newcard = newcard.strip('x').rstrip('x')
        #kartuna dipiceun ka meja
        proc = throw(fmove,newcard,pos)
        sMsg( proc)
        #lamun sukses miceun kartu, ganti giliran
        if proc.find('boga')<0:
          fmove = nextturn(fmove)
      else:
        #lamun kartuna lain
        warn = warnin("Teu meunang miceu kartu %s." % pcard)
        warn.Tunggu()
    #lamun teu boga kartu nu bisa maen, diliwat
    else:
      sMsg("Player%s liwat!" % str(fmove+1))
      time.sleep(2)
      #giliran pindah
      fmove = nextturn(fmove)
    clock.tick(20)
    #bersihan layar
    screen.fill(bg)
    sMsg(' ')
    #ngarepres gambar kartu di leungen
    for i in range(len(human)):
      human[i].update()
    #ngarepres gambar kartu di meja
    meja.update()
    pygame.display.flip()
      
  #game tamat, munculkeun skor
  win=score()
  #nanya rek maen deui moal
  playagain = cMsg("Maen Deui ?")
  #mun maen deui
  if playagain:
    return win
  #mun moal
  else:
    return 0

def initcbg():
    #nyiapkeun kordinat acak keur kartu di gambar menu
    cbgcord = [[],[]]
    n=0
    for i in range(7):
        for j in range(7-i):
          cbgcord[0].append(int(random.random()*size[0]))
          cbgcord[1].append(int(random.random()*size[1]))
          n+=1
    return cbgcord
  
def drawbg(cord):
    #ngagambar kartu ker latar menu
    n=0
    for i in range(7):
        for j in range(7-i):
            if n%2==0:
              pass
              drawcard(j+i,i,cord[0][n],cord[1][n],0)
            else:
              pass
              drawback(cord[0][n],cord[1][n],0)
            n+=1

def drawback(x,y,f):
    #ngagambar kartu nutup

    #siapkeun ukuran2 na (keur kartu nyangigir)
    hei=50
    wid=100
    lx=x-(wid/2)
    ty=y-(hei/2)
    rx=x+(wid/2)
    by=y+(hei/2)
    #mun kartu nangtung ukuran dirubah
    if f>0:
        hei=100
        wid=50
        lx=x-(wid/2)
        ty=y-(hei/2)
        rx=x+(wid/2)
        by=y+(hei/2)
    #ngagambar kartu jeung kalangkangna
    pygame.draw.rect(screen,white,[lx,ty,wid,hei],0)
    pygame.draw.rect(screen,grey,[lx,ty,wid,hei],3)
    pygame.draw.line(screen,black,(lx,by),(rx,by),3)
    pygame.draw.line(screen,black,(rx,ty),(rx,by),3)
    #ngagambar garis2na
    for x in range(lx,rx,5):
        x = x+5
        pygame.draw.line(screen,red,(x,ty),(x,by),2)
        pygame.draw.line(screen,blue,(x+1,ty),(x+1,by),2)
    #ngagambar garis2na
    for y in range(ty,by,5):
        y = y+5
        pygame.draw.line(screen,red,(lx,y),(rx,by),2)
        pygame.draw.line(screen,blue,(lx,y-1),(rx,y-1),2)
    return [lx,ty,rx,by]

def drawcard(l,r,x,y,f):
    #ngagambar kartu kabuka

    #nyiapkeun ukuran2na  (keur kartu ngagoler)
    hei=50
    wid=100
    lx=x-(wid/2)
    ty=y-(hei/2)
    rx=x+(wid/2)
    by=y+(hei/2)
    #posisi titik2na
    dotx = [[],[2],[3,1],[3,2,1],[3,3,1,1],[3,3,2,1,1],[3,3,2,2,1,1]]
    doty = [[],[0],[-1,1],[-1,0,1],[-1,1,-1,1],[-1,1,0,-1,1],[-1,1,-1,1,-1,1]]
    #posisi garis tengahna
    dvdr = [4,2]
    #mun kartu nangtung ukuran dirubah
    if f>0:
        hei=100
        wid=50
        lx=x-(wid/2)
        ty=y-(hei/2)
        rx=x+(wid/2)
        by=y+(hei/2)
        dotx = [[],[0],[-1,1],[-1,0,1],[-1,1,-1,1],[-1,1,0,-1,1],[-1,1,-1,1,-1,1]]
        doty = [[],[2],[3,1],[3,2,1],[3,3,1,1],[3,3,2,1,1],[3,3,2,2,1,1]]
        dvdr = [2,4]
    #ngagambar kartu jeung kalangkangna
    pygame.draw.rect(screen,white,[lx,ty,wid,hei],0)
    pygame.draw.rect(screen,grey,[lx,ty,wid,hei],3)
    #ngagambar garis tengah mun sare
    if f==0:
        pygame.draw.line(screen,red,(x,ty),(x,by),3)
    #ngagambar garis tengah mun nangtung
    else:
        pygame.draw.line(screen,red,(lx,y),(rx,y),3)
    #kalangkang kartuna
    pygame.draw.line(screen,black,(lx,by),(rx,by),3)
    pygame.draw.line(screen,black,(rx,ty),(rx,by),3)
    #ngagambar titik2na nu kiri
    #mun 1 titikna gede
    if l==1:
        rad=12
    #nu sejen mah leutik
    else:
        rad=6
    #ngagambar sesuai jumlah titikna
    for i in range(l):
        pygame.draw.circle(screen,red,[x-(dotx[l][i-1]*((x-lx)/dvdr[0])),y+(doty[l][i-1]*((y-ty)/dvdr[1]))],rad,0)
    #terus titik2 nu kanan
    if r==1:
        rad=12
    else:
        rad=6
    for i in range(r):
        pygame.draw.circle(screen,red,[x+(dotx[r][i-1]*((x-lx)/dvdr[0])),y-(doty[r][i-1]*((y-ty)/dvdr[1]))],rad,0)
    return [lx,ty,rx,by]

def wMsg(text):
  #popup keterangan ngan 1 tombol teu pake return
  warn = warnin(text)
  #nungguan diklik Oke
  warn.Tunggu()

def cMsg(text):
  #popup nanya pake 2 tombol
  tanya = confirm(text)
  #nunggu diklik oke ato batal
  res = tanya.Tunggu()
  #return sesuai nu di klikna
  return res

def sMsg(text=''):
  #ngaganti tulisan di statusbar
  sbar.update(text)
  #ngarepres layar
  pygame.display.flip()

class card(pygame.sprite.Sprite):
    #kelas card (kartu) nyieun turunan ti Sprite na pygame
    def __init__(self):
        #nga-init kelas kolotna
        pygame.sprite.Sprite.__init__(self)
        #ngaset ukuran2 kartu
        self.inhand=1
        self.left=0
        self.right=0
        self.topleft=[]
        self.bottomright=[]
        self.x=400
        self.y=300
        self.ori=0
        self.hide=0
    def setlr(self,l,r):
        #ngaset angka kiri kanan na
        self.left = l
        self.right = r
    def putinto(self,x=-5,y=-5,ori=-5,hide=0):
        #ngagambar kartu na
        #mun x<-5 hide na diganti
        if x<-5:
          self.hide=hide
        #mun x na lewih gd ti -4 ukuran2 x,y,ori jeung hide na diganti
        if x>-4:
          self.x=x
          self.y=y
          self.ori=ori
          self.hide=hide
        #mun hide na 1 digambar tukangna
        if self.hide==1:
          res=drawback(self.x,self.y,self.ori)
        #mun hide na 0 digambar hareupna
        else:
          res=drawcard(self.left,self.right,self.x,self.y,self.ori)
        self.topleft = [res[0],res[1]]
        self.bottomright = [res[2],res[3]]
    def pressed(self,mouse):
        #ngabaca klik mouse di kartu ieu
        if mouse[0] > self.topleft[0]:
            if mouse[1] > self.topleft[1]:
                if mouse[0] < self.bottomright[0]:
                    if mouse[1] < self.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False
        
class button(pygame.sprite.Sprite):
    #kelas button (tombol) nyieun turunan ti Sprite na pygame (lewih sederhana ti kartu)
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.topleft=[]
        self.bottomright=[]
        self.caption=''
    def putinto(self,x,y,w,h,caption):
        self.topleft=[x-(w/2),y-(h/2)]
        self.bottomright=[x+(w/2),y+(h/2)]
        self.caption=caption
        pygame.draw.rect(screen,red,[self.topleft[0],self.topleft[1],w,h],0)
        pygame.draw.rect(screen,grey,[self.topleft[0],self.topleft[1],w,h],3)
        pygame.draw.line(screen,black,(self.topleft[0],self.bottomright[1]),(self.bottomright[0],self.bottomright[1]),3)
        pygame.draw.line(screen,black,(self.bottomright[0],self.topleft[1]),(self.bottomright[0],self.bottomright[1]),3)
        font = pygame.font.Font(None, 25)
        text = font.render(caption,True,black)
        screen.blit(text, [x-(len(caption)*5),y])
    def pressed(self,mouse):
        if mouse[0] > self.topleft[0]:
            if mouse[1] > self.topleft[1]:
                if mouse[0] < self.bottomright[0]:
                    if mouse[1] < self.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False

class warnin(pygame.sprite.Sprite):
    #kelas warnin (keterangan) keur nampilkeun popup keterangan pake 1 tombol
    def __init__(self,cap):
        pygame.sprite.Sprite.__init__(self)
        self.topleft=[]
        self.bottomright=[]
        self.oktl=[]
        self.okbr=[]
        self.caption=cap
        x=size[0]/2
        y=size[1]/2
        w=400
        h=150
        self.topleft=[x-(w/2),y-(h/2)]
        self.bottomright=[x+(w/2),y+(h/2)]
        self.oktl=[self.bottomright[0]-80,self.bottomright[1]-30]
        self.okbr=[self.bottomright[0]-10,self.bottomright[1]-10]
        okw = self.okbr[0]-self.oktl[0]
        okh = self.okbr[1]-self.oktl[1]
        #kotak popupna jeung kalangkangna
        pygame.draw.rect(screen,yellow,[self.topleft[0],self.topleft[1],w,h],0)
        pygame.draw.rect(screen,grey,[self.topleft[0],self.topleft[1],w,h],3)
        pygame.draw.line(screen,black,(self.topleft[0],self.bottomright[1]),(self.bottomright[0],self.bottomright[1]),3)
        pygame.draw.line(screen,black,(self.bottomright[0],self.topleft[1]),(self.bottomright[0],self.bottomright[1]),3)
        #kotak tombolna jeung kalangkangna
        pygame.draw.rect(screen,grey,[self.oktl[0],self.oktl[1],okw,okh],0)
        pygame.draw.rect(screen,white,[self.oktl[0],self.oktl[1],okw,okh],3)
        pygame.draw.line(screen,black,(self.oktl[0],self.okbr[1]),(self.okbr[0],self.okbr[1]),3)
        pygame.draw.line(screen,black,(self.okbr[0],self.oktl[1]),(self.okbr[0],self.okbr[1]),3)
        #nulis bacaan keterangan na
        msg = [[cap,x-(len(cap)*5),y]]
        n=0
        if (len(cap)*5)>(w-20):
          cap=cap.rstrip(' ')+' '
          end=0
          beg=1
          msg=[]
          while beg!=end:
            beg=end
            end+=cap[end:end+30].rfind(' ')
            s=len(cap[beg:end].lstrip(' ').rstrip(' '))
            msg.append([])
            msg[n]=[cap[beg:end].lstrip(' ').rstrip(' '),x-(s*5)]
            n+=1
          for i in range(len(msg)):
            msg[i].append((y-(h/2))+(i*((h-20)/len(msg)))+20)
        font = pygame.font.Font(None, 25)
        for i in range(len(msg)):
          text = font.render(msg[i][0],True,black)
          screen.blit(text, [msg[i][1],msg[i][2]])
        #nulis judulna
        fontt = pygame.font.Font(None, 14)
        titl = fontt.render('AMANAT!',True,white)
        screen.blit(titl, [self.topleft[0]+5,self.topleft[1]+5])
        #nulis bacaan di tombolna
        okfont = pygame.font.Font(None, 12)
        oktxt = okfont.render('Nya!',True,black)
        screen.blit(oktxt, [self.oktl[0]+30,self.oktl[1]+6])
        pygame.display.flip()
    def buang(self):
        #mun ges teu dipake piceun ti layar
        self.topleft=[-1000,-1000]
        self.bottomright=[-500,-500]
        pygame.display.flip()
    def Tunggu(self):
        #nungguan dipencet ok na
        Wait = 0
        while Wait == 0:
          for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
              mouse = pygame.mouse.get_pos()
              if self.pressed(mouse):
                Wait=1
                self.buang()
                del self
          clock.tick(10)
    def pressed(self,mouse):
        #ngabaca klik mouse mun dipencet ok na
        if mouse[0] > self.oktl[0]:
            if mouse[1] > self.oktl[1]:
                if mouse[0] < self.okbr[0]:
                    if mouse[1] < self.okbr[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False

class confirm(pygame.sprite.Sprite):
    #siga nu warnin tp 2 tombol
    def __init__(self,cap):
        pygame.sprite.Sprite.__init__(self)
        self.topleft=[]
        self.bottomright=[]
        self.oktl=[]
        self.okbr=[]
        self.cctl=[]
        self.ccbr=[]
        self.caption=cap
        x=size[0]/2
        y=size[1]/2
        w=400
        h=150
        self.topleft=[x-(w/2),y-(h/2)]
        self.bottomright=[x+(w/2),y+(h/2)]
        self.oktl=[self.bottomright[0]-80-80,self.bottomright[1]-30]
        self.okbr=[self.bottomright[0]-10-80,self.bottomright[1]-10]
        okw = self.okbr[0]-self.oktl[0]
        okh = self.okbr[1]-self.oktl[1]
        self.cctl=[self.bottomright[0]-80,self.bottomright[1]-30]
        self.ccbr=[self.bottomright[0]-10,self.bottomright[1]-10]
        ccw = self.ccbr[0]-self.cctl[0]
        cch = self.ccbr[1]-self.cctl[1]
        #popupna
        pygame.draw.rect(screen,yellow,[self.topleft[0],self.topleft[1],w,h],0)
        pygame.draw.rect(screen,grey,[self.topleft[0],self.topleft[1],w,h],3)
        pygame.draw.line(screen,black,(self.topleft[0],self.bottomright[1]),(self.bottomright[0],self.bottomright[1]),3)
        pygame.draw.line(screen,black,(self.bottomright[0],self.topleft[1]),(self.bottomright[0],self.bottomright[1]),3)
        #ok na
        pygame.draw.rect(screen,grey,[self.oktl[0],self.oktl[1],okw,okh],0)
        pygame.draw.rect(screen,white,[self.oktl[0],self.oktl[1],okw,okh],3)
        pygame.draw.line(screen,black,(self.oktl[0],self.okbr[1]),(self.okbr[0],self.okbr[1]),3)
        pygame.draw.line(screen,black,(self.okbr[0],self.oktl[1]),(self.okbr[0],self.okbr[1]),3)
        #batal na
        pygame.draw.rect(screen,grey,[self.cctl[0],self.cctl[1],ccw,cch],0)
        pygame.draw.rect(screen,white,[self.cctl[0],self.cctl[1],ccw,cch],3)
        pygame.draw.line(screen,black,(self.cctl[0],self.ccbr[1]),(self.ccbr[0],self.ccbr[1]),3)
        pygame.draw.line(screen,black,(self.ccbr[0],self.cctl[1]),(self.ccbr[0],self.ccbr[1]),3)
        #bacaan na
        msg = [[cap,x-(len(cap)*5),y]]
        n=0
        if (len(cap)*5)>(w-20):
          cap=cap.rstrip(' ')+' '
          end=0
          beg=1
          msg=[]
          while beg!=end:
            beg=end
            end+=cap[end:end+30].rfind(' ')
            s=len(cap[beg:end].lstrip(' ').rstrip(' '))
            msg.append([])
            msg[n]=[cap[beg:end].lstrip(' ').rstrip(' '),x-(s*5)]
            n+=1
          for i in range(len(msg)):
            msg[i].append((y-(h/2))+(i*((h-20)/len(msg)))+20)
        font = pygame.font.Font(None, 25)
        for i in range(len(msg)):
          text = font.render(msg[i][0],True,black)
          screen.blit(text, [msg[i][1],msg[i][2]])
        #judulna
        fontt = pygame.font.Font(None, 14)
        titl = fontt.render('CONFIRM?',True,white)
        screen.blit(titl, [self.topleft[0]+5,self.topleft[1]+5])
        #bacaan ok na
        okfont = pygame.font.Font(None, 12)
        oktxt = okfont.render('Hayu',True,black)
        screen.blit(oktxt, [self.oktl[0]+30,self.oktl[1]+6])
        #bacaan batalna
        okfont = pygame.font.Font(None, 12)
        oktxt = okfont.render('Teu Jadi',True,black)
        screen.blit(oktxt, [self.cctl[0]+25,self.cctl[1]+6])
        pygame.display.flip()
    def buang(self):
        self.topleft=[-1000,-1000]
        self.bottomright=[-500,-500]
        pygame.display.flip()
    def Tunggu(self):
        Wait = 0
        while Wait == 0:
          for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
              mouse = pygame.mouse.get_pos()
              if self.OKpressed(mouse):
                Wait=1
                self.buang()
                return True
                del self
              if self.CCpressed(mouse):
                Wait=1
                self.buang()
                return False
                del self
          clock.tick(10)
    def OKpressed(self,mouse):
        if mouse[0] > self.oktl[0]:
            if mouse[1] > self.oktl[1]:
                if mouse[0] < self.okbr[0]:
                    if mouse[1] < self.okbr[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False
    def CCpressed(self,mouse):
        if mouse[0] > self.cctl[0]:
            if mouse[1] > self.cctl[1]:
                if mouse[0] < self.ccbr[0]:
                    if mouse[1] < self.ccbr[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False

class statusbar(pygame.sprite.Sprite):
    #kelas statusbar keur bacaan dihandap
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.wid=size[0]
        self.hei=20
        self.topleft=[0,size[1]-self.hei]
        self.bottomright=[size[0],size[1]]
        self.caption=''
        pygame.draw.rect(screen,grey,[self.topleft[0],self.topleft[1],self.wid,self.hei],0)
        pygame.draw.rect(screen,black,[self.topleft[0],self.topleft[1],self.wid,self.hei],2)
        pygame.draw.line(screen,white,(self.topleft[0],self.bottomright[1]),(self.bottomright[0],self.bottomright[1]),2)
        pygame.draw.line(screen,white,(self.bottomright[0],self.topleft[1]),(self.bottomright[0],self.bottomright[1]),2)
    def update(self, text=''):
        if text!='':
          self.caption=text
        pygame.draw.rect(screen,grey,[self.topleft[0],self.topleft[1],self.wid,self.hei],0)
        pygame.draw.rect(screen,black,[self.topleft[0],self.topleft[1],self.wid,self.hei],2)
        pygame.draw.line(screen,white,(self.topleft[0],self.bottomright[1]),(self.bottomright[0],self.bottomright[1]),2)
        pygame.draw.line(screen,white,(self.bottomright[0],self.topleft[1]),(self.bottomright[0],self.bottomright[1]),2)
        font = pygame.font.Font(None, 16)
        text = font.render(self.caption,True,white)
        screen.blit(text, [(self.wid/2)-((len(self.caption)*4)/2),self.bottomright[1]-(self.hei/2)-4])
        
class createchar(pygame.sprite.Sprite):
    #kelas player keur ngagambar kartu2 di leungeun
    def __init__(self,number=0,nama='Player'):
        pygame.sprite.Sprite.__init__(self)
        self.pwid=pbr[number][0]-ptl[number][0]
        self.phei=pbr[number][1]-ptl[number][1]
        self.hands=[]
        self.ori=pori[number]
        self.number=number
        self.name=[]
        self.pname=nama
        pygame.draw.rect(screen,red,[ptl[number][0],ptl[number][1],self.pwid,self.phei],0)
        font = pygame.font.Font(None, 16)
        text = font.render(nama,True,white)
        screen.blit(text, [ptl[number][0]+(self.pwid/2)-((len(nama)*4)/2),ptl[number][1]])
    def addCard(self,l,r):
        #fungsi ker nambah kartuna
        self.hands.append([])
        self.hands[-1] = card()
        self.hands[-1].setlr(l,r)
        self.name.append(str(l)+str(r))
        if self.ori==1:
          self.hands[-1].putinto(ptl[self.number][0]+(len(self.hands)*(self.pwid-50)/7),ptl[self.number][1]+(self.phei/2),self.ori)
        else:
          self.hands[-1].putinto(ptl[self.number][0]+(self.pwid/2),ptl[self.number][1]+(len(self.hands)*(self.phei-50)/7),self.ori)
    def addHidCard(self,l,r):
        #fungsi ker nambahan kartu nu nutup
        self.hands.append([])
        self.hands[-1] = card()
        self.hands[-1].setlr(l,r)
        self.name.append(str(l)+str(r))
        if self.ori==1:
          self.hands[-1].putinto(ptl[self.number][0]+(len(self.hands)*(self.pwid-50)/7),ptl[self.number][1]+(self.phei/2),self.ori,1)
        else:
          self.hands[-1].putinto(ptl[self.number][0]+(self.pwid/2),ptl[self.number][1]+(len(self.hands)*(self.phei-50)/7),self.ori,1)
    def update(self, reveal=0):
        #ker ngarepres gambarna
        pygame.draw.rect(screen,red,[ptl[self.number][0],ptl[self.number][1],self.pwid,self.phei],0)
        font = pygame.font.Font(None, 16)
        text = font.render(self.pname,True,white)
        screen.blit(text, [ptl[self.number][0]+(self.pwid/2)-((len(self.pname)*4)/2),ptl[self.number][1]])
        for i in range(len(self.hands)):
          if reveal==0:
            self.hands[i].putinto()
          else:
            self.hands[i].putinto(-10,-5,-5,0)

class table(pygame.sprite.Sprite):
    #kelas table(meja) keur nampung kartu2nu ges maen
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ltail = [373,300,0,0,3]
        self.rtail = [427,300,0,0,1]
        self.tcards = []
        self.tctr = 0
        self.tcrl = 0
        
    def checkDir(self,x0,y0,cd,ori):
      #nentukeun arah sanggeusna
      xmove = [0,54,0,-54]
      ymove = [54,0,-54,0]
      ret = [0,0,0,0]

      #cobaan lurus
      usethis=1
      xret = x0+xmove[cd]
      yret = y0+ymove[cd]
      ret[2] = cd
      ret[3] = ori
      #cek kord mun lurus
      #mun teu liwat batas
      if xret<620 and xret>180 and yret<420 and yret>180:
        #cek bisi nabrak
        for i in range(len(self.tcards)-1):
          if xret==self.tcards[i].x and yret==self.tcards[i].y:
            #mun nabrak ulah d pake
            usethis=0
      #mun liwat batas ulah d pake
      else:
        usethis=0
      #mun can kapanggih cobaan belok kiri
      if usethis==0:
        if xmove[cd]!=0:
          xret=x0+(xmove[cd]/2)
          yret=y0-(xmove[cd]/2)
        else:
          yret=y0+(ymove[cd]/2)
          xret=x0+(ymove[cd]/2)
        usethis=2
        ret[3]=(ret[3]-1)*-1
        ret[2]=ret[2]+1
        if ret[2]>3 : ret[2]=0
        #cek kord mun belok kiri
        #mun teu liwat batas
        if xret<620 and xret>180 and yret<420 and yret>180 and usethis==2:
          #cek bisi nabrak
          for i in range(len(self.tcards)-1):
            if xret==self.tcards[i].x and yret==self.tcards[i].y:
              #mun nabrak ulah d pake
              usethis=0
        #mun liwat batas ulah d pake
        else:
          usethis=0
        #mun can kapanggih cobaan belok kanan
        if usethis==0:
          if xmove[cd]!=0:
            xret=x0+(xmove[cd]/2)
            yret=y0+(xmove[cd]/2)
          else:
            yret=y0+(ymove[cd]/2)
            xret=x0-(ymove[cd]/2)
          usethis=3
          ret[2]=cd
          ret[3]=ori
          ret[3]=(ret[3]-1)*-1
          ret[2]=ret[2]-1
          if ret[2]<0 : ret[2]=3
      #ulah waka dicobaan deui bisi hang
      ret[0]=xret
      ret[1]=yret
      return ret
         
    def addCardR(self,l,r,ori=0):
        if self.rtail[3]>0:
          cd = self.rtail[4]
          newmove = self.checkDir(self.rtail[0], self.rtail[1], cd, self.rtail[2])
          self.rtail[0]=newmove[0]
          self.rtail[1]=newmove[1]
          self.rtail[4]=newmove[2]
          self.rtail[2]=newmove[3]
        self.tcards.append(card())
        self.tcards[-1].setlr(int(l),int(r))
        if self.rtail[4] in(0,3):
          self.tcards[-1].setlr(int(r),int(l))
        self.tcards[-1].putinto(self.rtail[0], self.rtail[1],self.rtail[2],0)
        self.rtail[3]+=1
        self.tctr = len(self.tcards)-1
        
    def addCardL(self,l,r,ori=0):
        if self.ltail[3]>0:
          cd = self.ltail[4]
          newmove = self.checkDir(self.ltail[0], self.ltail[1], cd, self.ltail[2])
          self.ltail[0]=newmove[0]
          self.ltail[1]=newmove[1]
          self.ltail[4]=newmove[2]
          self.ltail[2]=newmove[3]
        self.tcards.append(card())
        self.tcards[-1].setlr(int(l),int(r))
        if self.ltail[4] in (1,2):
          self.tcards[-1].setlr(int(r),int(l))
        self.tcards[-1].putinto(self.ltail[0], self.ltail[1],self.ltail[2],0)
        self.ltail[3]+=1
        self.tctl = len(self.tcards)-1
        
    def update(self):
        for i in range(len(self.tcards)):
          self.tcards[i].putinto()
        
        
        
#---------------------
#Bagian nu Utama
#---------------------


# ngajalankeun pygame
pygame.init()
 
# Nentukeun RGB keur warna2nu dipake
black = [  0,  0,  0]
bg = [  50,  50,  50]
white = [255,255,255]
blue =  [  0,  0,255]
green = [  0,255,  0]
red =   [255,  0,  0]
grey = [150,150,150]
yellow = [255,255,0]
 
# Ngatur ukuran layar
size=[800,600]
ptl = [[(size[0]-350)/2,size[1]-140],[size[0]-120,(size[1]-350)/2],[(size[0]-350)/2,0],[0,(size[1]-350)/2]]
pbr = [[size[0]-((size[0]-350)/2),size[1]-20],[size[0],size[1]-((size[1]-350)/2)],[size[0]-((size[0]-350)/2),120],[120,size[1]-((size[1]-350)/2)]]
pori = [1,0,1,0]
screen=pygame.display.set_mode(size)

# Nulis judul window na 
pygame.display.set_caption("Gapleh By Mech4")

 
done=False
clock = pygame.time.Clock()
bgcord = initcbg()
sbar = statusbar()

#Mun can anggeus
while done==False:
    clock.tick(10)

    #variabel2 globalna
    ctr=''
    ctl=''
    deck = []
    player = [[],[],[],[]]
    isAI = [1,1,1,1]
    phavebalak = [0,0,0,0,0,0,0]
    ptable = []
    fmove=0
    lastgapleh=0
    #mimiti tampil main menu
    select = ''
    while select not in ('0','1'):
        screen.fill(bg)
        drawbg(bgcord)
        for event in pygame.event.get():
            pygame.draw.rect(screen,white,[300,50,200,400],0)
            pygame.draw.rect(screen,red,[300,50,200,400],3)
            pygame.draw.line(screen,red,(300,150),(500,150),3)
            bPlay = button()
            bPlay.putinto(400,200,180,80,'Hayu')
            bOpt = button()
            bOpt.putinto(400,300,180,80,'Pamaen')
            bExit = button()
            bExit.putinto(400,400,180,80,'Balik')
            font = pygame.font.Font(None, 25)
            text = font.render("Maen Gapleh",True,black)
            screen.blit(text, [400-(10*5),100])
            if event.type == pygame.QUIT:
                done=True
                select='0'
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if bPlay.pressed(mouse):
                    select='1'
                if bOpt.pressed(mouse):
                    select='2'
                if bExit.pressed(mouse):
                    select='0'
            pygame.display.flip()
        if select=='2':
            #Menu option na
            del bPlay
            del bOpt
            del bExit
            screen.fill(bg)
            drawbg(bgcord)
            sMsg("Saha wae nu maen ?")
            c01 = card()
            c01.setlr(1,6)
            c01.putinto(100,100,0)
            while select=='2':
                for event in pygame.event.get():
                    pygame.draw.rect(screen,white,[200,50,400,400],0)
                    pygame.draw.rect(screen,red,[200,50,400,400],3)
                    pygame.draw.line(screen,red,(200,150),(600,150),3)
                    ha = ['(Jalma)','(Lain Jalma)']
                    bPl1 = button()
                    bPl1.putinto(400,200,380,50,'Jalma 1 %s' % ha[isAI[0]])
                    bPl2 = button()
                    bPl2.putinto(400,255,380,50,'Jalma 2 %s' % ha[isAI[1]])
                    bPl3 = button()
                    bPl3.putinto(400,310,380,50,'Jalma 3 %s' % ha[isAI[2]])
                    bPl4 = button()
                    bPl4.putinto(400,365,380,50,'Jalma 4 %s' % ha[isAI[3]])
                    bBack = button()
                    bBack.putinto(400,420,380,50,'Balik')
                    font = pygame.font.Font(None, 25)
                    text = font.render("SAHA WAE NU REK MAEN",True,black)
                    screen.blit(text, [400-(14*5),100])
                    if event.type == pygame.QUIT:
                        done=True
                        select='0'
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        if c01.pressed(mouse):
                            select='0'
                        if bPl1.pressed(mouse):
                            isAI[0]=(isAI[0]-1)*-1
                            screen.fill(bg)
                            drawbg(bgcord)
                            pygame.display.flip()
                        if bPl2.pressed(mouse):
                            isAI[1]=(isAI[1]-1)*-1
                            screen.fill(bg)
                            drawbg(bgcord)
                            pygame.display.flip()
                        if bPl3.pressed(mouse):
                            isAI[2]=(isAI[2]-1)*-1
                            screen.fill(bg)
                            drawbg(bgcord)
                            pygame.display.flip()
                        if bPl4.pressed(mouse):
                            isAI[3]=(isAI[3]-1)*-1
                            screen.fill(bg)
                            drawbg(bgcord)
                            pygame.display.flip()
                        if bBack.pressed(mouse):
                            select=''
                            screen.fill(bg)
                            drawbg(bgcord)
                            pygame.display.flip()
                pygame.display.flip()
            del bPl1
            del bPl2
            del bPl3
            del bPl4
            del bBack
    #mun mulai maen
        if select=='1':
          screen.fill(bg)
          sMsg('Now Playing....')
          human=[]
          meja = table()
          for i in range(4):
            human.append(createchar(i,'Player%d' % (i+1)))
          pygame.display.flip()
          res = 10*int(select)
          while res>0:
            shuffle()
            res=playtable(res)
            for i in range(len(deck)):
              deck.pop(0)
            for i in range(len(ptable)):
              ptable.pop(0)
            for i in range(len(player)):
              for j in range(len(player[i])):
                player[i].pop(0)
            for i in range(len(meja.tcards)):
              meja.tcards.pop()
            meja.ltail = [373,300,0,0,3]
            meja.rtail = [427,300,0,0,1]
          select=''
          del human
          del meja
    isexit = cMsg('Kade Meuntas !')
    if isexit:
      done=True
    else:
      done=False
      select=''
    pygame.display.flip()
pygame.quit ()
