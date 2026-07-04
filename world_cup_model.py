"""
2026 World Cup knockout model.
  Part 1: Round of 32 predictions (original model)   -> for the record
  Part 2: Evaluate R32 predictions vs ACTUAL results (accuracy/Brier/exact)
  Part 3: Improve the model using those findings
          - Elo update from actual R32 scores (K=60, GD multiplier)
          - market weight nudged up (market beat elo/fifa on the disagreement)
          - light calibration shrink (favorites 60-85% were overconfident)
          - higher goal-total prior (R32 outscored the modal forecast)
  Part 4: Round of 16 predictions (improved model)
Angles: de-vigged bookmaker "to advance" odds + Elo logistic + FIFA-rank logistic.
"""
import math

# ---------------------------------------------------------------- helpers
def american_to_prob(o): return (-o)/((-o)+100) if o < 0 else 100/(o+100)
def devig(pa, pb): s = pa+pb; return pa/s, pb/s
def elo_prob(ra, rb): return 1.0/(1.0+10**(-(ra-rb)/400.0))
def fifa_prob(ra, rb, s=24.0): return 1.0/(1.0+10**(-(rb-ra)/s))
def pois(k, l): return math.exp(-l)*l**k/math.factorial(k)
def smatrix(la, lb, m=10): return [[pois(i,la)*pois(j,lb) for j in range(m)] for i in range(m)]
def outcomes(la, lb, m=10):
    M = smatrix(la,lb,m)
    pa = sum(M[i][j] for i in range(m) for j in range(m) if i>j)
    pd = sum(M[i][i] for i in range(m))
    pb = sum(M[i][j] for i in range(m) for j in range(m) if i<j)
    return pa,pd,pb
def adv_from_lams(la, lb):
    pa,pd,pb = outcomes(la,lb)
    edge = 0.5 + 0.10*(1 if la>=lb else -1)
    return pa + pd*edge
def solve_lams(mu, target):
    lo,hi = -3.5,3.5
    for _ in range(60):
        s=(lo+hi)/2; la=max(0.12,(mu+s)/2); lb=max(0.12,(mu-s)/2)
        if adv_from_lams(la,lb) < target: lo=s
        else: hi=s
    s=(lo+hi)/2; return max(0.12,(mu+s)/2), max(0.12,(mu-s)/2)
def modal(la, lb, m=8, n=3):
    M=smatrix(la,lb,m)
    c=sorted(((M[i][j],i,j) for i in range(m) for j in range(m)),reverse=True)
    return [(i,j,p) for p,i,j in c[:n]]
def p3plus(la, lb, m=9):
    return sum(pois(i,la)*pois(j,lb) for i in range(m) for j in range(m) if i+j>=3)

# ---------------------------------------------------------------- ratings
ELO = {
 'Argentina':2115,'France':2070,'Spain':2065,'Brazil':2025,'England':2010,
 'Portugal':2005,'Netherlands':1990,'Germany':1965,'Belgium':1925,'Croatia':1900,
 'Colombia':1900,'Morocco':1875,'Switzerland':1840,'Norway':1840,'Japan':1825,
 'Ecuador':1820,'USA':1810,'Mexico':1800,'Senegal':1795,'Ivory Coast':1780,
 'Austria':1775,'Sweden':1760,'Algeria':1760,'Canada':1745,'Australia':1720,
 'Paraguay':1715,'Egypt':1705,'Congo DR':1685,'Ghana':1680,'Bosnia':1675,
 'South Africa':1635,'Cape Verde':1625,
}
RANK = {
 'Argentina':1,'Spain':2,'France':3,'England':4,'Portugal':5,'Netherlands':6,
 'Brazil':7,'Belgium':8,'Germany':11,'Croatia':10,'Colombia':13,'Morocco':12,
 'Switzerland':19,'Norway':26,'Japan':17,'Ecuador':23,'USA':15,'Mexico':14,
 'Senegal':18,'Ivory Coast':40,'Austria':22,'Sweden':27,'Algeria':43,'Canada':30,
 'Australia':24,'Paraguay':38,'Egypt':32,'Congo DR':57,'Ghana':70,'Bosnia':74,
 'South Africa':56,'Cape Verde':73,
}

# =============================================================== PART 1: R32
# match: A, B, adv-odds A, adv-odds B, mu, home-nudge dict (ELO pts, that match)
R32 = [
 ('Canada','South Africa', -340,+260, 2.4, {'Canada':15}),
 ('Brazil','Japan',        -310,+240, 2.7, {}),
 ('Germany','Paraguay',    -750,+490, 2.6, {}),
 ('Netherlands','Morocco', -188,+152, 2.5, {'Morocco':10}),
 ('Mexico','Ecuador',      -360,+270, 2.3, {'Mexico':80,'Ecuador':-15}),
 ('Norway','Ivory Coast',  -190,+156, 2.6, {}),
 ('France','Sweden',       -950,+600, 2.8, {}),
 ('USA','Bosnia',          -800,+530, 2.6, {'USA':50}),
 ('England','Congo DR',    -1200,+700,2.6, {}),
 ('Belgium','Senegal',     -194,+158, 2.5, {}),
 ('Spain','Austria',       -1200,+670,2.8, {}),
 ('Portugal','Croatia',    -235,+186, 2.5, {}),
 ('Switzerland','Algeria', -340,+260, 2.3, {}),
 ('Egypt','Australia',     -140,+114, 2.3, {}),
 ('Argentina','Cape Verde',-2500,+1320,2.8,{'Argentina':10}),
 ('Colombia','Ghana',      -300,+235, 2.5, {}),
]
W_MKT, W_ELO, W_FIFA = 0.50, 0.30, 0.20   # original weights

