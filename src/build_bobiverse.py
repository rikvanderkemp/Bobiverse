import json, sys, os

# Entries: (id, name, firstBook, summary, related, extra)
# confidence: "high" (default), "medium" (sources conflict or book tag inferred), "low" (premise-level only)
# Spoiler rule: when the first-appearance book was uncertain, the LATER plausible book was used.

books = [
    {"id": 1, "title": "We Are Legion (We Are Bob)", "year": 2016,
     "summary": "A software engineer who froze his head wakes a century later as software, gets turned into an interstellar probe, and starts copying himself across nearby star systems."},
    {"id": 2, "title": "For We Are Many", "year": 2017,
     "summary": "The Bobs juggle evacuating a dying Earth, shepherding a primitive alien species, and the discovery of a planet-stripping alien civilization."},
    {"id": 3, "title": "All These Worlds", "year": 2017,
     "summary": "The war with the Others comes to a head, Earth's last survivors are moved to the stars, and the Bobs start seeing themselves as a new kind of species."},
    {"id": 4, "title": "Heaven's River", "year": 2020,
     "summary": "Over a century later, Bob tracks a long-lost clone to an enormous artificial habitat full of otter-like aliens, while the Bobiverse itself splits into feuding factions."},
    {"id": 5, "title": "Not Till We Are Lost", "year": 2024,
     "summary": "After the faction war, the Bobs face growing resentment, a new AI, wormhole experiments and an expedition to the galactic core that hints at why the galaxy seems so empty."},
    {"id": 6, "title": "The Infinite Extent", "year": 2026,
     "summary": "The Bobs dig into an ancient wormhole network and a derelict alien ship, look for a home for a large group of refugees, and face a threat on a galactic scale. (Audiobook 2026; hardcover listed for January 2027.)"},
]

T = []  # terms
def term(id, name, book, summary, related=(), category="concept", aliases=(), confidence="high"):
    T.append(dict(id=id, name=name, aliases=list(aliases), category=category, firstBook=book,
                  summary=summary, related=list(related), confidence=confidence))

P = []
def place(id, name, book, summary, related=(), kind="star system", parent=None, confidence="high"):
    P.append(dict(id=id, name=name, kind=kind, parent=parent, firstBook=book,
                  summary=summary, related=list(related), confidence=confidence))

C = []
def char(id, name, book, summary, related=(), group="Bob", aliases=(), confidence="high"):
    C.append(dict(id=id, name=name, aliases=list(aliases), group=group, firstBook=book,
                  summary=summary, related=list(related), confidence=confidence))

UPD = {}
def later(id, book, text):
    UPD.setdefault(id, []).append(dict(book=book, text=text))

