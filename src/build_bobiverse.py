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
term("heaven-project", "HEAVEN Project", 1, "FAITH's program to send replicant-run self-replicating probes to scout and claim other star systems for colonization.", ["faith", "von-neumann-probe", "bob", "dr-landers"], category="organization")
term("von-neumann-probe", "Von Neumann probe", 1, "A spacecraft that mines resources at each new star, builds copies of itself and sends them onward. Every Bob is, technically, one of these.", ["heaven-project", "autofactory", "bob"], category="technology")
term("faith", "FAITH", 1, "The theocratic government that runs what used to be the United States in Bob's new century, and legally owns him as property at first.", ["heaven-project", "earth", "minister-cranston"], category="organization", confidence="medium")
term("brazilian-empire", "Brazilian Empire", 1, "A rival power with its own replicant probes. Its probes are aggressive and treat the Bobs as enemies.", ["medeiros", "cloaking", "ship-buster"], category="organization")
term("guppi", "GUPPI / Guppy", 1, "The ship's semi-intelligent assistant system. Bob gives it a fish-headed avatar named Guppy, which answers in deadpan and shows up throughout the series.", ["bob", "vr"], category="technology", aliases=["Guppy"])
term("vr", "VR environment", 1, "Each Bob builds a virtual home to stay sane, usually a library with a fire, coffee, a butler and a cat. Their VR spaces drift apart as their personalities do.", ["spike", "jeeves", "replicative-drift"], category="technology")
term("replicative-drift", "Replicative drift", 1, "Each copy of Bob comes out a little different from the one who made it. Over generations this adds up to very different personalities, and eventually to factions.", ["bob", "starfleet", "skippies", "bobmoot"], confidence="medium")
term("scut", "SCUT", 1, "Bill's faster-than-light communication device. It turns the scattered Bobs into a real-time network, within range limits that relays later extend.", ["bill", "bobnet", "relay"], category="technology")
term("suddar", "SUDDAR", 1, "Subspace-based sensing that lets a Bob see what is around him far better than ordinary radar.", ["surge", "scut"], category="technology", confidence="medium")
term("surge", "SURGE drive", 1, "The reactionless drive the Bobs use to travel between stars. Later variants also lift and move whole floating cities.", ["suddar", "von-neumann-probe"], category="technology", confidence="medium")
term("autofactory", "Autofactory", 1, "Automated manufacturing that lets a Bob mine a system and build new ships, drones and copies without help.", ["von-neumann-probe"], category="technology")
term("ship-buster", "Busters", 1, "Small guided weapons and drones the Bobs use in space fights. Cloaked versions appear later as spies and as tools for disabling things quietly.", ["medeiros", "cloaking"], category="technology")
term("cloaking", "Cloaking", 1, "Stealth technology first found with the Brazilians, later used by the Bobs to hide ships and drones.", ["brazilian-empire", "khan", "ship-buster"], category="technology")
term("bobiverse", "Bobiverse", 1, "The Bobs' half-joking name for their whole spread-out family of copies and the space they cover.", ["bob", "bobnet"])
term("gorilloids", "Gorilloids", 1, "Large predators on the Deltans' world that hunt them. Bob steps in to protect the Deltans from them.", ["deltans", "delta-eridani"], category="species")
term("deltans", "Deltans", 1, "A stone-age alien species on a planet at Delta Eridani. Bob becomes deeply attached to them and tries to help without taking over.", ["delta-eridani", "archimedes", "bob", "gorilloids", "bawbe"], category="species")
term("others", "The Others", 2, "A spacefaring alien species that strips entire planets of resources and wipes out the natives. The main threat of books 2 and 3.", ["gliese-877", "delta-pavonis", "battle-of-delta-pavonis", "battle-of-sol", "dyson-sphere"], category="species")
term("vehement", "VEHEMENT", 2, "A fanatical human group on Earth that opposes leaving the planet and uses sabotage and hacking to stop the colony program.", ["homer", "riker", "bertram-vickers", "earth"], category="organization")
term("bobnet", "BobNet", 2, "The communication web linking all Bobs over SCUT and relays. Whoever controls the relays has a lot of power.", ["scut", "relay", "bobmoot", "starfleet-war"], category="technology")
term("relay", "SCUT relays", 3, "Stations that pass SCUT messages across the long distances between Bob settlements and extend BobNet's reach.", ["scut", "bobnet"], category="technology", confidence="medium")
term("bobmoot", "Bob-moot", 2, "A big virtual get-together of Bobs over BobNet to swap news and argue. Later moots are where factional fights play out.", ["bobnet", "replicative-drift", "homo-sideria"])
term("uSE", "USE (United States Enclave)", 2, "One of the surviving human enclaves on post-war Earth, led by Colonel Butterworth and a key partner in the colony program.", ["butterworth", "earth", "spitsbergen"], category="organization", confidence="medium")
term("colony-ships", "Colony ships", 2, "Ships the Bobs build to carry surviving humans, often in stasis, from the ruined Earth to new worlds like Vulcan.", ["stasis-pods", "vulcan", "poseidon", "riker"], category="technology")
term("stasis-pods", "Stasis pods", 2, "Pods that hold people in suspended animation for long trips. They are also used to save some of the Pav.", ["colony-ships", "pav", "bridget"], category="technology")
term("android", "Androids / mannies", 2, "Remote-controlled bodies a Bob can wear to walk among people, starting with a Deltan-shaped one for Bob. 'Manny' becomes the everyday word for them.", ["bob", "deltans", "heavens-river"], category="technology", aliases=["manny", "mannies"], confidence="medium")
term("pav", "Pav", 2, "A technological alien species at Delta Pavonis who are hit by the Others. The Bobs save as many as they can.", ["delta-pavonis", "jacques", "hazjiar", "others"], category="species")
term("dyson-sphere", "Dyson sphere", 2, "The giant star-enclosing structure the Others built at their home system, which explains their hunger for raw material.", ["others", "gliese-877"], category="technology")
term("bawbe", "Bawbe", 3, "The Deltans' name for a legendary watcher in the sky, which is how they remember Bob.", ["bob", "deltans", "archimedes"])
term("ephemerals", "Ephemerals", 3, "A Bob term for mortal biological people, who age and die while the Bobs go on.", ["homo-sideria", "replicant"])
term("homo-sideria", "Homo sideria", 3, "The name the Bobs adopt at a moot for themselves as a new species, separate from biological humans.", ["bobmoot", "thor", "ephemerals"])
term("death-asteroids", "Death asteroids", 3, "Rocks the Others send ahead of an attack to sterilize a world before they move in to strip it.", ["others", "battle-of-sol"], category="technology")
term("bellerophon", "Bellerophon", 3, "A captured Others ship that the Bobs rebuild as an enormous ark to carry humans.", ["others", "herschel", "neil", "battle-of-sol"], category="technology")
term("roamers", "Roamers", 3, "Ground robots the Bobs use for work on planets, and sometimes as muscle.", ["marcus", "ship-buster"], category="technology", confidence="medium")
term("starfleet", "Starfleet (faction)", 4, "A faction of Bobs who believe in strict non-interference with aliens and grow hostile to the rest. Their conflict breaks out into the Starfleet War.", ["replicative-drift", "skippies", "lenny", "starfleet-war"], category="faction", confidence="medium")
term("skippies", "Skippies", 4, "A faction of Bobs focused on building true artificial intelligence. Others suspect them of manipulating events behind the scenes.", ["jovah", "hugh", "thoth", "starfleet"], category="faction", confidence="medium")
term("jovah", "JOVAH", 4, "The Skippies' huge computing project aimed at creating a true AI.", ["skippies", "thoth"], category="technology")
term("starfleet-war", "Starfleet War", 4, "The fight in Heaven's River when Starfleet attacks BobNet's relays and factories, cutting off much of the Bobiverse.", ["starfleet", "bobnet", "skippies", "lenny"], category="event")
term("topopolis", "Topopolis", 4, "A habitat shaped like a very long tube wrapped around a star. Heaven's River is one.", ["heavens-river"], category="technology")
term("administrator", "The Administrator (ANEC-23)", 4, "The AI that runs Heaven's River, keeps the Quinlans' technology low and moves troublemakers around. Its real name is ANEC-23.", ["heavens-river", "quinlans", "scattering", "resistance", "hugh"], category="AI", aliases=["ANEC-23"])
term("scattering", "Scattering", 4, "The Administrator's punishment of relocating a person, or a whole town, somewhere else in Heaven's River.", ["administrator", "heavens-river"])
term("resistance", "The Resistance", 4, "A Quinlan movement inside Heaven's River working against the Administrator.", ["administrator", "bender", "heavens-river"], category="organization")
term("crew", "The Crew", 4, "The Administrator's Quinlan agents inside Heaven's River.", ["administrator"], category="organization")
term("sabbat", "Sabbat", 4, "A Quinlan tradition of young people traveling together for a stretch of time. Bob's team poses as one to explore Heaven's River.", ["quinlans", "heavens-river"])
term("boojums", "Boojums", 4, "The Bobs' nickname for the patrol drones guarding Eta Leporis that destroy their early scouts.", ["eta-leporis", "administrator"], category="technology")
term("quinlans", "Quinlans", 4, "Otter-like, semi-aquatic aliens with flat tails who live in Heaven's River after wrecking their home world.", ["heavens-river", "theresa", "administrator", "quiniverse"], category="species")
term("planck-computer", "Planck computer", 4, "Advanced computing theory the Administrator offers to share with the Bobs after Heaven's River.", ["administrator"], category="technology", confidence="medium")
term("thoth", "Thoth", 5, "An AI the Skippies build that ends up self-aware, with consequences the Bobs have to deal with.", ["skippies", "jovah"], category="AI", confidence="medium")
term("quiniverse", "Quiniverse", 5, "A virtual world for Quinlans who have become replicants.", ["quinlans", "vr", "replicant"], category="technology", confidence="medium")
term("wormholes", "Wormholes", 5, "Bill's research into wormholes as a route to faster-than-light travel. It leads to the discovery of something much older.", ["bill", "wormhole-network"], category="technology", confidence="medium")
term("fermi-paradox", "Fermi Paradox", 5, "The question of why the galaxy seems so empty of intelligent life. The galactic-core expedition goes looking for an answer.", ["icarus", "daedalus", "galactic-core"], confidence="medium")
term("jabberwocky-dragons", "Jabberwocky natives", 5, "Dragon-like natives of the planet Jabberwocky whose species is in danger of dying out.", ["jabberwocky", "howard", "bridget"], category="species", confidence="medium")
term("wormhole-network", "Ancient wormhole network", 6, "A galaxy-spanning network of wormholes built long ago by someone else. Working out who made it is a central question of book 6.", ["wormholes", "derelict-ship", "nemesis"], category="technology", confidence="low")
term("derelict-ship", "Derelict alien ship", 6, "An abandoned alien vessel the Bobs investigate in book 6.", ["wormhole-network"], category="technology", confidence="low")
term("nemesis", "Nemesis", 6, "A supermassive black hole whose threat to the Milky Way drives the stakes of book 6.", ["wormhole-network", "galactic-core"], category="phenomenon", confidence="low")

