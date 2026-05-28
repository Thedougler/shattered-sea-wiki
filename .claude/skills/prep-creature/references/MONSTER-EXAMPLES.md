# Monster Design — Worked Examples

Two complete end-to-end examples showing expected quality and format: one creature (solo boss) and one villain NPC. Load this file when you need a quality benchmark or format reference.

---

## Example 1: The Hollow King (CR 11 Solo Boss)

### Concept Lock

**Identity:** An ancient undead entity that was never a wizard — a king who refused to die and bargained with void entities to hollow itself out and persist. Rules a dead kingdom of bone and ash.
**Want:** To fill its hollow interior with the warmth of living souls. It doesn't want power; it wants to *feel* again.
**Signature Moment:** Soulreach — the king reaches into a creature's chest and extracts their warmth, leaving them alive but grey, cold, and emotionally flatlined. Players who witness one Soulreach victim will not let it happen again.
**Fight Feel:** Dread and desperation. The Hollow King is slow, unstoppable, and terrible. Players should feel like they're running out of time.

---

### Lore

*The Hollow King does not haunt its throne room — it occupies it, the way cold occupies a room long after the fire has died.*

Once a king of a realm forgotten to all but the oldest histories, the being now called the Hollow King refused death with such singular ferocity that the void heard it and made an offer. It took the warmth from his chest in exchange for endless continuity. What remained rose from the burial mound one hundred years later, its crown fused to its skull, its ribcage a cage of corroded iron, its eyes two points of violet non-light. The name of the kingdom is gone. The name of the king is gone. Only the title remains.

The Hollow King does not feed in the manner of lesser undead. It reaches into the chests of the living — not with hands but with the hollow place inside itself — and pulls out warmth the way a winter wind pulls out heat. Those it takes from do not die, precisely. They continue. They breathe. They blink. They simply no longer feel anything, ever again, and the warmth flickers in the Hollow King's chest cavity for a few blessed hours before the void consumes it too.

Scholars who have studied the ruins theorize that the Hollow King is not seeking to conquer. It is seeking something specific. Those who have spoken with it and survived report it asked only one question before the reaching began: *"Is it still there?"* No one knows what *it* refers to. Some believe it was a child. Others, a love. Others still believe the question is the last vestige of the king's humanity — and that answering correctly might be the only way to end it without a fight.

**Adventure Hooks**
- A merchant caravan has gone missing in the ash lands. The sole survivor walked out three days later, alive but unable to feel heat, cold, pain, or joy. She sits in the nearest tavern and asks questions of every stranger: *"Is it still there?"*
- A scribe has found a partial name in an archive — one syllable of the king's true name. She believes speaking it within the palace will break the curse. She is probably right. She is definitely going to get herself killed without help.
- One of the player characters has a dream: a cold room, a crown on a skull, a hand reaching toward their chest, and a voice asking: *"Is it you?"*

---

**Telegraph**

> In the village nearest the ash lands, every building faces away from the eastern horizon — doors, windows, even smoke holes. The villagers explain they moved them because "the wind comes from that direction." There is no wind.

---

**Encounter Brief**

**Battlefield:** The palace throne room. Fifty feet across, ceiling lost in purple-black shadow, walls lined with silent hollow subjects standing at attention. Cold black stone floor. Four massive columns of bone and iron divide the room. The throne at the far end, raised on a dais — the Hollow King seated until it stands.

**Tactics:** Begins the encounter seated. Rises slowly, speaks its single question, then attacks. Targets the warmest-feeling character first (the healer, the paladin, whoever radiates the most goodness). Uses Soulreach on its first legendary action after moving adjacent. It is not tactical — it is *inevitable*. Moves toward its chosen target, legendary-action-stepping through columns, using Hollow Grasp to keep creatures restrained. Uses Void Exhale when three or more creatures cluster. Does not retreat. Does not flinch. Can be bargained with — but only if someone answers *"Is it still there?"* in a way that gives it pause (Charisma DC 18, or perfect roleplay).

**Pacing:** Opening dread (silent hollow subjects, the rising king, the cold) → mid-fight escalation (first Soulreach; players realize they need to protect the warmest character) → finale (king below 100 HP, Hollow Heart activates, the void in its chest becomes visible, and it becomes *desperate*).