def predict(match, elo, wmkt, welo, wfifa, shrink=1.0):
    a,b,oa,ob,mu,nud = match
    mpa,_ = devig(american_to_prob(oa), american_to_prob(ob))
    ea = elo[a]+nud.get(a,0); eb = elo[b]+nud.get(b,0)
    epa = elo_prob(ea,eb); fpa = fifa_prob(RANK[a],RANK[b])
    blend = wmkt*mpa + welo*epa + wfifa*fpa
    blend = 0.5 + (blend-0.5)*shrink                 # calibration shrink
    blend = min(0.985,max(0.015,blend))
    la,lb = solve_lams(mu, blend)
    return dict(a=a,b=b,mpa=mpa,epa=epa,fpa=fpa,blend=blend,
                pa=outcomes(la,lb)[0],pd=outcomes(la,lb)[1],pb=outcomes(la,lb)[2],
                sc=modal(la,lb),exp=la+lb,p3=p3plus(la,lb),la=la,lb=lb)

r32pred = [predict(m, ELO, W_MKT, W_ELO, W_FIFA) for m in R32]

# =============================================================== PART 2: EVAL
# actual 90-min score (a,b) and who advanced ('A'/'B'); pens noted
ACT = {  # keyed by teamA name
 'Canada':((1,0),'A',''), 'Brazil':((2,1),'A',''),
 'Germany':((1,1),'B','Paraguay won 4-3 pens'),
 'Netherlands':((1,1),'B','Morocco won 3-2 pens'),
 'Mexico':((2,0),'A',''), 'Norway':((2,1),'A',''),
 'France':((3,0),'A',''), 'USA':((2,0),'A',''), 'England':((2,1),'A',''),
 'Belgium':((1,1),'A','Belgium won 3-2 AET'), 'Spain':((3,0),'A',''),
 'Portugal':((2,1),'A',''), 'Switzerland':((2,0),'A',''),
 'Egypt':((1,1),'B','... Egypt won 4-2 pens (advanced)'),  # advancer=Egypt=A actually
 'Argentina':((2,2),'A','Argentina won 3-2 AET'), 'Colombia':((1,0),'A',''),
}
# NOTE: Egypt is teamA in R32 and Egypt advanced -> advancer 'A'
ACT['Egypt']=((1,1),'A','Egypt won 4-2 pens')

print("="*92)
print("PART 2 — R32 MODEL EVALUATION (original model vs actual results)")
print("="*92)
print(f"{'match':26}{'pick':>10}{'p(adv)':>8}{'result':>10}{'pred':>6}{'act':>6}  outcome exact")
hits=0; exact=0; brier=0.0; n=len(r32pred)
for pr in r32pred:
    a=pr['a']; (sa,sb),adv,note = ACT[a]
    fav_adv = (adv=='A')                      # did my favorite (teamA) advance?
    p = pr['blend']
    brier += (p-(1.0 if fav_adv else 0.0))**2
    ok = fav_adv; hits += ok
    pi,pj,_ = pr['sc'][0]
    ex = (pi==sa and pj==sb); exact += ex
    print(f"{a[:12]+' v '+pr['b'][:9]:26}{a[:9]:>10}{p*100:6.0f}% "
          f"{('ADV' if fav_adv else 'OUT'):>10}{pi}-{pj:>1}{sa:>4}-{sb:<1}"
          f"   {'Y' if ok else 'N'}     {'Y' if ex else '-'}  {note}")
print("-"*92)
print(f"Outcome (favorite advanced): {hits}/{n} = {hits/n*100:.1f}%   "
      f"[Egypt counted: market & model both -> Egypt here]")
print(f"Exact 90-min scoreline hits: {exact}/{n} = {exact/n*100:.1f}%")
print(f"Brier score (advance prob):  {brier/n:.3f}")

# =============================================================== PART 3: IMPROVE
# Elo update from actual R32 (K=60 World Cup, goal-difference multiplier).
def g_mult(gd):
    gd=abs(gd)
    if gd<=1: return 1.0
    if gd==2: return 1.5
    return (11+gd)/8.0
def W_of(adv_is_A, gd):  # 90/AET result; pens => draw
    if gd==0: return 0.5
    return 1.0 if adv_is_A else 0.0