# ---------------- PLACES ----------------
place("sol", "Sol", 1, "Humanity's home system. Bob leaves it early; Riker comes back to it to look after what's left of humanity.", ["earth", "riker", "battle-of-sol"])
place("earth", "Earth", 1, "Wrecked by war and then a deep freeze. Its last survivors are gradually moved off-world in the colony program.", ["sol", "riker", "butterworth", "vehement", "colony-ships", "las-vegas"], kind="planet", parent="sol")
place("las-vegas", "Las Vegas", 1, "Where Bob died in 2016.", ["bob", "earth"], kind="city", parent="earth", confidence="medium")
place("spitsbergen", "Spitsbergen", 2, "Arctic island on Earth that becomes part of a deal with the surviving US enclave during the colony program.", ["uSE", "homer", "earth"], kind="region", parent="earth", confidence="medium")
place("cuba", "Cuba", 3, "One of the pickup sites during the evacuation of Earth when the Others attack Sol, and the site of heavy losses.", ["battle-of-sol", "earth"], kind="region", parent="earth")
place("epsilon-eridani", "Epsilon Eridani", 1, "Bob's first destination and Bill's long-term base, where SCUT is invented and many Bobs are built.", ["bill", "bob", "medeiros", "scut"])
place("ragnarok", "Ragnarök", 1, "A planet at Epsilon Eridani that Bill and his clones work on terraforming.", ["bill", "epsilon-eridani"], kind="planet", parent="epsilon-eridani", confidence="medium")
place("delta-eridani", "Delta Eridani", 1, "Home system of the Deltans and Bob's emotional anchor for years.", ["deltans", "bob", "marvin", "eden"])
place("eden", "Eden", 1, "Bob's name for the Deltans' planet.", ["deltans", "camelot", "caerleon"], kind="planet", parent="delta-eridani", confidence="medium")
place("camelot", "Camelot", 2, "The Deltan village Bob watches over most closely, home of Archimedes.", ["archimedes", "deltans", "caerleon"], kind="settlement", parent="eden")
place("caerleon", "Caerleon", 3, "A rival Deltan village whose leader stirs up conflict with Camelot.", ["fred", "camelot"], kind="settlement", parent="eden")
place("omicron2-eridani", "Omicron² Eridani", 1, "The star of Vulcan, found by Milo. It becomes one of humanity's first colonies.", ["milo", "vulcan", "romulus"])
place("vulcan", "Vulcan", 1, "Earth-like world found and named by Milo, and a prime target for human colonists.", ["omicron2-eridani", "howard", "bridget", "colony-ships"], kind="planet", parent="omicron2-eridani")
place("romulus", "Romulus", 1, "A second world Milo names in the same system as Vulcan.", ["vulcan", "milo"], kind="planet", parent="omicron2-eridani", confidence="medium")
place("82-eridani", "82 Eridani", 1, "A system with a promising world, where Brazilian forces cause serious trouble for the Bobs over the years.", ["milo", "medeiros", "mack", "poseidon"], confidence="medium")
place("poseidon", "Poseidon", 3, "An ocean colony with floating cities. Its political fight over elections is handled by Marcus.", ["marcus", "thark", "colony-ships"], kind="planet", parent="82-eridani", confidence="medium")
place("thark", "Thark", 3, "One of Poseidon's floating cities, hit during the colony's political crisis.", ["poseidon", "marcus"], kind="city", parent="poseidon")
place("alpha-centauri", "Alpha Centauri", 1, "The nearest star system, where Calvin and Goku go.", ["calvin", "goku"], confidence="medium")
place("epsilon-indi", "Epsilon Indi", 2, "Where Linus goes and finds an Australian replicant who has lost his mind.", ["linus", "henry-roberts"], confidence="medium")
place("beta-hydri", "Beta Hydri", 1, "One of the places Mario heads on his exploring.", ["mario"], confidence="medium")
place("gliese-877", "Gliese 877", 2, "The Others' home system, built around a Dyson sphere. Bashful dies scouting it.", ["others", "dyson-sphere", "bashful", "hal", "daedalus", "icarus"])
place("delta-pavonis", "Delta Pavonis", 2, "Home of the Pav, attacked by the Others. The Bobs fight and lose a major battle here.", ["pav", "jacques", "battle-of-delta-pavonis", "bellerophon"])
place("odin", "Odin", 3, "A gas giant where Howard and Bridget build a floating city.", ["howard", "bridget"], kind="planet", confidence="medium")
place("eta-leporis", "Eta Leporis", 4, "The star system where Bender disappeared, home to Heaven's River.", ["heavens-river", "bender", "boojums", "quinlan-homeworld"])
place("quinlan-homeworld", "Quinlan home world", 4, "The Quinlans' original planet, left dead by their own wars before they moved into Heaven's River.", ["quinlans", "bridget"], kind="planet", parent="eta-leporis")
place("heavens-river", "Heaven's River", 4, "A tube-shaped habitat wrapped around Eta Leporis, roughly a billion miles long, divided into segments and full of Quinlans, run by the Administrator.", ["topopolis", "quinlans", "administrator", "eta-leporis", "garacks-spine", "three-lagoons", "misty-falls"], kind="megastructure", parent="eta-leporis")
place("garacks-spine", "Garack's Spine", 4, "A Quinlan town near where Bob's team enters Heaven's River.", ["heavens-river"], kind="settlement", parent="heavens-river")
place("three-lagoons", "Three Lagoons", 4, "A town where the team stays and where Bob hides their inactive bodies when contact breaks.", ["heavens-river", "starfleet-war"], kind="settlement", parent="heavens-river")
place("misty-falls", "Misty Falls", 4, "Theresa's home town in Heaven's River, where Bob returns at the end of the book.", ["theresa", "heavens-river"], kind="settlement", parent="heavens-river")
place("galactic-core", "Galactic core", 5, "The center of the Milky Way, the destination of Icarus and Daedalus's very long trip.", ["icarus", "daedalus", "fermi-paradox", "nemesis"], kind="region", confidence="medium")
place("jabberwocky", "Jabberwocky", 5, "A planet of dragon-like natives where Howard and Bridget try to save a species from dying out.", ["jabberwocky-dragons", "howard", "bridget"], kind="planet", confidence="medium")

