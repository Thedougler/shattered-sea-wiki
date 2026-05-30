---
title: Il Palio delle Voci — DM Notes
category: situation
type: situation
subtype: thread
campaign: shattered-sea
publish: false
audience: dm
status: planned
lifecycle: island
confidence_level: medium
region: calveno
aliases: []
tags:
  - thread
  - event
  - calveno
  - skill-challenge
summary: "DM mechanics for running the Palio as a skill challenge — phase structure, rival disruptions, party roles, recruitable NPCs, and reward tiers."
sources:
  - Homebrew
relationships:
  - relation: located_at
    target: "[[Calveno]]"
  - relation: public_page
    target: "[[Il-Palio-delle-Voci]]"
created: 2026-05-17
updated: 2026-05-17
---

# Il Palio delle Voci — DM Notes

## Situation

The Palio is a multi-phase skill challenge spanning three in-game nights. The party can enter as performers, but they don't need a bard to compete — stage crew and crowd work are full contributors. The goal is to have the most crowd at midnight on the final night. The challenge is not just performing well; rival bands actively try to outmanoeuvre them.

---

## Party Roles

**Performer** *(CHA-primary)*
- Performance (DC varies by phase) — core contribution each phase
- Persuasion — working the crowd between sets; pulling undecided audience
- Bardic Inspiration, Vicious Mockery, Enthrall, etc — full magical support valid

**Stage Crew** *(DEX/STR/WIS)*
- DEX Acrobatics — rigging dramatic entrances, aerial work, dangerous stage business
- STR Athletics — hauling props, managing pyrotechnics physically, building crowd-visible spectacle
- WIS Perception — timing a pyrotechnic or lighting cue at the exact right moment (advantage to Performer check that phase if successful DC 13)
- INT (Arcana or tools) — operating alchemical or mechanical stage effects; a failed check means a misfired effect (cloud of smoke, wrong colour, unexpected bang — roll on the chaos table)

**Crowd Work** *(WIS/CHA/INT)*
- Insight DC 12 — read what the crowd wants right now (success gives the Performer a theme/approach that grants +2 to their next check)
- Persuasion or Deception — redirect wandering audience members toward your stage
- Deception — spread a rumour about a rival band (rival loses 1 success from their running total; DC 14; detectable with Investigation DC 16)

Each party member can contribute one role per phase. Non-party recruits contribute a flat +2 to one role's result (see Recruitable NPCs).

---

## Phase Structure

### Phase 1 — La Prova (DC 12)
*First night. Short sets. First impressions.*

The party needs **2 successes from their available roles** to pass Phase 1.

- Pass: Establish a crowd base. Rival bands take note. 
- Fail: Crowd is polite but unconvinced. -1 to Phase 2 DCs doesn't apply; the party loses the opening Insight bonus (they don't know what this crowd wants yet).

**Rival action this phase:** La Canzone Nera sends a representative to "offer advice" — actually fishing for who the party's weakest link is. WIS Insight DC 13 to recognise this. If the party shares information, La Canzone Nera counters their Phase 2 approach directly.

### Phase 2 — La Sfida (DC 14)
*Second night. Full sets. Sabotage welcome.*

The party needs **3 successes from their available roles** to pass Phase 2. Each rival band also does something disruptive:

- **La Canzone Nera** — bribes the Mercatura stage platform crew. On a failed Stage Crew check this phase, a prop fails or lighting cuts out mid-performance. DC 15 Investigation to discover who arranged it.
- **Il Vento di Seta** — poaches the best viewing spot on the Velo Quarter bridge, physically blocking sightlines to the adjacent stage. Crowd Work DC 14 to counter (redirect via Le Paludi waterfront instead).
- **Le Ossa del Toro** — starts a crowd surge. A cluster of audience at their stage rushes toward the waterfront. If unaddressed, the party loses 1 success worth of audience automatically. Crowd Work DC 13 to intercept; STR DC 14 to physically redirect the surge.

The party chooses which rival disruption to address (they can only counter one per phase without extra actions). The others land.

**Pass Phase 2:** Going into the Grande Finale with momentum. +2 to all Phase 3 checks. One rival band is visibly struggling.

**Fail Phase 2:** Entering the finale as underdogs. The situation is recoverable. The Performer gets one "all-in" option (see Grande Finale).

### Phase 3 — Il Grande Finale (DC 16)
*Final night. Three hours. Simultaneous.*

The party needs **3 successes out of 4 possible role checks** to win.

The Grande Finale has one special mechanic: the **All-In**. Once per finale, any party member may declare All-In on their roll. They gain advantage, but on a failure they suffer a Complication (see table). They can only do this once as a group.

