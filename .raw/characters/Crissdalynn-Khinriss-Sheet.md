---


title: Crissdalynn Khinriss Sheet
type: entity
publish: false
created: '2026-04-23'
updated: '2026-05-24'
tags: []
campaign: shattered-sea
subtype: sheet
confidence_level: medium
sources: []
summary: "await dv.view('meta/scripts/pc-sheet', { section: 'header' });"
---

```dataviewjs
await dv.view("meta/scripts/pc-sheet", { section: "header" });
```

```dataviewjs
await dv.view("meta/scripts/pc-sheet", { section: "stats-strip" });
```

`````col
````col-md
flexGrow=1
===

```dataviewjs
await dv.view("meta/scripts/pc-sheet", { section: "left-column" });
```

<div class="ddb-slabel">Senses & Movement</div>

<div class="ddb-list">
  <div class="ddb-row"><span class="ddb-rname">Walk</span><span class="ddb-rbonus">40 ft</span></div>
  <div class="ddb-row"><span class="ddb-rname">Fly</span><span class="ddb-rbonus">30 ft</span></div>
  <div class="ddb-row"><span class="ddb-rname">Darkvision</span><span class="ddb-rbonus">None</span></div>
</div>

<div class="ddb-slabel">AC Notes</div>

<div class="ddb-list">
  <div class="ddb-row"><span class="ddb-rname">Base (Unarmored)</span><span class="ddb-rbonus">16</span></div>
  <div class="ddb-row"><span class="ddb-rname">Agile Parry</span><span class="ddb-rbonus">18</span></div>
</div>

````

````col-md
flexGrow=2
===

## Attacks

<table class="ddb-attacks">
  <thead>
    <tr>
      <th>Attack</th>
      <th style="text-align:center">Bonus</th>
      <th style="text-align:center">Damage</th>
      <th>Type</th>
      <th>Range</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="an">Longsword</td>
      <td class="ab">+5</td>
      <td class="ad">1d8+3</td>
      <td class="at">Slashing</td>
      <td class="ar">5 ft</td>
      <td class="ano">Kensei weapon · Versatile (1d10) · Finesse via Martial Arts</td>
    </tr>
    <tr>
      <td class="an">Unarmed (Talons)</td>
      <td class="ab">+6</td>
      <td class="ad">1d6+4</td>
      <td class="at">Slashing</td>
      <td class="ar">5 ft / 15 ft*</td>
      <td class="ano">Martial Arts die · Free BA after Attack action · Magical (tattoo) · *15 ft reach during Eldritch Maul · +1d6 force during Eldritch Maul</td>
    </tr>
    <tr>
      <td class="an">Longbow</td>
      <td class="ab">+5</td>
      <td class="ad">1d8+3</td>
      <td class="at">Piercing</td>
      <td class="ar">150/600 ft</td>
      <td class="ano">Kensei weapon · Kensei's Shot BA: +1d4 this turn</td>
    </tr>
    <tr>
      <td class="an">Deflect Counter</td>
      <td class="ab">+5</td>
      <td class="ad">2d6+3</td>
      <td class="at">B/P/S</td>
      <td class="ar">60 ft</td>
      <td class="ano">Reaction · only when Deflect Attacks reduces damage to 0 · costs 1 ki/focus</td>
    </tr>
  </tbody>
</table>

## Ki / Focus Points

```dataviewjs
await dv.view("meta/scripts/pc-sheet", { section: "resource-tracker" });
```

## Monk Features

<div class="ddb-feat">
  <div class="fname">Martial Arts</div>
  <div class="fbody">Use DEX for STR-based monk weapon and unarmed attacks. Unarmed strikes deal 1d6+DEX. Free unarmed strike as Bonus Action after Attack action.</div>
</div>

<div class="ddb-feat">
  <div class="fname">Unarmored Defense</div>
  <div class="fbody">AC = 10 + DEX mod + WIS mod while wearing no armor and no shield.</div>
</div>

<div class="ddb-feat">
  <div class="fname">Unarmored Movement · +10 ft</div>
  <div class="fbody">Speed increases by 10 ft while not wearing armor or a shield.</div>
</div>

<div class="ddb-feat">
  <div class="fname">Uncanny Metabolism <em>1/LR</em></div>
  <div class="fbody">Bonus Action: regain all expended ki/focus points + heal 1d6+3 HP.</div>
</div>

<div class="ddb-feat">
  <div class="fname">Flurry of Blows <em>1 Ki/Focus</em></div>
  <div class="fbody">After Attack action: Bonus Action to make 2 unarmed strikes.</div>
</div>

<div class="ddb-feat">
  <div class="fname">Patient Defense <em>1 Ki/Focus</em></div>
  <div class="fbody">Bonus Action: take the Dodge action.</div>
</div>

<div class="ddb-feat">
  <div class="fname">Step of the Wind <em>1 Ki/Focus</em></div>
  <div class="fbody">Bonus Action: Dash or Disengage. Jump distance doubled this turn.</div>
</div>

<div class="ddb-feat">
  <div class="fname">Deflect Attacks · Reaction</div>
  <div class="fbody">Reaction when hit by B/P/S attack: reduce damage by 1d10+6 (avg 11.5). If reduced to 0, spend 1 ki/focus to make a ranged unarmed attack (60 ft) as part of the reaction.</div>
</div>

<div class="ddb-feat">
  <div class="fname">Read the Current <em>1 Ki/Focus</em></div>
  <div class="fbody">Optional Kensei lesson. Once on your turn when you hit with an unarmed strike or Kensei weapon, spend 1 ki/focus point and choose this instead of another paid monk rider on that hit, such as Stunning Strike or Deft Strike. Ask one: best defense, weakest save, or current combat habit. No exact numbers, hidden lore, motives, or full statblocks.</div>
</div>

## Kensei Features (XGtE)

<div class="ddb-feat">
  <div class="fname">Kensei Weapons</div>
  <div class="fbody">Choose 2 weapons (1 melee, 1 ranged): Longsword + Longbow. These are monk weapons. Cannot be heavy or special.</div>
</div>

<div class="ddb-feat">
  <div class="fname">Agile Parry · Conditional</div>
  <div class="fbody">If you make an unarmed strike as part of the Attack action while holding a Kensei melee weapon, gain +2 AC until the start of your next turn (AC 18 total).</div>
</div>

<div class="ddb-feat">
  <div class="fname">Kensei's Shot · BA (at-will)</div>
  <div class="fbody">Bonus Action: ranged Kensei weapon attacks deal +1d4 damage this turn.</div>
</div>

## Species Traits

<div class="ddb-feat">
  <div class="fname">Flight · 30 ft</div>
  <div class="fbody">Fly speed 30 ft. Cannot fly while wearing medium or heavy armor.</div>
</div>

<div class="ddb-feat">
  <div class="fname">Talons</div>
  <div class="fbody">Natural unarmed weapon. Uses Martial Arts die (1d6+DEX) at level 3.</div>
</div>

<div class="ddb-feat">
  <div class="fname">Wind Caller <em>1/LR</em></div>
  <div class="fbody">Cast Gust of Wind (concentration). STR save or pushed 15 ft in a 60 ft line. WIS-based. No spell slots required.</div>
</div>

## Equipment

| Item | Notes |
|---|---|
| Longsword | Kensei weapon |
| Longbow | Kensei weapon |
| [[Eldritch-Claw-Tattoo\|Eldritch Claw Tattoo]] | Attuned (uncommon) · Passive: unarmed strikes are magical, +1 attack and damage · Active BA *Eldritch Maul* (1/dawn): 1 min, melee reach 15 ft via inky tendrils, +1d6 force on hit |
| Crystal dreidel | Kyzil's — meditates with it; throws rainbows in sunlight |
| Satchel of charts | Midchain navigational charts from the Red Lady |
| Geometric leatherwork | Decorative; does not grant armor AC |

<div class="ddb-coins">
  <div class="ddb-coin"><span class="cval">0</span><span class="clbl cp">CP</span></div>
  <div class="ddb-coin"><span class="cval">0</span><span class="clbl sp">SP</span></div>
  <div class="ddb-coin"><span class="cval">0</span><span class="clbl ep">EP</span></div>
  <div class="ddb-coin"><span class="cval">0</span><span class="clbl gp">GP</span></div>
  <div class="ddb-coin"><span class="cval">0</span><span class="clbl pp">PP</span></div>
</div>

## Notes

*All ability scores and derived stats are `[EST]` — estimated from class/race baselines. No player-submitted sheet on file. Skill proficiencies unknown — verify with player. Background not yet established.*

---

**See also:** [[Crissdalynn-Khinriss]] · [[Crissdalynn-Primer]]

````
`````

## Related

- [[Red-Lady]] — The Red Lady
- [[Master-Kyzil]] — Master Kyzil
- [[Midchain]] — The Midchain
