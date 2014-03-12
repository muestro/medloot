import medievia.parse

object1 = """
                Object: Marious's subterranean helm [helm marious subterranean]
                Item Type: ARMOR   Effects: INVISIBLE NO-DONATE NO-SACRIFICE  NO-DROP NO-STORE
                Item will give you following abilities:  REP_ROOT
                Equipable Location(s): TAKE HEAD
                Weight: 1     Value: 12167     Level Restriction: 23
                The object appears to be in perfect pristine condition.
                Days Left: Infinity
                AC-apply of 6
                Affects:
                    +40 to MANA
                    +3 to HITROLL
                """

object2 = """
            Object: a jewel-studded mitre, trimmed with gold thread [mitre jeweled gold]
            Item Type: WORN   Effects: INVISIBLE NO-DONATE NO-SACRIFICE NO-DROP  NO-STORE
            Equipable Location(s): TAKE HEAD
            Weight: 5     Value: 24389     Level Restriction: 27
            The object appears to be in perfect pristine condition.
            Days Left: Infinity
            Class Restrictions: ANTI_MAGE ANTI_THIEF ANTI_WARRIOR
            Affects:
                +32 to MANA
                +0 to INT
            Skill/Spell Modifiers:
                +8% to X-Heal (proficiency)
                -53% to Harm (proficiency)
                -49% to Hammer of Faith (proficiency)
                -51% to Demonfire (proficiency)
            """

object3 = """
            Object: a relic of vengeance [relic vengeance]
            Item Type: RELIC   Effects: ANTI-MAGE ANTI-THIEF ANTI-CLERIC  FRAGILE NO-QUEST
            Equipable Location(s): TAKE HOLD
            Weight: 5     Value: 1     Level Restriction: 31
            The object looks as if it will fall apart any day now.
            Days Left: 0
            Has 4 charges left.
            Affects:
                +1 to STR
            """


object4 = """
            Object: the dagger of unremitting vengeance [dagger vengeance]
            Item Type: WEAPON   Effects: NO_RENT ANTI-MAGE ANTI-THIEF ANTI-CLERIC NO_RELOAD BONDS NO-QUEST FORGED
            Equipable Location(s): TAKE
            Weight: 1     Value: 1     Level Restriction: 0
            Bound To: Azoth
            The object appears to be in perfect pristine condition.
            Days Left: 185
            Attributes: DAGGER  (BACKSTABBER)
            Damage Dice of 9d4
            Affects:
                +55 to HIT_POINTS
                +50 to MANA
                +6 to HITROLL
            """

object5 = """
            Object: the gloves of the golem maker [gloves golem maker]
            Item Type: ARMOR   Effects: INVISIBLE MAGIC NOEGG NO-DROP FRAGILE NO-STORE
            Equipable Location(s): TAKE HANDS
            Weight: 4     Value: 100000     Level Restriction: 26
            The object looks as if it will fall apart any day now.
            Days Left: 24
            AC-apply of 8
            Affects:
                +25 to HIT_POINTS
                -3 to DEX
            Skill/Spell Modifiers:
                -33% to Conjure Elemental (manacost)
            """

object6 = """
            Object: several blue and yellow striped scales of a craini [scales plate craini]
            Item Type: ARMOR   Effects: NoBits
            Equipable Location(s): TAKE BODY SHIELD
            Weight: 10     Value: 34096     Level Restriction: 20
            The object appears to be in perfect pristine condition.
            Days Left: Infinity
            AC-apply of 7
            Affects:
                +19 to MANA
                +2 to DAMROLL
            """

object7 = """
            Object: a bag of holding [bag holding]
            Item Type: CONTAINER   Effects: NoBits
            Equipable Location(s): TAKE HOLD
            Weight: 139     Value: 50     Level Restriction: 0
            The object appears to be in perfect pristine condition.
            Days Left: 185
            Available Weight: 45 stones
             ![ pristine] a treant bark shield
             ![ pristine] a flaming broadsword..glowing with a pale aura
             ![ pristine] a dragon's eyeball, encased in a glass sphere..glowing with a pale aura
              [ pristine] a feather quill
             ![ pristine] a necklace made from beads of obsidian..It glows blue!..glowing with a pale aura..humming quietl
            y
             ![ pristine] a pair of crystalline leg plates
             ![ pristine] a pair of mnayama wings
              [ pristine] a repaerdnim root
             ![ pristine] a sapphire swallowtail engraved bracelet
             ![ pristine] a silver disc inscribed with ancient Malindora runes(invisible)..glowing with a pale aura
             ![ pristine] the flickering abdomen of a firefly..It glows blue!
             ![ pristine] the griffon helm
             ![ pristine] the shield of Abiding Anguish
            """