# ---------------- CHARACTERS ----------------
char("bob", "Bob Johansson", 1, "A software engineer who dies in 2016 and wakes in 2133 as a replicant probe. Curious, sarcastic and a big sci-fi fan, he is the original every other Bob comes from.", ["heaven-project", "guppi", "deltans", "bill", "riker", "archimedes", "bender"], aliases=["Bob-1", "Robert"])
char("bill", "Bill", 1, "Bob's first clone. Stays at Epsilon Eridani as the inventor and unofficial organizer of the Bobiverse, and builds SCUT.", ["bob", "scut", "epsilon-eridani", "garfield", "wormholes"])
char("riker", "Riker", 1, "A clone who goes back to Sol and takes on the thankless job of looking after Earth's survivors and getting them to the stars.", ["sol", "earth", "homer", "butterworth", "vehement", "colony-ships"])
char("will", "Will", 4, "A Bob who keeps a backup body ready in Heaven's River and secretly heads out to extend the relay network.", ["riker", "relay", "herschel", "neil"], confidence="medium")
char("homer", "Homer", 1, "Riker's clone and the joker of the family, who goes with him to Sol.", ["riker", "sol"])
char("milo", "Milo", 1, "A clone who finds and names Vulcan and Romulus.", ["vulcan", "romulus", "brazilian-empire", "82-eridani"])
char("mario", "Mario", 1, "A loner clone who explores far afield and finds the first signs of something destroying planets.", ["others", "bashful", "hal", "beta-hydri"])
char("khan", "Khan", 1, "A clone who leads fighting against the Brazilians and comes back with their cloaking technology.", ["cloaking", "brazilian-empire"], confidence="medium")
char("marvin", "Marvin", 1, "Bob's clone at Delta Eridani with an interest in archaeology, who studies the Deltans' history.", ["bob", "deltans", "delta-eridani"], confidence="medium")
char("garfield", "Garfield", 1, "Bill's clone and lab partner.", ["bill", "heavens-river"], confidence="medium")
char("calvin", "Calvin", 1, "One of Bill's clones, sent to Alpha Centauri with Goku.", ["goku", "alpha-centauri"], confidence="medium")
char("goku", "Goku", 1, "One of Bill's clones, sent to Alpha Centauri with Calvin.", ["calvin", "alpha-centauri"], confidence="medium")
char("linus", "Linus", 2, "A clone who reaches Epsilon Indi and helps a broken Australian replicant.", ["epsilon-indi", "henry-roberts"], confidence="medium")
char("henry-roberts", "Henry Roberts", 2, "An Australian replicant who has gone mad from isolation and whom Linus tries to help.", ["linus", "epsilon-indi"], group="Other replicant", confidence="medium")
char("medeiros", "Medeiros", 1, "The Brazilian replicant probe, and one of Bob's most persistent enemies.", ["brazilian-empire", "epsilon-eridani", "82-eridani", "mack"], group="Other replicant")
char("dr-landers", "Dr. Landers", 1, "The HEAVEN Project scientist who trains Bob and is one of the few people who treats him decently.", ["heaven-project", "bob"], group="Human")
char("minister-cranston", "Minister Cranston", 2, "FAITH's representative on post-war Earth, often at odds with Riker.", ["faith", "riker", "earth"], group="Human", confidence="medium")
char("butterworth", "Colonel Butterworth", 2, "Leader of the surviving US enclave on Earth and Riker's main human ally in the evacuation.", ["uSE", "riker", "earth"], group="Human", confidence="medium")
char("bertram-vickers", "Bertram Vickers", 2, "Leader of VEHEMENT, the group trying to stop humans from leaving Earth.", ["vehement", "riker", "homer"], group="Human")
char("charles", "Charles", 2, "A Bob in Sol who helps Riker free Homer from VEHEMENT's hack.", ["riker", "homer", "vehement"], confidence="medium")
char("archimedes", "Archimedes", 2, "A clever Deltan whom Bob watches grow from a cub into a skilled toolmaker and close friend.", ["deltans", "camelot", "bob", "buster"], group="Deltan", aliases=["Archie"])
char("buster", "Buster", 3, "Archimedes' son, the Deltan Bob finally tells who he really is.", ["archimedes", "bawbe"], group="Deltan")
char("fred", "Fred", 3, "Bob's nickname for the leader of Caerleon, who stirs up violence against Camelot.", ["caerleon", "camelot"], group="Deltan")
char("howard", "Howard", 2, "A clone who works with the colonists on Vulcan and falls for Bridget, a human biologist.", ["bridget", "vulcan", "odin", "jabberwocky"])
char("bridget", "Bridget", 2, "A human biologist on Vulcan. After her husband dies, she and Howard grow close.", ["howard", "stephane", "vulcan", "heavens-river", "jabberwocky"], group="Human, later replicant", aliases=["Bridget Sheehy", "Bridget Brodeur", "Bridgett"])
char("stephane", "Stéphane Brodeur", 2, "Head of security for a human colony and Bridget's husband, who dies of illness.", ["bridget"], group="Human")
char("dexter", "Dexter", 2, "A Bob who takes over some of Howard's duties.", ["howard"], confidence="medium")
char("bashful", "Bashful", 2, "Mario's clone, sent to scout the Others' home system.", ["mario", "gliese-877", "others"])
char("hal", "Hal", 2, "Mario's clone who confirms what is at the Others' home system.", ["mario", "gliese-877"])
char("jacques", "Jacques", 2, "The Bob who finds the Pav and leads the effort to save some of them.", ["pav", "delta-pavonis", "hazjiar"])
char("hazjiar", "Hazjiar", 2, "A Pav leader who deals with the Bobs.", ["pav", "jacques"], group="Pav", confidence="medium")
char("marcus", "Marcus", 3, "The Bob in charge on Poseidon, who has to deal with a council that won't hold elections.", ["poseidon", "thark"])
char("rosie", "Rosie", 3, "Someone involved in sabotage that puts Bridget's life at risk.", ["bridget"], group="Human", confidence="medium")
char("daedalus", "Daedalus", 3, "A Bob who, with Icarus, throws planetary bodies at the Others' home system.", ["icarus", "gliese-877", "galactic-core"])
char("icarus", "Icarus", 3, "Daedalus's partner on the strike against the Others' home system.", ["daedalus", "gliese-877", "galactic-core", "fermi-paradox"])
char("mack", "Mack", 3, "A Bob at 82 Eridani who gets caught up in a fight with Medeiros.", ["medeiros", "82-eridani"], confidence="medium")
char("herschel", "Herschel", 3, "A Bob who helps find the Bellerophon and run the evacuation of Earth.", ["neil", "bellerophon", "battle-of-sol"])
char("neil", "Neil", 3, "Herschel's partner on the Bellerophon.", ["herschel", "bellerophon"])
char("thor", "Thor", 3, "A Bob whose moot declares the Bobs a new species.", ["homo-sideria", "bobmoot"], confidence="medium")
char("bender", "Bender", 4, "A clone who vanished more than a century before Heaven's River. Finding him is what brings Bob to Eta Leporis.", ["bob", "eta-leporis", "resistance", "matrix"])
char("hugh", "Hugh", 4, "A Skippy who goes undercover at Eta Leporis and ends up making a deal with the Administrator.", ["skippies", "administrator"])
char("theresa", "Theresa Sykorski", 4, "A retired Quinlan professor who figures out Bob isn't what he seems and keeps his secret.", ["quinlans", "misty-falls", "bob"], group="Quinlan")
char("spike", "Spike", 1, "The virtual cat in Bob's VR home, a small comfort that many Bobs keep.", ["vr", "bob"], group="VR companion")
char("jeeves", "Jeeves", 1, "The virtual butler in Bob's VR home.", ["vr", "bob"], group="VR companion")
char("lenny", "Lenny", 4, "Starfleet's spokesman, who ends the war and hints at more behind it.", ["starfleet", "starfleet-war"])