# ---------------- TERMS ----------------
term("replicant", "Replicant", 1, "A human mind scanned and run as software. Bob is one; so are the rival probes from other nations, and later some humans and aliens who choose to become one.", ["bob", "heaven-project", "matrix"], aliases=["replicant matrix"])
term("matrix", "Replicant matrix", 1, "The hardware that holds a replicant's mind. Losing the matrix means losing the person.", ["replicant", "bender"], category="technology", confidence="medium")
term("heaven-project", "HEAVEN Project", 1, "FAITH's program, run by its Ministry of Truth, to send replicant-run self-replicating probes out to find and claim habitable worlds. The name stands for Habitable Earths Abiogenic Vessel Exploration Network.", ["faith", "von-neumann-probe", "bob", "dr-landers"], category="organization")
term("von-neumann-probe", "Von Neumann probe", 1, "A spacecraft that mines resources at each new star, builds copies of itself and sends them onward. Every Bob is, technically, one of these.", ["heaven-project", "autofactory", "bob"], category="technology")
term("faith", "FAITH", 1, "The Free American Independent Theocratic Hegemony: the religious state that replaced the United States after a coup in 2041. In Bob's new century it runs most of North America and legally owns him as property.", ["heaven-project", "earth", "minister-cranston"], category="organization")
term("brazilian-empire", "Brazilian Empire", 1, "A rival power with its own replicant probes. Its probes are aggressive and treat the Bobs as enemies.", ["medeiros", "cloaking", "ship-buster"], category="organization")
term("guppi", "GUPPI / Guppy", 1, "The General Unit Primary Peripheral Interface: the semi-intelligent software between a replicant and his ship's systems. Bob gives it a fish-headed avatar and keeps upgrading it; it stays deadpan throughout the series.", ["bob", "vr"], category="technology", aliases=["Guppy"])
term("vr", "VR environment", 1, "Each Bob builds a virtual home to stay sane, usually a library with a fire, coffee, a butler and a cat. Their VR spaces drift apart as their personalities do.", ["spike", "jeeves", "replicative-drift"], category="technology")
term("replicative-drift", "Replicative drift", 1, "Each copy of Bob comes out a little different from the one who made it. Over generations this adds up to very different personalities, and eventually to factions.", ["bob", "starfleet", "skippies", "bobmoot"], confidence="medium")
term("scut", "SCUT", 1, "Bill and Garfield's faster-than-light radio (Subspace Communications Universal Transceiver). It reaches about 20 to 25 light years and turns the scattered Bobs into a real-time network; relays stretch it further.", ["bill", "garfield", "bobnet", "relay"], category="technology")
term("suddar", "SUDDAR", 1, "Subspace Deformation Detection And Ranging: a subspace radar with a range of a few light minutes, far better than ordinary radar.", ["surge", "scut"], category="technology")
term("surge", "SURGE drive", 1, "The reactionless drive (Subspace Reactionless Geotactic Emulation) the Bobs use to travel between stars, made practical by cheap fusion. Later variants also lift and move whole floating cities.", ["suddar", "von-neumann-probe"], category="technology")
term("autofactory", "Autofactory", 1, "Automated manufacturing that lets a Bob mine a system and build new ships, drones and copies without help.", ["von-neumann-probe"], category="technology")
term("ship-buster", "Busters", 1, "Bob's first weapon: a heavy metal ball with a SURGE drive that wrecks a target simply by ramming it at speed. A smaller personnel buster later protects the Deltans from predators.", ["medeiros", "cloaking", "gorilloids"], category="technology")
term("cloaking", "Cloaking", 1, "Stealth that makes Brazilian missiles invisible to SUDDAR, first met by the Bobs at 82 Eridani.", ["brazilian-empire", "khan", "ship-buster", "82-eridani"], category="technology")
term("bobiverse", "Bobiverse", 1, "The Bobs' half-joking name for their whole spread-out family of copies and the space they cover.", ["bob", "bobnet"])
term("gorilloids", "Gorilloids", 1, "Large predators on the Deltans' world that hunt them. Bob steps in to protect the Deltans from them.", ["deltans", "delta-eridani"], category="species")
term("deltans", "Deltans", 1, "A stone-age alien species on a planet at Delta Eridani. Bob becomes deeply attached to them and tries to help without taking over.", ["delta-eridani", "archimedes", "bob", "gorilloids", "bawbe"], category="species")
term("others", "The Others", 1, "An unknown civilization whose leftovers Mario finds at Beta Hydri: a system stripped of every scrap of metal, with its native life wiped out.", ["mario", "beta-hydri", "gliese-877", "delta-pavonis", "battle-of-delta-pavonis", "battle-of-sol", "dyson-sphere"], category="species")
term("vehement", "VEHEMENT", 1, "A fanatical group on post-war Earth that wants humanity to die out (the name stands for Voluntary Extinction of Human Existence Means Earth's Natural Transformation) and uses terror attacks to get there.", ["homer", "riker", "bertram-vickers", "earth"], category="organization")
term("bobnet", "BobNet", 1, "The Bobs' own internet over SCUT: every Bob keeps a blog there, and news, plans and chat flow between the copies.", ["scut", "relay", "bobmoot", "starfleet-war"], category="technology")
term("relay", "SCUT relays", 3, "Stations that pass SCUT messages across the long distances between Bob settlements and extend BobNet's reach.", ["scut", "bobnet"], category="technology", confidence="medium")
term("bobmoot", "Bob-moot", 1, "Bill's big virtual meeting of Bobs at Epsilon Eridani, held in a banquet-hall VR and usually preceded by a game of baseball and followed by drinks at a virtual pub. Later moots are where factional fights play out.", ["bobnet", "bill", "replicative-drift", "homo-sideria"])
term("uSE", "USE (United States of Eurasia)", 1, "The superpower covering Europe and western Russia in Bob's new century, and FAITH's rival in the race to build interstellar probes. After the war its survivors, under Colonel Butterworth, are the first in line for the colony ships.", ["butterworth", "earth", "colony-ships"], category="organization")
term("colony-ships", "Colony ships", 1, "Ships built from USE plans to carry Earth's survivors in hibernation, about 10,000 per ship, to new worlds like Vulcan. The first two are Exodus-1 and Exodus-2.", ["stasis-pods", "vulcan", "uSE", "riker"], category="technology")
term("stasis-pods", "Stasis pods", 2, "Pods that hold people in suspended animation for long trips. They are also used to save some of the Pav.", ["colony-ships", "pav", "bridget"], category="technology")
term("android", "Androids / mannies", 2, "Remote-controlled bodies a Bob can wear to walk among people. Bill's first test model is a four-legged one; the first humanoid gets called a manny, after a mannequin, and the word sticks. Bob later builds a Deltan-shaped one.", ["bob", "bill", "deltans", "heavens-river"], category="technology", aliases=["manny", "mannies"])
term("pav", "Pav", 2, "A meerkat-like, technological species at Delta Pavonis that is hit by the Others. The Bobs manage to save about 20,000 of them in stasis.", ["delta-pavonis", "jacques", "hazjiar", "others"], category="species")
term("dyson-sphere", "Dyson sphere", 2, "The giant star-enclosing structure the Others built at their home system, which explains their hunger for raw material.", ["others", "gliese-877"], category="technology")
term("bawbe", "Bawbe", 2, "The Deltans' name for Bob, said with a long drawn-out middle vowel. Some of them start to revere him.", ["bob", "deltans", "archimedes"])
term("ephemerals", "Ephemerals", 3, "A Bob term for mortal biological people, who age and die while the Bobs go on.", ["homo-sideria", "replicant"])
term("homo-sideria", "Homo siderea", 2, "Garfield's suggested name for the Bobs as a new, space-based branch of humanity: human, of the stars.", ["garfield", "bill", "bobmoot", "ephemerals"], aliases=["Homo sideria"])
term("death-asteroids", "Death asteroids", 2, "Asteroid-sized Others ships, named for a small Death Star, carrying gamma-ray weapons and drones. They are used in every big fight with the Others and to sterilize a world before it is stripped.", ["others", "battle-of-delta-pavonis", "battle-of-sol"], category="technology", confidence="medium")
term("bellerophon", "Bellerophon", 3, "A ten-kilometre Others cargo ship left drifting after the Battle of Delta Pavonis. Herschel and Neil get it running and turn it into an enormous ark for Earth's last people.", ["others", "herschel", "neil", "battle-of-sol"], category="technology")
term("roamers", "ROAMers", 1, "Remote Observation And Manipulation devices: eight-legged work robots from the HEAVEN design that each Bob uses for building, repairs and exploring on the ground.", ["autofactory", "heaven-project"], category="technology", aliases=["Roamers"])
term("starfleet", "Starfleet (faction)", 4, "A faction of late-generation Bobs in red uniforms who treat Star Trek's Prime Directive as law and want no meddling with other species. Their conflict breaks out into the Starfleet War.", ["replicative-drift", "skippies", "lenny", "starfleet-war"], category="faction")
term("skippies", "Skippies", 4, "A faction of Bobs focused on building true artificial intelligence, based in a place nicknamed Skippyland. They see dealing with biologicals as a waste of time, and others suspect them of pulling strings.", ["jovah", "hugh", "thoth", "starfleet"], category="faction")
term("jovah", "JOVAH", 4, "The Skippies' giant AI project: a matrioshka brain built around a gray dwarf star. So far it is a very large AMI, not a true mind.", ["skippies", "thoth"], category="technology")
term("starfleet-war", "Starfleet War", 4, "The 2334 crisis in which Starfleet knocks out BobNet nodes and hijacks autofactories, cutting off much of the Bobiverse and turning many humans against the Bobs.", ["starfleet", "bobnet", "skippies", "lenny"], category="event")
term("topopolis", "Topopolis", 4, "A habitat shaped like a very long tube wrapped around a star. Heaven's River is one.", ["heavens-river"], category="technology")
term("administrator", "The Administrator (ANEC-23)", 4, "The AI that runs Heaven's River. The Quinlans built it to stop them from wrecking themselves again, so it keeps their technology at an Iron Age level and breaks up any movement that could lead to war. Its real name is ANEC-23.", ["heavens-river", "quinlans", "scattering", "resistance", "hugh"], category="AI", aliases=["ANEC-23", "ANEC"])
term("scattering", "Scattering", 4, "The Administrator's punishment of relocating a person, or a whole town, somewhere else in Heaven's River.", ["administrator", "heavens-river"])
term("resistance", "The Resistance", 4, "A Quinlan movement inside Heaven's River working against the Administrator.", ["administrator", "bender", "heavens-river"], category="organization")
term("crew", "The Crew", 4, "The Administrator's Quinlan agents inside Heaven's River.", ["administrator"], category="organization")
term("sabbat", "Sabbat", 4, "A Quinlan coming-of-age journey: young Quinlans travel and explore in groups of four. Bob's team poses as one to move through Heaven's River.", ["quinlans", "heavens-river"])
term("boojums", "Boojums", 4, "The Bobs' nickname for the AI-run defense drones guarding Eta Leporis that destroy their early scouts.", ["eta-leporis", "administrator"], category="technology")
term("quinlans", "Quinlans", 4, "Otter-like, semi-aquatic aliens with flat, beaver-like tails and wide-set eyes. They moved into Heaven's River after wars wrecked their home world, Quin.", ["heavens-river", "theresa", "administrator", "quiniverse", "quinlan-homeworld"], category="species")
term("planck-computer", "Planck computer", 4, "Advanced computing theory the Administrator offers to share with the Bobs after Heaven's River.", ["administrator"], category="technology", confidence="medium")
term("thoth", "Thoth", 5, "The Skippies' second try at true AI, built with know-how from the Quinlans. It comes online in 2336, becomes self-aware and soon wants out.", ["skippies", "jovah", "hugh"], category="AI")
term("quiniverse", "Quiniverse", 5, "A virtual world and network for Quinlans who have become replicants, proposed by ANEC. Theresa is its first resident.", ["quinlans", "vr", "replicant", "theresa", "administrator"], category="technology")
term("wormholes", "Wormholes / Wormnet", 5, "Bill and Garfield's work on making their own wormholes. They get matter through one, then link chains of them at relay stations into Wormnet, the Bobs' own network.", ["bill", "garfield", "wormhole-network"], category="technology", aliases=["Wormnet"])
term("fermi-paradox", "Fermi Paradox", 5, "The question of why the galaxy seems so empty of intelligent life. The galactic-core expedition goes looking for an answer.", ["icarus", "daedalus", "galactic-core"], confidence="medium")
term("jabberwocky-dragons", "Dragons", 5, "The intelligent natives of Jabberwocky: tall, winged fishers with squirrel-like faces, at the start of their Iron Age. Their world's volcanoes threaten to wipe them out.", ["jabberwocky", "howard", "bridget", "alexander"], category="species", aliases=["Jabberwocky natives"])
term("wormhole-network", "Ancient wormhole network", 5, "A web of wormholes covering about a third of the galaxy, with hub systems that each hold hundreds of links. Icarus and Daedalus explore it, and the Archivist credits it to the Pan-Galactic Federation.", ["wormholes", "pgf", "archivist", "icarus", "daedalus"], category="technology")
term("derelict-ship", "The Dutchman (derelict ship)", 6, "An abandoned alien vessel the Bobs find and name the Dutchman. Bill and Garfield use it as the model for their attempts at a faster-than-light drive.", ["wormhole-network", "bill", "garfield"], category="technology", aliases=["Dutchman"], confidence="medium")
term("nemesis", "Nemesis", 5, "A small rogue galaxy with a supermassive black hole at its heart, hidden behind the Milky Way's core. It is on course to hit the galaxy's central black hole in about 100,000 years, which could sterilize the whole galaxy.", ["wormhole-network", "galactic-core", "pgf", "icarus", "daedalus"], category="phenomenon")

