"""Render Experimentopedia Markdown from tools/rows.json and tools/pages.json."""
import json,re,os,collections
B=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows=json.load(open(os.path.join(B,'tools/rows.json'))); pages=json.load(open(os.path.join(B,'tools/pages.json')))
def clean(s):
    s=re.sub(r'<ref[^>]*/>|<ref.*?</ref>','',s,flags=re.S)
    s=re.sub(r'\{\{[Qq]uote\|.*?\}\}','',s,flags=re.S)
    for _ in range(3): s=re.sub(r'\{\{[^{}]*\}\}','',s)
    s=re.sub(r'\[\[(?:File|Image):[^\]]*\]\]','',s)
    s=re.sub(r'\[\[[^|\]]*\|([^\]]*)\]\]',r'\1',s); s=re.sub(r'\[\[([^\]]*)\]\]',r'\1',s)
    s=re.sub(r'\[https?://\S+ ([^\]]*)\]',r'\1',s)
    s=re.sub(r"'{2,}",'',s); s=re.sub(r'<br\s*/?>','; ',s); s=re.sub(r'<[^>]+>','',s)
    s=s.replace('&nbsp;',' ')
    return re.sub(r'[ \t]+',' ',s).strip()
def name(r): return clean(r['name']) if r['name'].strip() not in ('','N/A') else ''
def slug(r): return r['num']
def infobox(t,k):
    m=re.search(r'\n\|\s*'+k+r'\s*=\s*(.*)',t); return clean(m.group(1)).strip('; ') if m else ''
def section(t,h):
    m=re.search(r'\n===?'+h+r'===?\n(.*?)(?=\n==)',t,re.S); 
    if not m: return ''
    paras=[clean(p) for p in m.group(1).split('\n') if p.strip() and not p.startswith(('[[File','{|','|','!'))]
    return '\n\n'.join(p for p in paras if p)
def sents(s): return re.split(r'(?<=[.!?])\s+(?=[A-Z])',s.strip())
CATS=[('weather','Weather and nature',r'weather|rain|snow|storm|wind|cloud|temperature|heat|cold|ice|freez|volcan|lava|water|ocean|wave|tornado|lightning'),
('destructive','Destruction and devouring',r'destroy|destruct|explo|demolish|devour|eat |eats|consum|bomb|weapon|battle|army|fight|attack|crush|smash'),
('mind','Mind, emotion and senses',r'hypno|mind|emotion|dream|memor|sleep|happy|sad|anger|angry|fear|love|cry|laugh|thought|telepath|illusion|insult|bad luck'),
('tech','Technology and science',r'electric|computer|machine|gravity|time|energy|power|magnet|radio|signal|technolog|robot|virus|teleport|portal|dimension'),
('body','Shapeshifting, size and duplication',r'shape|transform|size|shrink|grow|clone|duplicat|multipl|copy|disguise|invisib|mimic|stretch'),
('mischief','Mischief and civic disturbance',r'prank|annoy|mischief|steal|thief|mess|chaos|trick|disturb|noise|stink|smell|itch|traffic|loud|sneez'),
('helpful','Helpful and household',r'help|clean|cook|fix|repair|household|garden|chore|heal|cure|serve|wash|build')]
os.makedirs(os.path.join(B,'experiments'),exist_ok=True); os.makedirs(os.path.join(B,'categories'),exist_ok=True); os.makedirs(os.path.join(B,'series'),exist_ok=True)
NOTE='Little canonical info: this experiment is listed in official sources (often only in the Leroy & Stitch finale lineup, end credits, or the Stitch! anime) but the shows and films never explain what it looks like or does. Nothing has been invented to fill the gap.'
TRANS=[]
TRX=r'transmut|mutated form|mutated [A-Z]|2\.0|Delia (?:altered|modified)|was modified|third season of the|Neo-PowerChip|Powercell'
def transmuted(t):
    out=[]
    for para in t.split('\n'):
        if para.startswith(('[[File','|','{','!')): continue
        for x in sents(clean(para)):
            if re.search(TRX,x) and 'mutated cross' not in x and 'Disney Infinity' not in x and len(x)>30 and not re.search(r'\.(jpg|png|gif)|screenCapture',x,re.I) and x.lstrip('*') not in out: out.append(x.lstrip('* '))
    return out[:12]