object8 = """
            Object: a sapphire-studded chainmail scabbard [scabbard]
            Item Type: CONTAINER   Effects: INVISIBLE
            Equipable Location(s): TAKE WAIST
            Weight: 20     Value: 75000     Level Restriction: 22
            The object appears to be in perfect pristine condition.
            Days Left: Infinity
            Available Weight: 19 stones
            Nothing
            Affects:
                +23 to HIT_POINTS
                -10 to ARMOR
            """

object9 = """
            Object: the golden signet ring of Eldrick [eldrick golden ring signet]
            Item Type: WORN   Effects: GLOW BLESS ANTI-EVIL ANTI-NEUTRAL
            Equipable Location(s): TAKE FINGER
            Weight: 1     Value: 14000     Level Restriction: 28
            The object appears to be in perfect pristine condition.
            Days Left: Infinity
            Class Restrictions: ANTI_MAGE ANTI_CLERIC
            Affects:
                +4 to DAMROLL
                +0 to SAVING_SPELL
            """

object10 = """
            Object: the golden leggings of Eldrick [eldrick golden leggings]
            Item Type: ARMOR   Effects: GLOW INVISIBLE BLESS ANTI-EVIL ANTI-NEUTRAL
            Equipable Location(s): TAKE LEGS
            Weight: 15     Value: 15000     Level Restriction: 26
            The object appears to be in perfect pristine condition.
            Days Left: Infinity
            AC-apply of 5     Class Restrictions: ANTI_MAGE ANTI_CLERIC
            Affects:
                +3 to DAMROLL
                +20 to MANA
            """

object11 = """
            Object: a magnificent sword of ice [sword ice]
            Item Type: WEAPON   Effects: INVISIBLE ATTACK COLD
            Equipable Location(s): TAKE WIELD
            Weight: 18     Value: 5000     Level Restriction: 27
            The object appears to be in perfect pristine condition.
            Days Left: Infinity
            Attributes: ANTI_MAGE ANTI_CLERIC ANTI_THIEF
            Damage Dice of 7d7
            Affects:
                +4 to HITROLL
                +4 to DAMROLL
            """

object12 = """
            Object: the golden coin of Eldrick [eldrick golden coin gold]
            Item Type: WORN   Effects: GLOW BLESS ANTI-EVIL ANTI-NEUTRAL
            Equipable Location(s): TAKE HOLD
            Weight: 1     Value: 15000     Level Restriction: 27
            The object appears to be in perfect pristine condition.
            Days Left: Infinity
            Affects:
                +35 to HIT_POINTS
            """

object13 = """
            Object: the collar of the beast [collar beast]
            Item Type: WORN   Effects: INVISIBLE
            Equipable Location(s): TAKE NECK
            Weight: 15     Value: 9500     Level Restriction: 23
            The object appears to be in perfect pristine condition.
            Days Left: Infinity
            Affects:
                +15 to HIT_POINTS
                +3 to DAMROLL
            """

object14 = """
            Object: a repaerdnim root [root repaerdnim]
            Item Type: FOOD   Effects: NoBits
            Equipable Location(s): TAKE
            Weight: 1     Value: 10     Level Restriction: 0
            The object appears to be in perfect pristine condition.
            Days Left: 185
            """

object15 = """
            Object: a silver disc inscribed with ancient Malindora runes [disc silver silverdisc runes malindora]
            Item Type: WORN   Effects: GLOW INVISIBLE
            Equipable Location(s): TAKE HOLD
            Weight: 3     Value: 32800     Level Restriction: 16
            The object appears to be in perfect pristine condition.
            Days Left: Infinity
            Affects:
                +25 to HIT_POINTS
                +1 to HITROLL
            """

object16 = """
            Object: a silver disc inscribed with ancient Malindora runes [disc silver silverdisc runes malindora]
            Item Type: WORN   Effects: GLOW INVISIBLE
            Equipable Location(s): TAKE HOLD
            Weight: 3     Value: 32800     Level Restriction: 16
            The object appears to be in perfect pristine condition.
            Days Left: Infinity
            Affects:
                +25 to HIT_POINTS
                +1 to HITROLL
            """
from google.appengine.ext import db


'''
target = object2
print target
print "\nParsing...\n\n"

medievia.parse.parse(target)
'''
x = ["123", "1"]
x = db.StringListProperty()
print isinstance(x, list)