**Complications table (d6):**
1. A pyrotechnic misfires — cloud of coloured smoke covers the stage; Performance check next check at disadvantage
2. A string breaks / instrument goes out of tune mid-song — -1 automatic failure this phase
3. A crowd member climbs on stage and won't leave — must be managed as a bonus action or performer checks at -2
4. A rival band's fan starts a chant drowning out your set — Persuasion DC 15 to shut it down or lose this phase's Crowd Work result
5. It starts raining — Stage Crew check DC 14 or the lighting rig fails
6. Nothing bad happens. The crowd thinks it was intentional. +1 success this phase.

**At midnight:** Count successes across all three phases. Whoever has the most (among all bands) wins. Track rival band performance roughly — La Canzone Nera gets 2 automatic successes per phase (flawless but boring, crowds erode); Il Vento di Seta gets 2 per phase (consistent); Le Ossa del Toro gets 1 per phase but gets a bonus 2 in Phase 3 from sheer volume.

---

## Outcome Tiers

| Total Successes | Result | Reward |
|---|---|---|
| 0–3 | Respectable showing | Crowd remembers them warmly; no prize; the halfling at Ponte Bassa asks if they want to try again next year |
| 4–6 | Second place | 100 gp split; a Tessarine scout approaches about a booking (Concordat circuit connection) |
| 7–8 | Third (close) | Crowd respect; Le Ossa del Toro want to buy them a drink, which is its own thing |
| 9+ / Win | Palio banner + 300 gp | Iacopo Fieschi mentions the party to Cosimo Verantio as "people worth knowing"; Morsani appears at their stage just before midnight; the crowd knows their name |

---

## Recruitable NPCs

**Tomasso the Halfling** *(Ponte Bassa most evenings)* — A halfling fiddle player who hustles dockworkers for pocket money. Will join for a 10gp cut of any prize. Contributes +2 to Performer checks. Has an annoying habit of improvising when he thinks the tempo is wrong; DC 12 Performance check from the lead performer each phase to keep him on the arrangement or he goes off-script (which sometimes works: DC 14 Performance or +1 bonus success).

**The Rattkin from the Warren** — Ask Essa Two-Tooth. She will know someone. A young Rattkin plays an instrument that nobody in the party will be able to identify — six strings, played horizontally, sounds like two instruments arguing. Contributes +2 to Stage Crew checks (the visual is extremely strange and extremely good). Will not perform on the Mercatura stage due to unspecified prior incident; Velo Quarter or waterfront only.

**Prospero Morsani's Cabinet** — Morsani will not perform. He will, for the right question, lend a single prop from the locked wardrobe cabinet. The prop produces a spectacular visual effect usable once during the Grande Finale — treat as an automatic success on one Stage Crew check. He will not explain what it is beforehand. It will be appropriate. It will be strange.

---

## Key Facts

- Registration closes three days before La Prova. The committee office is on the Mercatura.
- La Canzone Nera has won three of the last five years. The committee families are bored of them but won't say so.
- The Velo Quarter crowd is the swing vote; whoever owns that stage going into the Finale has a significant advantage.
- Morsani appearing at a stage just before midnight has predicted the winner correctly for eleven consecutive years. Nobody knows how he knows.

## DM Notes

The Palio works best if the party enters with at least one non-performer. A party with no bard is not at a disadvantage — the Stage Crew and Crowd Work contributions are mathematically significant. The halfling Tomasso is available specifically to give parties without a charisma class an option.

If the party wins: give them the banner. Put it on their ship eventually. Let NPCs recognise it.

If the party loses honourably: Il Vento di Seta's Tessarine booking agent approaches anyway. "Not a win, but the crowd noticed you." This opens the same Concordat connection at half value.

Le Ossa del Toro will absolutely invite the party to play a joint set if they lose. No stakes, no crowd, just because they liked watching the party fight for it.

## Involved Parties

- [[Prospero-Morsani|Prospero Morsani]] — unpredictable variable; always present; always knows the outcome
- [[Iacopo-Fieschi|Iacopo Fieschi]] — watches the Finale; relays notable parties to Cosimo if they win
- [[content/shattered-sea/characters/npcs/Cosimo-Verantio|Cosimo Verantio]] — indirect; hears about winners through Fieschi

## Locations

- [[Calveno]] — the whole city is the venue
- [[Ponte-Bassa|The Ponte Bassa]] — where Tomasso is found; where the crowd gathers before events

## Triggers

- Party arrives in Calveno within three days of registration close
- Anyone in Calveno mentions the Palio (Hector Podge equivalent: Oleandro Fuschi at Ponte Bassa mentions it as small talk)
- The party asks about entertainment or ways to make money in the city

## Consequences

- **Win:** Calveno social capital; Cosimo aware of party; banner on the ship
- **Lose honourably:** Tessarine connection; Ossa del Toro friendship; the halfling wants to travel with them
- **Don't enter:** The Palio happens without them. La Canzone Nera wins again. The Velo Quarter crowd boos.

## Related Pages

[[Il-Palio-delle-Voci]] | [[Calveno]] | [[Prospero-Morsani]] | [[Iacopo-Fieschi]]

---

## Session Log

| Session | Development |
|---------|-------------|
