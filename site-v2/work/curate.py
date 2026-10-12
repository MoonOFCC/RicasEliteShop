import json, re

with open('/tmp/elite2/merged.json',encoding='utf-8') as f:
    M=json.load(f)

def find(cat, needles, avail='Disponível'):
    out=[]
    for it in M[cat]:
        n=it['name']
        if all(nd.lower() in n.lower() for nd in needles):
            if avail and it['avail']!=avail: continue
            out.append(it)
    out=sorted(out,key=lambda x:x['price'])
    return out[0] if out else None

PICKS = {
 'cpu': [
   ('Ryzen 3 4100',),('i3-12100F',),('Ryzen 5 4500',),('Ryzen 5 5500 AM4 6-Core',),
   ('Ryzen 5 5600 4.4GHz',),('5650G',),('8400F',),('7600X',),('9600X',),
   ('Ryzen 7 7700 AM5 3.8GHz/5.3GHz 8',),('9700X AM5 8-Core 5.5GHz',),('i7-14700 20-Core',),
   ('7800X3D',),('9800X3D',),
 ],
 'motherboard': [
   ('A520M-A PRO',),('A520M-HVS AM4, DDR4, M.2',),('PRO H610M-E DDR4',),('H610M-HDV/M.2+ D5 LGA 1700, DDR5',),
   ('A620AM-HVS',),('PRO H610M-E DDR5',),('B550M PRO',),('B760M-HDV/M.2 D4',),
   ('A620M-HDV/M.2 Socket AM5',),('PRO B760M-P D5',),('PRO B760-P II',),('B760 Gaming Plus WiFi',),
 ],
 'ram': [
   ('Netac','8GB 3200',),('Netac','16GB 3200',),('Fury Beast 8GB DDR4 3200',),('Delta RGB 8GB DDR4',),
   ('GR3200D464L22/16G',),('FURY Beast RGB 16GB DDR4 3200',),('KF432C16BB1/16',),
   ('PNY 16GB DDR5 4800',),('VULCAN (2x8GB)',),('Adata DIMM-DDR5 16GB 5600',),
   ('FURY Beast RGB DDR5 16GB 5600MHz CL36',),('Goodram Black V Silver',),
 ],
 'gpu': [
   (('GT 1030 2GB',),'Disponível'),(('RX 550 4GB',),'Disponível'),(('RX 6500 XT 8GB',),'Disponível'),
   (('RTX 5060 Ti 8GB VENTUS',),'Disponível'),(('RTX 4060 Ti VENTUS',),'Disponível'),(('RX 9070 GV-R9070GAMING',),'Disponível'),
   (('AFOX RTX 3050 8GB',),'Esgotado'),(('Phoenix RTX 3050',),'Esgotado'),(('RTX 3060 WindForce OC Rev.2 12GB',),'Esgotado'),
   (('DUAL-RTX4060-O8G',),'Esgotado'),(('RTX5060 SHADOW 2X OC',),'Esgotado'),(('RTX 5070 Eagle OC',),'Esgotado'),
 ],
 'ssd': [
   ('Emtec X150','240GB',),('Netac G930 256GB NVMe',),('SU650 240GB',),('Emtec X150','480GB',),
   ('Emtec X250 512GB',),('N538S 1TB',),('TeamGroup CX2 256GB',),('Lexar NM620 256GB',),
   ('SN580 500GB',),('SX8200 Pro','1TB',),('NV3 1TB',),('990 Pro 1TB',),
 ],
 'psu': [
   ('BASIC 500GR',),('Powerline3 Black',),('Gaming Unyka',),('Hyper 80+ Pro 550W',),
   ('CoolPower 650W',),('Unyka 500W ATX 80+ Bronze',),('DeepGaming 650W 80+ Bronze',),
   ('GP-650WHITE',),('Urano VX 750W',),('GM-700 700W',),('Urano TX 850W',),
   ('Hummer X 750W',),('MAG A750GL',),
 ],
 'case': [
   ('SilentHill H606, Silenciosa',),('M60 Black',),('Infinity ATOM RGB',),('MIR 100 ATX',),
   ('RockStar 2',),('Typhoon COC',),('MeshBox Pro',),('Infinity ATX, Design Modular',),
   ('Focus G Midi',),('Brufen C1',),('MAG Forge M100R, Midi',),('H6 Flow',),
 ],
 'cooler': [
   ('E80 - Silencioso',),('E126RGB',),('MCPU120',),('Wraith Prism',),
   ('H-123 PRO',),('SH4-A96',),('Sigma 540 ARGB',),('Sigma 540 BK',),
   ('H-224 ARGB',),('Ice Chill 120',),('IceBurg 240',),('CoreLiquid A13 240',),('NH-U14S',),
 ],
}

CATALOG={}
miss=[]
for cat, lst in PICKS.items():
    CATALOG[cat]=[]
    for entry in lst:
        if cat=='gpu':
            needles, av = entry
            it=find(cat, needles, avail=av)
        else:
            it=find(cat, entry, avail='Disponível')
        if it is None:
            miss.append((cat,entry)); continue
        # trim desc
        it2=dict(it); it2['desc']=it['desc'][:220]
        CATALOG[cat].append(it2)

print('miss:',miss)
for cat, items in CATALOG.items():
    print(f"{cat}: {len(items)}")
    for it in items:
        print(f"  {it['price']:8.2f} | {it['avail']:10} | {it['name'][:90]}")

with open('/tmp/elite2/catalog_raw.json','w',encoding='utf-8') as f:
    json.dump(CATALOG,f,ensure_ascii=False,indent=1)
print('saved raw')