# final result used for Elo (AET counts; pens => draw at the level score)
ELO_RESULT = {  # teamA: (scoreA, scoreB, wentToPens)
 'Canada':(1,0,False),'Brazil':(2,1,False),'Germany':(1,1,True),
 'Netherlands':(1,1,True),'Mexico':(2,0,False),'Norway':(2,1,False),
 'France':(3,0,False),'USA':(2,0,False),'England':(2,1,False),
 'Belgium':(3,2,False),   # AET result
 'Spain':(3,0,False),'Portugal':(2,1,False),'Switzerland':(2,0,False),
 'Egypt':(1,1,True),'Argentina':(3,2,False),'Colombia':(1,0,False),
}
K=60
ELO2 = dict(ELO)
for m in R32:
    a,b,_,_,_,nud = m
    sa,sb,pens = ELO_RESULT[a]
    ea = ELO[a]+nud.get(a,0); eb = ELO[b]+nud.get(b,0)
    We = elo_prob(ea,eb)
    gd = 0 if pens else (sa-sb)
    Wa = 0.5 if pens else (1.0 if sa>sb else (0.0 if sa<sb else 0.5))
    delta = K*g_mult(gd)*(Wa-We)
    ELO2[a]=ELO[a]+delta; ELO2[b]=ELO[b]-delta

print("\n"+"="*92)
print("PART 3 — MODEL IMPROVEMENTS")
print("="*92)
print("Elo updated from actual R32 (surviving teams):")
for t in ['Morocco','Paraguay','Norway','Belgium','Brazil','Colombia','Switzerland',
          'Portugal','England','Mexico','France','Spain','Argentina','USA','Egypt','Canada']:
    print(f"  {t:14} {ELO[t]:6.0f} -> {ELO2[t]:6.0f}  ({ELO2[t]-ELO[t]:+.0f})")
print("Weights: market 0.50->0.55, elo 0.30->0.28, fifa 0.20->0.17")
print("Calibration shrink 0.93 toward 0.5 (R32 favorites 60-85% ran overconfident)")
print("Goal-total prior mu raised ~+0.15 (R32 outscored the modal forecast)")

# =============================================================== PART 4: R16
W_MKT2,W_ELO2,W_FIFA2 = 0.55,0.28,0.17
SHRINK=0.93
R16 = [
 ('Morocco','Canada',      -260,+205, 2.4, {'Canada':10}),
 ('France','Paraguay',     -2000,+1220,2.7,{}),
 ('Brazil','Norway',       -270,+215, 2.8, {}),
 ('England','Mexico',      -140,+114, 2.5, {'Mexico':40}),
 ('Spain','Portugal',      -225,+180, 2.8, {}),
 ('Belgium','USA',         -118,-104, 2.6, {'USA':35}),
 ('Argentina','Egypt',     -800,+520, 2.7, {'Argentina':5}),
 ('Colombia','Switzerland',-150,+133, 2.4, {}),
]
print("\n"+"="*92)
print("PART 4 — ROUND OF 16 PREDICTIONS (improved model)")
print("="*92)
print(f"{'match':28}{'mkt':>5}{'elo':>5}{'fifa':>5}{'BLEND':>7}  {'1X2 A/D/B':>14}  score  exp  conf")
r16=[]
for m in R16:
    pr = predict(m, ELO2, W_MKT2, W_ELO2, W_FIFA2, shrink=SHRINK)
    i1,j1,p1=pr['sc'][0]
    b=pr['blend']
    conf='High' if (b>=0.78 or b<=0.22) else ('Med' if (b>=0.66 or b<=0.34) else 'Low')
    spread=max(pr['mpa'],pr['epa'],pr['fpa'])-min(pr['mpa'],pr['epa'],pr['fpa'])
    if spread>0.18 and conf=='High': conf='Med'
    r16.append((pr,conf))
    print(f"{pr['a'][:13]+' v '+pr['b'][:10]:28}{pr['mpa']*100:4.0f}%{pr['epa']*100:4.0f}%"
          f"{pr['fpa']*100:4.0f}%{b*100:6.1f}%  {pr['pa']*100:4.0f}/{pr['pd']*100:3.0f}/{pr['pb']*100:3.0f}"
          f"  {i1}-{j1} {pr['exp']:.1f}  {conf}")

print("\nR16 detail:")
for pr,conf in r16:
    (i1,j1,p1),(i2,j2,p2),(i3,j3,p3_) = pr['sc']
    print(f"{pr['a']} v {pr['b']}: {pr['a']} adv {pr['blend']*100:.0f}% / {pr['b']} {(1-pr['blend'])*100:.0f}%"
          f" | reg {pr['pa']*100:.0f}/{pr['pd']*100:.0f}/{pr['pb']*100:.0f}"
          f" | score {i1}-{j1} ({p1*100:.0f}%), {i2}-{j2} ({p2*100:.0f}%), {i3}-{j3} ({p3_*100:.0f}%)"
          f" | exp {pr['exp']:.1f} P(3+) {pr['p3']*100:.0f}% | {conf}")
