import json, re

with open('/tmp/elite2/catalog_raw.json',encoding='utf-8') as f:
    C=json.load(f)
with open('/tmp/elite2/merged.json',encoding='utf-8') as f:
    M=json.load(f)

# fix 3 missing SSDs
def find(cat, needles, avail='Disponível'):
    out=[]
    for it in M[cat]:
        if all(nd.lower() in it['name'].lower() for nd in needles):
            if avail and it['avail']!=avail: continue
            out.append(it)
    return sorted(out,key=lambda x:x['price'])[0] if out else None

for needles in [('X250','512GB'),('N538S',),('NM620',)]:
    it=find('ssd',needles)
    print(needles, '->', it['name'][:80], it['price'] if it else None)
    if it:
        it2=dict(it); it2['desc']=it['desc'][:220]
        C['ssd'].append(it2)
C['ssd']=sorted(C['ssd'],key=lambda x:x['price'])

# ---------- enrichment ----------
def cpu_specs(name, desc):
    t=(name+' '+desc).upper()
    sock='?'
    if 'AM5' in t: sock='AM5'
    elif 'AM4' in t or 'SKTAM4' in t: sock='AM4'
    elif 'LGA1700' in t or 'LGA 1700' in t or '1700' in name: sock='LGA1700'
    elif '1851' in t: sock='LGA1851'
    elif '1200' in t: sock='LGA1200'
    brand='AMD' if 'RYZEN' in t or 'AMD' in t else ('Intel' if 'INTEL' in t or 'CORE I' in t else '?')
    cores=None
    m=re.search(r'(\d+)\s*(?:N[ÚU]CLEOS?|CORE)',name,re.I)
    if m: cores=int(m.group(1))
    # TDP estimate
    tdp=65
    if re.search(r'9950X|9800X3D|7800X3D|7900X?|9900X|14700',name): tdp=120 if 'X3D' in name else (170 if '9950' in name else 125)
    elif re.search(r'9700X|7700X|7700 |9600X|7600X',name): tdp=105 if 'X' in name.split()[-1][:2] else 65
    elif '4100' in name or '4500' in name or '12100F' in name: tdp=65
    igpu = bool(re.search(r'RADEON GRAPHICS|RADEON 7|RADEON VEGA|760M|740M|Radeon',name,re.I)) and 'F' not in re.search(r'(12100F|8400F|5500)',name).group(0) if re.search(r'(12100F|8400F|5500)',name) else bool(re.search(r'RADEON|GRAPHICS|GRAF',t))
    if '12100F' in name or '8400F' in name: igpu=False
    return {'socket':sock,'brand':brand,'cores':cores,'tdp':tdp,'igpu':igpu}

def mb_specs(name):
    t=name.upper()
    if 'AM5' in t: sock='AM5'
    elif 'AM4' in t: sock='AM4'
    elif '1851' in t: sock='LGA1851'
    elif '1700' in t or 'H610' in t or 'B760' in t or 'Z790' in t: sock='LGA1700'
    elif '1200' in t or 'H510' in t or 'B560' in t: sock='LGA1200'
    else: sock='?'
    ddr='DDR5' if 'DDR5' in t or re.search(r'D5\b',t) or 'D 5' in name else 'DDR4'
    if 'MICRO' in t or re.search(r'\bM-ATX\b|MATX|M\.ATX|A520M|B550M|H610M|B760M|A620',t): form='mATX'
    elif re.search(r'\bATX\b',t): form='ATX'
    elif 'ITX' in t: form='ITX'
    else: form='mATX'
    wifi='WIFI' in t or 'WI-FI' in t
    return {'socket':sock,'ddr':ddr,'form':form,'wifi':wifi}

def ram_specs(name):
    t=name.upper()
    ddr='DDR5' if 'DDR5' in t else 'DDR4'
    m=re.search(r'(\d+)\s*GB',t)
    cap=int(m.group(1)) if m else 0
    m2=re.search(r'(\d{4})\s*MHZ',t)
    speed=int(m2.group(1)) if m2 else 0
    kit='2X' in t.replace(' ','') or '(2X' in t
    return {'ddr':ddr,'cap':cap,'speed':speed,'kit':kit}

def gpu_specs(name):
    t=name.upper()
    m=re.search(r'(\d+)\s*GB',t)
    vram=int(m.group(1)) if m else 0
    # power estimate
    w=75
    if 'RTX 5070' in t or 'RX 9070' in t: w=220
    elif 'RTX 5060 TI' in t or 'RTX5060 TI' in t: w=180
    elif 'RTX 4060 TI' in t: w=160
    elif 'RTX 4060' in t or 'RTX5060 SHADOW' in t: w=130
    elif 'RTX 3060' in t: w=170
    elif 'RTX 3050' in t: w=130
    elif 'RX 6500' in t: w=107
    elif 'RX 550' in t: w=50
    elif 'GT 1030' in t: w=30
    elif 'A1000' in t: w=50
    tier='office' if w<=60 else ('entry' if w<=130 else ('mid' if w<=180 else 'high'))
    return {'vram':vram,'watts':w,'tier':tier}