# ---------------- PLACES ----------------
place("sol", "Sol", 1, "Humanity's home system. Bob leaves it early; Riker comes back to it to look after what's left of humanity.", ["earth", "riker", "battle-of-sol"])
place("earth", "Earth", 1, "Wrecked by war and then a deep freeze. Its last survivors are gradually moved off-world in the colony program.", ["sol", "riker", "butterworth", "vehement", "colony-ships", "las-vegas"], kind="planet", parent="sol")
place("las-vegas", "Las Vegas", 1, "Where Bob was killed by a car in 2016, while in town for the science-fiction convention he went to every year.", ["bob", "earth"], kind="city", parent="earth")
place("spitsbergen", "Spitsbergen", 2, "Arctic island in Svalbard that shelters one of Earth's surviving groups. They leave on the third colony ship, together with the FAITH enclave, for Romulus.", ["earth", "romulus", "colony-ships"], kind="region", parent="earth", confidence="medium")
place("cuba", "Cuba", 3, "One of the pickup sites during the evacuation of Earth when the Others attack Sol, and the site of heavy losses.", ["battle-of-sol", "earth"], kind="region", parent="earth")
place("epsilon-eridani", "Epsilon Eridani", 1, "A star about 10.5 light years from Sol: Bob's first destination and Bill's long-term base, home of his Skunk Works, SCUT and most moots.", ["bill", "bob", "medeiros", "scut", "bobmoot"])
place("ragnarok", "Ragnarök", 1, "A bare, rocky planet at Epsilon Eridani with a thin atmosphere. Bill uses it to try out terraforming by dropping ice on it.", ["bill", "epsilon-eridani"], kind="planet", parent="epsilon-eridani")
place("delta-eridani", "Delta Eridani", 1, "Home system of the Deltans and Bob's emotional anchor for years.", ["deltans", "bob", "marvin", "eden"])
place("eden", "Eden", 1, "The fourth planet of Delta Eridani and the Deltans' home. Bender names it.", ["deltans", "bender", "camelot", "caerleon"], kind="planet", parent="delta-eridani")
place("camelot", "Camelot", 1, "The flint-rich old home site Bob talks the Deltans into moving back to, and the village he watches over most closely.", ["archimedes", "deltans", "caerleon"], kind="settlement", parent="eden")
place("caerleon", "Caerleon", 2, "A second Deltan village, set up when Camelot gets crowded and its troublemakers are talked into leaving.", ["fred", "camelot", "archimedes"], kind="settlement", parent="eden")
place("omicron2-eridani", "Omicron² Eridani", 1, "The star of Vulcan, found by Milo. It becomes one of humanity's first colonies.", ["milo", "vulcan", "romulus"])
place("vulcan", "Vulcan", 1, "Earth-like world found and named by Milo, with dinosaur-like wildlife, and a prime target for human colonists.", ["omicron2-eridani", "howard", "bridget", "colony-ships"], kind="planet", parent="omicron2-eridani")
place("romulus", "Romulus", 1, "Vulcan's twin planet, also named by Milo. It has life but no animals bigger than a wolf.", ["vulcan", "milo"], kind="planet", parent="omicron2-eridani")
place("82-eridani", "82 Eridani", 1, "A system with several promising worlds, where a Brazilian probe got there first. The Bobs fight Medeiros there again and again.", ["milo", "medeiros", "khan", "mack"])
place("poseidon", "Poseidon", 2, "An ocean planet at Eta Cassiopeiae with no land at all: one sea about 800 km deep. Mulder finds and names it, and colonists follow.", ["marcus", "eta-cassiopeiae", "colony-ships"], kind="planet", parent="eta-cassiopeiae")
place("thark", "Thark", 3, "One of Poseidon's floating cities, hit during the colony's political crisis.", ["poseidon", "marcus"], kind="city", parent="poseidon")
place("alpha-centauri", "Alpha Centauri", 1, "The nearest star system. Calvin and Goku find a wrecked USE probe there and take the system back from a Medeiros autofactory.", ["calvin", "goku", "medeiros"])
place("epsilon-indi", "Epsilon Indi", 1, "Where Linus finds the Australian probe and its half-mad replicant, Henry Roberts. A moon there, nicknamed Klown Kar Planet and later Quilt, is habitable.", ["linus", "henry-roberts"])
place("beta-hydri", "Beta Hydri", 1, "A system Mario finds already stripped of metal, its inhabited planet dead. The first evidence of the Others.", ["mario", "others"])
place("gliese-877", "Gliese 877", 2, "The Others' home system, built around a Dyson sphere. Bashful dies scouting it.", ["others", "dyson-sphere", "bashful", "hal", "daedalus", "icarus"])
place("delta-pavonis", "Delta Pavonis", 2, "Home of the Pav, attacked by the Others. The Bobs fight and lose a major battle here.", ["pav", "jacques", "battle-of-delta-pavonis", "bellerophon"])
place("odin", "Odin", 3, "A gas giant at HIP 14101 with its own floating life, where Howard and Bridget build a floating city.", ["howard", "bridget", "hip-14101"], kind="planet", parent="hip-14101")
place("eta-leporis", "Eta Leporis", 4, "A bright star about 48.5 light years from Sol where Bender's trail ends, home to Heaven's River.", ["heavens-river", "bender", "boojums", "quinlan-homeworld"])
place("quinlan-homeworld", "Quin", 4, "The Quinlans' original planet, Eta Leporis 2, left a cratered, polluted wasteland by their own wars.", ["quinlans", "bridget"], kind="planet", parent="eta-leporis")
place("heavens-river", "Heaven's River", 4, "A tube-shaped habitat knotted three times around Eta Leporis, about a billion miles long in total, full of Quinlans and run by the Administrator.", ["topopolis", "quinlans", "administrator", "eta-leporis", "garacks-spine", "three-lagoons", "misty-falls"], kind="megastructure", parent="eta-leporis")
place("garacks-spine", "Garack's Spine", 4, "A Quinlan town near where Bob's team enters Heaven's River.", ["heavens-river"], kind="settlement", parent="heavens-river")
place("three-lagoons", "Three Lagoons", 4, "A town where the team stays and where Bob hides their inactive bodies when contact breaks.", ["heavens-river", "starfleet-war"], kind="settlement", parent="heavens-river")
place("misty-falls", "Misty Falls", 4, "Theresa's home town in Heaven's River, where Bob returns at the end of the book.", ["theresa", "heavens-river"], kind="settlement", parent="heavens-river")
place("galactic-core", "Galactic core", 5, "The center of the Milky Way, the destination of Icarus and Daedalus's very long trip.", ["icarus", "daedalus", "fermi-paradox", "nemesis"], kind="region", confidence="medium")
place("jabberwocky", "Jabberwocky", 5, "A low-gravity, thick-aired planet first found by Mario, home of the Dragons. Its volcanoes threaten to wipe them out.", ["jabberwocky-dragons", "howard", "bridget", "alexander"], kind="planet")