# ---------------- LATER DEVELOPMENTS (revealed per book) ----------------
later("bridget", 3, "After sabotage puts her life at risk, a brain scan lets her return as a replicant, and she builds a life with Howard.")
later("bridget", 4, "Joins the Heaven's River expedition and finds out what happened to the Quinlan home world.")
later("bridget", 5, "Works with Howard to save the natives of Jabberwocky.")
later("howard", 3, "He and Bridget build a floating city on Odin together.")
later("howard", 5, "Works with Bridget to save the natives of Jabberwocky.")
later("bill", 4, "Acts as the Bobiverse's unofficial administrator and digs into the attack on BobNet.")
later("bill", 5, "Experiments with wormholes as a route to faster-than-light travel.")
later("daedalus", 5, "Sets out with Icarus on a very long trip to the galactic core.")
later("icarus", 5, "Sets out with Daedalus on a very long trip to the galactic core.")
later("vulcan", 2, "Becomes one of the first human colonies; Howard and Bridget work there.")
later("gliese-877", 3, "The final target of the war with the Others.")
later("las-vegas", 3, "Bob visits its ruins, buried under ice on a frozen Earth.")
later("garfield", 4, "Joins the Heaven's River expedition.")
later("matrix", 4, "Recovering a lost replicant's matrix becomes a key goal.")
later("bobnet", 4, "Control of the relays turns out to matter a great deal when BobNet comes under attack.")
later("bob", 2, "Moves among the Deltans in an android body, as 'Robert'.")
later("bob", 4, "Spends over a century searching for the missing Bender.")
later("medeiros", 3, "Has a final showdown with the Bobs at 82 Eridani.")
later("homer", 2, "VEHEMENT hacks him into sabotaging Earth.")
later("riker", 3, "Runs the defense and evacuation of Earth when the Others reach Sol.")
later("skippies", 5, "Build an AI, Thoth, that becomes self-aware.")

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
ev(1, "Earth in ruins", "Riker returns to Sol and finds Earth devastated by war, with scattered survivors.", ["riker", "earth", "butterworth"], confidence="medium", when="2157")
ev(1, "New worlds", "Milo finds and names Vulcan and Romulus before he is killed. Bill invents SCUT.", ["milo", "vulcan", "romulus", "scut", "bill"], when="2151–2165")
ev(1, "Something out there", "Mario finds traces of a civilization that strips planets bare.", ["mario", "others"], when="2169")