cat_members=collections.defaultdict(list); ser_members=collections.defaultdict(list); stats=collections.Counter(); alpha=[]
for r in rows:
    nm=name(r); title=f"Experiment {r['num']}"+(f": {nm}" if nm else '')
    t=pages.get(r.get('page',''),''); desc=clean(r['desc'])
    level='well-documented' if t else ('partial' if desc else 'sparse'); stats[level]+=1
    L=[f"# {title}",'',f"- Number: {r['num']}",f"- Name: {nm or 'No name given in canon'}",f"- Series: {r['series']}",f"- Pod color: {clean(r['pod']) or 'Not shown'}",f"- First listed in: {clean(r['eps']) or 'Unknown'}",f"- How much is known: {level}",'']
    occ=infobox(t,'occupation') if t else ''
    lead=''
    if t:
        m=re.search(r"\n'''.*?\n",t); lead=clean(m.group(0)) if m else ''
    blob=' '.join([desc,occ,lead]).lower()
    if not desc and not t:
        L+=['## Summary','',NOTE,'']
    else:
        L+=['## Summary','']
        if occ: L+=[f"Primary function: {occ}.",'']
        if lead: L+=[lead,'']
        elif desc: L+=[desc,'']
        app=section(t,'Physical appearance') if t else ''
        if app: L+=['## Appearance','',app,'']
        elif desc: L+=['## Appearance and abilities (from the experiment list)','',desc,'']
        pw=section(t,'Powers and abilities') or section(t,'Special [Aa]bilities') if t else ''
        if t: pw=pw or infobox(t,'powers')
        if pw: L+=['## Powers and abilities','',pw,'']
        wk=section(t,'Weaknesses') if t else ''
        if wk: L+=['## Weaknesses','',wk,'']
        pe=section(t,'Personality') if t else ''
        if pe: L+=['## Personality','',pe,'']
        lk=infobox(t,'likes') if t else ''; dl=infobox(t,'dislikes') if t else ''
        if lk or dl: L+=['## Likes and dislikes','']+([f"- Likes: {lk}"] if lk else [])+([f"- Dislikes: {dl}"] if dl else [])+['']
        otp=[s for s in sents(lead+' '+desc) if 'one true place' in s.lower()]
        L+=['## One true place','',otp[0] if otp else 'Not stated in canon.','']
        bg=section(t,'Background') if t else ''
        if bg: L+=['## Original purpose and background','',bg,'']
        if t:
            m=re.search(r'\n==Appearances==\n(.*?)(?=\n==[^=])',t,re.S)
            if m:
                ap=re.sub(r'\n===([^=]+)===\n',lambda x:'\n\n### '+clean(x.group(1))+'\n\n','\n'+m.group(1))
                ap='\n'.join((clean(l) if not l.startswith('###') else l) for l in ap.split('\n') if not re.match(r'^\s*[\]\}|]+\s*$',l) and not l.startswith(('[[File','{|','|-','!')))
                L+=['## Appearances and how Lilo and Stitch met it','',re.sub(r'\n{3,}','\n\n',ap).strip(),'']
            vo=infobox(t,'voice')
            tv=section(t,'Trivia') if False else ''
            m=re.search(r'\n==Trivia==\n(.*?)(?=\n==[^=])',t,re.S)
            tr=[clean(x) for x in re.findall(r'^\*+(.*)',m.group(1),re.M)] if m else []
            if vo or tr: L+=['## Trivia','']+([f"- Voice: {vo}"] if vo else [])+[f"- {x}" for x in tr if x]+['']
    tm=transmuted(t) if t and r['num']!='262' else []
    if tm:
        L+=['## Transmuted or altered form (Stitch! anime)','','In the Stitch! anime, Hämsterviel transmuted many experiments into evil minions (often marked with a yellow H on the forehead), and in season 3 Delia altered experiments to make them stronger, shown in the "2.0" episodes. Facts found for this experiment:','']+[f"- {x}" for x in tm]+['']
        TRANS.append((r,title))
    L+=['---','',"[Back to index](../INDEX.md)",'','Source: adapted from the Disney Wiki (disney.fandom.com) Experiments list'+(f" and the \"{r['page']}\" article" if t else '')+', licensed CC BY-SA. Unofficial fan reference.']
    open(os.path.join(B,'experiments',r['num']+'.md'),'w').write('\n'.join(L)+'\n')
    link=f"[{title}](experiments/{r['num']}.md)"
    ser_members[r['series']].append((r,title,level))
    if nm: alpha.append((nm,r,title))
    hit=False
    if desc or t:
        for k,lab,rx in CATS:
            if re.search(rx,blob): cat_members[k].append((r,title)); hit=True
        if not hit: cat_members['other'].append((r,title))
    else: cat_members['unknown'].append((r,title))
labels=dict((k,l) for k,l,_ in CATS); labels['other']='Other or unusual functions'; labels['unknown']='Function unknown (little canonical info)'
for k,mem in cat_members.items():
    open(os.path.join(B,'categories',k+'.md'),'w').write(f"# {labels[k]}\n\nSorted automatically by keywords in each experiment's description, so some experiments appear in more than one category.\n\n"+'\n'.join(f"- [{t}](../experiments/{r['num']}.md)" for r,t in mem)+"\n\n[Back to index](../INDEX.md)\n")