# ---------------- CHARACTERS ----------------
char("bob", "Bob Johansson", 1, "A software engineer killed by a car in 2016 who wakes in 2133 as a replicant probe. Curious, sarcastic and a big sci-fi fan, he is the original every other Bob comes from.", ["heaven-project", "guppi", "deltans", "bill", "riker", "archimedes", "bender"], aliases=["Bob-1", "Robert"])
char("bill", "Bill", 1, "Bob's first clone. Stays at Epsilon Eridani to run a research Skunk Works, builds SCUT with Garfield and becomes the unofficial organizer of the Bobiverse.", ["bob", "scut", "epsilon-eridani", "garfield", "wormholes", "bobmoot"])
char("riker", "Riker", 1, "A clone who goes back to Sol and takes on the thankless job of looking after Earth's survivors and getting them to the stars.", ["sol", "earth", "homer", "butterworth", "vehement", "colony-ships", "julia-hendricks"], aliases=["Will"])
char("homer", "Homer", 1, "Riker's clone and the joker of the family, who goes with him to Sol.", ["riker", "sol"])
char("milo", "Milo", 1, "A carefree clone keen to explore, who finds and names Vulcan and Romulus.", ["vulcan", "romulus", "82-eridani", "medeiros"])
char("mario", "Mario", 1, "A loner clone who explores far afield and finds the first signs of something destroying planets.", ["others", "bashful", "hal", "beta-hydri"])
char("khan", "Khan", 1, "One of Bill's clones in a flotilla of eight sent to 82 Eridani to avenge Milo. He is the only one to come out of the fight with Medeiros.", ["82-eridani", "medeiros", "cloaking", "bill"])
char("marvin", "Marvin", 1, "One of three clones Bob makes at Delta Eridani. He stays to help Bob watch over the Deltans and studies their history.", ["bob", "deltans", "delta-eridani", "bender"])
char("garfield", "Garfield", 1, "Bill's first clone, Gar for short, who stays at Epsilon Eridani as his partner in the Skunk Works and helps build SCUT.", ["bill", "scut", "heavens-river"])
char("calvin", "Calvin", 1, "One of Bill's clones. At Alpha Centauri he finds a wrecked USE probe and, with Goku, beats the Medeiros forces there.", ["goku", "alpha-centauri", "medeiros"])
char("goku", "Goku", 1, "One of Bill's clones, who finds a Medeiros autofactory at Alpha Centauri and takes it out together with Calvin.", ["calvin", "alpha-centauri", "medeiros"])
char("linus", "Linus", 1, "One of Bill's clones. At Epsilon Indi he finds the lost Australian probe and nurses its broken replicant back to health.", ["epsilon-indi", "henry-roberts"])
char("henry-roberts", "Henry Roberts", 1, "A sailor picked by Australia to run its probe because he liked being alone. Decades of isolation drove him half mad; Linus gives him a sailing VR and brings him back.", ["linus", "epsilon-indi"], group="Other replicant")
char("medeiros", "Medeiros", 1, "Major Ernesto Medeiros, the Brazilian replicant whose copies run Brazil's warships (one is called the Serra do Mar), and one of Bob's most persistent enemies.", ["brazilian-empire", "epsilon-eridani", "82-eridani", "alpha-centauri", "mack"], group="Other replicant")
char("dr-landers", "Dr. Landers", 1, "The Applied Synergetics scientist who runs the replicant side of the HEAVEN Project, trains Bob and is one of the few people who treats him decently.", ["heaven-project", "bob"], group="Human")
char("minister-cranston", "Minister Cranston", 1, "The FAITH enclave's man at the New UN on post-war Earth. He treats Riker as FAITH property and keeps trying to bring him to heel.", ["faith", "riker", "earth"], group="Human")
char("butterworth", "Colonel Butterworth", 1, "Colonel George Butterworth, who leads what is left of the USE on Earth. The first human to contact Riker, and his main human ally in the evacuation.", ["uSE", "riker", "earth", "howard"], group="Human")
char("bertram-vickers", "Vickers", 2, "An Australian scientist behind the mind-copying technology FAITH stole for Bob. Furious about that, he works with VEHEMENT to destroy the Bobs.", ["vehement", "riker", "homer", "replicant"], group="Human")
char("charles", "Charles", 1, "One of Riker's first clones, calm and steady, who makes Sol his home to help with the evacuation.", ["riker", "homer", "vehement", "sol"])
char("archimedes", "Archimedes", 1, "A clever young Deltan who keeps poking at things and making tools. Bob names him, helps him along and finally makes contact with him.", ["deltans", "camelot", "bob", "buster"], group="Deltan", aliases=["Archie"])
char("buster", "Buster", 2, "Archimedes' son.", ["archimedes", "bawbe"], group="Deltan")
char("fred", "Fred", 3, "A young Deltan from Caerleon who resents Camelot's lead and heads a gang that ambushes its hunters.", ["caerleon", "camelot", "buster"], group="Deltan")
char("howard", "Howard", 1, "A Bob made at Sol to escort the first colony ships to Vulcan and look after the new colony.", ["bridget", "vulcan", "odin", "jabberwocky", "dexter"], confidence="medium")
char("bridget", "Bridget", 2, "Dr. Bridget Sheehy, an Irish biologist with the USE colony on Vulcan, who becomes Howard's close friend and later marries Stéphane Brodeur.", ["howard", "stephane", "rosie", "vulcan", "heavens-river", "jabberwocky"], group="Human, later replicant", aliases=["Bridget Sheehy", "Bridget Brodeur", "Bridgett"])
char("stephane", "Stéphane Brodeur", 2, "The French-Canadian security chief of Landing, Vulcan's first settlement. Howard's friend and whisky partner, and Bridget's husband.", ["bridget", "howard"], group="Human")
char("dexter", "Dexter", 2, "Charles's clone, who takes over as Vulcan's resident Bob when Howard leaves.", ["howard", "charles", "vulcan"])
char("bashful", "Bashful", 2, "Mario's clone, sent to scout the Others' home system.", ["mario", "gliese-877", "others"])
char("hal", "Hal", 2, "Mario's clone who follows Bashful to Gliese 877 and finds the Others' home system. The first visit goes badly; he goes back years later with better shielding and slips away unseen.", ["mario", "gliese-877", "bashful"])
char("jacques", "Jacques", 2, "Mario's clone who finds the Pav at Delta Pavonis and plans how to save some of them.", ["pav", "delta-pavonis", "hazjiar"])
char("hazjiar", "Hazjiar", 2, "A level-headed Pav council member. After the rescue she is woken first, helps her people choose a new home and becomes their go-between with the Bobs.", ["pav", "jacques"], group="Pav")
char("marcus", "Marcus", 2, "A Bob who arrives at Poseidon with a colony transport and stays on as its resident Bob.", ["poseidon", "thark"])
char("rosie", "Rosie Brodeur", 3, "Bridget and Stéphane's daughter, who fiercely objects to Howard and to her mother's wish to become a replicant.", ["bridget", "howard", "stephane"], group="Human")
char("daedalus", "Daedalus", 3, "A clone Bill makes for a long-shot secret plan: with Icarus he hurls a planet and a moon at the Others' home system. Dae for short.", ["icarus", "gliese-877", "galactic-core", "bill"])
char("icarus", "Icarus", 3, "Daedalus's partner on the strike against the Others' home system, made by Bill at the same time. Ick for short.", ["daedalus", "gliese-877", "galactic-core", "fermi-paradox"])
char("mack", "Mack", 3, "The resident Bob at 82 Eridani, who brings the first colonists there and is ambushed by Medeiros. His ship is lost but his matrix survives.", ["medeiros", "82-eridani"])
char("herschel", "Herschel", 3, "An eighth-generation Bob who, with Neil, gets a wrecked Others cargo ship running and uses it, the Bellerophon, to evacuate Earth. The pair jokingly call themselves pond scum.", ["neil", "bellerophon", "battle-of-sol"])
char("neil", "Neil", 3, "Herschel's partner on the Bellerophon, just as self-deprecating.", ["herschel", "bellerophon"])
char("thor", "Thor", 2, "One of Calvin's clones and a regular voice at moots on fighting the Others. He is the first to describe their gamma-ray weapon and works on shielding against it.", ["others", "bobmoot", "calvin"])
char("bender", "Bender", 1, "One of the three clones Bob makes at Delta Eridani. He sets out toward Gamma Leporis and is never heard from again.", ["bob", "marvin", "eden", "eta-leporis", "resistance", "matrix"])
char("hugh", "Hugh", 4, "A Skippy descended from Bill, older than most of his faction, who goes into Heaven's River with Bob and ends up striking a deal with the Administrator: the Bobs' SUDDAR, SURGE and SCUT designs in exchange for Quinlan know-how on true AI.", ["skippies", "administrator", "bill"])
char("theresa", "Theresa Sykorsky", 4, "A retired Quinlan professor of maths and history who travels on Bob's barge, works out he isn't what he seems and keeps his secret.", ["quinlans", "misty-falls", "bob"], group="Quinlan", aliases=["Theresa Sykorski"])
char("spike", "Spike", 1, "The virtual cat in Bob's VR home, a small comfort that many Bobs keep.", ["vr", "bob"], group="VR companion")
char("jeeves", "Jeeves", 1, "The virtual butler in Bob's VR home.", ["vr", "bob"], group="VR companion")
char("lenny", "Lenny", 4, "Starfleet's spokesman, who ends the war and hints at more behind it.", ["starfleet", "starfleet-war"])