ev(2, "Colony program", "Riker organizes colony ships to move survivors off a dying Earth.", ["riker", "colony-ships", "earth", "butterworth"], when="2157–2170")
ev(2, "Archimedes", "Bob watches a bright Deltan cub, Archimedes, and gets more involved with Camelot.", ["archimedes", "camelot", "bob"], when="2166")
ev(2, "VEHEMENT strikes", "VEHEMENT hacks Homer and sabotages Earth's food supply. The fallout is devastating.", ["vehement", "homer", "riker", "bertram-vickers"], when="2175–2176")
ev(2, "Vulcan colony", "Howard helps the Vulcan colony and grows close to Bridget.", ["howard", "bridget", "vulcan"], when="2188–2189")
ev(2, "The Others confirmed", "Mario's clones scout the Others' home system; Bashful dies there.", ["others", "gliese-877", "bashful", "hal"], when="2187–2188")
ev(2, "Battle of Delta Pavonis", "The Bobs mass a fleet to defend the Pav and lose. They save some Pav in stasis.", ["battle-of-delta-pavonis", "pav", "jacques", "delta-pavonis"], when="2217")
ev(2, "Bob as Robert", "Bob moves among the Deltans in an android body.", ["bob", "android", "deltans"], when="2213")

ev(3, "Deltan politics", "Bob, living as Robert, is caught in a conflict between Camelot and Caerleon.", ["bob", "camelot", "caerleon", "fred"], when="2224–2225")
ev(3, "Farewell to Archimedes", "Archimedes dies of old age and Bob tells Buster the truth before leaving.", ["archimedes", "buster", "bawbe"], when="2233")
ev(3, "Bridget becomes a replicant", "Sabotage endangers Bridget, but a brain scan lets her come back as a replicant.", ["bridget", "howard", "rosie", "odin"], when="2220")
ev(3, "Poseidon's crisis", "Marcus forces Poseidon's council to hold elections.", ["marcus", "poseidon", "thark"], when="2214–2215")
ev(3, "Battle of Sol", "The Others reach Sol. The Bobs fight back and evacuate millions of people.", ["battle-of-sol", "bellerophon", "herschel", "cuba", "death-asteroids"], when="2257")
ev(3, "Striking the Others' home", "Daedalus and Icarus hurl planetary bodies at the Others' home system and end the threat.", ["daedalus", "icarus", "gliese-877", "others"], when="2257")
ev(3, "Homo sideria", "The Bobs declare themselves a new species. Bob visits a frozen Earth and moves on.", ["homo-sideria", "thor", "las-vegas"], when="~2258")