**The Moment:** The first successful Soulreach. A player character's warmth is extracted. Their hands go grey-white, breath stops pluming in the cold air, eyes lose focus. They can still act — but they feel nothing. The other players will not let this happen again.

---

### Stat Block

```statblock
layout: Basic 5e Layout
name: The Hollow King
size: Large
type: undead
alignment: neutral evil
ac: 17
ac_text: "natural armor, corroded crown"
hp: 195
hit_dice: "26d10 + 52"
speed: "30 ft."
stats: [20, 10, 14, 18, 16, 20]
saves:
  - Con: +6
  - Wis: +7
  - Cha: +9
skillsaves:
  - History: +8
  - Insight: +7
  - Perception: +7
damage_resistances: "cold; bludgeoning, piercing, and slashing from nonmagical attacks"
damage_immunities: "necrotic, poison"
condition_immunities: "charmed, exhaustion, frightened, paralyzed, poisoned"
senses: "darkvision 120 ft., passive Perception 17"
languages: "all languages it knew in life"
cr: 11
traits:
  - name: Hollow Heart
    desc: "When the Hollow King is reduced to 100 hit points or fewer, the void within its chest becomes visible — a sphere of absolute darkness 1 foot across that pulls at warmth. Any creature that starts its turn within 10 feet of the Hollow King takes 9 (2d8) cold damage."
  - name: Legendary Resistance (3/Day)
    desc: "If the Hollow King fails a saving throw, it can choose to succeed instead."
  - name: Turn Immunity
    desc: "The Hollow King is immune to effects that turn undead."
  - name: Undying
    desc: "If the Hollow King is destroyed, it reforms on its throne in 24 hours unless its crown is removed from its skull and immersed in running water."
actions:
  - name: Multiattack
    desc: "The Hollow King makes two Hollow Grasp attacks. It can replace one attack with Soulreach if available."
  - name: Hollow Grasp
    desc: "Melee Weapon Attack: +9 to hit, reach 10 ft., one target. Hit: 16 (2d10 + 5) cold damage, and the target is restrained (escape DC 17). The restraint ends early if the Hollow King uses this attack against a different target."
  - name: Soulreach (Recharge 5–6)
    desc: "The Hollow King reaches into the chest of one restrained or willing creature within 5 feet. The target must succeed on a DC 17 Charisma saving throw or take 45 (10d8) psychic damage and lose the ability to feel temperature, pain, and strong emotion until the effect ends. While this effect persists, the creature is immune to the frightened condition and cannot gain Inspiration. The creature may repeat the saving throw at the end of each of its long rests."
  - name: Void Exhale (Recharge 6)
    desc: "The Hollow King exhales a 30-foot cone of void energy. Each creature in that area must make a DC 17 Constitution saving throw, taking 35 (10d6) cold damage plus 14 (4d6) necrotic damage on a failed save, or half as much on a success. Creatures that fail cannot regain hit points until the start of the Hollow King's next turn."
reactions:
  - name: Void Step
    desc: "Trigger: A creature the Hollow King can see moves more than 10 feet away from it. Response: The Hollow King teleports to an unoccupied space within 5 feet of that creature. This movement does not provoke opportunity attacks."
legendary_actions:
  - name: ""
    desc: "The Hollow King can take 3 legendary actions, choosing from the options below. Only one legendary action option can be used at a time and only at the end of another creature's turn. The Hollow King regains spent legendary actions at the start of its turn."
  - name: Reach
    desc: "The Hollow King makes one Hollow Grasp attack."
  - name: Emanate Cold
    desc: "Each creature within 5 feet of the Hollow King takes 9 (2d8) cold damage."
  - name: The Hollow Step (Costs 2 Actions)
    desc: "The Hollow King teleports to an unoccupied space it can see within 60 feet, then makes one Hollow Grasp attack against a creature within reach."
```

> **Personality.** The Hollow King speaks slowly, with long pauses — as if each word costs it something. It tilts its head to one side when listening, crown scraping against its shoulder bone.
> **Motivation.** It believes one of the party members carries a warmth it recognizes from before the bargain. It wants to take it, just to feel it once.
> **Escape Condition.** The Hollow King does not escape — but if presented with something that makes it hesitate (its true name, a relic from its kingdom, a sincere answer to *"Is it still there?"*), it will stop advancing.