sfiles=[]
for i,(s,mem) in enumerate(ser_members.items()):
    fn=f"series-{s[0]}.md"; sfiles.append((s,fn,len(mem)))
    open(os.path.join(B,'series',fn),'w').write(f"# {s}\n\n"+'\n'.join(f"- [{t}](../experiments/{r['num']}.md) ({lv})" for r,t,lv in mem)+"\n\n[Back to index](../INDEX.md)\n")
alpha.sort(key=lambda x:x[0].lower())
open(os.path.join(B,'ALPHABETICAL.md'),'w').write("# Alphabetical index of named experiments\n\n"+'\n'.join(f"- {n}: [Experiment {r['num']}](experiments/{r['num']}.md)" for n,r,t in alpha)+"\n\n[Back to index](INDEX.md)\n")
I=["# Experimentopedia index","",f"{len(rows)} experiments. {stats['well-documented']} well-documented (own wiki article), {stats['partial']} partial (a description in the official list), {stats['sparse']} sparse (little canonical info).","","## Browse","","- [Alphabetical index of named experiments](ALPHABETICAL.md)","","## By series",""]
I+=[f"- [{s}](series/{fn}) ({n})" for s,fn,n in sfiles]+['','## By function','']
I+=[f"- [{labels[k]}](categories/{k}.md) ({len(m)})" for k,m in cat_members.items()]+['','## All experiments by number','']
I+=[f"- [{t}](experiments/{r['num']}.md)" for s in ser_members for r,t,lv in ser_members[s]]
open(os.path.join(B,'INDEX.md'),'w').write('\n'.join(I)+'\n'); print(stats)

extra=json.load(open(os.path.join(B,'tools/extra.json')))
os.makedirs(os.path.join(B,'special'),exist_ok=True); SP=[]
for pg,fn,intro in [('Dark End','dark-end','Unnumbered experiment made by Delia from Stitch-like blueprints; the final villain of Stitch! anime season 3.'),('Skunkuna','skunkuna','Experiment made by Hämsterviel, not Jumba, in the Stitch! anime.'),('Leroy Clones','leroy-clones','Clones of Experiment 629 (Leroy) made by Hämsterviel in Leroy & Stitch.')]:
    t=extra.get(pg)
    if not t: continue
    L=[f"# {pg}",'',intro,'']
    m=re.search(r"\n'''.*?\n",t)
    if m: L+=['## Summary','',clean(m.group(0)),'']
    for h,lab in [('Physical appearance','Appearance'),('Powers and abilities','Powers and abilities'),('Weaknesses','Weaknesses'),('Personality','Personality'),('Background','Background')]:
        x=section(t,h)
        if x: L+=[f"## {lab}",'',x,'']
    m=re.search(r'\n==Appearances==\n(.*?)(?=\n==[^=])',t,re.S)
    if m:
        ap=[('### '+clean(l.strip('= ')) if l.startswith('===') else clean(l)) for l in m.group(1).split('\n') if l.strip() and not l.startswith(('[[File','{|','|','!')) and not re.match(r'^\s*[\]\}]+\s*$',l)]
        L+=['## Appearances and how it was resolved','','\n\n'.join(a for a in ap if a),'']
    L+=['---','','[Back to index](../INDEX.md)','',f'Source: adapted from the Disney Wiki "{pg}" article, CC BY-SA. Unofficial fan reference.']
    open(os.path.join(B,'special',fn+'.md'),'w').write('\n'.join(L)+'\n'); SP.append((pg,fn))
open(os.path.join(B,'categories','transmuted.md'),'w').write("# Transmuted experiments (Stitch! anime)\n\nIn the Stitch! anime (2008 to 2011), Hämsterviel transmuted many of Jumba's experiments into stronger, evil minions, usually leaving a yellow H mark on the forehead. In season 3, Delia altered experiments further; those episodes are titled with \"2.0\". The anime is generally treated as non-canon to the Western series. Only experiments whose sources describe a changed form are listed; each page has a section called Transmuted or altered form.\n\n## Numbered experiments with a transmuted or altered form\n\n"+'\n'.join(f"- [{t}](../experiments/{r['num']}.md)" for r,t in TRANS)+"\n\n## Creations outside Jumba's numbering\n\n"+'\n'.join(f"- [{n}](../special/{f}.md)" for n,f in SP)+"\n\n[Back to index](../INDEX.md)\n")
I=open(os.path.join(B,'INDEX.md')).read().replace('## By series','## Stitch! anime and unnumbered creations\n\n- [Transmuted experiments (Stitch! anime)](categories/transmuted.md) ('+str(len(TRANS))+')\n'+'\n'.join(f"- [{n}](special/{f}.md)" for n,f in SP)+'\n\n## By series',1)
open(os.path.join(B,'INDEX.md'),'w').write(I); print('transmuted',len(TRANS),'special',SP)