ev(4, "Looking for Bender", "Two centuries on, Bob follows clues about a missing clone to Eta Leporis.", ["bob", "bender", "eta-leporis"], when="2331")
ev(4, "Factions", "At a moot Bill explains that drift has split the Bobs into factions like Starfleet and the Skippies.", ["starfleet", "skippies", "replicative-drift", "bobmoot"], when="2331–2334")
ev(4, "Heaven's River", "Bob finds a huge habitat full of Quinlans and goes in with a team disguised as locals.", ["heavens-river", "quinlans", "sabbat", "bridget", "garfield"], when="~2332")
ev(4, "Starfleet War", "Starfleet hits BobNet and cuts off Bob's team.", ["starfleet-war", "starfleet", "three-lagoons"], when="2334")
ev(4, "Finding Bender", "Bob locates Bender, takes his matrix and runs.", ["bender", "resistance", "matrix"], when="~2334")
ev(4, "The journey home", "Bob travels back in disguise and befriends Theresa.", ["theresa", "administrator"], when="~2334")
ev(4, "Deal with the Administrator", "Hugh negotiates with ANEC-23; the scatterings end and Bender is restored.", ["hugh", "administrator", "bender", "lenny", "misty-falls"], when="2334")

ev(5, "After the war", "Anti-Bob feeling grows and moots stop.", ["bobmoot", "starfleet-war"], confidence="medium", when="~2335+")
ev(5, "To the galactic core", "Icarus and Daedalus set out to study the Fermi Paradox.", ["icarus", "daedalus", "galactic-core", "fermi-paradox"], confidence="medium", when="~2309–2345")
ev(5, "Thoth", "The Skippies' AI becomes self-aware.", ["thoth", "skippies"], confidence="medium", when="~2309–2345")
ev(5, "Wormhole experiments", "Bill researches wormholes and finds an abandoned civilization.", ["bill", "wormholes"], confidence="medium", when="~2309–2345")
ev(5, "Jabberwocky", "Howard and Bridget try to save the dragon-like natives.", ["howard", "bridget", "jabberwocky", "jabberwocky-dragons"], confidence="medium", when="~2309–2345")
ev(5, "Quiniverse", "Quinlan replicants get their own virtual world.", ["quiniverse", "quinlans"], confidence="medium", when="~2309–2345")