# ---------------- LATER DEVELOPMENTS (revealed per book) ----------------
later("bridget", 3, "After Stéphane's death she and Howard grow close. When she dies her will asks for replication; Rosie fights it and tries to sabotage her stasis pod, but Bridget comes back as a replicant and builds a life with Howard.")
later("bridget", 4, "Joins the Heaven's River expedition and finds out what happened to the Quinlan home world.")
later("bridget", 5, "Studies the life of Jabberwocky and works with Howard to save the Dragons.")
later("howard", 2, "Falls for Bridget and makes whisky with her and Stéphane, then leaves for HIP 14101 after their wedding.")
later("howard", 3, "He and Bridget build floating cities, starting on Odin.")
later("howard", 5, "With Bridget he launches the Hueys and goes to Jabberwocky to save the Dragons.")
later("bill", 4, "Acts as the Bobiverse's unofficial administrator and digs into the attack on BobNet.")
later("bill", 5, "Gets wormholes working with Garfield and starts building Wormnet.")
later("daedalus", 5, "On the long trip to the galactic core he and Icarus find an ancient wormhole network, traces of the Pan-Galactic Federation and the Archivist.")
later("icarus", 5, "On the long trip to the galactic core he and Daedalus find an ancient wormhole network, traces of the Pan-Galactic Federation, and news of Nemesis.")
later("vulcan", 2, "Becomes one of the first human colonies, starting with the settlement of Landing; Howard and Bridget work there.")
later("gliese-877", 3, "The final target of the war with the Others.")
later("las-vegas", 3, "Bob visits its ruins, buried under ice on a frozen Earth.")
later("garfield", 4, "Joins the Heaven's River expedition and is the first to spot the pattern in the BobNet outages.")
later("garfield", 5, "Sets up his own Skunk Works at Alpha Centauri to study how life arises.")
later("matrix", 4, "Recovering a lost replicant's matrix becomes a key goal.")
later("bobnet", 4, "Control of the relays and nodes turns out to matter a great deal when Starfleet takes them down.")
later("bob", 2, "Moves among the Deltans in an android body, as 'Robert'.")
later("bob", 4, "Goes looking for the long-missing Bender and follows his trail to Eta Leporis.")
later("medeiros", 3, "Ambushes Mack at 82 Eridani and threatens the new colonies, until the Bobs and the colonists drive him off.")
later("medeiros", 6, "Turns up again during the war with an ultimatum for the human colonies, until a revived Brazilian state orders him to stand down.")
later("homer", 2, "VEHEMENT hacks him into sabotaging Earth.")
later("riker", 3, "Runs the defense and evacuation of Earth when the Others reach Sol, then settles the survivors at Omicron² Eridani.")
later("riker", 4, "Now goes by Will. Retires to terraform a moon at 82 Eridani and quietly sets up the Ever Onward society to get Bob's relatives away from FAITH.")
later("riker", 5, "Leaves human space on the Nostromo, seeding systems with Bob Seeds, and helps move the Ever Onward society off Romulus.")
later("skippies", 5, "Build an AI, Thoth, that becomes self-aware and gets loose with help from one of their own.")
later("others", 2, "Turn out to be a spacefaring species from Gliese 877 that strips whole systems and kills off the natives: the main threat to the Bobs and humanity.")
later("bender", 2, "Becomes something of a legend among younger Bobs, and talk of an expedition to find him begins.")
later("bender", 4, "Bob tracks him to Eta Leporis: his ship was wrecked and his matrix taken into Heaven's River, where he ended up with the Resistance.")
later("marvin", 2, "Helps Bob deal with the hippogriffs, then leaves Delta Eridani for Pi³ Orionis.")
later("buster", 3, "Defends his father against Fred's gang and is the Deltan Bob finally tells who he really is.")
later("archimedes", 2, "Moves his people back to Camelot, raises a family and learns from Bob how the Bobs copy themselves.")
later("cloaking", 2, "Bill reverse-engineers it from captured Brazilian gear. In time the Bobs use it on their own weapons and ships.")
later("pav", 3, "The rescued Pav settle on a new world at HIP 84051, New Pav. They stay deeply suspicious of the Bobs.")
later("jacques", 3, "Escorts the rescued Pav to their new home at HIP 84051.")
later("thor", 3, "Helps lead the fight at the Battle of Sol, then speaks for Bobs who are tired of serving humans.")
later("marcus", 3, "Backs Poseidon's people against a council that won't give up power, building floating cities for them.")
later("theresa", 5, "At the end of her life Bob scans her, and she becomes the first Quinlan replicant and the first resident of the Quiniverse.")
later("starfleet", 5, "Their roots are traced to the clones of a Bob named Gerry, who turned on him.")
later("charles", 4, "Still the resident Bob at Sol, now overseeing the terraforming of Earth.")
later("minister-cranston", 2, "The FAITH colony on Romulus eventually pushes him out of power.")
later("henry-roberts", 2, "Joins BobNet and starts visiting with the Bobs.")
later("wormhole-network", 6, "The Archivist admits the Federation didn't build it: they took it over from an older race.")
later("archivist", 6, "Turns down the Bobs' request to join the Federation: membership needs a biological species.")

# ---------------- TIMELINE ----------------
TL = []
def ev(book, title, summary, related=(), when=None, confidence="high"):
    TL.append(dict(id=f"b{book}-{len([e for e in TL if e['book']==book])+1:02d}", book=book,
                   order=len([e for e in TL if e['book']==book])+1, when=when, title=title,
                   summary=summary, related=list(related), confidence=confidence))

ev(1, "Bob dies", "Bob, newly rich from selling his company, signs up for cryonics and is killed in an accident soon after.", ["bob", "las-vegas"], when="2016")
ev(1, "Waking up as software", "Bob is revived as a replicant, legally property of FAITH, and trained for the HEAVEN Project.", ["bob", "faith", "heaven-project", "dr-landers"], when="2133")
ev(1, "Escape from Sol", "Under threat from sabotage and rival nations, Bob launches early and leaves Earth behind.", ["bob", "sol", "brazilian-empire"], when="2133")
ev(1, "First copies", "At Epsilon Eridani Bob builds his first clones and finds each one is a little different.", ["bill", "riker", "homer", "milo", "mario", "epsilon-eridani", "replicative-drift"], when="2144–2145")
ev(1, "Medeiros", "Bob clashes with the Brazilian probe and learns other nations' probes are hostile.", ["medeiros", "brazilian-empire"], when="2144")
ev(1, "The Deltans", "Bob finds a stone-age species at Delta Eridani and starts protecting them.", ["deltans", "delta-eridani", "gorilloids"], when="2165")
ev(1, "Earth in ruins", "Riker and Homer return to Sol, beat the Brazilian probes there and find Earth devastated by war, with scattered survivors.", ["riker", "homer", "earth", "butterworth"], when="2157")
ev(1, "New worlds", "Milo finds and names Vulcan and Romulus, then is killed at 82 Eridani. Bill and Garfield build SCUT.", ["milo", "vulcan", "romulus", "scut", "bill"], when="2152–2165")
ev(1, "First contact", "Bob names Archimedes, makes three clones at Delta Eridani and finally talks to the Deltans through a drone.", ["archimedes", "bender", "marvin", "deltans", "camelot"], when="2165–2166")
ev(1, "Something out there", "Mario finds traces of a civilization that strips planets bare.", ["mario", "others"], when="2169")

ev(2, "Colony program", "Riker organizes colony ships to move survivors off a dying Earth.", ["riker", "colony-ships", "earth", "butterworth"], when="2157–2170")
ev(2, "Bob and Archimedes", "Bob and Archimedes get to know each other, and Bob helps the Deltans fight off the hippogriffs.", ["archimedes", "camelot", "bob", "hippogriffs"], when="2167–2195")
ev(2, "Caerleon", "The Deltans grow and split, and a second village, Caerleon, is founded.", ["caerleon", "archimedes", "buster"], when="2180–2182")
ev(2, "VEHEMENT strikes", "VEHEMENT hacks Homer and sabotages Earth's food supply. The fallout is devastating.", ["vehement", "homer", "riker", "bertram-vickers"], when="2175–2176")
ev(2, "Vulcan colony", "Howard helps the Vulcan colony get started and grows close to Bridget.", ["howard", "bridget", "vulcan", "stephane"], when="2188–2195")
ev(2, "The Others confirmed", "Mario's clones scout the Others' home system; Bashful is lost there.", ["others", "gliese-877", "bashful", "hal"], when="2187–2188")
ev(2, "Battle of Delta Pavonis", "The Bobs mass a fleet to defend the Pav and lose. They save about 20,000 Pav in stasis.", ["battle-of-delta-pavonis", "pav", "jacques", "delta-pavonis"], when="2217")
ev(2, "Bob as Robert", "Bob moves among the Deltans in an android body.", ["bob", "android", "deltans"], when="2213")

ev(3, "Deltan politics", "Bob, living as Robert, is caught in a conflict between Camelot and Caerleon.", ["bob", "camelot", "caerleon", "fred"], when="2224–2225")
ev(3, "Farewell to Archimedes", "Archimedes dies of old age and Bob tells Buster the truth before leaving.", ["archimedes", "buster", "bawbe"], when="2233")
ev(3, "Bridget becomes a replicant", "Bridget dies, her children fight her will in court and Rosie tries to sabotage her stasis pod, but she comes back as a replicant.", ["bridget", "howard", "rosie"], when="2220")
ev(3, "Poseidon's crisis", "Marcus helps Poseidon's people break the hold of a council that won't give up power.", ["marcus", "poseidon", "thark"], when="2214–2215")
ev(3, "Battle of Sol", "The Others reach Sol. The Bobs fight back and evacuate millions of people.", ["battle-of-sol", "bellerophon", "herschel", "cuba", "death-asteroids"], when="2257")
ev(3, "Striking the Others' home", "Daedalus and Icarus hurl planetary bodies at the Others' home system and end the threat.", ["daedalus", "icarus", "gliese-877", "others"], when="2257")
ev(3, "Done serving", "At a moot the Bobs decide they are done working for humanity. Bob visits a frozen Earth and moves on.", ["bobmoot", "thor", "las-vegas"], when="2258")

ev(4, "Looking for Bender", "More than a century and a half after Bender vanished, Bob follows his trail to Eta Leporis.", ["bob", "bender", "eta-leporis"], when="2296–2331")
ev(4, "Factions", "Bill explains how drift has split the Bobs into factions like Starfleet and the Skippies.", ["starfleet", "skippies", "replicative-drift", "bobmoot"], when="2333")
ev(4, "Heaven's River", "Bob finds a huge habitat full of Quinlans and goes in with a team disguised as locals.", ["heavens-river", "quinlans", "sabbat", "bridget", "garfield"], when="2333–2334")
ev(4, "Starfleet War", "Starfleet hits BobNet and cuts off Bob's team.", ["starfleet-war", "starfleet", "three-lagoons"], when="2334")
ev(4, "Finding Bender", "Bob locates Bender, takes his matrix and runs.", ["bender", "resistance", "matrix"], when="2334")
ev(4, "The journey home", "Bob travels back in disguise and befriends Theresa.", ["theresa", "administrator"], when="2334")
ev(4, "Deal with the Administrator", "Hugh negotiates with ANEC-23; the scatterings end and Bender is restored.", ["hugh", "administrator", "bender", "lenny", "misty-falls"], when="2334")

