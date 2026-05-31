---


title: Belmore Sheet
type: entity
publish: false
created: '2026-04-23'
updated: '2026-04-23'
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
  <div class="ddb-row"><span class="ddb-rname">Darkvision</span><span class="ddb-rbonus">60 ft</span></div>
  <div class="ddb-row"><span class="ddb-rname">Climb Speed</span><span class="ddb-rbonus">30 ft</span></div>
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
      <td class="an">Spear (one-hand)</td>
      <td class="ab">+5</td>
      <td class="ad">1d6+5</td>
      <td class="at">Piercing</td>
      <td class="ar">5 / 20/60 ft</td>
      <td class="ano">Dueling +2; Sap mastery</td>
    </tr>
    <tr>
      <td class="an">Spear (versatile)</td>
      <td class="ab">+5</td>
      <td class="ad">1d8+3</td>
      <td class="at">Piercing</td>
      <td class="ar">5 ft</td>
      <td class="ano">Two-handed — no Dueling bonus</td>
    </tr>
    <tr>
      <td class="an">Cat's Claws</td>
      <td class="ab">+5</td>
      <td class="ad">1d6+3</td>
      <td class="at">Slashing</td>
      <td class="ar">5 ft</td>
      <td class="ano">Unarmed; no off-hand penalty</td>
    </tr>
    <tr>
      <td class="an">Spear (thrown)</td>
      <td class="ab">+5</td>
      <td class="ad">1d6+3</td>
      <td class="at">Piercing</td>
      <td class="ar">20/60 ft</td>
      <td class="ano">No Dueling bonus</td>
    </tr>
  </tbody>
</table>

## Battle Master — Superiority Dice

```dataviewjs
await dv.view("meta/scripts/pc-sheet", { section: "resource-tracker" });
```

<table class="ddb-attacks" style="margin-top:8px">
  <thead>
    <tr><th>Maneuver</th><th>Trigger</th><th>Effect</th></tr>
  </thead>
  <tbody>
    <tr>
      <td class="an">Trip Attack</td>
      <td class="at">On hit</td>
      <td class="ano">+1d8 damage; STR save DC 13 or knocked prone</td>
    </tr>
    <tr>
      <td class="an">Menacing Attack</td>
      <td class="at">On hit</td>
      <td class="ano">+1d8 damage; WIS save DC 13 or Frightened until your next turn</td>
    </tr>
    <tr>
      <td class="an">Riposte</td>
      <td class="at">Enemy misses (Reaction)</td>
      <td class="ano">Melee attack; +1d8 damage on hit</td>
    </tr>
  </tbody>
</table>

## Fighter Features

<div class="ddb-feat">
  <div class="fname">Fighting Style — Dueling</div>
  <div class="fbody">+2 damage with a one-handed weapon when no other weapon is in your hand. Applies to spear one-handed.</div>
</div>

<div class="ddb-feat">
  <div class="fname">Second Wind <em>1/SR</em></div>
  <div class="fbody">Bonus action. Regain <strong>1d10+3 HP</strong> (avg 8.5). Recharges on Short or Long Rest.</div>
</div>

<div class="ddb-feat">
  <div class="fname">Action Surge <em>1/SR</em></div>
  <div class="fbody">Take one additional action on your turn. Recharges on Short or Long Rest.</div>
</div>

<div class="ddb-feat">
  <div class="fname">Know Your Enemy</div>
  <div class="fbody">Spend 1 minute observing a creature. Learn two of: STR, DEX, CON, AC, HP, class levels, Fighter levels — compared to your own.</div>
</div>

<div class="ddb-feat">
  <div class="fname">Weapon Mastery — Spear (Sap)</div>
  <div class="fbody">On a hit, target has disadvantage on its next attack roll before the start of your next turn.</div>
</div>

## Tabaxi Traits

<div class="ddb-feat">
  <div class="fname">Feline Agility</div>
  <div class="fbody">Double speed (60 ft) for one turn. Recharges after a turn spent without moving.</div>
</div>

<div class="ddb-feat">
  <div class="fname">Cat's Claws</div>
  <div class="fbody">Unarmed strikes deal 1d6 slashing. Climb speed 30 ft.</div>
</div>

<div class="ddb-feat">
  <div class="fname">Cat's Talent</div>
  <div class="fbody">Proficiency in Perception and Stealth.</div>
</div>

## Equipment

![[Belmore-Equipment.base]]

<div class="ddb-feat">
  <div class="fname">Bracers of Archery <em>(uncommon)</em></div>
  <div class="fbody">+2 bonus to attack rolls with ranged weapons. Proficiency with longbow and shortbow while worn.</div>
</div>

<div class="ddb-coins">
  <div class="ddb-coin"><span class="cval">0</span><span class="clbl cp">CP</span></div>
  <div class="ddb-coin"><span class="cval">0</span><span class="clbl sp">SP</span></div>
  <div class="ddb-coin"><span class="cval">0</span><span class="clbl ep">EP</span></div>
  <div class="ddb-coin"><span class="cval">0</span><span class="clbl gp">GP</span></div>
  <div class="ddb-coin"><span class="cval">0</span><span class="clbl pp">PP</span></div>
</div>

## Background & Personality

> [!quote]- Personality & Drives
> **Traits:** *(verify)*  
> **Ideals:** *(verify)*  
> **Bonds:** *(verify)*  
> **Flaws:** *(verify)*

## Notes

*Data gaps — verify with player: background, alignment, exact proficiency picks (second skill from Fighter class unconfirmed), maneuver selection, feat selection.*

---

**See also:** [[Stripes-Bitemore|Belmore]] · [[Belmore-Primer]]

````
`````

## Related

- [[Tabaxi]] — Tabaxi
- [[Bracers-of-Archery]] — Bracers of Archery
- [[bonds]] — bonds