def ssd_specs(name):
    t=name.upper()
    cap=0
    m=re.search(r'(\d+(?:\.\d+)?)\s*TB',t)
    m2=re.search(r'(\d+)\s*GB',t)
    if m: cap=int(float(m.group(1))*1000)
    elif m2: cap=int(m2.group(1))
    nvme='NVME' in t or 'SN580' in t or 'SN850' in t or '990 PRO' in t or 'LEGEND' in t or 'G930' in t or 'NM620' in t or 'SX8200' in t or 'P300' in t or 'PX500' in t or 'PX600' in t
    ff='M.2' if ('M.2' in t or 'M2' in t or nvme) else '2.5"'
    return {'cap':cap,'nvme':nvme,'form':ff}

def psu_specs(name):
    t=name.upper()
    m=re.search(r'(\d{3,4})\s*W',t)
    w=int(m.group(1)) if m else 0
    cert='80+ Gold' if 'GOLD' in t or '80P GOLD' in t else ('80+ Bronze' if 'BRONZE' in t else ('80+ Platinum' if 'PLATIN' in t else 'Standard'))
    mod='MODULAR' in t
    return {'watts':w,'cert':cert,'modular':mod}

def case_specs(name):
    t=name.upper()
    # support: most ATX mid towers support ATX/mATX/ITX; mATX-only cases support mATX/ITX
    if re.search(r'MICRO-?ATX|M60 |SILENTHILL|M100R|MIR B200',t) and 'ATX' not in t.replace('MICRO ATX','').replace('MICRO-ATX',''):
        sup=['mATX','ITX']; size='mATX'
    else:
        sup=['ATX','mATX','ITX']; size='ATX'
    if 'FULL TOWER' in t or 'ABYSS' in t: size='Full-ATX'
    glass='VIDRO' in t or 'TEMPER' in t or 'TG ' in t or 'FLOW' in t or 'FORGE' in t
    rgb='RGB' in t or 'ARGB' in t
    return {'support':sup,'size':size,'glass':glass,'rgb':rgb}

def cooler_specs(name, desc):
    t=(name+' '+desc).upper()
    water='WATER' in t or 'LIQUID' in t or 'CORELIQUID' in t or 'ICEBURG' in t or 'ICE CHILL' in t
    m=re.search(r'(\d+)\s*W\s*TDP|TDP\s*(\d+)W',t)
    tdp=int(m.group(1) or m.group(2)) if m else (250 if water and '240' in t else (150 if water else 100))
    if 'NH-U14S' in name: tdp=220
    elif 'H-224' in name: tdp=180
    elif 'SIGMA 540' in t: tdp=200
    socks=[]
    for s in ['AM5','AM4','AM3','LGA1700','LGA1200','LGA115','1700','1200','115X']:
        if s in t.replace(' ',''): socks.append(s)
    if 'INTEL/AMD' in t.replace(' ','') or 'COMPAT' in t: socks=['AM4','AM5','LGA1700','LGA1200']
    if 'WRAITH' in t: socks=['AM4','AM5']
    rgb='RGB' in t or 'ARGB' in t
    return {'water':water,'tdp':tdp,'sockets':socks,'rgb':rgb}

ENRICHED={}
for cat, items in C.items():
    out=[]
    for it in items:
        spec={}
        if cat=='cpu': spec=cpu_specs(it['name'],it['desc'])
        elif cat=='motherboard': spec=mb_specs(it['name'])
        elif cat=='ram': spec=ram_specs(it['name'])
        elif cat=='gpu': spec=gpu_specs(it['name'])
        elif cat=='ssd': spec=ssd_specs(it['name'])
        elif cat=='psu': spec=psu_specs(it['name'])
        elif cat=='case': spec=case_specs(it['name'])
        elif cat=='cooler': spec=cooler_specs(it['name'],it['desc'])
        it2=dict(it); it2['spec']=spec
        out.append(it2)
    ENRICHED[cat]=out

# print verification
for cat, items in ENRICHED.items():
    print('='*30, cat)
    for it in items:
        print(f"  {it['name'][:70]:70} -> {it['spec']}")

with open('/home/user/work/catalog.json','w',encoding='utf-8') as f:
    json.dump(ENRICHED,f,ensure_ascii=False,indent=1)
print('saved catalog.json')