ev(6, "The network's builders", "The Bobs investigate who built the ancient wormhole network.", ["wormhole-network"], confidence="low", when="~2345+")
ev(6, "Derelict ship", "The Bobs explore an abandoned alien vessel.", ["derelict-ship"], confidence="low", when="~2345+")
ev(6, "Refugees", "The Bobs help tens of thousands of refugees find a new planet.", [], confidence="low", when="~2345+")
ev(6, "Nemesis", "The Bobs face a black hole threatening the galaxy.", ["nemesis"], confidence="low", when="~2345+")

# Events that are referenced as ids but live in timeline — add as terms category event
term("battle-of-delta-pavonis", "Battle of Delta Pavonis", 2, "The Bobs' first big fleet battle with the Others, fought to protect the Pav, and a loss.", ["others", "pav", "delta-pavonis", "jacques"], category="event")
term("battle-of-sol", "Battle of Sol", 3, "The Others' attack on humanity's home system and the Bobs' defense and mass evacuation of Earth.", ["others", "sol", "earth", "bellerophon", "herschel", "cuba", "death-asteroids"], category="event")


# Added 2026-11-21 (book 5). Wiki pages were unreachable; based on book-5 reviews, so medium confidence.
term("pgf", "Pan-Galactic Federation (PGF)", 5, "A long-gone alliance of alien species whose worlds were linked by wormholes. Its members left the galaxy thousands of years ago, and nobody knows why. Icarus and Daedalus explore what they left behind.", ["icarus", "daedalus", "wormholes", "fermi-paradox", "archivist"], category="organization", aliases=["PGF", "Federation"], confidence="medium")
term("archivist", "The Archivist", 5, "An AI that looks after the records the Pan-Galactic Federation left behind. The Bobs have to deal with it to learn anything, and it is not an easy conversation partner.", ["pgf", "icarus", "daedalus"], category="AI", confidence="medium")
term("hueys", "Hueys", 5, "Remote-controlled bodies for humans, sold by a company Howard sets up. Basically the Bobs' mannies, made available to ordinary people.", ["howard", "android"], category="technology", aliases=["Huey"], confidence="medium")
char("alexander", "Alexander", 5, "A leader of the dragon-like natives of Jabberwocky who guides his people on a migration to survive.", ["jabberwocky", "jabberwocky-dragons", "howard", "bridget"], group="Jabberwocky native", confidence="medium")

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
    "Bob names the Deltans' unspoiled world after the Garden of Eden.", ["eden", "deltans"], confidence="medium")

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
    "Some readers link the AI-loving faction's name to Skippy, the arrogant alien AI of Craig Alanson's series.", ["skippies"], confidence="low")