---

## Example 2: Sera Vael, the Unrepentant (Villain NPC, CR 7)

### Concept Lock

**Identity:** A former cleric of a death goddess who lost her faith when the goddess didn't respond to her prayers for her dying child. She didn't turn to evil — she turned to *certainty*. Life and death are just mechanics, and she resents anyone who pretends otherwise.
**Want:** To prove, definitively, that prayer does nothing and meaning is a lie we tell ourselves. She engineers situations where people pray for deliverance and then delivers them herself — on her terms.
**Fear:** That she's wrong. That her daughter is somewhere, watching.
**Tell:** She addresses corpses directly before she leaves a scene, speaking quietly, as if finishing a conversation.

---

**Encounter Brief**

**Battlefield:** A temple Sera has repurposed as a base — sacred objects removed, replaced with meticulous order. Pews pushed to the walls. A circle of chalk equations on the floor. Three Cult Fanatics positioned at the exits.

**Tactics:** Opens by casting *silence* to neutralize enemy spellcasters. Stays mobile — repositions after every attack using Step of the Grave. Uses *inflict wounds* at high level when she can close to melee; she is not afraid of contact. Does not use lethal force on the first combat — she wants to make her point. If brought below 20 HP, triggers Fading Light and flees.

---

### Stat Block

```statblock
layout: Basic 5e Layout
name: Sera Vael, the Unrepentant
size: Medium
type: humanoid
subtype: human
alignment: neutral evil
ac: 15
ac_text: breastplate
hp: 117
hit_dice: "18d8 + 36"
speed: "30 ft."
stats: [12, 14, 14, 16, 20, 14]
saves:
  - Wis: +8
  - Cha: +5
skillsaves:
  - Arcana: +6
  - Insight: +8
  - Medicine: +8
  - Religion: +9
damage_resistances: necrotic
senses: "passive Perception 15"
languages: "Common, Elvish, Abyssal"
cr: 7
traits:
  - name: Spellcasting
    desc: "Sera is a 10th-level spellcaster (Wisdom, spell save DC 16, +8 to hit). She has the following cleric spells prepared: Cantrips (at will): chill touch, sacred flame, thaumaturgy; 1st level (4 slots): bane, cure wounds, inflict wounds; 2nd level (3 slots): blindness/deafness, silence, spiritual weapon; 3rd level (3 slots): animate dead, bestow curse, speak with dead; 4th level (3 slots): blight, death ward; 5th level (2 slots): antilife shell, contagion."
  - name: Unnerving Certainty
    desc: "Sera has advantage on saving throws against being frightened. When a creature within 30 feet of her fails a death saving throw, she regains 9 (2d8) hit points."
actions:
  - name: Multiattack
    desc: "Sera makes two Necrotic Touch attacks, or casts a cantrip and makes one Necrotic Touch attack."
  - name: Necrotic Touch
    desc: "Melee Spell Attack: +8 to hit, reach 5 ft., one creature. Hit: 16 (2d10 + 5) necrotic damage."
bonus_actions:
  - name: Step of the Grave
    desc: "Sera teleports up to 30 feet to an unoccupied space she can see. She can use this bonus action a number of times equal to her Wisdom modifier (5), regaining all uses on a long rest."
reactions:
  - name: Inevitable End
    desc: "When Sera reduces a creature to 0 hit points, she can use her reaction to animate the creature as a zombie. The zombie acts on initiative count 10 and follows Sera's verbal commands."
  - name: Fading Light (1/Day)
    desc: "When Sera is reduced to 20 hit points or fewer, she casts dimension door as a reaction, teleporting with one willing creature she touches."
```

> **Personality.** Sera speaks with the measured calm of someone who has decided nothing can hurt her anymore. She always finishes a sentence before reacting to anything — attack, spell, or plea.
> **Motivation.** She wants the party to see her prove her thesis: that whatever god they serve didn't save the people in this temple, and she did — by ending their suffering efficiently.
> **Escape Condition.** At 20 HP or fewer, she triggers Fading Light and retreats. She considers this inefficient, not defeat, and will plan accordingly for next time. She always whispers something to the nearest corpse before she goes.
