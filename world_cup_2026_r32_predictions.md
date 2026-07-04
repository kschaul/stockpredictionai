# 2026 FIFA World Cup — Knockout Predictions (R32 + R16)

*Generated 2026-06-28, updated 2026-07-04. Covers all 16 Round-of-32 matches
(now **played** — with a full model evaluation) and the 8 **Round-of-16**
matches (upcoming, July 4–7), across the USA, Mexico and Canada.*

> **Jump to:** [R32 predictions](#summary-table--all-16-matches) ·
> [R32 results & model evaluation](#round-of-32--results--model-evaluation) ·
> [Round-of-16 predictions](#round-of-16-predictions-improved-model)

Each match reports **who advances** (probability, including extra time +
penalties) and a **most-likely regulation scoreline** (90 minutes — what "2–1"
means). Knockout matches cannot end in a draw, so the draw % below is the chance
the tie goes to extra time / penalties.

---

## Methodology (multiple angles, blended)

For every match three independent angles are converted to a win probability and
combined with a weighted ensemble, then a Poisson goal model produces the
scoreline:

| Angle | Weight | Source |
|---|---|---|
| **Bookmaker market** — de-vigged "to advance" odds | **50%** | FanDuel / DraftKings / BetMGM (~Jun 27) |
| **ELO model** — World Football Elo logistic + venue/altitude/form nudge | **30%** | eloratings-style ratings |
| **FIFA ranking** — logistic on rank gap | **20%** | FIFA/Coca-Cola ranking (Jun 2026) |

**Engineered features** per match: ELO rating + **ELO difference**, FIFA rank +
**rank difference**, de-vigged market probability, group-stage form (points /
goals-per-game), and context flags (home advantage, **Mexico City altitude**,
Monterrey/Dallas heat, rest days). Home/altitude nudges (in ELO points):
Mexico +80 (Estadio Azteca, 2,240 m), USA +50, Canada +15.

**Exact score**: each team's expected goals (λ) is solved so the Poisson model's
implied advance probability matches the blended probability, given a match
goal-total prior (µ ≈ 2.3–2.8 set by the teams' attacking/defensive profiles).
The **modal** (most likely) scoreline is reported, plus the runner-up score.

### Why the scorelines look low (mode ≠ mean)

A common and fair question: *"1–0/2–0 looks low vs the group stage — are the
bookies really expecting that few goals?"* No. Two things are being confused:

- The **most likely single scoreline (the mode)** is *always* low. Goals are rare,
  discrete (Poisson) events, so probability is spread thinly across dozens of
  scorelines — no single exact score tops ~12–21%. The mode is 1–0 / 1–1 / 2–0
  even when a game is expected to be open.
- The **expected (average) total goals** is a different, higher number. This
  model expects **≈2.3–2.8 goals per match (avg ≈2.55)** — right where bookmakers
  set their **Over/Under "match total" lines (2.5–3.0)**. In fact, **P(3 or more
  goals) is ~40–53% in every tie** (shown per match below). So the market and the
  model agree there will be goals; the single-scoreline headline just hides it.

Also note **knockout football is structurally lower-scoring than the group stage**
(more caution, game-management when ahead, weaker opponents sitting deep, fear of
elimination). The 2026 group stage was a goal-fest (~3.0/game); a step down in
single-elimination is expected — by the bookies too.

**Confidence**: High = blended ≥78%; Med = ≥66%; Low = closer than that, or the
three angles disagree materially.

---

## Accuracy validation (backtest)

Direct in-tournament backtesting of the 2026 group stage wasn't possible (the
egress policy blocked the stats sites that hold full goal-by-goal tables), so the
same ELO/odds method was validated on the **most recent comparable dataset — the
2022 World Cup knockout stage (16 matches)**, using pre-match ratings:

- **Favorite-advances accuracy: 13/16 = 81.3%** (the 3 misses were Morocco's run
  past Spain & Portugal, and Croatia over Brazil — classic knockout chaos).
- **Brier score (advance): 0.188** (0 = perfect, 0.25 = coin-flip) → well
  calibrated.
- **Exact-scoreline** hit rate for any football model is inherently low (~8–12%);
  treat scorelines as the single most likely result, not a lock.

**Expectation for this R32:** because many of these ties are lopsided (Argentina,
France, England, Spain, Germany, USA are heavy favorites), realistic outcome
accuracy is **~80–85%** — i.e. expect roughly **2–3 of the 16 favorites to fall**.

---

## Summary table — all 16 matches

"Most likely score" is the single modal scoreline; "Exp. goals" is the model's
expected **total** goals (≈ the bookmaker Over/Under line) with P(3+ goals).

| # | Match | Predicted to advance | Advance prob | Most likely score | Exp. goals (P 3+) | Conf. |
|---|---|---|---|---|---|---|
| 1 | Canada vs South Africa | **Canada** | 75% | 1–0 | 2.4 (43%) | Med |
| 2 | Brazil vs Japan | **Brazil** | 73% | 1–0 | 2.7 (51%) | Med |
| 3 | Germany vs Paraguay | **Germany** | 85% | 2–0 | 2.6 (48%) | High |
| 4 | Netherlands vs Morocco | **Netherlands** | 63% | 1–1 (NED on pens) | 2.5 (46%) | Low |
| 5 | Mexico vs Ecuador | **Mexico** | 69% | 1–0 | 2.3 (40%) | Med |
| 6 | Norway vs Ivory Coast | **Norway** | 65% | 1–1 (NOR on pens) | 2.6 (48%) | Low |
| 7 | France vs Sweden | **France** | 87% | 2–0 | 2.8 (53%) | High |
| 8 | USA vs Bosnia & Herz. | **USA** | 85% | 2–0 | 2.6 (48%) | Med |
| 9 | England vs Congo DR | **England** | 90% | 2–0 | 2.6 (48%) | High |
| 10 | Belgium vs Senegal | **Belgium** | 66% | 1–0 | 2.5 (46%) | Med |
| 11 | Spain vs Austria | **Spain** | 87% | 2–0 | 2.8 (53%) | High |
| 12 | Portugal vs Croatia | **Portugal** | 65% | 1–0 | 2.5 (46%) | Low |
| 13 | Switzerland vs Algeria | **Switzerland** | 73% | 1–0 | 2.3 (40%) | Med |
| 14 | Egypt vs Australia | **Coin-flip** (model: Australia 52 / Egypt 48; market: Egypt) | ~50% | 1–1 (pens) | 2.3 (40%) | Low |
| 15 | Argentina vs Cape Verde | **Argentina** | 95% | 2–0 | 2.8 (53%) | High |
| 16 | Colombia vs Ghana | **Colombia** | 79% | 1–0 | 2.5 (46%) | Med |

**Upset / coin-flip watch:** Egypt–Australia (only match where the model and the
bookies disagree on the favorite), Netherlands–Morocco, Norway–Ivory Coast,
Portugal–Croatia, and Belgium–Senegal are the five genuine toss-ups most likely
to spring a surprise or need extra time.

---

## Per-match detail

Each table shows the three angles (market / ELO / FIFA win prob for the favorite),
the blended advance probability, the regulation result split, and the scoreline.

### 1. Canada vs South Africa — Jun 28, SoFi Stadium (Los Angeles)
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Canada to advance | 74% | 67% | 92% | **75%** |

- **Regulation 1X2:** Canada 61% · Draw 24% · South Africa 15%
- **Predicted score: Canada 1–0** (runner-up 2–0). Advance: **Canada 75%**.
- **Exp. total goals ≈ 2.4** · P(3+)=43% · top scorelines: 1–0 (15%), 2–0 (13%), 1–1 (11%).
- *Rationale:* Co-host Canada has the ELO edge and a big ranking gap; South Africa
  over-performed to reach the last 32 but lacks the cutting edge. Low-scoring
  Canada win expected.

### 2. Brazil vs Japan — Jun 29, NRG Stadium (Houston)
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Brazil to advance | 72% | 76% | 72% | **73%** |

- **Regulation 1X2:** Brazil 60% · Draw 23% · Japan 18%
- **Predicted score: Brazil 1–0** (runner-up 2–0). Advance: **Brazil 73%**.
- **Exp. total goals ≈ 2.7** · P(3+)=51% · top scorelines: 1–0 (12%), 2–0 (11%), 1–1 (11%).
- *Rationale:* All three angles agree. Japan are the most dangerous "small"
  favorite-killer in the field (pace, pressing), so a one-goal margin and real
  upset risk; Brazil's quality should still tell.

### 3. Germany vs Paraguay — Jun 29, Gillette Stadium (Foxborough)
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Germany to advance | 84% | 81% | 93% | **85%** |

- **Regulation 1X2:** Germany 74% · Draw 18% · Paraguay 8%
- **Predicted score: Germany 2–0** (runner-up 1–0). Advance: **Germany 85%**.
- **Exp. total goals ≈ 2.6** · P(3+)=48% · top scorelines: 2–0 (16%), 1–0 (15%), 3–0 (11%).
- *Rationale:* Class gap is large; Paraguay are organized and hard to break down,
  capping the margin rather than the outcome.

### 4. Netherlands vs Morocco — Jun 29, Estadio BBVA (Monterrey)
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Netherlands to advance | 62% | 65% | 64% | **63%** |

- **Regulation 1X2:** Netherlands 48% · Draw 26% · Morocco 26%
- **Predicted score: 1–1** → Netherlands on penalties (runner-up 1–0 NED). Advance: **Netherlands 63%**.
- **Exp. total goals ≈ 2.5** · P(3+)=46% · top scorelines: 1–1 (12%), 1–0 (12%), 2–1 (9%).
- *Rationale:* A 2022 semifinalist in Morocco vs a top-6 Dutch side — genuine
  toss-up. Monterrey heat and Morocco's resilience point to a tight, low-margin
  game that could go the distance.

### 5. Mexico vs Ecuador — Jun 30, Estadio Azteca (Mexico City)
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Mexico to advance | 74% | 61% | 70% | **69%** |

- **Regulation 1X2:** Mexico 54% · Draw 26% · Ecuador 20%
- **Predicted score: Mexico 1–0** (runner-up 1–1). Advance: **Mexico 69%**.
- **Exp. total goals ≈ 2.3** · P(3+)=40% · top scorelines: 1–0 (15%), 1–1 (12%), 2–0 (11%).
- *Rationale:* **Altitude + home crowd at the Azteca** is the swing factor — Mexico
  hadn't conceded in the group and are nearly unbeaten there. Ecuador defend well
  and travel + thin air hurt them, so a narrow Mexico win.

### 6. Norway vs Ivory Coast — Jun 30
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Norway to advance | 63% | 59% | 79% | **65%** |

- **Regulation 1X2:** Norway 50% · Draw 25% · Ivory Coast 25%
- **Predicted score: 1–1** → Norway on penalties (runner-up 1–0 NOR). Advance: **Norway 65%**.
- **Exp. total goals ≈ 2.6** · P(3+)=48% · top scorelines: 1–1 (12%), 1–0 (12%), 2–1 (9%).
- *Rationale:* Haaland gives Norway the higher ceiling and ranking edge, but Ivory
  Coast's athleticism makes this close — extra time is live.

### 7. France vs Sweden — Jun 30
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| France to advance | 86% | 86% | 91% | **87%** |

- **Regulation 1X2:** France 78% · Draw 16% · Sweden 7%
- **Predicted score: France 2–0** (runner-up 1–0). Advance: **France 87%**.
- **Exp. total goals ≈ 2.8** · P(3+)=53% · top scorelines: 2–0 (16%), 1–0 (14%), 3–0 (12%).
- *Rationale:* Tournament co-favorite vs a third-placed qualifier; France's depth
  is overwhelming.

### 8. USA vs Bosnia & Herzegovina — Jul 1, Levi's Stadium (Santa Clara)
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| USA to advance | 85% | 74% | ~99% | **85%** |

- **Regulation 1X2:** USA 74% · Draw 18% · Bosnia 8%
- **Predicted score: USA 2–0** (runner-up 1–0). Advance: **USA 85%**.
- **Exp. total goals ≈ 2.6** · P(3+)=48% · top scorelines: 2–0 (16%), 1–0 (15%), 3–0 (11%).
- *Rationale:* Co-host on home soil with the larger ranking gap; the ELO model is
  more cautious (Bosnia have danger men), hence Medium not High confidence.

### 9. England vs Congo DR — Jul 1, Mercedes-Benz Stadium (Atlanta)
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| England to advance | 88% | 87% | ~99% | **90%** |

- **Regulation 1X2:** England 81% · Draw 14% · Congo DR 4%
- **Predicted score: England 2–0** (runner-up 1–0). Advance: **England 90%**.
- **Exp. total goals ≈ 2.6** · P(3+)=48% · top scorelines: 2–0 (19%), 1–0 (17%), 3–0 (14%).
- *Rationale:* Strongest favorite of the round alongside Argentina; comfortable.

### 10. Belgium vs Senegal — Jul 1, Lumen Field (Seattle)
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Belgium to advance | 63% | 68% | 72% | **66%** |

- **Regulation 1X2:** Belgium 51% · Draw 26% · Senegal 23%
- **Predicted score: Belgium 1–0** (runner-up 1–1). Advance: **Belgium 66%**.
- **Exp. total goals ≈ 2.5** · P(3+)=46% · top scorelines: 1–0 (13%), 1–1 (12%), 2–0 (10%).
- *Rationale:* Belgium have more individual quality; Senegal's power and pace make
  this one of the tighter "favorite" games — upset is plausible.

### 11. Spain vs Austria — Jul 2, SoFi Stadium (Los Angeles)
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Spain to advance | 88% | 84% | 87% | **87%** |

- **Regulation 1X2:** Spain 77% · Draw 16% · Austria 7%
- **Predicted score: Spain 2–0** (runner-up 1–0). Advance: **Spain 87%**.
- **Exp. total goals ≈ 2.8** · P(3+)=53% · top scorelines: 2–0 (16%), 1–0 (14%), 3–0 (12%).
- *Rationale:* Reigning Euro champions and tournament co-favorite; Austria are
  organized but outclassed.

### 12. Portugal vs Croatia — Jul 2, BMO Field (Toronto)
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Portugal to advance | 67% | 65% | 62% | **65%** |

- **Regulation 1X2:** Portugal 50% · Draw 26% · Croatia 25%
- **Predicted score: Portugal 1–0** (runner-up 1–1). Advance: **Portugal 65%**.
- **Exp. total goals ≈ 2.5** · P(3+)=46% · top scorelines: 1–0 (12%), 1–1 (12%), 2–0 (9%).
- *Rationale:* The marquee toss-up — Portugal's squad depth vs Croatia's
  tournament savvy and midfield control. Real extra-time risk.

### 13. Switzerland vs Algeria — Jul 2, BC Place (Vancouver)
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Switzerland to advance | 74% | 61% | 91% | **73%** |

- **Regulation 1X2:** Switzerland 58% · Draw 25% · Algeria 17%
- **Predicted score: Switzerland 1–0** (runner-up 2–0). Advance: **Switzerland 73%**.
- **Exp. total goals ≈ 2.3** · P(3+)=40% · top scorelines: 1–0 (16%), 2–0 (13%), 1–1 (11%).
- *Rationale:* Swiss tournament reliability and ranking edge; Algeria can frustrate,
  so a low-scoring Swiss win.

### 14. Egypt vs Australia — Jul 3, AT&T Stadium (Dallas) ⚠️ model ≠ market
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Egypt to advance | 56% | 48% | 32% | **48%** |

- **Regulation 1X2:** Egypt 36% · Draw 28% · Australia 36%
- **Predicted score: 1–1** → penalties. Advance: essentially **50/50** (model edges
  **Australia 52%**, the bookies edge **Egypt ~55%**).
- **Exp. total goals ≈ 2.3** · P(3+)=40% · top scorelines: 1–1 (13%), 1–0 (12%), 0–1 (12%).
- *Rationale:* **The one match where the angles disagree.** The market trusts Salah
  and Egypt; ELO and the FIFA ranking favor Australia. Treat as a true coin-flip
  most likely decided in extra time or on penalties. Lowest-confidence call of the
  round.

### 15. Argentina vs Cape Verde — Jul 3, Hard Rock Stadium (Miami)
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Argentina to advance | 93% | 95% | ~100% | **95%** |

- **Regulation 1X2:** Argentina 90% · Draw 9% · Cape Verde 1%
- **Predicted score: Argentina 2–0** (runner-up 3–0). Advance: **Argentina 95%**.
- **Exp. total goals ≈ 2.8** · P(3+)=53% · top scorelines: 2–0 (21%), 3–0 (19%), 1–0 (16%).
- *Rationale:* Reigning champions vs debutants who advanced on three draws — the
  safest pick in the bracket; only the margin is in question.

### 16. Colombia vs Ghana — Jul 3, Arrowhead Stadium (Kansas City)
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Colombia to advance | 72% | 78% | ~100% | **79%** |

- **Regulation 1X2:** Colombia 66% · Draw 21% · Ghana 12%
- **Predicted score: Colombia 1–0** (runner-up 2–0). Advance: **Colombia 79%**.
- **Exp. total goals ≈ 2.5** · P(3+)=46% · top scorelines: 1–0 (15%), 2–0 (14%), 1–1 (10%).
- *Rationale:* Colombia's ELO and ranking edge are sizeable; Ghana qualified as a
  third-placed team and are the weaker side, though dangerous on the break.

---

## Round of 32 — results & model evaluation

The R32 has been played. Grading the predictions above against the **actual
results** (this is the real-world validation, replacing the pre-tournament 2022
backtest):

| Match | My pick (p adv) | Result | Pred score | Actual (90′) | Pick ✓ | Score ✓ |
|---|---|---|---|---|:--:|:--:|
| Canada v South Africa | Canada 75% | Canada through | 1–0 | **1–0** | ✅ | ✅ |
| Brazil v Japan | Brazil 73% | Brazil through | 1–0 | 2–1 | ✅ | — |
| Germany v Paraguay | Germany 85% | **Paraguay** (4–3 pens) | 2–0 | 1–1 | ❌ | — |
| Netherlands v Morocco | Netherlands 63% | **Morocco** (3–2 pens) | 1–1 | **1–1** | ❌ | ✅ |
| Mexico v Ecuador | Mexico 69% | Mexico through | 1–0 | 2–0 | ✅ | — |
| Norway v Ivory Coast | Norway 65% | Norway through | 1–1 | 2–1 | ✅ | — |
| France v Sweden | France 87% | France through | 2–0 | 3–0 | ✅ | — |
| USA v Bosnia | USA 85% | USA through | 2–0 | **2–0** | ✅ | ✅ |
| England v Congo DR | England 90% | England through | 2–0 | 2–1 | ✅ | — |
| Belgium v Senegal | Belgium 66% | Belgium (3–2 AET) | 1–0 | 1–1 | ✅ | — |
| Spain v Austria | Spain 87% | Spain through | 2–0 | 3–0 | ✅ | — |
| Portugal v Croatia | Portugal 65% | Portugal through | 1–0 | 2–1 | ✅ | — |
| Switzerland v Algeria | Switzerland 73% | Switzerland through | 1–0 | 2–0 | ✅ | — |
| Egypt v Australia | *coin-flip* (mkt: Egypt) | **Egypt** (4–2 pens) | 1–1 | **1–1** | ⚠️ | ✅ |
| Argentina v Cape Verde | Argentina 95% | Argentina (3–2 AET) | 2–0 | 2–2 | ✅ | — |
| Colombia v Ghana | Colombia 79% | Colombia through | 1–0 | **1–0** | ✅ | ✅ |

**Scorecard**
- **Advancement: 14/16 higher-rated teams went through (88%)**; by the model's
  *explicit* pick it was **13/16** — the one ⚠️ is Egypt, which I called a 50/50
  and leaned Australia while the market leaned Egypt (market was right).
- **Exact 90-minute scoreline: 5/16 = 31%** (Canada 1–0, Netherlands 1–1, USA 2–0,
  Egypt 1–1, Colombia 1–0) — well above the ~8–12% typical for football models.
- **Brier score (advance): 0.135** — better than the 0.188 pre-tournament backtest
  and far better than a coin-flip (0.25). The two upsets (Germany, Netherlands)
  were exactly the "expect 2–3 favorites to fall" the model warned about.

**Lessons that fed the model update**
1. *Favorites in the 60–85% band were slightly overconfident* — Germany lost at
   85%, and Belgium, Argentina, Morocco, Egypt all needed extra time / penalties.
   Regulation was tighter than modeled.
2. *Games outscored the modal forecast* (France 3–0, Spain 3–0, Brazil 2–1,
   Argentina 3–2) — the goal-total prior was a touch low.
3. *The market beat the ELO/FIFA angle on the lone disagreement* (Egypt).

### What changed for the Round of 16 (improved model)

- **ELO refreshed from actual R32 results** (standard Elo update, K=60, goal-diff
  multiplier). Biggest risers among survivors: Switzerland +35, Mexico +35, Norway
  +25, USA +23, Portugal +21, Canada +20, Belgium +19; Argentina barely moved (+3,
  won as expected). Eliminated teams' ratings drop out.
- **Market weight raised 0.50 → 0.55** (ELO 0.30→0.28, FIFA 0.20→0.17) — the market
  earned it on the Egypt call.
- **Calibration shrink (×0.93 toward 50%)** to correct the observed favorite
  overconfidence.
- **Goal-total prior µ raised ~+0.15** to match the higher R32 scoring.

---

## Round of 16 predictions (improved model)

*8 matches, July 4–7. Model & market agree on the favorite in **all eight** this
round (no direction disagreement like Egypt); four are genuine coin-flips.*

| # | Match | Advances | Prob | Score | Exp. goals (P 3+) | Conf. |
|---|---|---|---|---|---|---|
| 1 | Morocco vs Canada | **Morocco** | 69% | 1–0 | 2.4 (43%) | Med |
| 2 | France vs Paraguay | **France** | 89% | 2–0 | 2.7 (51%) | High |
| 3 | Brazil vs Norway | **Brazil** | 72% | 1–0 | 2.8 (53%) | Med |
| 4 | England vs Mexico | **England** | 61% | 1–1 (ENG pens) | 2.5 (46%) | Low |
| 5 | Spain vs Portugal | **Spain** | 61% | 1–1 (ESP pens) | 2.8 (53%) | Low |
| 6 | Belgium vs USA | **Belgium** | 56% | 1–1 (BEL pens) | 2.6 (48%) | Low |
| 7 | Argentina vs Egypt | **Argentina** | 86% | 2–0 | 2.7 (51%) | High |
| 8 | Colombia vs Switzerland | **Colombia** | 58% | 1–1 (COL pens) | 2.4 (43%) | Low |

**Coin-flip watch:** Belgium–USA (56/44), Colombia–Switzerland (58/42),
England–Mexico and Spain–Portugal (both 61/39) are the four ties most likely to
go to extra time or spring an upset. **Tie of the round:** Spain vs Portugal — two
title contenders meeting far too early.

### R16 per-match detail

Angles = market / ELO (post-R32) / FIFA win prob for the favorite.

**1. Morocco vs Canada — Jul 4**
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Morocco to advance | 69% | 65% | 85% | **69%** |
- Reg 1X2: Morocco 54% · Draw 26% · Canada 21%. **Score 1–0** (alt 1–1, 2–0). Exp 2.4, P(3+)=43%.
- *Giant-killers of the Dutch, Morocco carry the quality edge; Canada's co-host energy keeps it a one-goal game.*

**2. France vs Paraguay — Jul 4**
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| France to advance | 93% | 88% | 97% | **89%** |
- Reg 1X2: France 80% · Draw 15% · Paraguay 5%. **Score 2–0** (alt 1–0, 3–0). Exp 2.7, P(3+)=51%.
- *Paraguay's shock of Germany won't repeat against France's depth; comfortable.*

**3. Brazil vs Norway — Jul 5**
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Brazil to advance | 70% | 73% | 86% | **72%** |
- Reg 1X2: Brazil 58% · Draw 23% · Norway 19%. **Score 1–0** (alt 1–1, 2–0). Exp 2.8, P(3+)=53%.
- *Brazil favored, but Haaland gives Norway a real puncher's chance — highest upset ceiling of the "clear" favorites.*

**4. England vs Mexico — Jul 5**
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| England to advance | 56% | 69% | 72% | **61%** |
- Reg 1X2: England 46% · Draw 26% · Mexico 28%. **Score 1–1** → England pens (alt 1–0, 2–1). Exp 2.5, P(3+)=46%.
- *England the better squad, but Mexico's home crowd + altitude make it a coin-flip that could go the distance.*

**5. Spain vs Portugal — Jul 6 (Arlington, TX)**
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Spain to advance | 66% | 58% | 57% | **61%** |
- Reg 1X2: Spain 47% · Draw 25% · Portugal 29%. **Score 1–1** → Spain pens (alt 1–0, 2–1). Exp 2.8, P(3+)=53%.
- *The tie of the round — Euro champions vs Portugal's golden generation. Spain a slight edge; extra time very much in play.*

**6. Belgium vs USA — Jul 6**
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Belgium to advance | 51% | 61% | 66% | **56%** |
- Reg 1X2: Belgium 40% · Draw 26% · USA 33%. **Score 1–1** → Belgium pens (alt 1–0, 0–1). Exp 2.6, P(3+)=48%.
- *True toss-up: Belgium's individual quality vs the co-host USA's crowd. The bookies have it near pick'em.*

**7. Argentina vs Egypt — Jul 7 (Atlanta)**
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Argentina to advance | 85% | 92% | 95% | **86%** |
- Reg 1X2: Argentina 76% · Draw 17% · Egypt 8%. **Score 2–0** (alt 1–0, 3–0). Exp 2.7, P(3+)=51%.
- *Egypt's shootout luck runs out against the champions' quality; Argentina comfortable.*

**8. Colombia vs Switzerland — Jul 7 (Vancouver)**
| Angle | Market | ELO | FIFA | **Blend** |
|---|---|---|---|---|
| Colombia to advance | 58% | 56% | 64% | **58%** |
- Reg 1X2: Colombia 41% · Draw 27% · Switzerland 31%. **Score 1–1** → Colombia pens (alt 1–0, 0–1). Exp 2.4, P(3+)=43%.
- *Two well-drilled, clean-sheet sides; Colombia a slim edge in a cagey, low-scoring tie.*

---

## Caveats

- Probabilities are model output, not certainties; expect ~2–3 favorites to lose.
- Group-stage goal tables and live line-ups (injuries/suspensions) could not be
  fully sourced under the network policy, so form is approximated — the market
  odds (which already price in team news) carry the load.
- ELO and FIFA-rank values are best-estimate as of June 2026.

## Sources
- Bracket & schedule: [Sky Sports](https://www.skysports.com/football/news/11095/13556636/world-cup-2026-bracket-and-knockout-fixtures-whos-facing-who-in-the-last-32-and-route-to-final), [CBS Sports](https://www.cbssports.com/soccer/news/2026-fifa-world-cup-bracket-knockout-stage/), [Olympics.com](https://www.olympics.com/en/news/fifa-world-cup-2026-bracket-round-32-full-schedule-live-updates)
- Odds: [FOX Sports R32 odds](https://www.foxsports.com/stories/soccer/2026-world-cup-round-32-odds), [ESPN betting](https://www.espn.com/espn/betting/story/_/id/48386952/), [BetMGM](https://sports.betmgm.com/en/blog/world-cup/mexico-vs-ecuador-prediction-odds-preview-world-cup-june-30-bm16/), [DraftKings Network](https://dknetwork.draftkings.com/2026/06/27/opening-odds-for-australia-vs-egypt-in-the-2026-fifa-world-cup-round-of-32/)
- Predictions / supercomputer: [Opta Analyst](https://theanalyst.com/articles/who-will-win-2026-fifa-world-cup-predictions-opta-supercomputer), [ESPN previews](https://www.espn.com/soccer/story/_/id/49118437/), [NBC Sports](https://www.nbcsports.com/soccer/news/2026-world-cup-round-of-32-confirmed-schedule-predictions-for-knockout-round)
- Rankings: [FIFA/Coca-Cola Men's Ranking](https://inside.fifa.com/fifa-world-ranking/men), [ESPN Top 50 (Jun 2026)](https://www.espn.co.uk/football/story/_/id/46664763/fifa-mens-top-50-world-rankings)