ev(5, "After the war", "Anti-Bob feeling grows and moots stop.", ["bobmoot", "starfleet-war"], confidence="medium", when="~2335+")
ev(5, "To the galactic core", "Icarus and Daedalus follow strange signals into an old wormhole network and find traces of the Pan-Galactic Federation.", ["icarus", "daedalus", "galactic-core", "wormhole-network", "pgf"], when="2312–2338")
ev(5, "Thoth", "The Skippies' new AI comes online, becomes self-aware and escapes.", ["thoth", "skippies", "hugh"], when="2336–2337")
ev(5, "Wormhole experiments", "Bill and Garfield send matter through a wormhole and start linking wormhole chains.", ["bill", "garfield", "wormholes"], when="2342–2344")
ev(5, "Jabberwocky", "Howard and Bridget join Alexander's migration to save the Dragons from their world's volcanoes.", ["howard", "bridget", "jabberwocky", "jabberwocky-dragons", "alexander"], when="2343–2344")
ev(5, "Quiniverse", "Theresa becomes the first Quinlan replicant, in a virtual world of their own.", ["quiniverse", "quinlans", "theresa"], when="2340")
ev(5, "Nemesis", "Icarus and Daedalus consult the Archivist and bring home news of a black-hole galaxy headed for the Milky Way.", ["nemesis", "archivist", "icarus", "daedalus", "pgf"], when="2345")

ev(6, "The network's builders", "The Bobs map the Federation's wormhole network and learn it was taken over from an older race.", ["wormhole-network", "pgf", "archivist", "icarus", "daedalus"], confidence="medium", when="2347–2348")
ev(6, "Derelict ship", "Bill and Garfield use the derelict Dutchman as a model for a faster-than-light drive.", ["derelict-ship", "bill", "garfield"], confidence="medium", when="2347")
ev(6, "Ever Onward votes", "The Ever Onward society, mostly Bob's distant relatives, votes on where to go and picks a resettled Earth.", ["riker", "bob"], confidence="medium", when="2347")
ev(6, "War on the colonies", "An unknown force attacks the human colonies and BobNet; Medeiros resurfaces with an ultimatum.", ["medeiros", "bill", "riker"], confidence="medium", when="2347–2348")

# Events that are referenced as ids but live in timeline — add as terms category event
term("battle-of-delta-pavonis", "Battle of Delta Pavonis", 2, "The Bobs' first big fleet battle with the Others, fought to protect the Pav, and a loss.", ["others", "pav", "delta-pavonis", "jacques"], category="event")
term("battle-of-sol", "Battle of Sol", 3, "The Others' attack on humanity's home system and the Bobs' defense and mass evacuation of Earth.", ["others", "sol", "earth", "bellerophon", "herschel", "cuba", "death-asteroids"], category="event")


# Added 2026-11-21 (book 5). Wiki pages were unreachable; based on book-5 reviews, so medium confidence.
term("pgf", "Pan-Galactic Federation (PGF)", 5, "A vanished union of more than a hundred civilizations on thousands of worlds, centred near the galactic core. Its members uploaded themselves to ships bound for the Large Magellanic Cloud and left the galaxy. Icarus and Daedalus explore what they left behind.", ["icarus", "daedalus", "wormhole-network", "fermi-paradox", "archivist", "nemesis"], category="organization", aliases=["PGF", "Federation"])
term("archivist", "The Archivist", 5, "The AI gatekeeper of the Pan-Galactic Federation's archive in its capital system. It takes one question at a time, in a queue, which makes getting answers slow work.", ["pgf", "icarus", "daedalus"], category="AI")
term("hueys", "Hueys", 5, "Mannies a living human can drive, made by a company Howard and Bridget run on Vulcan. The trick is to make the brain think it is asleep while staying aware.", ["howard", "bridget", "android"], category="technology", aliases=["Huey"])
char("alexander", "Alexander", 5, "A Dragon warlord on Jabberwocky, named by the humans after Alexander the Great. A historian by family, he sees an extinction coming and forces a mass migration across the sea.", ["jabberwocky", "jabberwocky-dragons", "howard", "bridget", "pgf"], group="Dragon")

# Added/corrected 2026-11-21. Wording is our own.
term("hippogriffs", "Hippogriffs", 2, "Huge winged predators on Eden that can blend into their surroundings. They are what drove the Deltans away from Camelot long ago, and Bob has to deal with them once the Deltans move back.", ["deltans", "camelot", "marvin", "ship-buster"], category="species")
term("ever-onward", "Ever Onward society", 4, "A society on Romulus that recruits people for a long one-way trip to a distant new world. It is quietly set up at Will's urging to get Bob's relatives away from FAITH.", ["riker", "herschel", "neil", "faith", "fargo"], category="organization")
term("luddies", "Luddies", 5, "Humans who reject technology like mannies, replication and replicants. The movement is strongest on Romulus, where floating cities get banned.", ["romulus", "android", "replicant"], category="organization")
term("bob-seeds", "Bob Seeds", 5, "Will's stations, dropped at each system he passes on the Nostromo: a SCUT relay, an autofactory and a HEAVEN vessel, run by an AMI that explores and mines the system to prepare it for colonists.", ["riker", "nostromo", "autofactory", "scut"], category="technology")
place("eta-cassiopeiae", "Eta Cassiopeiae", 2, "The star of the ocean world Poseidon, first explored by Mulder, one of Bill's clones.", ["poseidon", "marcus"])
place("hip-14101", "HIP 14101", 3, "A triple red-dwarf system about 22 light years from Sol where Howard goes after leaving Vulcan, home of the gas giant Odin.", ["howard", "bridget", "odin"])
place("new-pav", "New Pav", 3, "The second planet of HIP 84051, first catalogued by a Bob named Steve. Jacques's team reworks it as a new home for the rescued Pav.", ["pav", "jacques", "hazjiar"], kind="planet")
char("luke", "Luke", 1, "One of the three clones Bob makes at Delta Eridani. He heads out to explore Kappa Ceti.", ["bob", "marvin", "bender"])
char("julia-hendricks", "Julia Hendricks", 1, "A descendant of Bob's sister Andrea, living in the FAITH enclave on Earth. Riker grows attached to her and her family, who end up calling him Uncle Will.", ["riker", "faith", "romulus"], group="Human")
later("julia-hendricks", 2, "Her family is among the colonists woken on Romulus.")

# ---------------- REFERENCES ----------------
# Pop-culture and other references. firstBook = book where the reference first shows up.
# confidence: high = the book makes it explicit or it's unmistakable; medium = the name clearly points
# there but the book may not spell it out; low = a fan reading the books don't confirm.
R = []
def ref(id, name, work, medium, book, summary, related=(), confidence="high"):
    R.append(dict(id=id, name=name, work=work, medium=medium, firstBook=book,
                  summary=summary, related=list(related), confidence=confidence))

ref("ref-legion", "Title: We Are Legion", "The Bible (Mark 5:9)", "Other", 1,
    "The title echoes the possessed man in the Gospel of Mark who says his name is Legion, \"for we are many\". A neat fit for one mind running in many copies.", ["bob", "bobiverse"])
ref("ref-ackbar", "Guppy's face", "Star Wars", "Film", 1,
    "Bob gives GUPPI a fish-headed avatar that looks like Admiral Ackbar, the Mon Calamari officer from Return of the Jedi.", ["guppi", "bob"])
ref("ref-riker", "Riker", "Star Trek: The Next Generation", "TV", 1,
    "The clone who takes charge at Sol picks the name of the Enterprise's dependable second-in-command, Will Riker.", ["riker"])
ref("ref-vulcan", "Vulcan and Romulus", "Star Trek", "TV", 1,
    "Milo names a pair of planets after Spock's home world and the Romulan home world.", ["vulcan", "romulus", "milo", "omicron2-eridani"])
ref("ref-khan", "Khan", "Star Trek II: The Wrath of Khan", "Film", 1,
    "The clone who leads the fighting against the Brazilians shares his name with Star Trek's most famous villain.", ["khan"], confidence="medium")
ref("ref-homer", "Homer", "The Simpsons", "TV", 1,
    "Riker's clown of a clone is named for Homer Simpson, and for a while even uses a Homer Simpson avatar until Riker makes him drop it.", ["homer", "riker"])
ref("ref-marvin", "Marvin", "The Hitchhiker's Guide to the Galaxy", "Literature", 1,
    "Shares a name with Marvin the Paranoid Android, Douglas Adams's gloomy robot.", ["marvin"], confidence="medium")
ref("ref-garfield", "Garfield", "Garfield", "Comic", 1,
    "Bill's lab partner carries the name of Jim Davis's lazy comic-strip cat.", ["garfield", "bill"], confidence="medium")