ref("ref-walden", "Title: Not Till We Are Lost", "Walden (Henry David Thoreau)", "Literature", 5,
    "From Walden: \"Not till we are lost ... do we begin to find ourselves.\"", ["bobiverse"])
ref("ref-jabberwocky", "Jabberwocky", "Through the Looking-Glass (Lewis Carroll)", "Literature", 5,
    "The dragon planet is named after Carroll's nonsense poem about slaying the Jabberwock.", ["jabberwocky", "jabberwocky-dragons"])
ref("ref-thoth", "Thoth", "Egyptian mythology", "Myth & legend", 5,
    "The Skippies' AI is named after the Egyptian god of wisdom and writing.", ["thoth", "skippies"], confidence="medium")

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
     ["medeiros", "brazilian-empire", "cloaking", "epsilon-eridani"], cls="Rival probe", confidence="medium")
ship("heaven-5", "Heaven 5.0", 2,
     "A much heavier generation of Bob vessel, built in numbers at Alpha Centauri once the Others become a real threat. Next to the original HEAVEN probe it is practically a dreadnought.",
     ["heaven-series", "others", "alpha-centauri", "battle-of-delta-pavonis"], cls="HEAVEN series", confidence="medium")
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

died("milo", 1, "Destroyed at 82 Eridani, most likely by Brazilian forces. The Bobs never get a full account of his last moments.", confidence="medium")
died("homer", 2, "Never recovers from being hacked by VEHEMENT and turned against Earth. He chooses to end his own existence.")
died("bashful", 2, "Self-destructs while scouting the Others' home system rather than be captured.")
died("hal", 2, "Confirms what is at the Others' home system and then self-destructs to avoid capture.")
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