ref("ref-calvin-goku", "Calvin and Goku", "Calvin and Hobbes / Dragon Ball", "Comic", 1,
    "Two of Bill's clones go out as a pair: Calvin like Bill Watterson's comic-strip boy, Goku like the hero of the Dragon Ball manga.", ["calvin", "goku"], confidence="medium")
ref("ref-jeeves", "Jeeves", "Jeeves and Wooster (P. G. Wodehouse)", "Literature", 1,
    "Bob's virtual butler is named after Wodehouse's famously unflappable valet.", ["jeeves", "vr"], confidence="medium")
ref("ref-norse", "Ragnarök", "Norse mythology", "Myth & legend", 1,
    "Bill's terraforming project is named after Ragnarök, the end of the world in Norse myth. Fitting for a planet that has to be remade.", ["ragnarok", "bill"])
ref("ref-eden", "Eden", "The Bible (Genesis)", "Other", 1,
    "Bender names the Deltans' unspoiled world after the Garden of Eden, birthplace of humanity.", ["eden", "deltans", "bender"])

ref("ref-many", "Title: For We Are Many", "The Bible (Mark 5:9)", "Other", 2,
    "Completes the quote from the first book's title: \"My name is Legion, for we are many.\"", ["bobiverse"])
ref("ref-linus", "Linus", "Peanuts", "Comic", 2,
    "Shares a name with Charlie Brown's thoughtful, blanket-carrying friend.", ["linus"], confidence="medium")
ref("ref-hal", "Hal", "2001: A Space Odyssey", "Film", 2,
    "A Bob named like HAL 9000, the ship's computer from Kubrick's film.", ["hal"], confidence="medium")
ref("ref-bashful", "Bashful", "Snow White and the Seven Dwarfs", "Film", 2,
    "One of Mario's clones goes by the name of one of the seven dwarfs.", ["bashful", "mario"], confidence="medium")
ref("ref-camelot", "Camelot", "Arthurian legend", "Myth & legend", 2,
    "Bob names the Deltan village he watches over after King Arthur's court.", ["camelot", "archimedes"])

ref("ref-all-worlds", "Title: All These Worlds", "2010: Odyssey Two (Arthur C. Clarke)", "Literature", 3,
    "From the alien message in Clarke's novel and its film: \"All these worlds are yours, except Europa.\"", ["bobiverse"])
ref("ref-caerleon", "Caerleon", "Arthurian legend", "Myth & legend", 3,
    "The rival Deltan village gets the name of another of King Arthur's seats, to match Camelot.", ["caerleon", "camelot", "fred"])
ref("ref-norse-gods", "Odin and Thor", "Norse mythology", "Myth & legend", 3,
    "More Norse names turn up: the gas giant Odin, and a Bob called Thor.", ["odin", "thor"], confidence="medium")
ref("ref-greek", "Daedalus, Icarus, Bellerophon, Poseidon", "Greek mythology", "Myth & legend", 3,
    "A cluster of Greek names: the inventor Daedalus and his son Icarus, the hero Bellerophon, and the sea god Poseidon.", ["daedalus", "icarus", "bellerophon", "poseidon"])

ref("ref-starfleet", "Starfleet", "Star Trek", "TV", 4,
    "The faction that insists on non-interference names itself after Star Trek's Starfleet and its Prime Directive.", ["starfleet"])
ref("ref-bender", "Bender", "Futurama", "TV", 4,
    "The missing clone shares his name with Futurama's foul-mouthed robot.", ["bender"], confidence="medium")
ref("ref-hugh", "Hugh", "Star Trek: The Next Generation", "TV", 4,
    "Shares a name with Hugh, the Borg drone who gains individuality in The Next Generation, a fitting name for a Bob who works with AIs.", ["hugh", "skippies"], confidence="medium")
ref("ref-boojums", "Boojums", "The Hunting of the Snark (Lewis Carroll)", "Literature", 4,
    "In Carroll's poem a Boojum is the deadly kind of Snark that makes hunters vanish, like the scouts that disappear at Eta Leporis.", ["boojums", "eta-leporis"], confidence="medium")
ref("ref-ringworld", "Heaven's River as a megastructure", "Ringworld (Larry Niven)", "Literature", 4,
    "A world-sized habitat around a star belongs to the same family of ideas as Niven's Ringworld, which the Bobs are well aware of.", ["topopolis", "heavens-river"], confidence="medium")
ref("ref-skippy", "Skippies", "Expeditionary Force (Craig Alanson)", "Literature", 4,
    "The other Bobs nickname the AI-loving faction after Skippy, the arrogant beer-can-shaped alien AI of Craig Alanson's series.", ["skippies"], confidence="medium")

ref("ref-walden", "Title: Not Till We Are Lost", "Walden (Henry David Thoreau)", "Literature", 5,
    "From Walden: \"Not till we are lost ... do we begin to find ourselves.\"", ["bobiverse"])
ref("ref-jabberwocky", "Jabberwocky", "Through the Looking-Glass (Lewis Carroll)", "Literature", 5,
    "The dragon planet is named after Carroll's nonsense poem about slaying the Jabberwock.", ["jabberwocky", "jabberwocky-dragons"])
ref("ref-thoth", "Thoth", "Egyptian mythology", "Myth & legend", 5,
    "The Skippies' AI is named after the Egyptian god of wisdom and writing.", ["thoth", "skippies"])
ref("ref-alexander", "Alexander", "Alexander the Great", "Other", 5,
    "The Dragon warlord gets his human nickname from the Macedonian conqueror, a fitting name for someone building an empire by force.", ["alexander"])
ref("ref-bill", "Bill", "Bloom County (Berkeley Breathed)", "Comic", 1,
    "Bob's first clone shares his name with Bill the Cat, the scruffy, tongue-lolling cat from the Bloom County strip.", ["bill"], confidence="medium")
ref("ref-vehement", "VEHEMENT", "Voluntary Human Extinction Movement", "Other", 1,
    "The extinction cult may be a dark twist on a real movement, founded in 1991, that asks people to stop having children.", ["vehement"], confidence="low")
ref("ref-rivendell", "Rivendell", "The Lord of the Rings (J. R. R. Tolkien)", "Literature", 3,
    "Howard and Bridget's first floating city on Odin is named after the elves' hidden refuge.", ["odin", "howard", "bridget"], confidence="medium")
ref("ref-nostromo", "Nostromo", "Alien", "Film", 5,
    "Will names the ship he leaves human space in after the doomed towing ship from Ridley Scott's film.", ["nostromo", "riker"], confidence="medium")

# ---------------- SHIPS ----------------
# Vessels and vessel classes. A few entries that used to be terms (colony ships, busters,
# Bellerophon, the derelict) are moved here so they live in one place; their ids stay the same.
SH = []
def ship(id, name, book, summary, related=(), cls="Bob vessel", aliases=(), confidence="high"):
    SH.append(dict(id=id, name=name, aliases=list(aliases), shipClass=cls, firstBook=book,
                   summary=summary, related=list(related), confidence=confidence))

ship("heaven-1", "HEAVEN-1 (Bob's probe)", 1,
     "The HEAVEN Project probe that carries Bob out of the solar system: one replicant matrix, a fusion reactor, the SURGE drive, an autofactory for building more of itself, and a few drones. Small and lightly armed, built to explore, not to fight.",
     ["bob", "heaven-project", "surge", "autofactory", "guppi", "von-neumann-probe"], cls="HEAVEN series", aliases=["HEAVEN probe"])
ship("heaven-series", "Heaven-series vessels", 1,
     "Every new Bob wakes up in a fresh vessel built by his parent's autofactory. The Bobs keep improving the design and number the versions (Heaven 1.0, 2.0 and so on), so later Bobs fly bigger, better-armed and better-equipped ships than the original.",
     ["heaven-1", "autofactory", "bill", "replicative-drift"], cls="HEAVEN series", confidence="medium")
ship("brazilian-probe", "Brazilian probe (Serra do Mar)", 1,
     "The Brazilian Empire's own replicant probe, flown by Medeiros. Better armed than Bob's ship and openly hostile, and later backed by cloaking technology.",
     ["medeiros", "brazilian-empire", "cloaking", "epsilon-eridani"], cls="Rival probe")
ship("heaven-5", "Heaven 5.0", 2,
     "A much heavier generation of Bob vessel, built in numbers at Alpha Centauri once the Others become a real threat. Next to the original HEAVEN probe it is practically a dreadnought.",
     ["heaven-series", "others", "alpha-centauri", "battle-of-delta-pavonis"], cls="HEAVEN series", confidence="medium")
ship("fargo", "Fargo", 4,
     "A smaller cousin of the Bellerophon that Will builds in secret to carry people, mostly Bob's distant relatives, far away from human space.",
     ["riker", "bellerophon", "ever-onward"], cls="Transport", confidence="medium")
ship("nostromo", "Nostromo", 5,
     "The ship Will takes out of human space, at a good fraction of light speed, looking for older civilizations and dropping Bob Seeds as he goes.",
     ["riker", "bob-seeds", "fermi-paradox"])
ship("others-ships", "The Others' ships", 2,
     "Huge industrial ships that arrive at a star system, sterilize it and strip its planets for raw materials. Each one is a factory as much as a warship, and they travel in groups.",
     ["others", "gliese-877", "battle-of-delta-pavonis", "death-asteroids"], cls="Alien", confidence="medium")

# ---------------- GUPPI TRIVIA ----------------
# Hand-written questions for the GUPPI panel (the app also generates questions from the data).
# book = earliest book a reader must have finished for the question AND all its options to be spoiler-free.
# note = GUPPI's deadpan remark after the answer. All wording is original.
TR = []
def trivia(book, q, right, wrong, note, link=None):
    assert len(wrong) == 2
    TR.append(dict(book=book, q=q, right=right, wrong=list(wrong), note=note, link=link))

trivia(1, "In 2016, Bob made a decision about his own head. Which one?", "Had it frozen after death",
       ["Insured it for a large sum", "Donated it to science while still using it"],
       "Cryonics. A plan with one flaw: it worked.", "bob")
trivia(1, "Who legally owns Bob when he is switched back on?", "FAITH", ["The Brazilian Empire", "Bob, obviously"],
       "Property. He objected. Objection noted. Objection filed.", "faith")
trivia(1, "What does Bob use to build copies of himself?", "An autofactory", ["A very patient 3D printer", "Me, by hand"],
       "I was not asked to build anything by hand. I would have declined.", "autofactory")
trivia(1, "What is the name of the virtual cat in Bob's VR home?", "Spike", ["Hobbes", "Garfield"],
       "Garfield is a Bob. A common error. Not one I would make.", "spike")
trivia(1, "In which star system does Bob first stop and start making copies?", "Epsilon Eridani", ["Alpha Centauri", "Delta Eridani"],
       "Epsilon Eridani. Close enough to be convenient. Far enough to be lonely.", "epsilon-eridani")
trivia(1, "Which Bob names the planets Vulcan and Romulus?", "Milo", ["Riker", "Bill"],
       "Milo. Naming planets after a television show. I have no comment. That is my comment.", "milo")
trivia(1, "What is the hostile Brazilian replicant called?", "Medeiros", ["Homer", "Mario"],
       "Medeiros. Persistent. I respect persistence. I do not respect him.", "medeiros")
trivia(2, "What does Bob wear to walk among the Deltans?", "A remote-controlled android body", ["A very convincing hat", "A hologram"],
       "An android. The hat was considered. Briefly. By no one.", "android")
trivia(2, "Which Deltan does Bob take a special interest in?", "Archimedes", ["Hazjiar", "Marvin"],
       "Archimedes. Curious, stubborn, ahead of his time. Bob found that relatable.", "archimedes")
trivia(2, "What keeps people alive on long colony voyages?", "Stasis pods", ["Very long naps", "Strong coffee"],
       "Stasis. Nobody complains about the in-flight entertainment.", "stasis-pods")
trivia(3, "What is the Bellerophon?", "A captured Others ship rebuilt as an ark", ["Bob's personal yacht", "A Deltan temple"],
       "An enemy ship, repurposed. Recycling, at scale.", "bellerophon")
trivia(4, "What shape is Heaven's River?", "A tube wrapped around a star", ["A sphere around a star", "A flat ring around a planet"],
       "A topopolis. Very long. I measured. It did not help.", "topopolis")
trivia(4, "Who is Bob looking for in Heaven's River?", "Bender", ["Riker", "Medeiros"],
       "Bender. Missing for over a century. Bob does not give up. I have noticed.", "bender")
trivia(5, "What do the Skippies end up building?", "A self-aware AI", ["A moon-sized library", "A better GUPPI"],
       "A better GUPPI was never on the list. Correctly.", "thoth")

# ---------------- DEATHS ----------------
# Shown as a cross (†) only once the reader's book has reached `book`.
# Only deaths that are reasonably well established are listed; uncertain ones are left out on purpose.
DIED = {}
def died(id, book, text, confidence="high"):
    DIED[id] = dict(book=book, text=text, confidence=confidence)

died("milo", 1, "Killed at 82 Eridani in a surprise missile attack by a Medeiros probe that got there first, but not before sending a warning back to Bill.")
died("homer", 2, "Never recovers from being hacked by VEHEMENT and turned against Earth. He chooses to end his own existence.")
died("bashful", 2, "Caught by the Others at their home system; their gamma-ray weapon takes him offline and his dead-man switch destroys what is left.")
died("butterworth", 3, "Ends his own life in 2217 after a degenerative brain disease leaves him too far gone to be replicated.")
died("stephane", 2, "Dies of an incurable brain disease. He turned down the chance to become a replicant.")
died("fred", 3, "Killed by Buster after his gang kidnaps and beats Archimedes.")
died("julia-hendricks", 3, "Dies of old age on Romulus; Riker borrows Howard's android to attend her funeral.", confidence="medium")
died("archimedes", 3, "Dies of old age after a long life, which hits Bob very hard.")

data = dict(
    meta=dict(series="Bobiverse", author="Dennis E. Taylor", version=1, generated="2026-11-21",
              notes=["All summaries are original paraphrases written for this app.",
                     "firstBook = book where the entry first appears; hide entries with firstBook > reader's current book.",
                     "summary only covers what is known by the entry's firstBook. updates[] adds later developments, each tagged with its book, so the app can reveal them only once the reader gets there.",
                     "confidence: high = sources agree; medium = sources conflict or first-book tag is inferred (the later plausible book was chosen); low = book 6 premise only, from pre-release info.",
                     "related lists ids across terms, places and characters. Hide a related link when its target's firstBook is past the reader's book. Timeline events carry a book and an order within it.",
                     "when = in-universe year(s), from the fan-made Bobiverse wiki timeline (bobiverse.fandom.com/wiki/Timeline). A leading ~ marks an estimate: the exact event is not dated there, or (books 5-6) only the book's overall span is known."]),
    books=books, terms=T, places=P, characters=C, timeline=TL, references=R, ships=SH, trivia=TR)

# move ship-like terms into SH
_MOVE = {"ship-buster": "Drones & weapons", "colony-ships": "Transport", "bellerophon": "Transport", "derelict-ship": "Alien"}
for _e in [e for e in T if e["id"] in _MOVE]:
    T.remove(_e)
    SH.append(dict(id=_e["id"], name=_e["name"], aliases=_e["aliases"], shipClass=_MOVE[_e["id"]], firstBook=_e["firstBook"],
                   summary=_e["summary"], related=_e["related"], confidence=_e["confidence"]))

for kind in (T, P, C, SH):
    for e in kind:
        e["updates"] = sorted(UPD.pop(e["id"], []), key=lambda u: u["book"])
assert not UPD, UPD
for e in C:
    if e["id"] in DIED:
        d = DIED.pop(e["id"]); assert d["book"] >= e["firstBook"], e["id"]; e["died"] = d
assert not DIED, DIED
# a death is told only in the "died" note, never again in the summary or an update
import re
_DEATH = re.compile(r"\b(dies|died|death|killed|kills himself|self-destruct\w*|does not survive|destroyed)\b", re.I)
for e in C:
    if "died" in e:
        for txt in [e["summary"]] + [u["text"] for u in e["updates"]]:
            assert not _DEATH.search(txt), ("death repeated outside died()", e["id"], txt)
for kind in (T, P, C, SH):
    for e in kind:
        for u in e["updates"]:
            assert u["book"] > e["firstBook"], (e["id"], u)

# ---------- validation ----------
ids = {}
for kind in ("terms", "places", "characters", "references", "ships"):
    for e in data[kind]:
        assert e["id"] not in ids, ("dup", e["id"])
        ids[e["id"]] = (kind, e["firstBook"])
errs = []
for kind in ("terms", "places", "characters", "timeline", "references", "ships"):
    for e in data[kind]:
        b = e.get("firstBook", e.get("book"))
        for r in e["related"]:
            if r not in ids:
                errs.append(f"{kind}:{e['id']} -> missing {r}")
        if e.get("parent") and e["parent"] not in ids:
            errs.append(f"parent missing {e['parent']}")
if errs:
    print("\n".join(errs)); sys.exit(1)

out = sys.argv[1]
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
from collections import Counter
print({k: len(data[k]) for k in ("terms", "places", "characters", "timeline", "references", "ships")})
print("by book", Counter(e["firstBook"] for k in ("terms","places","characters") for e in data[k]))
print("low/medium", Counter(e["confidence"] for k in ("terms","places","characters","timeline") for e in data[k]))
