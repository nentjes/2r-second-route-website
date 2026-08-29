#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2R-website generator. Genereert de hele site (home, roadmap, verhalen)
in zes talen uit de data hieronder. Nieuw verhaal toevoegen? Voeg een
item toe aan STORIES en run: python3 build.py
"""
import os, html, json

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'public')
LANGS = ['nl', 'en', 'de', 'fr', 'es', 'pt']

LANG_LABEL = {'nl': 'NL', 'en': 'EN', 'de': 'DE', 'fr': 'FR', 'es': 'ES', 'pt': 'PT'}
HTML_LANG = {'nl': 'nl', 'en': 'en', 'de': 'de', 'fr': 'fr', 'es': 'es', 'pt': 'pt'}

# ---------------------------------------------------------------------------
# Categorie-labels (dezelfde 9 rubrieken als in de app, vertaald)
# ---------------------------------------------------------------------------
CATEGORIES = {
    'geschiedenis':    {'nl': 'Geschiedenis',        'en': 'History',            'de': 'Geschichte',            'fr': 'Histoire',              'es': 'Historia',               'pt': 'História'},
    'architectuur':    {'nl': 'Architectuur',        'en': 'Architecture',       'de': 'Architektur',           'fr': 'Architecture',          'es': 'Arquitectura',           'pt': 'Arquitetura'},
    'kunst':           {'nl': 'Kunst & Cultuur',     'en': 'Art & Culture',      'de': 'Kunst & Kultur',        'fr': 'Art & Culture',         'es': 'Arte y Cultura',         'pt': 'Arte e Cultura'},
    'natuur':          {'nl': 'Natuur',              'en': 'Nature',             'de': 'Natur',                 'fr': 'Nature',                'es': 'Naturaleza',             'pt': 'Natureza'},
    'eten en drinken': {'nl': 'Eten & Drinken',      'en': 'Food & Drink',       'de': 'Essen & Trinken',       'fr': 'Gastronomie',           'es': 'Comida y Bebida',        'pt': 'Comida e Bebida'},
    'mensen':          {'nl': 'Mensen & Verhalen',   'en': 'People & Stories',   'de': 'Menschen & Geschichten','fr': 'Gens & Récits',         'es': 'Gente e Historias',      'pt': 'Pessoas e Histórias'},
    'sport':           {'nl': 'Sport',               'en': 'Sport',              'de': 'Sport',                 'fr': 'Sport',                 'es': 'Deporte',                'pt': 'Desporto'},
    'techniek':        {'nl': 'Techniek & Industrie','en': 'Tech & Industry',    'de': 'Technik & Industrie',   'fr': 'Technique & Industrie', 'es': 'Técnica e Industria',    'pt': 'Técnica e Indústria'},
    'fotografie':      {'nl': 'Uitzicht & Fotografie','en': 'Views & Photography','de': 'Aussicht & Fotografie', 'fr': 'Panoramas & Photo',     'es': 'Miradores y Fotografía', 'pt': 'Miradouros e Fotografia'},
}

# ---------------------------------------------------------------------------
# Sitebrede tekst per taal
# ---------------------------------------------------------------------------
SITE = {
'nl': dict(
    nav_product='Product', nav_roadmap='Roadmap', nav_stories='Verhalen', nav_privacy='Privacy', nav_cta='Probeer 2R →',
    hero_eyebrow='2R · de reisgenoot die verhalen ziet',
    hero_h1='Niet de bestemming,<br>maar de reis maakt ons wijs.',
    hero_lede='2R vertelt niet alleen wat je ziet. Terwijl je eerste route (Google Maps, Waze) je van A naar B brengt, brengt <b>Route</b> onderweg kennis, verwondering en gesprekken op gang.',
    hero_btn_demo='Hoor een verhaal', hero_btn_roadmap='Rijd een stukje mee',
    hero_caption_coord='52.1045° N', hero_caption_note='Een avond onderweg · Utrecht',
    listen_label='01 · Een stem naast je', listen_h2='De wereld buiten wordt<br>een verhaal binnen.',
    listen_p='Geen lijst met weetjes. Route kiest één betekenisvol verhaal, vertelt het rustig en laat daarna weer ruimte voor het landschap — en voor elkaar.',
    listen_now='Route vertelt', listen_title='De verborgen geschiedenis<br>van het landschap', listen_sub='Gidsmodus · fragment binnenkort',
    journey_label='02 · Europa rijdt met je mee', journey_route_label='Europa · Route 02', journey_route_meta='vier windstreken · één reis',
    invite_label='Voor de volgende keer dat je instapt', invite_h2='Wat zal Route op jouw<br>volgende reis vertellen?',
    invite_p='Neem een warme stem, een levend reisboek en een beetje verwondering met je mee.', invite_btn='Neem Route mee',
    footer_tagline='Niet de bestemming, maar de reis maakt ons wijs.',
    footer_credit='Gebouwd door Roel Nentjes, samen met Claude (Anthropic).',
    stat1_num='9', stat1_lbl='interesse-rubrieken — elk apart getest',
    stat2_num='6', stat2_lbl='talen, live in de app en op deze site',
    stat3_num='4', stat3_lbl='reismodi — auto, fiets, te voet, trein', stat4_num='∞', stat4_lbl='plekken — overal, live gegenereerd',
    steps_eyebrow='Hoe het werkt', steps_h2='Van rijden naar luisteren in drie stappen',
    step1_h='Zet Route aan', step1_p='Eén knop. Kies je interesses — geschiedenis, natuur, kunst, eten & drinken — of typ er zelf een in.',
    step2_h='Rijd, fiets of wandel', step2_p='2R volgt je route via GPS en zoekt live naar wat er om je heen te vertellen valt — bij lokale bronnen, niet alleen Wikipedia.',
    step3_h='Luister naar Route', step3_p='Een warme, expressieve stem vertelt — eerlijk over wat je écht kunt zien, nooit doen-alsof.',
    why_eyebrow='Waarom 2R anders is', why_h2='Geen encyclopedie. Een reisgezel.',
    why_p="Bestaande reisverteller-apps werken met vooraf ingesproken scripts — beperkt tot populaire routes, hetzelfde verhaal voor iedereen. 2R genereert live, overal, en past zich aan jouw interesses aan.",
    f1_h='Lokale bronnen eerst', f1_p="Gemeentesites, VVV's en erfgoedorganisaties — niet alleen Wikipedia. In het buitenland wordt de lokale taal gebruikt en in jouw taal naverteld.",
    f2_h='Gidsmodus', f2_p='Eén doorlopend verhaal met het gebied als rode draad — land, provincie, streek, plaats — in plaats van losse weetjes.',
    f3_h='Eerlijk, altijd', f3_p='Route doet nooit alsof hij weet wat je ziet. Dichtbij: "kijk eens". Verder weg: "een omweg waard" — nooit andersom.',
    f4_h='Privacy-eerst', f4_p='Geen locatie-opslag, geen account nodig. Elk verzoek staat op zichzelf.',
    f5_h='Individueel of familie', f5_p='Eigen interesses, of content voor de hele auto — met spelletjes en quizjes onderweg in de maak.',
    f6_h='Werkt overal', f6_p='Getest in Nederland én tijdens een rit door Lombardije — dezelfde kwaliteit, in jouw taal verteld.',
    stories_eyebrow='03 · De steden spreken', stories_h2='Vijf steden.<br>Vijf verschillende stemmen.',
    stories_p='Van Amsterdam naar Parijs, Wenen, Rome en Lissabon: iedere stad heeft haar eigen ritme, maar onderweg worden de verhalen van Europa één levend reisboek.',
    stories_view_all='Bekijk alle verhalen →',
    cta_h='2R is nu in besloten test', cta_p='De app draait live in TestFlight en op het web. Wil je meetesten, of wil je 2R gebruiken om jouw regio, museum of restaurant onder de aandacht te brengen?', cta_btn='Neem contact op',
    footer_contact='Contact',
    footer_family='Onderdeel van de <a href="https://nentjes.nl">1R</a>-familie — zie ook <a href="https://autestme.com">Autestme</a> en <a href="https://kindertekening.com">Kindertekening</a>, andere projecten van dezelfde makers.',
    rm_eyebrow='Roadmap', rm_h1="Waar 2R vandaan komt, en waar we naartoe gaan",
    rm_lede='2R begon als een idee tijdens een autorit: onderweg viel er zoveel te zien, maar niemand om het uit te leggen. Dit is wat er sindsdien is gebouwd, en wat hierna komt.',
    rm_live='Vandaag live', rm_testflight='In TestFlight', rm_soon='Hierna', rm_later='Later',
    rm_cta_h='Wil je meebouwen aan dit verhaal?', rm_cta_p='Als tester, als lokale partner, of gewoon omdat je het idee net zo leuk vindt als wij.',
    stories_index_eyebrow='Archief', stories_index_h1='Verhalen die Route heeft verteld',
    stories_index_lede='Elk verhaal hieronder is echt door 2R gegenereerd tijdens het testen — inclusief bron, zodat je kunt nalezen waar het vandaan komt.',
    story_source_lbl='Bron', story_told_by='verteld door Route',
    story_back='← Terug naar alle verhalen',
),
'en': dict(
    nav_product='Product', nav_roadmap='Roadmap', nav_stories='Stories', nav_privacy='Privacy', nav_cta='Try 2R →',
    hero_eyebrow='2R · the travel companion that sees stories',
    hero_h1='Not the destination —<br>the journey makes us wise.',
    hero_lede="2R doesn't just tell you what you're seeing. While your first route (Google Maps, Waze) gets you from A to B, <b>Route</b> brings knowledge, wonder and conversation along the way.",
    hero_btn_demo='Hear a story', hero_btn_roadmap='Ride along for a bit',
    hero_caption_coord='52.1045° N', hero_caption_note='An evening on the road · Utrecht',
    listen_label='01 · A voice beside you', listen_h2='The world outside becomes<br>a story within.',
    listen_p='No list of facts. Route picks one meaningful story, tells it calmly, then makes room again for the landscape — and for each other.',
    listen_now='Route is telling', listen_title='The hidden history<br>of the landscape', listen_sub='Guide mode · sample coming soon',
    journey_label='02 · Europe rides along with you', journey_route_label='Europe · Route 02', journey_route_meta='four compass points · one journey',
    invite_label='For the next time you get in', invite_h2='What will Route tell you<br>on your next trip?',
    invite_p='Bring a warm voice, a living travel journal, and a little wonder.', invite_btn='Take Route with you',
    footer_tagline='Not the destination — the journey makes us wise.',
    footer_credit='Built by Roel Nentjes, together with Claude (Anthropic).',
    stat1_num='9', stat1_lbl='interest categories — each individually tested',
    stat2_num='6', stat2_lbl='languages, live in the app and on this site',
    stat3_num='4', stat3_lbl='travel modes — car, bike, walk, train', stat4_num='∞', stat4_lbl='places — anywhere, generated live',
    steps_eyebrow='How it works', steps_h2='From driving to listening, in three steps',
    step1_h='Turn Route on', step1_p='One switch. Pick your interests — history, nature, art, food & drink — or type in your own.',
    step2_h='Drive, cycle or walk', step2_p="2R follows your route via GPS and searches live for what's worth telling — from local sources, not just Wikipedia.",
    step3_h='Listen to Route', step3_p='A warm, expressive voice narrates — honestly about what you can actually see, never pretending.',
    why_eyebrow='Why 2R is different', why_h2='Not an encyclopedia. A travel companion.',
    why_p='Existing travel-narrator apps rely on pre-recorded scripts — limited to popular routes, the same story for everyone. 2R generates live, everywhere, and adapts to your interests.',
    f1_h='Local sources first', f1_p='Municipal sites, tourism boards and heritage organisations — not just Wikipedia. Abroad, local-language sources are used and retold in your own language.',
    f2_h='Guide mode', f2_p='One continuous story with the region as its through-line — country, province, area, town — instead of disconnected facts.',
    f3_h='Always honest', f3_p='Route never pretends to know what you can see. Close by: "look now." Further away: "worth a detour" — never the other way around.',
    f4_h='Privacy-first', f4_p='No location storage, no account required. Every request stands on its own.',
    f5_h='Solo or family', f5_p='Your own interests, or content for the whole car — with games and quizzes for the road in the works.',
    f6_h='Works anywhere', f6_p='Tested in the Netherlands and on a drive through Lombardy, Italy — same quality, narrated in your own language.',
    stories_eyebrow='03 · The cities speak', stories_h2='Five cities.<br>Five different voices.',
    stories_p='From Amsterdam to Paris, Vienna, Rome and Lisbon: every city has its own rhythm, but on the road the stories of Europe become one living travel journal.',
    stories_view_all='View all stories →',
    cta_h='2R is currently in closed testing', cta_p='The app is live in TestFlight and on the web. Want to help test, or use 2R to put your region, museum or restaurant on the map?', cta_btn='Get in touch',
    footer_contact='Contact',
    footer_family='Part of the <a href="https://nentjes.nl">1R</a> family — see also <a href="https://autestme.com">Autestme</a> and <a href="https://kindertekening.com">Kindertekening</a>, other projects by the same makers.',
    rm_eyebrow='Roadmap', rm_h1="Where 2R came from, and where we're going",
    rm_lede="2R started as an idea during a road trip: there was so much to see along the way, and no one to explain it. Here's what's been built since, and what's next.",
    rm_live='Live today', rm_testflight='In TestFlight', rm_soon='Coming soon', rm_later='Later',
    rm_cta_h='Want to help build this?', rm_cta_p='As a tester, as a local partner, or simply because you like the idea as much as we do.',
    stories_index_eyebrow='Archive', stories_index_h1='Stories Route has told',
    stories_index_lede='Every story below was genuinely generated by 2R while testing — with its source attached, so you can check where it came from.',
    story_source_lbl='Source', story_told_by='narrated by Route',
    story_back='← Back to all stories',
),
'de': dict(
    nav_product='Produkt', nav_roadmap='Roadmap', nav_stories='Geschichten', nav_privacy='Datenschutz', nav_cta='2R testen →',
    hero_eyebrow='2R · der Reisebegleiter, der Geschichten sieht',
    hero_h1='Nicht das Ziel —<br>die Reise macht uns weise.',
    hero_lede='2R erzählt nicht nur, was du siehst. Während deine erste Route (Google Maps, Waze) dich von A nach B bringt, bringt <b>Route</b> unterwegs Wissen, Staunen und Gespräche in Gang.',
    hero_btn_demo='Höre eine Geschichte', hero_btn_roadmap='Fahr ein Stück mit',
    hero_caption_coord='52,1045° N', hero_caption_note='Ein Abend unterwegs · Utrecht',
    listen_label='01 · Eine Stimme neben dir', listen_h2='Die Welt draußen wird<br>zur Geschichte drinnen.',
    listen_p='Keine Liste von Fakten. Route wählt eine bedeutsame Geschichte, erzählt sie ruhig und lässt danach wieder Raum für die Landschaft — und füreinander.',
    listen_now='Route erzählt', listen_title='Die verborgene Geschichte<br>der Landschaft', listen_sub='Guide-Modus · Hörprobe folgt',
    journey_label='02 · Europa fährt mit dir mit', journey_route_label='Europa · Route 02', journey_route_meta='vier Himmelsrichtungen · eine Reise',
    invite_label='Für das nächste Mal, wenn du einsteigst', invite_h2='Was wird Route dir auf<br>deiner nächsten Reise erzählen?',
    invite_p='Nimm eine warme Stimme, ein lebendiges Reisetagebuch und ein bisschen Staunen mit.', invite_btn='Nimm Route mit',
    footer_tagline='Nicht das Ziel — die Reise macht uns weise.',
    footer_credit='Gebaut von Roel Nentjes, gemeinsam mit Claude (Anthropic).',
    stat1_num='9', stat1_lbl='Interessen-Rubriken — jede einzeln getestet',
    stat2_num='6', stat2_lbl='Sprachen, live in der App und auf dieser Website',
    stat3_num='4', stat3_lbl='Reisemodi — Auto, Rad, zu Fuß, Bahn', stat4_num='∞', stat4_lbl='Orte — überall, live generiert',
    steps_eyebrow='So funktioniert es', steps_h2='In drei Schritten vom Fahren zum Zuhören',
    step1_h='Route einschalten', step1_p='Ein Schalter. Wähle deine Interessen — Geschichte, Natur, Kunst, Essen & Trinken — oder gib eigene ein.',
    step2_h='Fahren, radeln oder gehen', step2_p='2R folgt deiner Route per GPS und sucht live nach Erzählenswertem — aus lokalen Quellen, nicht nur Wikipedia.',
    step3_h='Route zuhören', step3_p='Eine warme, ausdrucksstarke Stimme erzählt — ehrlich über das, was du wirklich sehen kannst, nie vorgetäuscht.',
    why_eyebrow='Warum 2R anders ist', why_h2='Kein Lexikon. Ein Reisebegleiter.',
    why_p='Bestehende Reiseerzähler-Apps arbeiten mit vorab aufgenommenen Skripten — begrenzt auf beliebte Routen, dieselbe Geschichte für alle. 2R generiert live, überall, und passt sich deinen Interessen an.',
    f1_h='Lokale Quellen zuerst', f1_p='Gemeindeseiten, Tourismusverbände und Denkmalorganisationen — nicht nur Wikipedia. Im Ausland werden lokalsprachige Quellen genutzt und in deiner Sprache nacherzählt.',
    f2_h='Guide-Modus', f2_p='Eine durchgehende Geschichte mit der Region als rotem Faden — Land, Provinz, Gegend, Ort — statt einzelner Fakten.',
    f3_h='Immer ehrlich', f3_p='Route tut nie so, als wüsste sie, was du siehst. Ganz nah: "schau mal". Weiter weg: "einen Umweg wert" — nie andersherum.',
    f4_h='Datenschutz zuerst', f4_p='Keine Standortspeicherung, kein Konto nötig. Jede Anfrage steht für sich.',
    f5_h='Einzeln oder Familie', f5_p='Eigene Interessen, oder Inhalte für das ganze Auto — mit Spielen und Quiz für unterwegs in Arbeit.',
    f6_h='Funktioniert überall', f6_p='Getestet in den Niederlanden und auf einer Fahrt durch die Lombardei — gleiche Qualität, in deiner Sprache erzählt.',
    stories_eyebrow='03 · Die Städte sprechen', stories_h2='Fünf Städte.<br>Fünf verschiedene Stimmen.',
    stories_p='Von Amsterdam über Paris, Wien, Rom bis Lissabon: Jede Stadt hat ihren eigenen Rhythmus, doch unterwegs werden die Geschichten Europas zu einem einzigen lebendigen Reisetagebuch.',
    stories_view_all='Alle Geschichten ansehen →',
    cta_h='2R befindet sich derzeit im geschlossenen Test', cta_p='Die App läuft live in TestFlight und im Web. Möchtest du mittesten oder 2R nutzen, um deine Region, dein Museum oder Restaurant bekannt zu machen?', cta_btn='Kontakt aufnehmen',
    footer_contact='Kontakt',
    footer_family='Teil der <a href="https://nentjes.nl">1R</a>-Familie — siehe auch <a href="https://autestme.com">Autestme</a> und <a href="https://kindertekening.com">Kindertekening</a>, weitere Projekte derselben Macher.',
    rm_eyebrow='Roadmap', rm_h1='Woher 2R kommt, und wohin es geht',
    rm_lede='2R begann als Idee während einer Autofahrt: Unterwegs gab es so viel zu sehen, aber niemanden, der es erklärte. Das wurde seitdem gebaut, und das kommt als Nächstes.',
    rm_live='Heute live', rm_testflight='In TestFlight', rm_soon='Demnächst', rm_later='Später',
    rm_cta_h='Möchtest du mitbauen?', rm_cta_p='Als Tester, als lokaler Partner, oder einfach weil dir die Idee genauso gut gefällt wie uns.',
    stories_index_eyebrow='Archiv', stories_index_h1='Geschichten, die Route erzählt hat',
    stories_index_lede='Jede Geschichte unten wurde tatsächlich von 2R während der Tests generiert — mit Quellenangabe, damit du nachlesen kannst, woher sie stammt.',
    story_source_lbl='Quelle', story_told_by='erzählt von Route',
    story_back='← Zurück zu allen Geschichten',
),
'fr': dict(
    nav_product='Produit', nav_roadmap='Roadmap', nav_stories='Histoires', nav_privacy='Confidentialité', nav_cta='Essayer 2R →',
    hero_eyebrow="2R · le compagnon de voyage qui voit les histoires",
    hero_h1="Pas la destination —<br>c'est le voyage qui nous rend sages.",
    hero_lede="2R ne se contente pas de raconter ce que vous voyez. Pendant que votre premier itinéraire (Google Maps, Waze) vous mène d'un point A à un point B, <b>Route</b> apporte en chemin de la connaissance, de l'émerveillement et des conversations.",
    hero_btn_demo='Écouter une histoire', hero_btn_roadmap='Faire un bout de route',
    hero_caption_coord='52,1045° N', hero_caption_note='Une soirée sur la route · Utrecht',
    listen_label='01 · Une voix à vos côtés', listen_h2='Le monde extérieur devient<br>une histoire intérieure.',
    listen_p='Pas une liste de faits. Route choisit une histoire qui a du sens, la raconte calmement, puis laisse de nouveau place au paysage — et à vous.',
    listen_now='Route raconte', listen_title="L'histoire cachée<br>du paysage", listen_sub='Mode guide · extrait à venir',
    journey_label="02 · L'Europe vous accompagne", journey_route_label='Europe · Itinéraire 02', journey_route_meta='quatre points cardinaux · un seul voyage',
    invite_label='Pour la prochaine fois que vous montez en voiture', invite_h2='Que vous racontera Route<br>lors de votre prochain trajet ?',
    invite_p="Emportez une voix chaleureuse, un carnet de voyage vivant et un peu d'émerveillement.", invite_btn='Emportez Route avec vous',
    footer_tagline="Pas la destination — c'est le voyage qui nous rend sages.",
    footer_credit='Conçu par Roel Nentjes, avec Claude (Anthropic).',
    stat1_num='9', stat1_lbl="catégories d'intérêt — chacune testée individuellement",
    stat2_num='6', stat2_lbl="langues, disponibles dans l'app et sur ce site",
    stat3_num='4', stat3_lbl='modes — voiture, vélo, à pied, train', stat4_num='∞', stat4_lbl='lieux — partout, générés en direct',
    steps_eyebrow='Comment ça marche', steps_h2="De la route à l'écoute, en trois étapes",
    step1_h='Activez Route', step1_p="Un interrupteur. Choisissez vos centres d'intérêt — histoire, nature, art, gastronomie — ou saisissez les vôtres.",
    step2_h='Roulez, pédalez ou marchez', step2_p="2R suit votre itinéraire par GPS et cherche en direct ce qui vaut la peine d'être raconté — à partir de sources locales, pas seulement Wikipédia.",
    step3_h='Écoutez Route', step3_p="Une voix chaleureuse et expressive raconte — honnêtement, sur ce que vous pouvez réellement voir, jamais en faisant semblant.",
    why_eyebrow='Pourquoi 2R est différent', why_h2='Pas une encyclopédie. Un compagnon de voyage.',
    why_p="Les applications de guide de voyage existantes reposent sur des scripts préenregistrés — limitées aux itinéraires populaires, la même histoire pour tout le monde. 2R génère en direct, partout, et s'adapte à vos centres d'intérêt.",
    f1_h="Les sources locales d'abord", f1_p="Sites municipaux, offices de tourisme et organisations patrimoniales — pas seulement Wikipédia. À l'étranger, les sources en langue locale sont utilisées puis racontées dans votre propre langue.",
    f2_h='Mode guide', f2_p='Un récit continu avec la région comme fil conducteur — pays, province, terroir, ville — plutôt que des faits isolés.',
    f3_h='Toujours honnête', f3_p='Route ne prétend jamais savoir ce que vous voyez. Tout près : "regardez". Plus loin : "vaut le détour" — jamais l\'inverse.',
    f4_h="La confidentialité d'abord", f4_p="Aucune conservation de localisation, aucun compte requis. Chaque requête est indépendante.",
    f5_h='Solo ou en famille', f5_p="Vos propres centres d'intérêt, ou du contenu pour toute la voiture — avec des jeux et des quiz pour la route en préparation.",
    f6_h='Fonctionne partout', f6_p='Testé aux Pays-Bas et lors d\'un trajet en Lombardie, en Italie — même qualité, racontée dans votre propre langue.',
    stories_eyebrow='03 · Les villes prennent la parole', stories_h2='Cinq villes.<br>Cinq voix différentes.',
    stories_p="D'Amsterdam à Paris, Vienne, Rome et Lisbonne : chaque ville a son propre rythme, mais en chemin, les histoires de l'Europe deviennent un seul carnet de voyage vivant.",
    stories_view_all='Voir toutes les histoires →',
    cta_h="2R est actuellement en test fermé", cta_p="L'application fonctionne en direct sur TestFlight et sur le web. Envie de participer aux tests, ou d'utiliser 2R pour mettre en avant votre région, musée ou restaurant ?", cta_btn='Nous contacter',
    footer_contact='Contact',
    footer_family='Fait partie de la famille <a href="https://nentjes.nl">1R</a> — voir aussi <a href="https://autestme.com">Autestme</a> et <a href="https://kindertekening.com">Kindertekening</a>, d\'autres projets des mêmes créateurs.',
    rm_eyebrow='Feuille de route', rm_h1="D'où vient 2R, et où nous allons",
    rm_lede="2R est né d'une idée pendant un road trip : il y avait tant à voir en chemin, et personne pour l'expliquer. Voici ce qui a été construit depuis, et ce qui arrive ensuite.",
    rm_live="En direct aujourd'hui", rm_testflight='Sur TestFlight', rm_soon='Bientôt', rm_later='Plus tard',
    rm_cta_h='Envie de nous aider à construire cela ?', rm_cta_p="En tant que testeur, partenaire local, ou tout simplement parce que vous aimez cette idée autant que nous.",
    stories_index_eyebrow='Archives', stories_index_h1='Histoires racontées par Route',
    stories_index_lede="Chaque histoire ci-dessous a réellement été générée par 2R lors de nos tests — avec sa source jointe, pour que vous puissiez vérifier d'où elle vient.",
    story_source_lbl='Source', story_told_by='racontée par Route',
    story_back='← Retour à toutes les histoires',
),
'es': dict(
    nav_product='Producto', nav_roadmap='Roadmap', nav_stories='Historias', nav_privacy='Privacidad', nav_cta='Prueba 2R →',
    hero_eyebrow='2R · el compañero de viaje que ve historias',
    hero_h1='No el destino —<br>el viaje es lo que nos hace sabios.',
    hero_lede='El 2R no solo cuenta lo que ves. Mientras tu primera ruta (Google Maps, Waze) te lleva de A a B, <b>Route</b> aporta conocimiento, asombro y conversación por el camino.',
    hero_btn_demo='Escucha una historia', hero_btn_roadmap='Recorre un tramo con nosotros',
    hero_caption_coord='52,1045° N', hero_caption_note='Una tarde en la carretera · Utrecht',
    listen_label='01 · Una voz a tu lado', listen_h2='El mundo de fuera se convierte<br>en una historia dentro.',
    listen_p='Sin listas de datos. Route elige una historia con sentido, la cuenta con calma y luego vuelve a dejar espacio para el paisaje —y para vosotros.',
    listen_now='Route está contando', listen_title='La historia oculta<br>del paisaje', listen_sub='Modo guía · fragmento en breve',
    journey_label='02 · Europa viaja contigo', journey_route_label='Europa · Ruta 02', journey_route_meta='cuatro puntos cardinales · un solo viaje',
    invite_label='Para la próxima vez que subas al coche', invite_h2='¿Qué te contará Route<br>en tu próximo viaje?',
    invite_p='Llévate una voz cálida, un diario de viaje vivo y un poco de asombro.', invite_btn='Llévate a Route',
    footer_tagline='No el destino — el viaje es lo que nos hace sabios.',
    footer_credit='Creado por Roel Nentjes, junto con Claude (Anthropic).',
    stat1_num='9', stat1_lbl='categorías de interés — cada una probada individualmente',
    stat2_num='6', stat2_lbl='idiomas, disponibles en la app y en este sitio',
    stat3_num='4', stat3_lbl='modos — coche, bici, a pie, tren', stat4_num='∞', stat4_lbl='lugares — en cualquier sitio, en vivo',
    steps_eyebrow='Cómo funciona', steps_h2='De conducir a escuchar, en tres pasos',
    step1_h='Activa Route', step1_p='Un interruptor. Elige tus intereses —historia, naturaleza, arte, gastronomía— o escribe los tuyos.',
    step2_h='Conduce, pedalea o camina', step2_p='2R sigue tu ruta por GPS y busca en vivo qué vale la pena contar —a partir de fuentes locales, no solo Wikipedia.',
    step3_h='Escucha a Route', step3_p='Una voz cálida y expresiva narra —con honestidad sobre lo que realmente puedes ver, nunca fingiendo.',
    why_eyebrow='Por qué 2R es diferente', why_h2='No es una enciclopedia. Es un compañero de viaje.',
    why_p='Las apps de narración de viajes existentes usan guiones pregrabados —limitadas a rutas populares, la misma historia para todos. 2R genera en vivo, en cualquier lugar, y se adapta a tus intereses.',
    f1_h='Fuentes locales primero', f1_p='Webs municipales, oficinas de turismo y organizaciones patrimoniales —no solo Wikipedia. En el extranjero se usan fuentes en el idioma local y se cuentan en tu propio idioma.',
    f2_h='Modo guía', f2_p='Una historia continua con la región como hilo conductor —país, provincia, comarca, localidad— en lugar de datos aislados.',
    f3_h='Siempre honesto', f3_p='Route nunca finge saber lo que puedes ver. Cerca: "mira ahora". Más lejos: "vale la pena el desvío" —nunca al revés.',
    f4_h='La privacidad primero', f4_p='Sin almacenamiento de ubicación, sin necesidad de cuenta. Cada solicitud es independiente.',
    f5_h='Individual o en familia', f5_p='Tus propios intereses, o contenido para todo el coche —con juegos y quizzes para el camino en desarrollo.',
    f6_h='Funciona en cualquier lugar', f6_p='Probado en los Países Bajos y en un viaje por Lombardía, Italia —misma calidad, narrada en tu propio idioma.',
    stories_eyebrow='03 · Las ciudades hablan', stories_h2='Cinco ciudades.<br>Cinco voces distintas.',
    stories_p='De Ámsterdam a París, Viena, Roma y Lisboa: cada ciudad tiene su propio ritmo, pero en el camino las historias de Europa se convierten en un único diario de viaje vivo.',
    stories_view_all='Ver todas las historias →',
    cta_h='2R está actualmente en pruebas cerradas', cta_p='La app funciona en vivo en TestFlight y en la web. ¿Quieres ayudar a probarla, o usar 2R para dar a conocer tu región, museo o restaurante?', cta_btn='Contáctanos',
    footer_contact='Contacto',
    footer_family='Parte de la familia <a href="https://nentjes.nl">1R</a> —mira también <a href="https://autestme.com">Autestme</a> y <a href="https://kindertekening.com">Kindertekening</a>, otros proyectos de los mismos creadores.',
    rm_eyebrow='Hoja de ruta', rm_h1='De dónde viene 2R y hacia dónde vamos',
    rm_lede='2R nació como una idea durante un viaje en coche: había tanto que ver en el camino, y nadie para explicarlo. Esto es lo que se ha construido desde entonces, y lo que viene después.',
    rm_live='En vivo hoy', rm_testflight='En TestFlight', rm_soon='Próximamente', rm_later='Más adelante',
    rm_cta_h='¿Quieres ayudar a construir esto?', rm_cta_p='Como probador, como socio local, o simplemente porque te gusta la idea tanto como a nosotros.',
    stories_index_eyebrow='Archivo', stories_index_h1='Historias que Route ha contado',
    stories_index_lede='Cada historia a continuación fue generada realmente por 2R durante las pruebas —con su fuente incluida, para que puedas comprobar de dónde viene.',
    story_source_lbl='Fuente', story_told_by='narrado por Route',
    story_back='← Volver a todas las historias',
),
'pt': dict(
    nav_product='Produto', nav_roadmap='Roadmap', nav_stories='Histórias', nav_privacy='Privacidade', nav_cta='Experimente 2R →',
    hero_eyebrow='2R · o companheiro de viagem que vê histórias',
    hero_h1='Não o destino —<br>a viagem é o que nos torna sábios.',
    hero_lede='O 2R não conta apenas o que você vê. Enquanto sua primeira rota (Google Maps, Waze) o leva de A a B, <b>Route</b> traz conhecimento, encantamento e boas conversas pelo caminho.',
    hero_btn_demo='Ouça uma história', hero_btn_roadmap='Ande um trecho com a gente',
    hero_caption_coord='52,1045° N', hero_caption_note='Uma noite na estrada · Utrecht',
    listen_label='01 · Uma voz ao seu lado', listen_h2='O mundo de fora se torna<br>uma história por dentro.',
    listen_p='Nenhuma lista de fatos. A Route escolhe uma história com significado, narra com calma e depois abre espaço de novo para a paisagem — e para vocês.',
    listen_now='A Route está narrando', listen_title='A história escondida<br>da paisagem', listen_sub='Modo guia · trecho em breve',
    journey_label='02 · A Europa viaja com você', journey_route_label='Europa · Rota 02', journey_route_meta='quatro pontos cardeais · uma só viagem',
    invite_label='Para a próxima vez que você entrar no carro', invite_h2='O que a Route vai contar<br>na sua próxima viagem?',
    invite_p='Leve uma voz calorosa, um diário de viagem vivo e um pouco de encantamento.', invite_btn='Leve a Route com você',
    footer_tagline='Não o destino — a viagem é o que nos torna sábios.',
    footer_credit='Criado por Roel Nentjes, com a Claude (Anthropic).',
    stat1_num='9', stat1_lbl='categorias de interesse — cada uma testada individualmente',
    stat2_num='6', stat2_lbl='idiomas, disponíveis no app e neste site',
    stat3_num='4', stat3_lbl='modos — carro, bici, a pé, comboio', stat4_num='∞', stat4_lbl='lugares — em qualquer lugar, ao vivo',
    steps_eyebrow='Como funciona', steps_h2='De dirigir a ouvir, em três passos',
    step1_h='Ative a Route', step1_p='Um interruptor. Escolha seus interesses — história, natureza, arte, gastronomia — ou digite os seus.',
    step2_h='Dirija, pedale ou caminhe', step2_p='O 2R segue sua rota por GPS e busca ao vivo o que vale a pena contar — de fontes locais, não só a Wikipédia.',
    step3_h='Ouça a Route', step3_p='Uma voz calorosa e expressiva narra — com honestidade sobre o que você realmente pode ver, nunca fingindo.',
    why_eyebrow='Por que o 2R é diferente', why_h2='Não é uma enciclopédia. É um companheiro de viagem.',
    why_p='Os apps de narração de viagem existentes usam roteiros pré-gravados — limitados a rotas populares, a mesma história para todos. O 2R gera ao vivo, em qualquer lugar, e se adapta aos seus interesses.',
    f1_h='Fontes locais primeiro', f1_p='Sites municipais, órgãos de turismo e organizações de patrimônio — não só a Wikipédia. No exterior, fontes no idioma local são usadas e recontadas no seu próprio idioma.',
    f2_h='Modo guia', f2_p='Uma história contínua com a região como fio condutor — país, província, região, cidade — em vez de fatos isolados.',
    f3_h='Sempre honesto', f3_p='A Route nunca finge saber o que você pode ver. Perto: "olhe agora". Mais longe: "vale o desvio" — nunca o contrário.',
    f4_h='Privacidade em primeiro lugar', f4_p='Sem armazenamento de localização, sem conta necessária. Cada solicitação é independente.',
    f5_h='Individual ou em família', f5_p='Seus próprios interesses, ou conteúdo para todo o carro — com jogos e quizzes para a estrada a caminho.',
    f6_h='Funciona em qualquer lugar', f6_p='Testado nos Países Baixos e em uma viagem pela Lombardia, Itália — mesma qualidade, narrada no seu próprio idioma.',
    stories_eyebrow='03 · As cidades falam', stories_h2='Cinco cidades.<br>Cinco vozes diferentes.',
    stories_p='De Amsterdã a Paris, Viena, Roma e Lisboa: cada cidade tem seu próprio ritmo, mas pelo caminho as histórias da Europa se tornam um único diário de viagem vivo.',
    stories_view_all='Ver todas as histórias →',
    cta_h='O 2R está atualmente em teste fechado', cta_p='O app está ao vivo no TestFlight e na web. Quer ajudar a testar, ou usar o 2R para divulgar sua região, museu ou restaurante?', cta_btn='Entrar em contato',
    footer_contact='Contato',
    footer_family='Parte da família <a href="https://nentjes.nl">1R</a> — veja também <a href="https://autestme.com">Autestme</a> e <a href="https://kindertekening.com">Kindertekening</a>, outros projetos dos mesmos criadores.',
    rm_eyebrow='Roteiro', rm_h1='De onde o 2R veio, e para onde vamos',
    rm_lede='O 2R começou como uma ideia durante uma viagem de carro: havia tanto para ver pelo caminho, e ninguém para explicar. Isto é o que foi construído desde então, e o que vem a seguir.',
    rm_live='Ao vivo hoje', rm_testflight='No TestFlight', rm_soon='Em breve', rm_later='Mais tarde',
    rm_cta_h='Quer ajudar a construir isso?', rm_cta_p='Como testador, como parceiro local, ou simplesmente porque gosta da ideia tanto quanto nós.',
    stories_index_eyebrow='Arquivo', stories_index_h1='Histórias que a Route contou',
    stories_index_lede='Cada história abaixo foi genuinamente gerada pelo 2R durante os testes — com a fonte anexada, para que você possa conferir de onde veio.',
    story_source_lbl='Fonte', story_told_by='narrado pela Route',
    story_back='← Voltar para todas as histórias',
),
}

# ---------------------------------------------------------------------------
# Privacybeleid — zelfde juridische tekst als worker/src/index.js PRIVACY_HTML,
# vertaald. Bij inhoudelijke wijzigingen: hier én daar aanpassen.
# ---------------------------------------------------------------------------
PRIVACY = {
'nl': dict(
    eyebrow='Privacy', title='Privacybeleid — 2R', updated='Laatst bijgewerkt: augustus 2026',
    intro='2R (werktitel: MapsInfo) is een reisgids-app die tijdens het rijden, fietsen of wandelen gesproken verhalen vertelt over de omgeving. Dit beleid legt uit welke gegevens de app gebruikt en waarom — haarfijn, zonder kleine lettertjes.',
    h_location='Locatie',
    location_items=[
        'Je GPS-locatie wordt gebruikt om te bepalen welke verhalen relevant zijn.',
        '<strong>Standaard wordt je locatie niet opgeslagen en niet gelogd.</strong> Elk verzoek aan de server bevat alleen de naam en context van een specifieke plek — geen locatiegeschiedenis, geen rittenregistratie.',
        '<strong>Uitgebreide logboeken zijn een opt-in voor het testteam.</strong> Alleen als je het zélf aanzet (ontgrendeld met een diagnose-code die we met onze vaste testers delen) leggen we meer vast — waaronder je GPS-positie, rijrichting en snelheid op het moment dat een verhaal wordt gemaakt — om fouten in de verhalen op te sporen en de app te verbeteren. Dit staat standaard uit, geldt alleen zolang jij het zelf aan hebt staan, wordt nooit met derden gedeeld, en kun je op elk moment weer uitzetten.',
    ],
    h_stories='Verhalen &amp; spraak (verwerkers)',
    stories_items=[
        'Om verhalen te genereren sturen we plaatsnamen en korte context naar <strong>Google (Gemini API)</strong>.',
        'Om de tekst voor te lezen sturen we die tekst naar <strong>ElevenLabs</strong> voor spraaksynthese.',
        'Voor feitelijke informatie wordt rechtstreeks vanaf je toestel <strong>Wikipedia</strong> geraadpleegd, en voor routes <strong>OpenStreetMap / OSRM</strong> — deze verzoeken lopen niet via onze server.',
        'Gegenereerde verhalen en spraakfragmenten worden tijdelijk gecachet (hergebruikt voor andere gebruikers op dezelfde plek) om kosten en wachttijd te beperken.',
    ],
    h_limits='Gebruikslimieten',
    limits_text='Om misbruik te voorkomen houden we per IP-adres een technische, tijdelijke teller bij (maximaal 48 uur bewaard). Dit is uitsluitend een aantal, nooit gekoppeld aan een profiel, naam of account, en wordt nooit gedeeld met derden.',
    h_accounts='Accounts',
    accounts_text='De app vereist geen account, inloggen of registratie.',
    h_contact='Contact',
    contact_text='Vragen over dit beleid? Mail naar <a href="mailto:nimco@nentjes.nl">nimco@nentjes.nl</a>.',
),
'en': dict(
    eyebrow='Privacy', title='Privacy Policy — 2R', updated='Last updated: August 2026',
    intro="2R (working title: MapsInfo) is a travel-guide app that narrates the world around you while you drive, cycle or walk. This policy explains exactly what data the app uses and why — no fine print.",
    h_location='Location',
    location_items=[
        'Your GPS location is used to determine which stories are relevant.',
        '<strong>By default your location is never stored and never logged.</strong> Every request to the server contains only the name and context of a specific place — no location history, no trip logging.',
        '<strong>Extended logging is an opt-in for our testing team.</strong> Only if you switch it on yourself (unlocked with a diagnostics code we share with our regular testers) do we record more — including your GPS position, heading and speed at the moment a story is generated — to track down bugs and improve the app. This is off by default, applies only while you have it enabled, is never shared with third parties, and can be turned off at any time.',
    ],
    h_stories='Stories &amp; voice (processors)',
    stories_items=[
        'To generate stories we send place names and brief context to <strong>Google (Gemini API)</strong>.',
        'To narrate the text aloud, that text is sent to <strong>ElevenLabs</strong> for voice synthesis.',
        'Factual information is fetched directly from your device from <strong>Wikipedia</strong>, and route data from <strong>OpenStreetMap / OSRM</strong> — these requests never pass through our server.',
        'Generated stories and audio fragments are cached temporarily (reused for other users at the same location) to reduce cost and wait time.',
    ],
    h_limits='Usage limits',
    limits_text='To prevent abuse we keep a technical, temporary counter per IP address (kept for a maximum of 48 hours). This is only a number, never linked to a profile, name or account, and never shared with third parties.',
    h_accounts='Accounts',
    accounts_text='The app requires no account, login or registration.',
    h_contact='Contact',
    contact_text='Questions about this policy? Email <a href="mailto:nimco@nentjes.nl">nimco@nentjes.nl</a>.',
),
'de': dict(
    eyebrow='Datenschutz', title='Datenschutzerklärung — 2R', updated='Zuletzt aktualisiert: August 2026',
    intro='2R (Arbeitstitel: MapsInfo) ist eine Reiseführer-App, die während der Fahrt, beim Radfahren oder Wandern gesprochene Geschichten über die Umgebung erzählt. Diese Erklärung beschreibt genau, welche Daten die App verwendet und warum — ohne Kleingedrucktes.',
    h_location='Standort',
    location_items=[
        'Dein GPS-Standort wird verwendet, um zu bestimmen, welche Geschichten relevant sind.',
        '<strong>Standardmäßig wird dein Standort nicht gespeichert und nicht protokolliert.</strong> Jede Anfrage an den Server enthält nur den Namen und Kontext eines bestimmten Ortes — kein Standortverlauf, keine Fahrtenaufzeichnung.',
        '<strong>Erweiterte Protokolle sind ein Opt-in für unser Testteam.</strong> Nur wenn du es selbst aktivierst (freigeschaltet mit einem Diagnose-Code, den wir mit unseren festen Testern teilen), erfassen wir mehr — einschließlich deiner GPS-Position, Fahrtrichtung und Geschwindigkeit im Moment der Geschichtenerstellung — um Fehler aufzuspüren und die App zu verbessern. Das ist standardmäßig aus, gilt nur solange du es aktiviert hast, wird nie an Dritte weitergegeben und kann jederzeit wieder ausgeschaltet werden.',
    ],
    h_stories='Geschichten &amp; Sprache (Auftragsverarbeiter)',
    stories_items=[
        'Um Geschichten zu generieren, senden wir Ortsnamen und kurzen Kontext an <strong>Google (Gemini API)</strong>.',
        'Um den Text vorzulesen, wird dieser Text zur Sprachsynthese an <strong>ElevenLabs</strong> gesendet.',
        'Sachinformationen werden direkt von deinem Gerät aus bei <strong>Wikipedia</strong> abgerufen, Routendaten bei <strong>OpenStreetMap / OSRM</strong> — diese Anfragen laufen nicht über unseren Server.',
        'Generierte Geschichten und Audiofragmente werden vorübergehend zwischengespeichert (wiederverwendet für andere Nutzer am selben Ort), um Kosten und Wartezeit zu verringern.',
    ],
    h_limits='Nutzungsgrenzen',
    limits_text='Um Missbrauch zu verhindern, führen wir pro IP-Adresse einen technischen, temporären Zähler (maximal 48 Stunden gespeichert). Das ist ausschließlich eine Zahl, nie mit einem Profil, Namen oder Konto verknüpft, und wird nie an Dritte weitergegeben.',
    h_accounts='Konten',
    accounts_text='Die App erfordert kein Konto, keine Anmeldung und keine Registrierung.',
    h_contact='Kontakt',
    contact_text='Fragen zu dieser Erklärung? Schreib an <a href="mailto:nimco@nentjes.nl">nimco@nentjes.nl</a>.',
),
'fr': dict(
    eyebrow='Confidentialité', title='Politique de confidentialité — 2R', updated='Dernière mise à jour : août 2026',
    intro="2R (nom de travail : MapsInfo) est une application de guide de voyage qui raconte à voix haute ce qui vous entoure pendant que vous conduisez, roulez à vélo ou marchez. Cette politique explique précisément quelles données l'application utilise, et pourquoi — sans petits caractères.",
    h_location='Localisation',
    location_items=[
        'Votre position GPS est utilisée pour déterminer quelles histoires sont pertinentes.',
        "<strong>Par défaut, votre position n'est jamais stockée ni journalisée.</strong> Chaque requête envoyée au serveur ne contient que le nom et le contexte d'un lieu précis — pas d'historique de localisation, pas de suivi de trajet.",
        "<strong>La journalisation étendue est une option (opt-in) pour notre équipe de test.</strong> Ce n'est que si vous l'activez vous-même (déverrouillée par un code de diagnostic que nous partageons avec nos testeurs réguliers) que nous enregistrons davantage — dont votre position GPS, votre direction et votre vitesse au moment où une histoire est générée — afin de repérer les erreurs et d'améliorer l'application. C'est désactivé par défaut, ne s'applique que tant que vous l'avez activé, n'est jamais partagé avec des tiers, et peut être désactivé à tout moment.",
    ],
    h_stories='Histoires et voix (sous-traitants)',
    stories_items=[
        'Pour générer les histoires, nous envoyons les noms de lieux et un court contexte à <strong>Google (API Gemini)</strong>.',
        'Pour lire le texte à voix haute, ce texte est envoyé à <strong>ElevenLabs</strong> pour la synthèse vocale.',
        'Les informations factuelles sont récupérées directement depuis votre appareil sur <strong>Wikipédia</strong>, et les données d\'itinéraire via <strong>OpenStreetMap / OSRM</strong> — ces requêtes ne passent jamais par notre serveur.',
        'Les histoires générées et les fragments audio sont mis en cache temporairement (réutilisés pour d\'autres utilisateurs au même endroit) afin de réduire les coûts et le temps d\'attente.',
    ],
    h_limits="Limites d'utilisation",
    limits_text="Pour prévenir les abus, nous conservons un compteur technique temporaire par adresse IP (conservé 48 heures maximum). Il ne s'agit que d'un nombre, jamais lié à un profil, un nom ou un compte, et jamais partagé avec des tiers.",
    h_accounts='Comptes',
    accounts_text="L'application ne nécessite aucun compte, connexion ni inscription.",
    h_contact='Contact',
    contact_text='Des questions sur cette politique ? Écrivez à <a href="mailto:nimco@nentjes.nl">nimco@nentjes.nl</a>.',
),
'es': dict(
    eyebrow='Privacidad', title='Política de privacidad — 2R', updated='Última actualización: agosto de 2026',
    intro='2R (nombre provisional: MapsInfo) es una app de guía de viaje que narra en voz alta lo que te rodea mientras conduces, pedaleas o caminas. Esta política explica con precisión qué datos usa la app y por qué — sin letra pequeña.',
    h_location='Ubicación',
    location_items=[
        'Tu ubicación GPS se usa para determinar qué historias son relevantes.',
        '<strong>Por defecto, tu ubicación nunca se almacena ni se registra.</strong> Cada solicitud al servidor contiene solo el nombre y el contexto de un lugar concreto — sin historial de ubicación, sin registro de trayectos.',
        '<strong>El registro ampliado es opcional (opt-in) para nuestro equipo de pruebas.</strong> Solo si lo activas tú mismo (desbloqueado con un código de diagnóstico que compartimos con nuestros testers habituales) registramos más información — incluida tu posición GPS, dirección y velocidad en el momento de generar una historia — para detectar errores y mejorar la app. Está desactivado por defecto, solo se aplica mientras lo tengas activado, nunca se comparte con terceros y puedes desactivarlo en cualquier momento.',
    ],
    h_stories='Historias y voz (encargados del tratamiento)',
    stories_items=[
        'Para generar historias enviamos nombres de lugares y contexto breve a <strong>Google (API de Gemini)</strong>.',
        'Para narrar el texto en voz alta, ese texto se envía a <strong>ElevenLabs</strong> para la síntesis de voz.',
        'La información factual se obtiene directamente desde tu dispositivo en <strong>Wikipedia</strong>, y los datos de ruta desde <strong>OpenStreetMap / OSRM</strong> — estas solicitudes nunca pasan por nuestro servidor.',
        'Las historias generadas y los fragmentos de audio se almacenan en caché temporalmente (reutilizados para otros usuarios en el mismo lugar) para reducir el coste y el tiempo de espera.',
    ],
    h_limits='Límites de uso',
    limits_text='Para prevenir abusos mantenemos un contador técnico y temporal por dirección IP (conservado un máximo de 48 horas). Es solo un número, nunca vinculado a un perfil, nombre o cuenta, y nunca se comparte con terceros.',
    h_accounts='Cuentas',
    accounts_text='La app no requiere ninguna cuenta, inicio de sesión ni registro.',
    h_contact='Contacto',
    contact_text='¿Preguntas sobre esta política? Escribe a <a href="mailto:nimco@nentjes.nl">nimco@nentjes.nl</a>.',
),
'pt': dict(
    eyebrow='Privacidade', title='Política de Privacidade — 2R', updated='Última atualização: agosto de 2026',
    intro='O 2R (nome provisório: MapsInfo) é um app de guia de viagem que narra em voz alta o que está à sua volta enquanto você dirige, pedala ou caminha. Esta política explica exatamente quais dados o app usa e por quê — sem letras miúdas.',
    h_location='Localização',
    location_items=[
        'Sua localização GPS é usada para determinar quais histórias são relevantes.',
        '<strong>Por padrão, sua localização nunca é armazenada nem registrada.</strong> Cada solicitação ao servidor contém apenas o nome e o contexto de um local específico — sem histórico de localização, sem registro de trajetos.',
        '<strong>O registro ampliado é opcional (opt-in) para a nossa equipe de testes.</strong> Só se você mesmo ativar (desbloqueado com um código de diagnóstico que compartilhamos com nossos testadores habituais) registramos mais informações — incluindo sua posição GPS, direção e velocidade no momento em que uma história é gerada — para identificar erros e melhorar o app. Fica desativado por padrão, só se aplica enquanto você o mantiver ativado, nunca é compartilhado com terceiros e pode ser desativado a qualquer momento.',
    ],
    h_stories='Histórias e voz (operadores)',
    stories_items=[
        'Para gerar histórias, enviamos nomes de locais e um breve contexto para o <strong>Google (API Gemini)</strong>.',
        'Para narrar o texto em voz alta, esse texto é enviado à <strong>ElevenLabs</strong> para síntese de voz.',
        'Informações factuais são obtidas diretamente do seu dispositivo na <strong>Wikipédia</strong>, e dados de rota via <strong>OpenStreetMap / OSRM</strong> — essas solicitações nunca passam pelo nosso servidor.',
        'Histórias geradas e fragmentos de áudio ficam em cache temporariamente (reutilizados para outros usuários no mesmo local) para reduzir custo e tempo de espera.',
    ],
    h_limits='Limites de uso',
    limits_text='Para evitar abusos, mantemos um contador técnico e temporário por endereço IP (guardado por no máximo 48 horas). Isso é apenas um número, nunca vinculado a um perfil, nome ou conta, e nunca compartilhado com terceiros.',
    h_accounts='Contas',
    accounts_text='O app não exige conta, login ou registro.',
    h_contact='Contato',
    contact_text='Dúvidas sobre esta política? Escreva para <a href="mailto:nimco@nentjes.nl">nimco@nentjes.nl</a>.',
),
}

# ---------------------------------------------------------------------------
# De "rijd een stukje mee"-sectie op de homepage: vier windstreken van
# Europa, elk met een eigen scène-foto die meebeweegt met de tekst terwijl
# je scrollt (net als het gekozen Codex-voorbeeld). Per taal: lijst van
# (regio, tijd, kop, tekst); de afbeelding is per windstreek hetzelfde
# volgnummer in alle talen (zie EUROPE_IMAGES).
# ---------------------------------------------------------------------------
EUROPE_IMAGES = ['europe-north-norway.jpg', 'europe-west-france.jpg', 'europe-east-czechia.jpg', 'europe-south-italy.jpg']

EUROPE_STOPS = {
'nl': [
    ('Noord · Sognefjord, Noorwegen', '06:50 · Langs het fjord', 'De ochtend begint waar de bergen het water raken.', 'Route vertelt hoe het ijs hier de weg heeft voorbereid — duizenden jaren voordat wij hem konden rijden.'),
    ('West · Bourgogne, Frankrijk', '13:20 · Na de regen', 'Een abdij verschijnt tussen de platanen.', 'Geen ansichtkaart, maar een dorp dat nog altijd leeft rond stenen die al generaties verhalen bewaren.'),
    ('Oost · Zuid-Bohemen, Tsjechië', '09:10 · Door de ochtendmist', 'De toren maakt van de horizon een hoofdstuk.', 'De vorm van de spits verraadt een geschiedenis die vanuit Wenen naar deze kleine heuvelstad reisde.'),
    ('Zuid · Puglia, Italië', '19:12 · Tussen de olijfbomen', 'Het avondlicht brengt iedereen even tot stilte.', 'Dan vertelt Route hoe mensen, steen en bomen hier al eeuwen leren leven met hitte, droogte en elkaar.'),
],
'en': [
    ('North · Sognefjord, Norway', '06:50 · Along the fjord', 'The morning begins where the mountains meet the water.', 'Route tells how the ice shaped this road — thousands of years before we could ever drive it.'),
    ('West · Burgundy, France', '13:20 · After the rain', 'An abbey appears between the plane trees.', 'Not a postcard, but a village that still lives around stones that have kept stories for generations.'),
    ('East · South Bohemia, Czechia', '09:10 · Through the morning mist', 'The tower turns the horizon into a chapter.', 'The shape of the spire reveals a history that travelled from Vienna to this small hilltop town.'),
    ('South · Puglia, Italy', '19:12 · Among the olive trees', 'The evening light brings everyone to a brief stillness.', 'Then Route tells how people, stone and trees have learned to live here for centuries — with heat, drought and each other.'),
],
'de': [
    ('Norden · Sognefjord, Norwegen', '06:50 · Entlang des Fjords', 'Der Morgen beginnt dort, wo die Berge das Wasser berühren.', 'Route erzählt, wie das Eis diesen Weg vorbereitet hat — Jahrtausende bevor wir ihn befahren konnten.'),
    ('Westen · Burgund, Frankreich', '13:20 · Nach dem Regen', 'Eine Abtei erscheint zwischen den Platanen.', 'Keine Postkarte, sondern ein Dorf, das noch immer um Steine herum lebt, die seit Generationen Geschichten bewahren.'),
    ('Osten · Südböhmen, Tschechien', '09:10 · Durch den Morgennebel', 'Der Turm macht den Horizont zu einem Kapitel.', 'Die Form der Turmspitze verrät eine Geschichte, die von Wien bis in dieses kleine Hügelstädtchen reiste.'),
    ('Süden · Apulien, Italien', '19:12 · Zwischen den Olivenbäumen', 'Das Abendlicht bringt alle für einen Moment zur Ruhe.', 'Dann erzählt Route, wie Menschen, Stein und Bäume hier seit Jahrhunderten lernen, mit Hitze, Trockenheit und einander zu leben.'),
],
'fr': [
    ('Nord · Sognefjord, Norvège', '06 h 50 · Le long du fjord', "Le matin commence là où les montagnes rencontrent l'eau.", "Route raconte comment la glace a façonné cette route — des millénaires avant que nous puissions la parcourir."),
    ('Ouest · Bourgogne, France', '13 h 20 · Après la pluie', 'Une abbaye apparaît entre les platanes.', "Pas une carte postale, mais un village qui vit encore autour de pierres gardiennes d'histoires depuis des générations."),
    ('Est · Bohême du Sud, Tchéquie', '09 h 10 · Dans la brume matinale', "La tour transforme l'horizon en chapitre.", "La forme de la flèche trahit une histoire qui a voyagé de Vienne jusqu'à cette petite ville sur la colline."),
    ('Sud · Pouilles, Italie', '19 h 12 · Entre les oliviers', "La lumière du soir apaise chacun, l'espace d'un instant.", "Route raconte alors comment les habitants, la pierre et les arbres apprennent ici depuis des siècles à vivre avec la chaleur, la sécheresse et les uns les autres."),
],
'es': [
    ('Norte · Sognefjord, Noruega', '06:50 · A lo largo del fiordo', 'La mañana empieza donde las montañas tocan el agua.', 'Route cuenta cómo el hielo preparó esta carretera —miles de años antes de que pudiéramos recorrerla.'),
    ('Oeste · Borgoña, Francia', '13:20 · Después de la lluvia', 'Una abadía aparece entre los plátanos.', 'No es una postal, sino un pueblo que aún vive alrededor de piedras que guardan historias desde hace generaciones.'),
    ('Este · Bohemia del Sur, Chequia', '09:10 · Entre la niebla matinal', 'La torre convierte el horizonte en un capítulo.', 'La forma de la aguja delata una historia que viajó desde Viena hasta esta pequeña ciudad en la colina.'),
    ('Sur · Apulia, Italia', '19:12 · Entre los olivos', 'La luz del atardecer trae a todos, por un momento, la calma.', 'Entonces Route cuenta cómo las personas, la piedra y los árboles llevan siglos aprendiendo a convivir aquí con el calor, la sequía y los unos con los otros.'),
],
'pt': [
    ('Norte · Sognefjord, Noruega', '06:50 · Ao longo do fiorde', 'A manhã começa onde as montanhas tocam a água.', 'A Route conta como o gelo preparou esta estrada — milhares de anos antes de podermos percorrê-la.'),
    ('Oeste · Borgonha, França', '13:20 · Depois da chuva', 'Uma abadia aparece entre os plátanos.', 'Não é um cartão-postal, mas uma vila que ainda vive em torno de pedras que guardam histórias há gerações.'),
    ('Leste · Boêmia do Sul, Tchéquia', '09:10 · Através da névoa da manhã', 'A torre transforma o horizonte num capítulo.', 'A forma da torre revela uma história que viajou de Viena até esta pequena cidade na colina.'),
    ('Sul · Apúlia, Itália', '19:12 · Entre as oliveiras', 'A luz da tarde traz a todos, por um instante, quietude.', 'Então a Route conta como pessoas, pedra e árvores aprendem aqui há séculos a conviver com o calor, a seca e uns com os outros.'),
],
}

# ---------------------------------------------------------------------------
# "Vijf steden, vijf stemmen": redactionele showcase op de homepage van wat
# Route zou kunnen vertellen — illustratief, dus bewust los van het echte,
# feitelijk gecontroleerde verhalen-archief (STORIES/dat leeft onder /stories/).
# Per taal: lijst van (categorie, plaats, titel, tekst); image via CITY_IMAGES.
# ---------------------------------------------------------------------------
CITY_IMAGES = ['city-amsterdam.jpg', 'city-paris.jpg', 'city-vienna.jpg', 'city-rome.jpg', 'city-lisbon.jpg']

CITY_STORIES = {
'nl': [
    ('Water & handel', 'Amsterdam, Nederland', 'De stad die haar straten van water maakte', 'Langs de grachten vertelt Route hoe kooplieden, ambachtslieden en nieuwkomers samen een wereldstad bouwden op palen en vertrouwen.'),
    ('Stad & revolutie', 'Parijs, Frankrijk', 'De boulevard die een oude stad opnieuw leerde ademen', 'Voorbij het natte trottoir hoor je waarom Parijs werd opengebroken — en hoe brede lanen het leven, de macht en de ontmoeting veranderden.'),
    ('Muziek & architectuur', 'Wenen, Oostenrijk', 'Waar iedere gevel het ritme van een rijk bewaart', 'Een tram schuift langs de Ringstraße. Route laat horen hoe hofcultuur, koffiehuizen en muziek nog altijd in het dagelijkse Wenen meeklinken.'),
    ('Geschiedenis & leven', 'Rome, Italië', 'Een stad die nooit op één tijdstip leeft', 'Achter een scooter verschijnen tempelzuilen en woonhuizen. In Rome liggen het oude rijk en het gewone leven niet naast, maar door elkaar.'),
    ('Zee & verlangen', 'Lissabon, Portugal', 'De heuvels die altijd naar de oceaan kijken', 'Terwijl de straat naar de Taag afdaalt, vertelt Route over ontdekkingsreizen, aardbevingen en het Portugese verlangen naar wat achter de horizon ligt.'),
],
'en': [
    ('Water & trade', 'Amsterdam, Netherlands', 'The city that made its streets from water', 'Along the canals, Route tells how merchants, craftspeople and newcomers built a world city together — on piles and on trust.'),
    ('City & revolution', 'Paris, France', 'The boulevard that taught an old city to breathe again', 'Beyond the wet pavement you hear why Paris was cut open — and how wide avenues changed life, power and encounter.'),
    ('Music & architecture', 'Vienna, Austria', 'Where every façade keeps the rhythm of an empire', 'A tram glides along the Ringstraße. Route lets you hear how court culture, coffeehouses and music still echo through everyday Vienna.'),
    ('History & life', 'Rome, Italy', 'A city that never lives in just one era', "Behind a scooter, temple columns and apartment blocks appear. In Rome, the old empire and everyday life don't sit side by side — they run through each other."),
    ('Sea & longing', 'Lisbon, Portugal', 'The hills that always look toward the ocean', 'As the street descends toward the Tagus, Route tells of voyages of discovery, earthquakes, and the Portuguese longing for what lies beyond the horizon.'),
],
'de': [
    ('Wasser & Handel', 'Amsterdam, Niederlande', 'Die Stadt, die ihre Straßen aus Wasser baute', 'Entlang der Grachten erzählt Route, wie Kaufleute, Handwerker und Neuankömmlinge gemeinsam eine Weltstadt bauten — auf Pfählen und auf Vertrauen.'),
    ('Stadt & Revolution', 'Paris, Frankreich', 'Der Boulevard, der eine alte Stadt neu atmen lehrte', 'Jenseits des nassen Bürgersteigs hörst du, warum Paris aufgebrochen wurde — und wie breite Alleen das Leben, die Macht und die Begegnung veränderten.'),
    ('Musik & Architektur', 'Wien, Österreich', 'Wo jede Fassade den Rhythmus eines Reiches bewahrt', 'Eine Straßenbahn gleitet die Ringstraße entlang. Route lässt hören, wie Hofkultur, Kaffeehäuser und Musik noch immer im Wiener Alltag mitschwingen.'),
    ('Geschichte & Leben', 'Rom, Italien', 'Eine Stadt, die nie in nur einer Zeit lebt', 'Hinter einem Motorroller erscheinen Tempelsäulen und Wohnhäuser. In Rom liegen das alte Reich und der Alltag nicht nebeneinander, sondern ineinander.'),
    ('Meer & Sehnsucht', 'Lissabon, Portugal', 'Die Hügel, die immer zum Ozean blicken', 'Während die Straße zum Tejo hinabführt, erzählt Route von Entdeckungsreisen, Erdbeben und der portugiesischen Sehnsucht nach dem, was hinter dem Horizont liegt.'),
],
'fr': [
    ('Eau & commerce', 'Amsterdam, Pays-Bas', "La ville qui a fait ses rues avec de l'eau", "Le long des canaux, Route raconte comment marchands, artisans et nouveaux venus ont bâti ensemble une ville-monde — sur des pieux, et sur la confiance."),
    ('Ville & révolution', 'Paris, France', "Le boulevard qui a réappris à une vieille ville à respirer", "Au-delà du trottoir mouillé, on entend pourquoi Paris fut éventrée — et comment de larges avenues ont changé la vie, le pouvoir et la rencontre."),
    ('Musique & architecture', 'Vienne, Autriche', "Où chaque façade garde le rythme d'un empire", "Un tram glisse le long du Ring. Route fait entendre comment la culture de cour, les cafés et la musique résonnent encore dans le Vienne quotidien."),
    ('Histoire & vie', 'Rome, Italie', 'Une ville qui ne vit jamais à une seule époque', "Derrière un scooter apparaissent des colonnes de temple et des immeubles. À Rome, l'ancien empire et la vie quotidienne ne sont pas côte à côte, mais entremêlés."),
    ('Mer & désir', 'Lisbonne, Portugal', "Les collines qui regardent toujours vers l'océan", "Tandis que la rue descend vers le Tage, Route raconte les voyages de découverte, les tremblements de terre et le désir portugais pour ce qui se trouve au-delà de l'horizon."),
],
'es': [
    ('Agua y comercio', 'Ámsterdam, Países Bajos', 'La ciudad que construyó sus calles con agua', 'A lo largo de los canales, Route cuenta cómo comerciantes, artesanos y recién llegados construyeron juntos una ciudad global —sobre pilotes y sobre la confianza.'),
    ('Ciudad y revolución', 'París, Francia', 'El bulevar que enseñó a respirar de nuevo a una ciudad antigua', 'Más allá de la acera mojada se oye por qué se abrió París en canal —y cómo las grandes avenidas cambiaron la vida, el poder y el encuentro.'),
    ('Música y arquitectura', 'Viena, Austria', 'Donde cada fachada guarda el ritmo de un imperio', 'Un tranvía se desliza por el Ring. Route deja oír cómo la cultura de corte, los cafés y la música aún resuenan en el día a día vienés.'),
    ('Historia y vida', 'Roma, Italia', 'Una ciudad que nunca vive en una sola época', 'Detrás de una vespa aparecen columnas de templos y bloques de viviendas. En Roma, el imperio antiguo y la vida cotidiana no están uno junto al otro, sino entrelazados.'),
    ('Mar y anhelo', 'Lisboa, Portugal', 'Las colinas que siempre miran hacia el océano', 'Mientras la calle desciende hacia el Tajo, Route habla de viajes de descubrimiento, terremotos y el anhelo portugués por lo que hay más allá del horizonte.'),
],
'pt': [
    ('Água e comércio', 'Amsterdã, Países Baixos', 'A cidade que fez suas ruas de água', 'Ao longo dos canais, a Route conta como mercadores, artesãos e recém-chegados construíram juntos uma cidade global — sobre estacas e sobre confiança.'),
    ('Cidade e revolução', 'Paris, França', 'O boulevard que ensinou uma cidade antiga a respirar de novo', 'Além da calçada molhada, ouve-se por que Paris foi reaberta — e como largas avenidas mudaram a vida, o poder e o encontro.'),
    ('Música e arquitetura', 'Viena, Áustria', 'Onde cada fachada guarda o ritmo de um império', 'Um bonde desliza pela Ringstraße. A Route deixa ouvir como a cultura da corte, os cafés e a música ainda ecoam no dia a dia vienense.'),
    ('História e vida', 'Roma, Itália', 'Uma cidade que nunca vive numa única época', 'Atrás de uma vespa aparecem colunas de templos e prédios residenciais. Em Roma, o antigo império e a vida cotidiana não ficam lado a lado, mas entrelaçados.'),
    ('Mar e desejo', 'Lisboa, Portugal', 'As colinas que sempre olham para o oceano', 'Enquanto a rua desce em direção ao Tejo, a Route conta sobre viagens de descobrimento, terremotos e o desejo português por aquilo que está além do horizonte.'),
],
}

# ---------------------------------------------------------------------------
# Roadmap-items: (status_key, title-dict, desc-dict)  status: live/testflight/soon/later
# ---------------------------------------------------------------------------
ROADMAP_ITEMS = [
    ('live', dict(nl='AI-verhalen uit lokale bronnen', en='AI stories from local sources', de='KI-Geschichten aus lokalen Quellen', fr='Histoires IA à partir de sources locales', es='Historias de IA a partir de fuentes locales', pt='Histórias de IA a partir de fontes locais'),
     dict(nl="Live gegenereerd per locatie, met voorrang voor gemeentesites, VVV's en erfgoedorganisaties — niet alleen Wikipedia.",
          en='Generated live per location, prioritising municipal sites, tourism boards and heritage organisations — not just Wikipedia.',
          de='Live pro Standort generiert, mit Priorität für Gemeindeseiten, Tourismusverbände und Denkmalorganisationen — nicht nur Wikipedia.',
          fr='Générées en direct par lieu, en privilégiant les sites municipaux, offices de tourisme et organisations patrimoniales — pas seulement Wikipédia.',
          es='Generadas en vivo por ubicación, priorizando webs municipales, oficinas de turismo y organizaciones patrimoniales —no solo Wikipedia.',
          pt='Geradas ao vivo por localização, priorizando sites municipais, órgãos de turismo e organizações de patrimônio — não só a Wikipédia.')),
    ('live', dict(nl='Expressieve vertelstem', en='Expressive narration voice', de='Ausdrucksstarke Erzählstimme', fr='Voix narrative expressive', es='Voz narrativa expresiva', pt='Voz narrativa expressiva'),
     dict(nl='Een warme, natuurlijke stem — met zuchtjes, lachjes en spontane spreektaal in plaats van een robotstem.',
          en='A warm, natural voice — with sighs, laughter and natural speech, instead of a robotic one.',
          de='Eine warme, natürliche Stimme — mit Seufzern, Lachen und spontaner Sprache statt einer Roboterstimme.',
          fr='Une voix chaleureuse et naturelle — avec soupirs, rires et langage spontané, au lieu d\'une voix robotique.',
          es='Una voz cálida y natural —con suspiros, risas y habla espontánea en lugar de una voz robótica.',
          pt='Uma voz calorosa e natural — com suspiros, risadas e fala espontânea, em vez de uma voz robótica.')),
    ('live', dict(nl='Gidsmodus', en='Guide mode', de='Guide-Modus', fr='Mode guide', es='Modo guía', pt='Modo guia'),
     dict(nl='Eén doorlopend verhaal met het gebied als rode draad — land, provincie, streek, plaats — in plaats van losse verhaaltjes per plek.',
          en='One continuous story with the region as its through-line — country, province, area, town — instead of disconnected snippets per location.',
          de='Eine durchgehende Geschichte mit der Region als rotem Faden — Land, Provinz, Gegend, Ort — statt einzelner Schnipsel pro Standort.',
          fr='Un récit continu avec la région comme fil conducteur — pays, province, terroir, ville — plutôt que des fragments isolés par lieu.',
          es='Una historia continua con la región como hilo conductor —país, provincia, comarca, localidad— en lugar de fragmentos sueltos por ubicación.',
          pt='Uma história contínua com a região como fio condutor — país, província, região, cidade — em vez de fragmentos isolados por local.')),
    ('live', dict(nl='Werkt in heel Europa', en='Works across Europe', de='Funktioniert in ganz Europa', fr="Fonctionne dans toute l'Europe", es='Funciona en toda Europa', pt='Funciona em toda a Europa'),
     dict(nl='In het buitenland wordt de lokale Wikipedia gebruikt (Italiaans, Frans, Duits...) en in jouw taal naverteld.',
          en='Abroad, the local Wikipedia is used (Italian, French, German…) and retold in your own language.',
          de='Im Ausland wird die lokale Wikipedia genutzt (Italienisch, Französisch, Deutsch…) und in deiner Sprache nacherzählt.',
          fr='À l\'étranger, la Wikipédia locale est utilisée (italien, français, allemand…) et racontée dans votre propre langue.',
          es='En el extranjero se usa la Wikipedia local (italiano, francés, alemán…) y se cuenta en tu propio idioma.',
          pt='No exterior, a Wikipédia local é usada (italiano, francês, alemão…) e recontada no seu próprio idioma.')),
    ('live', dict(nl='Negen interesses, en je eigen', en='Nine interests, and your own', de='Neun Interessen, und deine eigenen', fr='Neuf centres d\'intérêt, et les vôtres', es='Nueve intereses, y los tuyos', pt='Nove interesses, e os seus'),
     dict(nl='Geschiedenis, natuur, kunst, sport, eten & drinken en meer — plus een vrij invoerveld voor elke andere interesse.',
          en='History, nature, art, sport, food & drink and more — plus a free-text field for any other interest.',
          de='Geschichte, Natur, Kunst, Sport, Essen & Trinken und mehr — plus ein Freitextfeld für jedes andere Interesse.',
          fr='Histoire, nature, art, sport, gastronomie et plus — plus un champ libre pour tout autre centre d\'intérêt.',
          es='Historia, naturaleza, arte, deporte, gastronomía y más —además de un campo libre para cualquier otro interés.',
          pt='História, natureza, arte, desporto, gastronomia e mais — além de um campo livre para qualquer outro interesse.')),
    ('testflight', dict(nl='De iOS-app', en='The iOS app', de='Die iOS-App', fr="L'app iOS", es='La app de iOS', pt='O app iOS'),
     dict(nl='2R draait als echte iPhone-app in besloten test, met eigen 2R-icoon en achtergrond-locatie.',
          en='2R runs as a real iPhone app in closed testing, with its own 2R icon and background location.',
          de='2R läuft als echte iPhone-App im geschlossenen Test, mit eigenem 2R-Icon und Standort im Hintergrund.',
          fr='2R fonctionne comme une vraie app iPhone en test fermé, avec sa propre icône 2R et la localisation en arrière-plan.',
          es='2R funciona como una app real de iPhone en pruebas cerradas, con su propio icono 2R y ubicación en segundo plano.',
          pt='O 2R funciona como um app real de iPhone em teste fechado, com ícone próprio e localização em segundo plano.')),
    ('soon', dict(nl='Verhalen van reizigers', en='Traveler stories', de='Geschichten von Reisenden', fr='Histoires de voyageurs', es='Historias de viajeros', pt='Histórias de viajantes'),
     dict(nl='Mensen die hun eigen streek kennen kunnen zelf verhalen toevoegen — getypt of ingesproken — met naamsvermelding en menselijke goedkeuring vooraf.',
          en='People who know their own region can add their own stories — typed or recorded — with attribution and human approval before publishing.',
          de='Menschen, die ihre eigene Region kennen, können eigene Geschichten hinzufügen — getippt oder aufgenommen — mit Namensnennung und menschlicher Freigabe vor der Veröffentlichung.',
          fr='Les personnes qui connaissent leur propre région peuvent ajouter leurs propres histoires — écrites ou enregistrées — avec attribution et validation humaine avant publication.',
          es='Las personas que conocen su propia región pueden añadir sus propias historias —escritas o grabadas— con atribución y aprobación humana antes de publicarse.',
          pt='Pessoas que conhecem sua própria região podem adicionar suas próprias histórias — digitadas ou gravadas — com atribuição e aprovação humana antes da publicação.')),
    ('soon', dict(nl='Reismuziek van 2R zelf', en='Road music from 2R itself', de='Reisemusik von 2R selbst', fr='Musique de voyage de 2R', es='Música de viaje de 2R', pt='Música de viagem do próprio 2R'),
     dict(nl='Naast je eigen muziek kan 2R straks ook zelf passende reismuziek tussen de verhalen laten spelen. Welk genre dat is, bepaal je zelf — reismuziek is voor iedereen iets persoonlijks.',
          en='Beyond your own music, 2R will also be able to play fitting road music of its own between the stories. Which genre is up to you — road music is personal.',
          de='Neben deiner eigenen Musik kann 2R künftig auch selbst passende Reisemusik zwischen den Geschichten abspielen. Welches Genre, entscheidest du selbst — Reisemusik ist etwas Persönliches.',
          fr="En plus de votre propre musique, 2R pourra bientôt diffuser lui-même une musique de voyage adaptée entre les récits. Le genre, c'est vous qui le choisissez — la musique de voyage est personnelle.",
          es='Además de tu propia música, 2R podrá reproducir también su propia música de viaje entre las historias. Qué género, lo eliges tú: la música de viaje es algo personal.',
          pt='Além da sua própria música, o 2R poderá tocar também a sua própria música de viagem entre as histórias. O género escolhe você — música de viagem é algo pessoal.')),
    ('soon', dict(nl='Handsfree spraakfeedback', en='Hands-free voice feedback', de='Freihändiges Sprach-Feedback', fr='Retour vocal mains libres', es='Comentarios por voz manos libres', pt='Feedback por voz sem usar as mãos'),
     dict(nl='"Dat klopt niet", "vertel meer" of "vijf minuten stil" — allemaal via spraak, want de bestuurder raakt de telefoon niet aan.',
          en='"That\'s not right", "tell me more" or "five minutes of quiet" — all by voice, because the driver never touches the phone.',
          de='„Das stimmt nicht", „erzähl mehr" oder „fünf Minuten Ruhe" — alles per Sprache, denn der Fahrer berührt das Telefon nie.',
          fr='« Ce n\'est pas exact », « dis-m\'en plus » ou « cinq minutes de silence » — tout à la voix, car le conducteur ne touche jamais le téléphone.',
          es='"Eso no es correcto", "cuéntame más" o "cinco minutos de silencio" —todo por voz, porque quien conduce nunca toca el teléfono.',
          pt='"Isso não está certo", "conte mais" ou "cinco minutos de silêncio" — tudo por voz, porque quem dirige nunca toca no telefone.')),
    ('testflight', dict(nl='Achtergrond-audio, met je eigen muziek eronder', en='Background audio, with your own music underneath', de='Hintergrund-Audio, mit deiner eigenen Musik darunter', fr='Audio en arrière-plan, avec votre musique en dessous', es='Audio en segundo plano, con tu propia música debajo', pt='Áudio em segundo plano, com a sua música por baixo'),
     dict(nl='Route vertelt door met het scherm uit of je navigatie-app ervoor, en je eigen muziek (Spotify, radio, podcast) duikt vanzelf zachtjes weg zodra de verteller begint — en zwelt weer aan als het verhaal klaar is.',
          en='Route keeps narrating with the screen off or your navigation app in front, and your own music (Spotify, radio, podcast) automatically ducks the moment the narrator starts — and swells back when the story ends.',
          de='Route erzählt weiter bei ausgeschaltetem Bildschirm oder mit deiner Navi-App im Vordergrund, und deine eigene Musik (Spotify, Radio, Podcast) wird automatisch leiser, sobald der Erzähler beginnt — und schwillt wieder an, wenn die Geschichte endet.',
          fr="Route continue de raconter écran éteint ou avec votre app de navigation devant, et votre musique (Spotify, radio, podcast) baisse automatiquement dès que le narrateur commence — puis remonte quand l'histoire se termine.",
          es='Route sigue narrando con la pantalla apagada o tu app de navegación delante, y tu propia música (Spotify, radio, podcast) baja automáticamente en cuanto empieza el narrador — y vuelve a subir cuando termina la historia.',
          pt='A Route continua narrando com a tela desligada ou seu app de navegação à frente, e a sua música (Spotify, rádio, podcast) baixa automaticamente assim que o narrador começa — e volta a subir quando a história termina.')),
    ('soon', dict(nl='Familie-modus met spelletjes', en='Family mode with games', de='Familienmodus mit Spielen', fr='Mode famille avec des jeux', es='Modo familiar con juegos', pt='Modo família com jogos'),
     dict(nl='Content voor de hele auto, met quizjes en spelletjes onderweg.',
          en='Content for the whole car, with quizzes and games for the road.',
          de='Inhalte für das ganze Auto, mit Quiz und Spielen für unterwegs.',
          fr='Du contenu pour toute la voiture, avec des quiz et des jeux pour la route.',
          es='Contenido para todo el coche, con quizzes y juegos para el camino.',
          pt='Conteúdo para todo o carro, com quizzes e jogos para a estrada.')),
    ('later', dict(nl='Partnervermeldingen', en='Partner listings', de='Partner-Einträge', fr='Mentions partenaires', es='Menciones de socios', pt='Menções de parceiros'),
     dict(nl="Restaurants, musea en attracties die — altijd duidelijk gelabeld — een vermelding kunnen krijgen op hun locatie.",
          en='Restaurants, museums and attractions can get a clearly labelled mention at their location.',
          de='Restaurants, Museen und Attraktionen können eine klar gekennzeichnete Erwähnung an ihrem Standort erhalten.',
          fr='Restaurants, musées et attractions peuvent obtenir une mention clairement identifiée à leur emplacement.',
          es='Restaurantes, museos y atracciones pueden obtener una mención claramente etiquetada en su ubicación.',
          pt='Restaurantes, museus e atrações podem receber uma menção claramente identificada em seu local.')),
    ('later', dict(nl='Android', en='Android', de='Android', fr='Android', es='Android', pt='Android'),
     dict(nl='Dezelfde app, gebouwd voor Android — zelfde codebasis, zelfde ervaring.',
          en='The same app, built for Android — same codebase, same experience.',
          de='Dieselbe App, gebaut für Android — gleiche Codebasis, gleiches Erlebnis.',
          fr='La même application, conçue pour Android — même base de code, même expérience.',
          es='La misma app, creada para Android —misma base de código, misma experiencia.',
          pt='O mesmo app, criado para Android — mesma base de código, mesma experiência.')),
    ('later', dict(nl='CarPlay & Android Auto', en='CarPlay & Android Auto', de='CarPlay & Android Auto', fr='CarPlay & Android Auto', es='CarPlay y Android Auto', pt='CarPlay e Android Auto'),
     dict(nl='2R als audio-app naast je navigatie op het autoscherm.',
          en='2R as an audio app alongside your navigation on the car display.',
          de='2R als Audio-App neben deiner Navigation auf dem Autodisplay.',
          fr="2R comme application audio à côté de votre navigation sur l'écran de la voiture.",
          es='2R como app de audio junto a tu navegación en la pantalla del coche.',
          pt='O 2R como app de áudio junto à sua navegação na tela do carro.')),
]

# ---------------------------------------------------------------------------
# ROADMAP als filmische reis in vier hoofdstukken (herbouw 29 aug, Codex-briefing).
# De items hierboven blijven de bron van waarheid; hieronder alleen de nieuwe
# redactionele omlijsting (hero, hoofdstuktitels, slot). Statuslabels komen uit
# SITE[lang] (rm_live/rm_testflight/rm_soon/rm_later) en worden per hoofdstuk
# één keer getoond.
# ---------------------------------------------------------------------------
RM_HERO = dict(
    eyebrow=dict(nl='Roadmap · Waar de weg begon', en='Roadmap · Where the road began',
                 de='Roadmap · Wo der Weg begann', fr='Feuille de route · Où la route a commencé',
                 es='Hoja de ruta · Donde empezó el camino', pt='Roteiro · Onde a estrada começou'),
    h1=dict(nl='We zijn pas net vertrokken.', en="We've only just set off.",
            de='Wir sind gerade erst aufgebrochen.', fr='Nous venons à peine de partir.',
            es='Acabamos de ponernos en marcha.', pt='Mal partimos.'),
    lede=dict(
        nl='2R begon als een idee tijdens een autorit. Onderweg viel er zoveel te zien, maar niemand om het uit te leggen. Dit is wat er sindsdien is gebouwd — en wat er achter de volgende bocht op ons wacht.',
        en="2R started as an idea during a road trip. There was so much to see along the way, and no one to explain it. Here's what's been built since — and what's waiting around the next bend.",
        de='2R begann als Idee während einer Autofahrt. Unterwegs gab es so viel zu sehen, aber niemanden, der es erklärte. Das wurde seitdem gebaut — und das wartet hinter der nächsten Kurve auf uns.',
        fr="2R est né d'une idée pendant un road trip. Il y avait tant à voir en chemin, et personne pour l'expliquer. Voici ce qui a été construit depuis — et ce qui nous attend au prochain tournant.",
        es='2R nació como una idea durante un viaje en coche. Había tanto que ver en el camino, y nadie para explicarlo. Esto es lo que se ha construido desde entonces — y lo que nos espera a la vuelta de la próxima curva.',
        pt='O 2R começou como uma ideia durante uma viagem de carro. Havia tanto para ver pelo caminho, e ninguém para explicar. Isto é o que foi construído desde então — e o que nos espera depois da próxima curva.'),
)

RM_CHAPTERS = [
    dict(num='01', status='live',
         title=dict(nl='Al onderweg', en='Already on the road', de='Schon unterwegs',
                    fr='Déjà en route', es='Ya en camino', pt='Já a caminho'),
         sub=dict(nl='Dit reist vandaag al met je mee.', en='This is already traveling with you today.',
                  de='Das reist heute schon mit dir mit.', fr="Ceci voyage déjà avec vous aujourd'hui.",
                  es='Esto ya viaja hoy contigo.', pt='Isto já viaja com você hoje.')),
    dict(num='02', status='testflight',
         title=dict(nl='Nu de weg op', en='Onto the road now', de='Jetzt auf die Straße',
                    fr='Sur la route maintenant', es='Ahora a la carretera', pt='Agora na estrada'),
         sub=dict(nl='Dit wordt nu buiten de werkplaats getest.', en='This is being tested outside the workshop now.',
                  de='Das wird jetzt außerhalb der Werkstatt getestet.', fr="Ceci est maintenant testé hors de l'atelier.",
                  es='Esto se está probando ahora fuera del taller.', pt='Isto já está sendo testado fora da oficina.')),
    dict(num='03', status='soon',
         title=dict(nl='Achter de volgende bocht', en='Around the next bend', de='Hinter der nächsten Kurve',
                    fr='Au prochain tournant', es='A la vuelta de la próxima curva', pt='Depois da próxima curva'),
         sub=dict(nl='Dit ligt achter de eerstvolgende bocht.', en='This lies just around the next bend.',
                  de='Das liegt gleich hinter der nächsten Kurve.', fr='Ceci se trouve juste au prochain tournant.',
                  es='Esto está justo a la vuelta de la próxima curva.', pt='Isto está logo depois da próxima curva.')),
    dict(num='04', status='later',
         title=dict(nl='Aan de horizon', en='On the horizon', de='Am Horizont',
                    fr="À l'horizon", es='En el horizonte', pt='No horizonte'),
         sub=dict(nl='Dit zien we verderop aan de horizon.', en='This is further off, on the horizon.',
                  de='Das sehen wir weiter draußen am Horizont.', fr="Ceci se profile plus loin, à l'horizon.",
                  es='Esto se ve más adelante, en el horizonte.', pt='Isto está mais adiante, no horizonte.')),
]

RM_CLOSE = dict(
    eyebrow=dict(nl='Aan de horizon', en='On the horizon', de='Am Horizont',
                 fr="À l'horizon", es='En el horizonte', pt='No horizonte'),
    h=dict(nl='Rijd mee aan het vervolg.', en="Ride along for what's next.",
           de='Fahr mit ins nächste Kapitel.', fr='Faites route avec nous pour la suite.',
           es='Acompáñanos en lo que viene.', pt='Venha junto para o que vem a seguir.'),
    p=dict(
        nl='Als tester, lokale verteller of partner — of gewoon omdat je net zo benieuwd bent naar wat er achter de volgende bocht ligt als wij.',
        en="As a tester, a local storyteller or a partner — or simply because you're as curious about what's around the next bend as we are.",
        de='Als Tester, lokaler Erzähler oder Partner — oder einfach, weil du genauso neugierig bist wie wir, was hinter der nächsten Kurve liegt.',
        fr="Comme testeur, conteur local ou partenaire — ou simplement parce que vous êtes aussi curieux que nous de ce qu'il y a au prochain tournant.",
        es='Como probador, narrador local o socio — o simplemente porque tienes tanta curiosidad como nosotros por lo que hay a la vuelta de la próxima curva.',
        pt='Como testador, narrador local ou parceiro — ou simplesmente porque você está tão curioso quanto nós para saber o que há depois da próxima curva.'),
    btn=dict(nl='Neem contact op', en='Get in touch', de='Kontakt aufnehmen',
             fr='Prenez contact', es='Ponte en contacto', pt='Entre em contato'),
)

RM_ALT = dict(
    open=dict(
        nl='Open reisjournaal op schoot tijdens een autorit naar een Europees dorp.',
        en='Open travel journal on a lap during a car ride toward a European village.',
        de='Aufgeschlagenes Reisetagebuch auf dem Schoß während einer Autofahrt zu einem europäischen Dorf.',
        fr="Carnet de voyage ouvert sur les genoux pendant un trajet en voiture vers un village européen.",
        es='Diario de viaje abierto sobre el regazo durante un trayecto en coche hacia un pueblo europeo.',
        pt='Diário de viagem aberto no colo durante um trajeto de carro rumo a uma vila europeia.'),
    close=dict(
        nl='Twee reizigers kijken vanuit de auto uit over een weg naar de horizon.',
        en='Two travelers look out from the car over a road toward the horizon.',
        de='Zwei Reisende blicken aus dem Auto über eine Straße zum Horizont.',
        fr="Deux voyageurs regardent depuis la voiture une route vers l'horizon.",
        es='Dos viajeros miran desde el coche una carretera hacia el horizonte.',
        pt='Dois viajantes olham do carro para uma estrada rumo ao horizonte.'),
)

# ---------------------------------------------------------------------------
# VERHALEN — echte, tijdens het testen gegenereerde en gecheckte verhalen
# ---------------------------------------------------------------------------
STORIES = [
    dict(slug='villa-horev-bilthoven', category='geschiedenis', location='Bilthoven, Nederland', date='15 augustus 2026',
         source_label='Wikipedia — Horev (Bilthoven)', source_url='https://nl.wikipedia.org/?curid=397649',
         title=dict(nl='Villa Horev', en='Villa Horev', de='Villa Horev', fr='Villa Horev', es='Villa Horev', pt='Villa Horev'),
         text=dict(
            nl="Kijk eens naar Villa Horev, hier op de hoek van de Soestdijkseweg Zuid en de Boslaan. De naam is een prachtig acroniem voor Hoop Op Rust En Vrede. Die rust zocht de eerste bewoner, de heer Reijsenbach, na zijn jaren als president van de Javasche Bank in voormalig Nederlands-Indië. Rond negentienhonderd trokken veel welgestelde repatrianten naar de gezonde bossen van Bilthoven.",
            en="Look at Villa Horev, here on the corner of Soestdijkseweg Zuid and Boslaan. The name is a beautiful acronym for \"Hope for Rest and Peace.\" That rest is what the first resident, Mr Reijsenbach, was seeking after his years as president of the Javasche Bank in what was then the Dutch East Indies. Around 1900, many wealthy returnees moved to the healthy woodlands of Bilthoven.",
            de="Schau dir Villa Horev an, hier an der Ecke Soestdijkseweg Zuid und Boslaan. Der Name ist ein schönes Akronym für „Hoffnung auf Ruhe und Frieden“. Diese Ruhe suchte der erste Bewohner, Herr Reijsenbach, nach seinen Jahren als Präsident der Javasche Bank im damaligen Niederländisch-Ostindien. Um 1900 zogen viele wohlhabende Rückkehrer in die gesunden Wälder von Bilthoven.",
            fr="Regardez la Villa Horev, ici à l'angle de la Soestdijkseweg Zuid et de la Boslaan. Le nom est un bel acronyme pour « Espoir de Repos et de Paix ». C'est ce repos que recherchait le premier habitant, M. Reijsenbach, après ses années en tant que président de la Javasche Bank dans les anciennes Indes orientales néerlandaises. Vers 1900, de nombreux rapatriés fortunés s'installèrent dans les forêts salubres de Bilthoven.",
            es="Mira la Villa Horev, aquí en la esquina de Soestdijkseweg Zuid y Boslaan. El nombre es un bonito acrónimo de «Esperanza de Descanso y Paz». Ese descanso era lo que buscaba el primer residente, el señor Reijsenbach, tras sus años como presidente del Banco de Java en las antiguas Indias Orientales Neerlandesas. Hacia 1900, muchos repatriados adinerados se trasladaron a los saludables bosques de Bilthoven.",
            pt="Olhe para a Villa Horev, aqui na esquina da Soestdijkseweg Zuid com a Boslaan. O nome é um belo acrônimo para \"Esperança de Descanso e Paz\". Foi esse descanso que o primeiro morador, o Sr. Reijsenbach, buscou após seus anos como presidente do Banco de Java nas então Índias Orientais Holandesas. Por volta de 1900, muitos repatriados abastados se mudaram para as saudáveis florestas de Bilthoven.")),
    dict(slug='dvsu-timber-broers', category='sport', location='De Bilt, Nederland', date='17 augustus 2026',
         source_label='Wikipedia — DVSU', source_url='https://nl.wikipedia.org/wiki/DVSU',
         title=dict(nl='Voetbalclub DVSU en de gebroeders Timber', en='Football club DVSU and the Timber brothers', de='Fußballverein DVSU und die Timber-Brüder', fr='Le club de football DVSU et les frères Timber', es='El club de fútbol DVSU y los hermanos Timber', pt='O clube de futebol DVSU e os irmãos Timber'),
         text=dict(
            nl="Aan je linkerhand, op een paar honderd meter afstand, ligt een brok pure voetbalhistorie: de amateurclub DVSU. Die afkorting staat voor Door Vriendschap Sterk Utrecht. Hier in De Bilt en omgeving begon het allemaal in negentienhonderdtweeëndertig. Moet je horen: zelfs de bekende voetbaltweeling Jurriën en Quinten Timber zette hier ooit hun eerste stappen op het veld! Van modderige weitjes tot de kweekvijver van internationals.",
            en="On your left, a few hundred metres away, lies a piece of pure football history: the amateur club DVSU. The name stands for \"United Through Friendship, Utrecht.\" It all began here in De Bilt and the surrounding area back in 1932. Here's the thing: even the well-known football twins Jurriën and Quinten Timber once took their first steps on this pitch! From muddy fields to a breeding ground for internationals.",
            de="Zu deiner Linken, ein paar hundert Meter entfernt, liegt ein Stück reine Fußballgeschichte: der Amateurverein DVSU. Der Name steht für „Durch Freundschaft stark, Utrecht“. Hier in De Bilt und Umgebung fing alles neunzehnhundertzweiunddreißig an. Hör mal zu: sogar die bekannten Fußball-Zwillinge Jurriën und Quinten Timber machten hier einst ihre ersten Schritte auf dem Platz! Von matschigen Wiesen zur Talentschmiede für Nationalspieler.",
            fr="Sur votre gauche, à quelques centaines de mètres, se trouve un morceau de pure histoire du football : le club amateur DVSU. Ce nom signifie « Unis par l'amitié, Utrecht ». Tout a commencé ici, à De Bilt et ses environs, en mille neuf cent trente-deux. Écoutez ceci : même les célèbres jumeaux du football Jurriën et Quinten Timber ont fait leurs premiers pas sur ce terrain ! De prairies boueuses à véritable vivier d'internationaux.",
            es="A tu izquierda, a unos cientos de metros, se encuentra un pedazo de pura historia del fútbol: el club amateur DVSU. El nombre significa «Unidos por la Amistad, Utrecht». Todo comenzó aquí, en De Bilt y sus alrededores, en mil novecientos treinta y dos. Escucha esto: ¡hasta los conocidos gemelos del fútbol Jurriën y Quinten Timber dieron aquí sus primeros pasos en el campo! De prados embarrados a auténtico semillero de internacionales.",
            pt="À sua esquerda, a poucas centenas de metros, está um pedaço de pura história do futebol: o clube amador DVSU. O nome significa \"Unidos pela Amizade, Utrecht\". Tudo começou aqui, em De Bilt e arredores, em mil novecentos e trinta e dois. Escute só: até os conhecidos gêmeos do futebol Jurriën e Quinten Timber deram aqui os seus primeiros passos em campo! De campos enlameados a verdadeiro celeiro de jogadores internacionais.")),
    dict(slug='chiesa-santi-pietro-paolo-luino', category='architectuur', location='Luino, Italië', date='17 augustus 2026',
         source_label='luino.va.it', source_url='https://www.luino.va.it/',
         title=dict(nl='De parochiekerk van Luino', en='The parish church of Luino', de='Die Pfarrkirche von Luino', fr='L\'église paroissiale de Luino', es='La iglesia parroquial de Luino', pt='A igreja paroquial de Luino'),
         text=dict(
            nl="Kijk eens hoe statig de parochiekerk van de Heilige Petrus en Paulus opdoemt in het hart van Luino. Wat je nu ziet, is het meesterwerk van de lokale architect Natale Pugnetti, die dit heiligdom rond achttienhonderdveertig voltooide in een harmonieuze, laat-neoklassieke stijl. Let op de indrukwekkende voorgevel met zijn vier klassieke Dorische zuilen die rust en orde uitstralen. Binnen ontvouwt zich een monumentaal Latijns kruis met elegante tongewelven.",
            en="Look how stately the parish church of Saints Peter and Paul rises in the heart of Luino. What you're seeing is the masterpiece of local architect Natale Pugnetti, who completed this sanctuary around 1840 in a harmonious, late-neoclassical style. Notice the impressive facade with its four classical Doric columns radiating calm and order. Inside, a monumental Latin cross unfolds with elegant barrel vaults.",
            de="Schau, wie stattlich die Pfarrkirche der Heiligen Petrus und Paulus im Herzen von Luino aufragt. Was du siehst, ist das Meisterwerk des lokalen Architekten Natale Pugnetti, der dieses Heiligtum um achtzehnhundertvierzig in einem harmonischen, spätklassizistischen Stil vollendete. Beachte die beeindruckende Fassade mit ihren vier klassischen dorischen Säulen, die Ruhe und Ordnung ausstrahlen. Im Inneren entfaltet sich ein monumentales lateinisches Kreuz mit eleganten Tonnengewölben.",
            fr="Regardez comme l'église paroissiale des Saints Pierre et Paul s'élève majestueusement au cœur de Luino. Ce que vous voyez là est le chef-d'œuvre de l'architecte local Natale Pugnetti, qui acheva ce sanctuaire vers mille huit cent quarante dans un style néoclassique tardif et harmonieux. Remarquez l'imposante façade avec ses quatre colonnes doriques classiques dégageant calme et ordre. À l'intérieur se déploie une croix latine monumentale aux élégantes voûtes en berceau.",
            es="Mira qué majestuosa se alza la iglesia parroquial de San Pedro y San Pablo en el corazón de Luino. Lo que ves es la obra maestra del arquitecto local Natale Pugnetti, que completó este santuario hacia mil ochocientos cuarenta en un estilo neoclásico tardío y armonioso. Fíjate en la impresionante fachada con sus cuatro columnas dóricas clásicas que irradian calma y orden. En el interior se despliega una monumental cruz latina con elegantes bóvedas de cañón.",
            pt="Veja como se ergue majestosa a igreja paroquial de São Pedro e São Paulo no coração de Luino. O que você está vendo é a obra-prima do arquiteto local Natale Pugnetti, que concluiu este santuário por volta de mil oitocentos e quarenta num estilo neoclássico tardio e harmonioso. Repare na imponente fachada com suas quatro colunas dóricas clássicas que irradiam calma e ordem. No interior desdobra-se uma monumental cruz latina com elegantes abóbadas de berço.")),
    dict(slug='kasteel-nijenrode-breukelen', category='geschiedenis', location='Breukelen, Nederland', date='18 augustus 2026',
         source_label='Wikipedia — Kasteel Nijenrode', source_url='https://nl.wikipedia.org/wiki/Kasteel_Nijenrode',
         title=dict(nl='Kasteel Nijenrode', en='Nijenrode Castle', de='Schloss Nijenrode', fr='Le château de Nijenrode', es='El castillo de Nijenrode', pt='O castelo de Nijenrode'),
         text=dict(
            nl="Een kleine vijfhonderd meter van onze route vandaan, verscholen in de bossen aan het water, ligt het échte icoon van deze hoek: Kasteel Nijenrode. Gesticht rond twaalfhonderdvijfenzeventig door Gerard Splinter van Ruwiel en door de eeuwen heen getekend door oorlog, vlammen en wederopbouw. Hollandse meesters zoals Salomon van Ruysdael legden de weerspiegeling van die trotse torens al vast op doek. Tegenwoordig gonst er een heel andere energie als universiteit, maar de eeuwenoude ophaalbruggen ademen nog puur ridderverleden.",
            en="Just under five hundred metres from our route, tucked away in the woods by the water, lies the true icon of this corner: Nijenrode Castle. Founded around 1275 by Gerard Splinter van Ruwiel and shaped over the centuries by war, fire and rebuilding. Dutch masters such as Salomon van Ruysdael captured the reflection of those proud towers on canvas long ago. Today a very different energy hums through it as a university, but the centuries-old drawbridges still breathe pure knightly history.",
            de="Knapp fünfhundert Meter von unserer Route entfernt, versteckt in den Wäldern am Wasser, liegt das wahre Wahrzeichen dieser Ecke: Schloss Nijenrode. Gegründet um zwölfhundertfünfundsiebzig von Gerard Splinter van Ruwiel und über die Jahrhunderte geprägt von Krieg, Feuer und Wiederaufbau. Holländische Meister wie Salomon van Ruysdael hielten die Spiegelung dieser stolzen Türme schon lange auf Leinwand fest. Heute pulsiert dort als Universität eine ganz andere Energie, doch die jahrhundertealten Zugbrücken atmen noch reine Rittervergangenheit.",
            fr="À moins de cinq cents mètres de notre itinéraire, niché dans les bois au bord de l'eau, se trouve la véritable icône de ce coin : le château de Nijenrode. Fondé vers mille deux cent soixante-quinze par Gerard Splinter van Ruwiel et façonné au fil des siècles par la guerre, le feu et la reconstruction. Des maîtres hollandais comme Salomon van Ruysdael ont depuis longtemps capturé sur toile le reflet de ces tours fières. Aujourd'hui, une tout autre énergie y règne en tant qu'université, mais les pont-levis séculaires respirent encore un pur passé chevaleresque.",
            es="A menos de quinientos metros de nuestra ruta, escondido en los bosques junto al agua, se encuentra el verdadero icono de este rincón: el castillo de Nijenrode. Fundado hacia mil doscientos setenta y cinco por Gerard Splinter van Ruwiel y marcado a lo largo de los siglos por la guerra, el fuego y la reconstrucción. Maestros holandeses como Salomon van Ruysdael ya plasmaron en lienzo el reflejo de esas orgullosas torres. Hoy vibra allí una energía muy distinta como universidad, pero los puentes levadizos centenarios aún respiran puro pasado caballeresco.",
            pt="A pouco menos de quinhentos metros da nossa rota, escondido nos bosques junto à água, está o verdadeiro ícone deste canto: o castelo de Nijenrode. Fundado por volta de mil duzentos e setenta e cinco por Gerard Splinter van Ruwiel e moldado ao longo dos séculos por guerra, fogo e reconstrução. Mestres holandeses como Salomon van Ruysdael já registraram em tela o reflexo dessas torres orgulhosas. Hoje pulsa ali uma energia bem diferente como universidade, mas as pontes levadiças centenárias ainda respiram puro passado de cavaleiros.")),
    dict(slug='daan-boom-utrecht', category='mensen', location='Utrecht, Nederland', date='17 augustus 2026',
         source_label='Wikipedia — Daan Boom', source_url='https://nl.wikipedia.org/wiki/Daan_Boom',
         title=dict(nl='Daan Boom, Utrechts mediatalent', en='Daan Boom, Utrecht media talent', de='Daan Boom, Medientalent aus Utrecht', fr='Daan Boom, talent médiatique d\'Utrecht', es='Daan Boom, talento mediático de Utrecht', pt='Daan Boom, talento midiático de Utrecht'),
         text=dict(
            nl="Utrecht staat natuurlijk bekend om zijn vissersverleden en klederdracht, maar het is evengoed de ultieme bakermat van Nederlandse smaakmakers en publiekslievelingen. Denk aan Daan Boom, geboren en getogen in de stad, die zijn carrière begon als kinderster en uitgroeide tot een waar media-icoon met het programma Streetlab. Lang voordat sociale media bestonden, wisten ze hier al hoe je een publiek inpakt.",
            en="Utrecht is of course known for its fishing heritage and traditional dress, but it's just as much the ultimate birthplace of Dutch trendsetters and public darlings. Take Daan Boom, born and raised in the city, who started his career as a child star and grew into a true media icon with the show Streetlab. Long before social media existed, people here already knew how to win over an audience.",
            de="Utrecht ist natürlich bekannt für seine Fischereivergangenheit und Trachten, aber genauso ist es die ultimative Geburtsstätte niederländischer Trendsetter und Publikumslieblinge. Denk an Daan Boom, geboren und aufgewachsen in der Stadt, der seine Karriere als Kinderstar begann und mit der Sendung Streetlab zu einer wahren Medienikone wurde. Lange bevor es soziale Medien gab, wusste man hier schon, wie man ein Publikum für sich gewinnt.",
            fr="Utrecht est bien sûr connue pour son passé de pêche et ses costumes traditionnels, mais c'est tout autant le berceau ultime des tendances et des chouchous du public néerlandais. Prenez Daan Boom, né et élevé dans la ville, qui a commencé sa carrière comme enfant star et est devenu une véritable icône médiatique avec l'émission Streetlab. Bien avant l'existence des réseaux sociaux, on savait déjà ici comment conquérir un public.",
            es="Utrecht es conocida, por supuesto, por su pasado pesquero y sus trajes tradicionales, pero es igualmente la cuna definitiva de las tendencias y los favoritos del público neerlandés. Fíjate en Daan Boom, nacido y criado en la ciudad, que comenzó su carrera como estrella infantil y se convirtió en un verdadero icono mediático con el programa Streetlab. Mucho antes de que existieran las redes sociales, aquí ya sabían cómo cautivar a un público.",
            pt="Utrecht é conhecida, claro, pelo seu passado de pesca e trajes tradicionais, mas é igualmente o berço definitivo de tendências e queridinhos do público holandês. Veja o caso de Daan Boom, nascido e criado na cidade, que começou a carreira como estrela mirim e se tornou um verdadeiro ícone da mídia com o programa Streetlab. Muito antes de existirem as redes sociais, já se sabia por aqui como conquistar um público.")),
    dict(slug='loenderveense-plas', category='natuur', location='Wijdemeren, Nederland', date='17 augustus 2026',
         source_label='Wikipedia — Loenderveense Plas', source_url='https://nl.wikipedia.org/wiki/Loenderveense_Plas',
         title=dict(nl='De Loenderveense Plas', en='Loenderveense Plas', de='Der Loenderveense Plas', fr='Le Loenderveense Plas', es='El Loenderveense Plas', pt='O Loenderveense Plas'),
         text=dict(
            nl="Hier in Wijdemeren rij je door een landschap dat letterlijk door mensenhanden is gevormd. Vroeger werd hier op grote schaal turf gewonnen, waardoor diepe veenplassen ontstonden. Even van de snelweg af, op bijna twee kilometer afstand, ligt de Loenderveense Plas. Het water is er zó schoon en stil, omdat het deels dienstdoet als drinkwaterbekken en afgesloten is voor pleziervaart. Daardoor broeden er zeldzame vogels in de rietkragen, zoals de schuwe woudaap en de purperreiger.",
            en="Here in Wijdemeren you're driving through a landscape literally shaped by human hands. Peat was once extracted here on a large scale, creating deep peat lakes. Just off the motorway, almost two kilometres away, lies the Loenderveense Plas. The water there is so clean and still because part of it serves as a drinking-water reservoir and is closed to recreational boating. As a result, rare birds nest in the reed beds, such as the shy little bittern and the purple heron.",
            de="Hier in Wijdemeren fährst du durch eine Landschaft, die buchstäblich von Menschenhand geformt wurde. Früher wurde hier im großen Stil Torf abgebaut, wodurch tiefe Moorseen entstanden. Etwas abseits der Autobahn, fast zwei Kilometer entfernt, liegt der Loenderveense Plas. Das Wasser dort ist so klar und still, weil es teilweise als Trinkwasserreservoir dient und für den Freizeitverkehr gesperrt ist. Dadurch brüten seltene Vögel in den Schilfgürteln, wie die scheue Zwergdommel und der Purpurreiher.",
            fr="Ici, à Wijdemeren, vous traversez un paysage littéralement façonné par la main de l'homme. Autrefois, on y extrayait la tourbe à grande échelle, créant de profonds étangs tourbeux. Juste à l'écart de l'autoroute, à près de deux kilomètres, se trouve le Loenderveense Plas. Son eau est si propre et si calme car elle sert en partie de réservoir d'eau potable et est fermée à la navigation de plaisance. Résultat : de rares oiseaux nichent dans les roselières, comme le timide blongios nain et le héron pourpré.",
            es="Aquí, en Wijdemeren, conduces por un paisaje literalmente moldeado por manos humanas. Antiguamente se extraía turba a gran escala, lo que creó profundos lagos de turbera. Justo al salir de la autopista, a casi dos kilómetros, se encuentra el Loenderveense Plas. Sus aguas son tan limpias y tranquilas porque en parte sirven como depósito de agua potable y están cerradas a la navegación recreativa. Por eso anidan allí aves raras entre los cañaverales, como el esquivo avetorillo común y la garza imperial.",
            pt="Aqui em Wijdemeren você atravessa uma paisagem literalmente moldada por mãos humanas. Antigamente, extraía-se turfa aqui em grande escala, criando lagos profundos de turfeira. Logo depois da autoestrada, a quase dois quilômetros, fica o Loenderveense Plas. Suas águas são tão limpas e paradas porque parte delas serve como reservatório de água potável e está fechada à navegação de lazer. Por isso, aves raras nidificam nos canaviais, como o tímido garção-pequeno e a garça-purpúrea.")),
]

# ---------------------------------------------------------------------------
# HTML-bouwstenen
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# "Zo werkt 2R" — praktische handleiding (de app linkt hiernaartoe).
# ---------------------------------------------------------------------------
NAV_HOWTO = {
    'nl': 'Zo werkt het', 'en': 'How it works', 'de': "So geht's",
    'fr': 'Utilisation', 'es': 'Cómo funciona', 'pt': 'Como funciona',
}
HOWTO = {
'nl': dict(
    eyebrow='Zo werkt 2R', title='Zo werkt 2R',
    lede='2R is je reisgezel die vertelt. Je start hem, je rijdt, en onderweg hoor je verhalen over de plekken die je passeert. Hieronder alles wat je moet weten — in een paar minuten.',
    sections=[
        dict(h='🚗 Beginnen', p='Tik in de app op <b>Start de reis</b> en sta je locatie toe. 2R vertelt vanzelf over de plekken die je passeert — geen account, niets vooraf in te stellen.'),
        dict(h='🎵 Samen met je muziek', p='Speel gerust je eigen muziek (Spotify, Apple Music, de radio — wat dan ook). Die gaat automatisch <b>zachter</b> zodra een verhaal begint, en zwelt weer aan als het klaar is. Zet je “Muziektips per streek” aan, dan krijg je onderweg een tik naar passende muziek per gebied. 2R streamt zelf geen muziek.'),
        dict(h='➤ Het blauwe pijltje bovenin', p='Gebruik je ondertussen Maps of je muziek-app, dan toont iOS bovenin een <b>blauw pijltje</b> (➤) dat aangeeft dat 2R je locatie gebruikt. <b>Dat hoort zo</b> — zo blijft 2R doorvertellen op de achtergrond. Tik erop om terug te keren naar 2R.'),
        dict(h='🔊 Je stem kiezen', p='Kies bij <b>Instellingen → Stem</b> je vertelstem en de klank: natuurlijk (rustig en zuinig) of expressief (het meest menselijk, met aarzelingen en zuchtjes). Met “Beluister deze stem” hoor je ’m meteen.'),
        dict(h='🧭 Hoe je reist', p='Vertel 2R of je met de auto, fiets, te voet of de trein gaat. Hij past het tempo en de afstand van de verhalen daarop aan.'),
        dict(h='🎯 Reisquiz voor het gezin', p='Zet de reisquiz aan voor één vraag na elk verhaal. De bijrijder tikt het antwoord aan — met een scorebord per rit.'),
        dict(h='🧪 Stilstaand uitproberen', p='Wil je 2R proberen zonder te rijden? Gebruik de <b>Route Simulator</b> in het menu om een rit na te bootsen.'),
    ],
    cta_h='Klaar om te rijden?', cta_p='2R draait live in TestFlight en op het web.', cta_btn='Probeer 2R →',
),
'en': dict(
    eyebrow='How 2R works', title='How 2R works',
    lede='2R is your travelling companion that tells stories. You start it, you drive, and along the way you hear stories about the places you pass. Here is everything you need to know — in a few minutes.',
    sections=[
        dict(h='🚗 Getting started', p='In the app, tap <b>Start the journey</b> and allow location access. 2R automatically narrates the places you pass — no account, nothing to set up first.'),
        dict(h='🎵 Alongside your music', p='Play your own music (Spotify, Apple Music, the radio — anything). It automatically <b>fades down</b> when a story starts and swells back up when it ends. Turn on “Music tips per region” for a tap toward fitting music along the way. 2R never streams music itself.'),
        dict(h='➤ The blue arrow at the top', p='If you switch to Maps or your music app, iOS shows a small <b>blue arrow</b> (➤) at the top indicating 2R is using your location. <b>This is expected</b> — it lets 2R keep narrating in the background. Tap it to return to 2R.'),
        dict(h='🔊 Choosing your voice', p='Under <b>Settings → Voice</b>, pick your narrating voice and the tone: natural (calm and economical) or expressive (the most human, with hesitations and sighs). “Preview this voice” lets you hear it right away.'),
        dict(h='🧭 How you travel', p='Tell 2R whether you go by car, bike, on foot or by train. It adapts the pace and distance of the stories accordingly.'),
        dict(h='🎯 Travel quiz for the family', p='Turn on the travel quiz for one question after each story. The passenger taps the answer — with a scoreboard per trip.'),
        dict(h='🧪 Try it standing still', p='Want to try 2R without driving? Use the <b>Route Simulator</b> in the menu to simulate a trip.'),
    ],
    cta_h='Ready to drive?', cta_p='2R runs live in TestFlight and on the web.', cta_btn='Try 2R →',
),
}

# "Zo werkt het" als vijf filmische scènes (beelden van Codex, 29 aug).
# Volgorde/beeld gedeeld over alle talen; tekst per taal (nl/en; rest valt op en).
HOWTO_IMAGES = ['howto-01-vertrek.jpg', 'howto-02-onderweg.jpg', 'howto-03-verhaal.jpg', 'howto-04-muziek.jpg', 'howto-05-ritme.jpg']

FAQ_LABEL = {'nl': 'Goed om te weten voor vertrek', 'en': 'Good to know before you go',
             'de': 'Gut zu wissen vor der Abfahrt', 'fr': 'Bon à savoir avant de partir',
             'es': 'Bueno saber antes de salir', 'pt': 'Bom saber antes de partir'}

HOWTO_SCENES = {
'nl': [
    ('Hoofdstuk 01 · Voor je vertrekt', 'Eén knop. Daarna krijgt de wereld buiten een stem.',
     'Start Route voordat je wegrijdt en kies hoe je reist. Terwijl jij rijdt, kijkt Route vooruit en kiest het verhaal dat deze plek betekenis geeft.'),
    ('Hoofdstuk 02 · Onderweg', 'Vanaf hier rijdt de verteller met je mee.',
     'Eén tik en de reis begint. Route volgt je via GPS en zoekt live wat er om je heen te vertellen valt — met voorrang voor lokale bronnen, niet alleen Wikipedia.'),
    ('Hoofdstuk 03 · Het verhaal', 'Route kiest één betekenisvol verhaal.',
     'Geen lijst met weetjes. Per plek één verhaal, rustig verteld, met ruimte voor de weg en voor elkaar — en je hoort waar het vandaan komt.'),
    ('Hoofdstuk 04 · Jouw muziek', 'De muziek zakt. Een stem komt naast je zitten.',
     'Je eigen muziek — Spotify, radio, podcast — duikt vanzelf zachtjes weg zodra de verteller begint, en zwelt weer aan als het verhaal klaar is.'),
    ('Hoofdstuk 05 · Jouw ritme', 'Luisteren, even stil zijn, of samen spelen.',
     'Luister, tik op "stil" als je rust wilt, of speel samen een reisquiz. Jij bepaalt het ritme; Route past zich aan.'),
],
'en': [
    ('Chapter 01 · Before you leave', 'One tap. Then the world outside finds a voice.',
     'Start Route before you set off and choose how you travel. As you drive, Route looks ahead and picks the story that gives this place meaning.'),
    ('Chapter 02 · On the road', 'From here, the narrator rides along with you.',
     'One tap and the journey begins. Route follows your GPS and finds, live, what there is to tell around you — favouring local sources, not just Wikipedia.'),
    ('Chapter 03 · The story', 'Route picks one meaningful story.',
     'Not a list of facts. One story per place, calmly told, with room for the road and for each other — and you hear where it comes from.'),
    ('Chapter 04 · Your music', 'The music softens. A voice sits down beside you.',
     'Your own music — Spotify, radio, podcast — automatically ducks the moment the narrator starts, and swells back up when the story ends.'),
    ('Chapter 05 · Your pace', 'Listen, fall quiet, or play together.',
     'Listen, tap "quiet" when you want a pause, or play a travel quiz together. You set the pace; Route adapts.'),
],
}


def _strip_lead_glyph(s):
    # Verwijder leidende emoji/symbolen + spatie (geen emoji-koppen op de site).
    i = 0
    while i < len(s) and not (s[i].isalnum() or s[i] == '<'):
        i += 1
    return s[i:].lstrip()


def build_howto(lang):
    h = HOWTO.get(lang, HOWTO['en'])
    scenes_data = HOWTO_SCENES.get(lang, HOWTO_SCENES['en'])
    scenes = ''
    for i, (eyebrow, kop, tekst) in enumerate(scenes_data):
        laad = 'fetchpriority="high"' if i == 0 else 'loading="lazy"'
        kt = 'h1' if i == 0 else 'h2'   # de eerste scène draagt de H1 van de pagina
        scenes += f'''  <section class="howto-scene">
    <img class="howto-photo" src="/images/{HOWTO_IMAGES[i]}" alt="{html.escape(kop)}" {laad} decoding="async">
    <div class="hero-shade" aria-hidden="true"></div>
    <div class="hero-content">
      <p class="eyebrow on-photo">{html.escape(eyebrow)}</p>
      <{kt}>{html.escape(kop)}</{kt}>
      <p class="howto-lede">{html.escape(tekst)}</p>
    </div>
  </section>
'''
    faq = ''.join(f'''      <details class="howto-faq">
        <summary>{_strip_lead_glyph(sec['h'])}</summary>
        <p>{sec['p']}</p>
      </details>
''' for sec in h['sections'])
    body = f'''{scenes}  <section class="block"><div class="wrap" style="max-width:720px;">
    <div class="section-label">{FAQ_LABEL.get(lang, FAQ_LABEL['en'])}</div>
    <div class="howto-faq-list">
{faq}    </div>
    <div class="howto-cta">
      <h2>{h['cta_h']}</h2>
      <p>{h['cta_p']}</p>
      <a class="nav-cta" href="https://mapsinfo.roelnentjes.workers.dev">{h['cta_btn']}</a>
    </div>
  </div></section>
'''
    return page_shell(lang, h['title'] + ' — 2R (Second Route)', h['lede'][:150], 'howto', body)

def nav(lang, active):
    s = SITE[lang]
    def link(href, label, key):
        cls = ' class="active"' if key == active else ''
        return f'<a href="{href}"{cls}>{label}</a>'
    others = ''.join(
        f'<a href="/{l}/">{LANG_LABEL[l]}</a>' if l != lang else f'<a href="/{l}/" class="active">{LANG_LABEL[l]}</a>'
        for l in LANGS
    )
    return f'''<header class="site">
  <div class="site-nav">
    <a class="brand" href="/{lang}/">
      <img class="brand-mark" src="/icon-2r.png" alt="2R">
      <span>Second Route</span>
    </a>
    <button class="menu-toggle" id="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-panel" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
    <nav class="nav-links">
      <span class="nav-only-links">
        {link(f'/{lang}/', s['nav_product'], 'product')}
        {link(f'/{lang}/zo-werkt-het.html', NAV_HOWTO[lang], 'howto')}
        {link(f'/{lang}/roadmap.html', s['nav_roadmap'], 'roadmap')}
        {link(f'/{lang}/stories/', s['nav_stories'], 'stories')}
        {link(f'/{lang}/privacy.html', s['nav_privacy'], 'privacy')}
      </span>
      <div class="lang-switch">{others}</div>
      <a class="nav-cta" href="https://mapsinfo.roelnentjes.workers.dev">{s['nav_cta']}</a>
    </nav>
  </div>
  <div class="mobile-panel" id="mobile-panel">
    <div class="mobile-panel-links">
      {link(f'/{lang}/', s['nav_product'], 'product')}
      {link(f'/{lang}/zo-werkt-het.html', NAV_HOWTO[lang], 'howto')}
      {link(f'/{lang}/roadmap.html', s['nav_roadmap'], 'roadmap')}
      {link(f'/{lang}/stories/', s['nav_stories'], 'stories')}
      {link(f'/{lang}/privacy.html', s['nav_privacy'], 'privacy')}
    </div>
    <div class="lang-switch">{others}</div>
    <a class="nav-cta" href="https://mapsinfo.roelnentjes.workers.dev">{s['nav_cta']}</a>
  </div>
</header>
<script>
(function(){{
  var btn = document.getElementById('menu-toggle');
  var panel = document.getElementById('mobile-panel');
  if (!btn || !panel) return;
  btn.addEventListener('click', function(){{
    var open = !panel.classList.contains('open');
    panel.classList.toggle('open', open);
    btn.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }});
  panel.querySelectorAll('a').forEach(function(a){{
    a.addEventListener('click', function(){{
      panel.classList.remove('open');
      btn.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
    }});
  }});
}})();
</script>'''

def footer(lang):
    s = SITE[lang]
    return f'''<footer class="site">
  <div class="footer-grid">
    <a class="footer-brand" href="/{lang}/">
      <img class="brand-mark" src="/icon-2r.png" alt="2R">
      <span>Second Route</span>
    </a>
    <div class="footer-links">
      <a href="/{lang}/roadmap.html">{s['nav_roadmap']}</a>
      <a href="/{lang}/stories/">{s['nav_stories']}</a>
      <a href="/{lang}/privacy.html">{s['nav_privacy']}</a>
      <a href="mailto:nimco@nentjes.nl">{s['footer_contact']}</a>
    </div>
  </div>
  <p class="footer-family">{s['footer_tagline']}</p>
  <p class="footer-credit">{s['footer_credit']} <a href="https://github.com/nentjes/2r-second-route-website">GitHub</a></p>
</footer>'''

def page_shell(lang, title, description, active, body, extra_head=''):
    return f'''<!DOCTYPE html>
<html lang="{HTML_LANG[lang]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="icon" href="/icon-2r.png">
<link rel="apple-touch-icon" href="/icon-2r.png">
<link rel="stylesheet" href="/style.css">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:image" content="/og.jpg">
</head>
<body>
{nav(lang, active)}
<main>
{body}
</main>
{footer(lang)}
{extra_head}
</body>
</html>
'''

def story_card(lang, st):
    s = SITE[lang]
    cat = CATEGORIES[st['category']][lang]
    excerpt = st['text'][lang][:150].rsplit(' ', 1)[0] + '…'
    return f'''<a class="story-card" href="/{lang}/stories/{st['slug']}.html">
  <span class="story-cat">{cat}</span>
  <h3>{html.escape(st['title'][lang])}</h3>
  <p>{html.escape(excerpt)}</p>
  <span class="story-meta">{html.escape(st['location'])}</span>
</a>'''

# Editorial verhaalkaart voor de homepage-showcase (met foto-crop uit de
# moodboard-beelden), i.p.v. de eenvoudige kaart van het volledige archief.
# Redactionele stads-kaart voor de homepage-showcase ("vijf steden, vijf
# stemmen") — schone cover-foto per stad, geen uitsnede-trucje nodig.
CITY_SLUGS = ['amsterdam', 'parijs', 'wenen', 'rome', 'lissabon']
try:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'city_texts.json'), encoding='utf-8') as _ctf:
        CITY_STORY_TEXT = json.load(_ctf)   # slug -> {taal: volledig verhaal}
except Exception:
    CITY_STORY_TEXT = {}


# Volledige stads-verhaalpagina in de filmische homepage-taal: de stadsfoto als
# hero, daaronder het verhaal in een rustige leeskolom. Zo leidt "Route vertelt"
# onder een stad naar HET verhaal van díe stad (wens Roel 29 aug), niet naar de
# app op je huidige plek.
def build_city_story(lang, index):
    s = SITE[lang]
    cat, place, title, teaser = CITY_STORIES[lang][index]
    slug = CITY_SLUGS[index]
    verhaal = (CITY_STORY_TEXT.get(slug) or {}).get(lang) or teaser
    alineas = ''.join(f'<p>{html.escape(p.strip())}</p>' for p in verhaal.split('\n') if p.strip()) or f'<p>{html.escape(verhaal)}</p>'
    body = f'''  <section class="city-hero" style="background-image:url('/images/{CITY_IMAGES[index]}')">
    <div class="hero-shade" aria-hidden="true"></div>
    <div class="hero-content">
      <p class="eyebrow on-photo">{html.escape(cat)} &middot; {html.escape(place)}</p>
      <h1>{html.escape(title)}</h1>
    </div>
  </section>
  <section class="block"><div class="wrap" style="max-width:660px;">
    <p><a href="/{lang}/" style="color:var(--text-faint); text-decoration:none; font-size:14px;">&larr; {html.escape(s['nav_product'])}</a></p>
    <div class="city-story-body">{alineas}</div>
    <p style="margin-top:34px;"><a class="btn-primary" href="https://apps.apple.com/app/id6802613397">{s['invite_btn']} <span>&#8599;</span></a></p>
  </div></section>
'''
    return page_shell(lang, f"{html.escape(title)} — 2R (Second Route)", teaser, 'product', body)


def city_story_card(lang, index):
    cat, place, title, copy = CITY_STORIES[lang][index]
    card_cls = f'story story-{index + 1}'
    return f'''<a class="{card_cls}" href="/{lang}/stad/{CITY_SLUGS[index]}.html">
  <div class="story-photo" style="background-image:url('/images/{CITY_IMAGES[index]}')"></div>
  <div class="story-body">
    <div class="story-topline"><span>{html.escape(cat)}</span><span>{html.escape(place)}</span></div>
    <h3>{html.escape(title)}</h3>
    <p>{html.escape(copy)}</p>
    <span class="story-cta">{SITE[lang]['listen_now']} <span>▶</span></span>
  </div>
</a>'''

# Site-audio (alleen NL-homepage): een filmische introvertelling die begint zodra
# de bezoeker iets aanraakt (browsers staan geluid niet toe vóór interactie), met
# een altijd-zichtbare geluidsknop die 'm direct dempt en de keuze onthoudt.
# Het audiobestand heeft bewust een vaste naam (/audio/2r-intro.mp3): een nieuwe
# muziek/stem-master hoeft alleen dat ene bestand te vervangen — geen code-wijziging.
# Geen emoji/icoon-glyphs (vaste 2route.nl-regel): alleen type + een CSS-golfje.
# Zet op True zodra de DEFINITIEVE muziek/stem-master klaarstaat als
# public/audio/2r-intro.mp3. Zolang False verschijnt de speler NERGENS op de
# live site (Robins proefstem is te jong voor de filmische kwaliteit — 29 aug).
# Go-live: (1) definitieve mp3 op die vaste naam zetten, (2) AUDIO_LIVE = True,
# (3) python3 build.py, (4) npx wrangler deploy.
AUDIO_LIVE = True

SITE_AUDIO_NL = '''
<div id="site-audio" class="site-audio" data-state="uit">
  <audio id="sa-el" src="/audio/2r-intro.mp3" preload="none"></audio>
  <button id="sa-toggle" class="sa-toggle" type="button" aria-pressed="false" title="Geluid aan of uit">
    <span class="sa-wave" aria-hidden="true"><i></i><i></i><i></i></span>
    <span class="sa-label">Geluid uit</span>
  </button>
  <input id="sa-vol" class="sa-vol" type="range" min="0" max="100" value="70" aria-label="Volume">
</div>
<script>
(function () {
  var box = document.getElementById('site-audio');
  var el = document.getElementById('sa-el');
  if (!box || !el) return;
  var toggle = document.getElementById('sa-toggle');
  var label = toggle.querySelector('.sa-label');
  var vol = document.getElementById('sa-vol');
  var MUTE = 'siteAudioMuted', VOL = 'siteAudioVol', GESTART = 'siteAudioGestart';
  function lees(k){ try { return localStorage.getItem(k); } catch (e) { return null; } }
  function schrijf(k, v){ try { localStorage.setItem(k, v); } catch (e) {} }
  var startVol = parseInt(lees(VOL), 10); if (isNaN(startVol)) startVol = 70;
  vol.value = startVol; el.volume = startVol / 100;
  function toon(staat){ box.dataset.state = staat; label.textContent = (staat === 'aan' ? 'Geluid aan' : 'Geluid uit'); toggle.setAttribute('aria-pressed', staat === 'aan' ? 'true' : 'false'); }
  toon('uit');
  function speel(){ el.play().then(function(){ toon('aan'); try { sessionStorage.setItem(GESTART, '1'); } catch (e) {} }).catch(function(){ toon('uit'); }); }
  var gedempt = lees(MUTE) === '1';
  var alGestart = false; try { alGestart = sessionStorage.getItem(GESTART) === '1'; } catch (e) {}
  if (!gedempt && !alGestart) {
    var evs = ['pointerdown', 'keydown', 'scroll', 'touchstart'];
    var start = function (e){ if (e && box.contains(e.target)) return; speel(); af(); };
    var af = function (){ evs.forEach(function (ev){ window.removeEventListener(ev, start, true); }); };
    evs.forEach(function (ev){ window.addEventListener(ev, start, true); });
  }
  el.addEventListener('play', function(){ toon('aan'); });
  el.addEventListener('pause', function(){ toon('uit'); });
  el.addEventListener('ended', function(){ toon('uit'); });
  toggle.addEventListener('click', function (e){
    e.stopPropagation();
    if (el.paused) { schrijf(MUTE, '0'); speel(); }
    else { el.pause(); schrijf(MUTE, '1'); toon('uit'); }
  });
  vol.addEventListener('input', function(){ el.volume = vol.value / 100; schrijf(VOL, vol.value); });
})();
</script>
'''

def build_home(lang):
    s = SITE[lang]
    stops = EUROPE_STOPS[lang]
    steps = f'''<div class="steps">
        <div class="step"><span class="num-badge">I</span><h3>{s['step1_h']}</h3><p>{s['step1_p']}</p></div>
        <div class="step"><span class="num-badge">II</span><h3>{s['step2_h']}</h3><p>{s['step2_p']}</p></div>
        <div class="step"><span class="num-badge">III</span><h3>{s['step3_h']}</h3><p>{s['step3_p']}</p></div>
      </div>'''
    features = f'''<div class="features">
        <div class="feature"><span class="num-mark">I</span><h3>{s['f1_h']}</h3><p>{s['f1_p']}</p></div>
        <div class="feature"><span class="num-mark">II</span><h3>{s['f2_h']}</h3><p>{s['f2_p']}</p></div>
        <div class="feature"><span class="num-mark">III</span><h3>{s['f3_h']}</h3><p>{s['f3_p']}</p></div>
        <div class="feature"><span class="num-mark">IV</span><h3>{s['f4_h']}</h3><p>{s['f4_p']}</p></div>
        <div class="feature"><span class="num-mark">V</span><h3>{s['f5_h']}</h3><p>{s['f5_p']}</p></div>
        <div class="feature"><span class="num-mark">VI</span><h3>{s['f6_h']}</h3><p>{s['f6_p']}</p></div>
      </div>'''
    story_cards = ''.join(city_story_card(lang, i) for i in range(5))

    journey_scenes_html = ''.join(
        f'<div class="journey-scene{" active" if i == 0 else ""}" data-scene="{i}" style="background-image:url(\'/images/{EUROPE_IMAGES[i]}\')"></div>'
        for i in range(len(stops))
    )
    journey_steps_html = ''.join(f'''<article class="journey-step" data-journey-stop="{i}">
          <span>{region}<br>{time}</span>
          <h3>{h}</h3>
          <p>{p}</p>
        </article>''' for i, (region, time, h, p) in enumerate(stops))
    first_region_short = stops[0][0].split(' · ')[-1]

    body = f'''  <section class="hero" id="top">
    <video class="hero-photo" aria-hidden="true" autoplay muted loop playsinline preload="auto" poster="/images/europe-south-italy.jpg">
      <source src="/images/hero-drive-loop.mp4" type="video/mp4">
    </video>
    <div class="hero-shade" aria-hidden="true"></div>
    <div class="hero-content">
      <p class="eyebrow on-photo">{s['hero_eyebrow']}</p>
      <h1>{s['hero_h1']}</h1>
      <p class="hero-lede">{s['hero_lede']}</p>
      <div class="hero-actions">
        <a class="btn-primary" href="https://mapsinfo.roelnentjes.workers.dev">{s['hero_btn_demo']} <span>↗</span></a>
        <a class="text-link" href="#reis">{s['hero_btn_roadmap']} <span>↓</span></a>
      </div>
    </div>
    <div class="hero-caption"><span>{s['hero_caption_coord']}</span><span>{s['hero_caption_note']}</span></div>
  </section>

  <section class="listening" id="luisteren">
    <div class="section-label">{s['listen_label']}</div>
    <div class="listening-copy">
      <h2>{s['listen_h2']}</h2>
      <p>{s['listen_p']}</p>
    </div>
    <div class="audio-experience">
      <div class="audio-halo">
        <span class="play-button">▶</span>
      </div>
      <div class="audio-meta">
        <span>{s['listen_now']}</span>
        <strong>{s['listen_title']}</strong>
        <small>{s['listen_sub']}</small>
      </div>
    </div>
  </section>

  <section class="journey" id="reis">
    <div class="journey-visual" aria-hidden="true">
      <div class="window-frame">
        {journey_scenes_html}
        <span class="window-reflection"></span>
      </div>
      <div class="map-card">
        <span class="lbl">{s['journey_route_label']}</span>
        <strong id="journey-region">{first_region_short}</strong>
        <div class="route-line"><i></i><i></i><i></i></div>
        <span class="lbl">{s['journey_route_meta']}</span>
      </div>
    </div>
    <div class="journey-narrative">
      <div class="section-label">{s['journey_label']}</div>
      {journey_steps_html}
    </div>
  </section>

  <script>
  (function(){{
    var regions = {json.dumps([stop[0].split(' · ')[-1] for stop in stops], ensure_ascii=False)};
    var scenes = document.querySelectorAll('.journey-scene');
    var regionEl = document.getElementById('journey-region');
    var steps = document.querySelectorAll('[data-journey-stop]');
    if (!steps.length || !('IntersectionObserver' in window)) return;
    var observer = new IntersectionObserver(function(entries){{
      entries.forEach(function(entry){{
        if (!entry.isIntersecting) return;
        var idx = Number(entry.target.dataset.journeyStop);
        scenes.forEach(function(sc){{ sc.classList.toggle('active', Number(sc.dataset.scene) === idx); }});
        if (regionEl && regions[idx]) regionEl.textContent = regions[idx];
      }});
    }}, {{ rootMargin: '-32% 0px -52% 0px', threshold: 0 }});
    steps.forEach(function(el){{ observer.observe(el); }});
  }})();
  </script>

  <section class="block" style="padding-bottom:0;"><div class="wrap">
    <div class="section-head"><div class="eyebrow">{s['steps_eyebrow']}</div><h2 style="font-size:clamp(24px,3.4vw,34px);margin-top:14px;">{s['steps_h2']}</h2></div>
    {steps}
    <div class="stat-strip">
      <div class="stat"><div class="num">{s['stat1_num']}</div><div class="lbl">{s['stat1_lbl']}</div></div>
      <div class="stat"><div class="num">{s['stat2_num']}</div><div class="lbl">{s['stat2_lbl']}</div></div>
      <div class="stat"><div class="num">{s['stat3_num']}</div><div class="lbl">{s['stat3_lbl']}</div></div>
      <div class="stat"><div class="num">{s['stat4_num']}</div><div class="lbl">{s['stat4_lbl']}</div></div>
    </div>
  </div></section>

  <section class="block"><div class="wrap">
    <div class="section-head"><div class="eyebrow">{s['why_eyebrow']}</div><h2 style="font-size:clamp(24px,3.4vw,34px);margin-top:14px;">{s['why_h2']}</h2><p>{s['why_p']}</p></div>
    {features}
  </div></section>

  <section class="block" id="verhalen"><div class="wrap">
    <div class="stories-head">
      <div><div class="section-label">{s['stories_eyebrow']}</div><h2>{s['stories_h2']}</h2></div>
      <p>{s['stories_p']}</p>
    </div>
    <div class="story-grid">{story_cards}</div>
    <p style="margin-top:26px;"><a class="text-link on-paper" href="/{lang}/stories/">{s['stories_view_all']} <span>→</span></a></p>
  </div></section>

  <section class="invitation" id="meenemen">
    <div class="invitation-image" aria-hidden="true"></div>
    <div class="invitation-content">
      <p class="eyebrow on-photo">{s['invite_label']}</p>
      <h2>{s['invite_h2']}</h2>
      <p>{s['invite_p']}</p>
      <a class="btn-primary" href="https://apps.apple.com/app/id6802613397">{s['invite_btn']} <span>↗</span></a>
    </div>
  </section>
'''
    title = {'nl': '2R (Second Route) — De reisgezel die vertelt wat je onderweg ziet',
             'en': '2R (Second Route) — The travel companion that narrates what you see',
             'de': '2R (Second Route) — Der Reisebegleiter, der erzählt, was du siehst',
             'fr': '2R (Second Route) — Le compagnon de voyage qui raconte ce que vous voyez',
             'es': '2R (Second Route) — El compañero de viaje que narra lo que ves',
             'pt': '2R (Second Route) — O companheiro de viagem que narra o que você vê'}[lang]
    # Live tellers (testers/verhalen vandaag) zijn van de publieke pagina
    # gehaald: dat was interne telemetrie en liet ongewild de prille schaal
    # zien. De strip toont nu stabiele productfeiten (stat3/stat4 in SITE).
    return page_shell(lang, title, s['hero_lede'].replace('<b>', '').replace('</b>', ''), 'product', body, extra_head=(SITE_AUDIO_NL if (lang == 'nl' and AUDIO_LIVE) else ''))

def build_roadmap(lang):
    s = SITE[lang]
    status_label = {'live': s['rm_live'], 'testflight': s['rm_testflight'], 'soon': s['rm_soon'], 'later': s['rm_later']}
    chapters = ''
    for ch in RM_CHAPTERS:
        st = ch['status']
        items = ''.join(
            f'''<div class="rm-item">
            <h3>{t[lang]}</h3>
            <p>{d[lang]}</p>
          </div>\n'''
            for gkey, t, d in ROADMAP_ITEMS if gkey == st
        )
        chapters += f'''<article class="rm-chapter rm-reveal">
        <div class="rm-chapter-aside">
          <span class="rm-chapter-num">{ch['num']}</span>
          <span class="rm-chapter-status rm-st-{st}">{status_label[st]}</span>
        </div>
        <div class="rm-chapter-main">
          <h2>{ch['title'][lang]}</h2>
          <p class="rm-chapter-sub">{ch['sub'][lang]}</p>
          <div class="rm-items">
          {items}</div>
        </div>
      </article>\n'''
    body = f'''  <section class="rm-hero">
    <img class="rm-hero-img" src="/images/roadmap-01-waar-de-weg-begon.jpg" alt="{RM_ALT['open'][lang]}" width="1536" height="1024" fetchpriority="high">
    <div class="rm-hero-shade" aria-hidden="true"></div>
    <div class="rm-hero-content">
      <p class="eyebrow on-photo">{RM_HERO['eyebrow'][lang]}</p>
      <h1>{RM_HERO['h1'][lang]}</h1>
      <p class="rm-hero-lede">{RM_HERO['lede'][lang]}</p>
    </div>
  </section>

  <section class="rm-route"><div class="wrap">
    {chapters}
  </div></section>

  <section class="rm-close">
    <img class="rm-close-img" src="/images/roadmap-02-aan-de-horizon.jpg" alt="{RM_ALT['close'][lang]}" width="1536" height="1024" loading="lazy">
    <div class="rm-close-shade" aria-hidden="true"></div>
    <div class="rm-close-content rm-reveal">
      <p class="eyebrow on-photo">{RM_CLOSE['eyebrow'][lang]}</p>
      <h2>{RM_CLOSE['h'][lang]}</h2>
      <p class="rm-close-p">{RM_CLOSE['p'][lang]}</p>
      <a class="btn-primary" href="mailto:nimco@nentjes.nl">{RM_CLOSE['btn'][lang]}</a>
    </div>
  </section>
'''
    return page_shell(lang, f"Roadmap — 2R (Second Route)", s['rm_lede'], 'roadmap', body)

# Nieuwe redactionele omlijsting voor de privacypagina (herbouw 29 aug). De
# juridische kernteksten blijven in PRIVACY[lang]; hieronder alleen de rustige
# samenvattingen, tabel en het slot. Faithful vertaald, geen nieuwe claims.
PRIV_EXTRA = {
'nl': dict(
    h1='Jouw reis blijft van jou.', alt='Een telefoon ligt met het scherm naar beneden naast een reisboek en wegenkaart in een geparkeerde auto.',
    lede='2R gebruikt alleen wat nodig is om onderweg het juiste verhaal te vertellen. Geen account, geen rittenregistratie en standaard geen opgeslagen locatie. Hier leggen we precies uit wat er wél gebeurt.',
    promises=[('01', 'Geen account nodig', 'Je hoeft niet in te loggen of je naam achter te laten.'),
              ('02', 'Geen rittenregistratie', 'Standaard bouwen we geen geschiedenis op van waar je bent geweest.'),
              ('03', 'Testlogs alleen met toestemming', 'Uitgebreidere diagnosegegevens staan standaard uit en zijn alleen opt-in.')],
    toc_label='Op deze pagina',
    table_head=('Dienst', 'Waarvoor', 'Welke informatie'),
    table_rows=[('Google / Gemini API', 'verhaal genereren', 'plaatsnaam en korte context'),
                ('ElevenLabs', 'spraak maken', 'tekst van het verhaal'),
                ('Wikipedia', 'feitelijke informatie', 'rechtstreeks verzoek vanaf toestel'),
                ('OpenStreetMap / OSRM', 'kaart en route', 'rechtstreeks verzoek vanaf toestel')],
    note1='Standaard wordt je locatie niet opgeslagen en niet gelogd.',
    note2='Uitgebreide logboeken zijn alleen beschikbaar als opt-in voor het testteam.',
    close_h='Nog een vraag?', close_p='Privacy hoort begrijpelijk te zijn. Als iets niet duidelijk is, horen we het graag.', close_btn='Mail ons',
),
'en': dict(
    h1='Your journey stays yours.', alt='A phone lies face down next to a travel journal and road map in a parked car.',
    lede='2R uses only what it needs to tell the right story along the way. No account, no trip logging and no stored location by default. Here we explain exactly what does happen.',
    promises=[('01', 'No account needed', "You don't need to log in or leave your name."),
              ('02', 'No trip logging', "By default we don't build a history of where you've been."),
              ('03', 'Test logs only with consent', 'More detailed diagnostics are off by default and opt-in only.')],
    toc_label='On this page',
    table_head=('Service', 'What for', 'What information'),
    table_rows=[('Google / Gemini API', 'generate a story', 'place name and brief context'),
                ('ElevenLabs', 'create speech', 'the story text'),
                ('Wikipedia', 'factual information', 'direct request from your device'),
                ('OpenStreetMap / OSRM', 'map and route', 'direct request from your device')],
    note1='By default your location is never stored and never logged.',
    note2='Extended logging is only available as an opt-in for the testing team.',
    close_h='Still have a question?', close_p="Privacy should be understandable. If anything is unclear, we'd like to hear it.", close_btn='Email us',
),
'de': dict(
    h1='Deine Reise bleibt deine.', alt='Ein Telefon liegt mit dem Bildschirm nach unten neben einem Reisetagebuch und einer Straßenkarte in einem geparkten Auto.',
    lede='2R nutzt nur das, was nötig ist, um unterwegs die richtige Geschichte zu erzählen. Kein Konto, keine Fahrtenaufzeichnung und standardmäßig kein gespeicherter Standort. Hier erklären wir genau, was wirklich passiert.',
    promises=[('01', 'Kein Konto nötig', 'Du musst dich nicht anmelden oder deinen Namen hinterlassen.'),
              ('02', 'Keine Fahrtenaufzeichnung', 'Standardmäßig führen wir keine Historie darüber, wo du warst.'),
              ('03', 'Testprotokolle nur mit Zustimmung', 'Ausführlichere Diagnosedaten sind standardmäßig aus und nur per Opt-in.')],
    toc_label='Auf dieser Seite',
    table_head=('Dienst', 'Wofür', 'Welche Informationen'),
    table_rows=[('Google / Gemini API', 'Geschichte erzeugen', 'Ortsname und kurzer Kontext'),
                ('ElevenLabs', 'Sprache erzeugen', 'Text der Geschichte'),
                ('Wikipedia', 'Sachinformationen', 'direkte Anfrage vom Gerät'),
                ('OpenStreetMap / OSRM', 'Karte und Route', 'direkte Anfrage vom Gerät')],
    note1='Standardmäßig wird dein Standort nicht gespeichert und nicht protokolliert.',
    note2='Ausführliche Protokolle gibt es nur als Opt-in für das Testteam.',
    close_h='Noch eine Frage?', close_p='Datenschutz sollte verständlich sein. Wenn etwas unklar ist, hören wir gern davon.', close_btn='Schreib uns',
),
'fr': dict(
    h1='Votre voyage reste le vôtre.', alt="Un téléphone posé écran vers le bas à côté d'un carnet de voyage et d'une carte routière dans une voiture garée.",
    lede="2R n'utilise que ce qui est nécessaire pour raconter la bonne histoire en chemin. Pas de compte, pas d'enregistrement des trajets et, par défaut, aucune localisation conservée. Voici exactement ce qui se passe.",
    promises=[('01', 'Aucun compte nécessaire', 'Pas besoin de vous connecter ni de laisser votre nom.'),
              ('02', 'Aucun enregistrement des trajets', "Par défaut, nous ne conservons pas d'historique de vos déplacements."),
              ('03', 'Journaux de test seulement avec accord', 'Les diagnostics détaillés sont désactivés par défaut et uniquement sur option.')],
    toc_label='Sur cette page',
    table_head=('Service', 'Pour quoi', 'Quelles informations'),
    table_rows=[('Google / Gemini API', 'générer un récit', 'nom du lieu et bref contexte'),
                ('ElevenLabs', 'créer la voix', 'le texte du récit'),
                ('Wikipedia', 'informations factuelles', "requête directe depuis l'appareil"),
                ('OpenStreetMap / OSRM', 'carte et itinéraire', "requête directe depuis l'appareil")],
    note1="Par défaut, votre localisation n'est ni conservée ni enregistrée.",
    note2="Les journaux détaillés ne sont disponibles qu'en option pour l'équipe de test.",
    close_h='Encore une question ?', close_p="La confidentialité doit être compréhensible. Si quelque chose n'est pas clair, dites-le-nous.", close_btn='Écrivez-nous',
),
'es': dict(
    h1='Tu viaje sigue siendo tuyo.', alt='Un teléfono boca abajo junto a un diario de viaje y un mapa de carreteras en un coche aparcado.',
    lede='2R usa solo lo necesario para contar la historia adecuada por el camino. Sin cuenta, sin registro de trayectos y, por defecto, sin ubicación guardada. Aquí explicamos exactamente qué sí ocurre.',
    promises=[('01', 'Sin cuenta', 'No necesitas iniciar sesión ni dejar tu nombre.'),
              ('02', 'Sin registro de trayectos', 'Por defecto no creamos un historial de dónde has estado.'),
              ('03', 'Registros de prueba solo con permiso', 'Los diagnósticos más detallados están desactivados por defecto y son solo opt-in.')],
    toc_label='En esta página',
    table_head=('Servicio', 'Para qué', 'Qué información'),
    table_rows=[('Google / Gemini API', 'generar la historia', 'nombre del lugar y breve contexto'),
                ('ElevenLabs', 'crear la voz', 'el texto de la historia'),
                ('Wikipedia', 'información factual', 'solicitud directa desde el dispositivo'),
                ('OpenStreetMap / OSRM', 'mapa y ruta', 'solicitud directa desde el dispositivo')],
    note1='Por defecto tu ubicación no se guarda ni se registra.',
    note2='Los registros ampliados solo están disponibles como opt-in para el equipo de pruebas.',
    close_h='¿Alguna otra pregunta?', close_p='La privacidad debe ser comprensible. Si algo no está claro, nos gustaría saberlo.', close_btn='Escríbenos',
),
'pt': dict(
    h1='A sua viagem continua sua.', alt='Um telefone virado para baixo ao lado de um diário de viagem e de um mapa rodoviário num carro estacionado.',
    lede='O 2R usa apenas o necessário para contar a história certa pelo caminho. Sem conta, sem registo de trajetos e, por padrão, sem localização guardada. Aqui explicamos exatamente o que de facto acontece.',
    promises=[('01', 'Sem conta necessária', 'Você não precisa fazer login nem deixar o seu nome.'),
              ('02', 'Sem registo de trajetos', 'Por padrão, não criamos um histórico de onde você esteve.'),
              ('03', 'Registos de teste apenas com consentimento', 'Diagnósticos mais detalhados estão desativados por padrão e são apenas opt-in.')],
    toc_label='Nesta página',
    table_head=('Serviço', 'Para quê', 'Que informação'),
    table_rows=[('Google / Gemini API', 'gerar a história', 'nome do lugar e breve contexto'),
                ('ElevenLabs', 'criar a voz', 'o texto da história'),
                ('Wikipedia', 'informação factual', 'pedido direto a partir do aparelho'),
                ('OpenStreetMap / OSRM', 'mapa e rota', 'pedido direto a partir do aparelho')],
    note1='Por padrão, a sua localização não é guardada nem registada.',
    note2='Registos detalhados só estão disponíveis como opt-in para a equipa de teste.',
    close_h='Ainda tem uma pergunta?', close_p='A privacidade deve ser compreensível. Se algo não estiver claro, queremos saber.', close_btn='Escreva-nos',
),
}

def build_privacy(lang):
    p = PRIVACY[lang]
    pe = PRIV_EXTRA[lang]
    location_lis = '\n'.join(f'<li>{item}</li>' for item in p['location_items'])
    promises = ''.join(
        f'<div class="priv-promise"><span class="priv-pnum">{n}</span><div class="priv-pbody"><h3>{t}</h3><p>{d}</p></div></div>'
        for n, t, d in pe['promises'])
    toc_items = [('loc', p['h_location']), ('verhalen', p['h_stories']), ('limieten', p['h_limits']),
                 ('accounts', p['h_accounts']), ('contact', p['h_contact'])]
    toc = ''.join(f'<li><a href="#{aid}">{lbl}</a></li>' for aid, lbl in toc_items)
    th = pe['table_head']
    rows = ''.join(
        f'<tr><th scope="row">{s}</th><td data-label="{th[1]}">{w}</td><td data-label="{th[2]}">{i}</td></tr>'
        for s, w, i in pe['table_rows'])
    caching = p['stories_items'][3] if len(p['stories_items']) > 3 else ''
    body = f'''  <section class="priv-hero">
    <img class="priv-hero-img" src="/images/privacy-header-stille-telefoon.jpg" alt="{pe['alt']}" width="1536" height="1024" fetchpriority="high">
    <div class="priv-hero-shade" aria-hidden="true"></div>
    <div class="priv-hero-content">
      <p class="eyebrow on-photo">{p['eyebrow']}</p>
      <h1>{pe['h1']}</h1>
      <p class="priv-hero-lede">{pe['lede']}</p>
      <p class="priv-updated">{p['updated']}</p>
    </div>
  </section>

  <section class="priv-promises"><div class="wrap">{promises}</div></section>

  <section class="priv-body"><div class="wrap priv-grid">
    <nav class="priv-toc" aria-label="{pe['toc_label']}">
      <p class="priv-toc-label">{pe['toc_label']}</p>
      <ul>{toc}</ul>
    </nav>
    <div class="priv-text">
      <p class="priv-intro">{p['intro']}</p>

      <section id="loc" class="priv-sec">
        <h2>{p['h_location']}</h2>
        <p class="priv-fieldnote">{pe['note1']}</p>
        <p class="priv-fieldnote">{pe['note2']}</p>
        <ul>{location_lis}</ul>
      </section>

      <section id="verhalen" class="priv-sec">
        <h2>{p['h_stories']}</h2>
        <table class="priv-table">
          <thead><tr><th scope="col">{th[0]}</th><th scope="col">{th[1]}</th><th scope="col">{th[2]}</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
        <p class="priv-cache">{caching}</p>
      </section>

      <section id="limieten" class="priv-sec">
        <h2>{p['h_limits']}</h2>
        <p>{p['limits_text']}</p>
      </section>

      <section id="accounts" class="priv-sec">
        <h2>{p['h_accounts']}</h2>
        <p>{p['accounts_text']}</p>
      </section>

      <section id="contact" class="priv-sec">
        <h2>{p['h_contact']}</h2>
        <p>{p['contact_text']}</p>
      </section>
    </div>
  </div></section>

  <section class="priv-close"><div class="wrap">
    <h2>{pe['close_h']}</h2>
    <p>{pe['close_p']}</p>
    <a class="btn-primary" href="mailto:nimco@nentjes.nl">{pe['close_btn']}</a>
  </div></section>
'''
    return page_shell(lang, p['title'], pe['lede'][:150], 'privacy', body)

# --- Live verhalen uit de app (goedgekeurd op de besloten leespagina) ------
# Zoekbaar en met kaart, zodat het archief bruikbaar blijft als het groeit.
LIVE_STORIES_LABELS = {
    'nl': {'kop': 'Vers van onderweg', 'lede': 'Deze verhalen zijn onderweg door 2R verteld en door ons nagelezen. Zoek op een plaats, een streek, een land of gewoon op een woord.', 'zoek': 'Zoek op plaats, streek, land of woord…', 'alles': 'Alles', 'leeg': 'Niets gevonden — probeer een ander woord.', 'nog': 'Nog geen verhalen vrijgegeven.', 'resultaat': 'verhalen', 'kaart': 'Op de kaart'},
    'en': {'kop': 'Fresh from the road', 'lede': 'These stories were told by 2R along the way and checked by us. Search by place, region, country or simply a word.', 'zoek': 'Search place, region, country or word…', 'alles': 'All', 'leeg': 'Nothing found — try another word.', 'nog': 'No stories released yet.', 'resultaat': 'stories', 'kaart': 'On the map'},
    'de': {'kop': 'Frisch von unterwegs', 'lede': 'Diese Geschichten hat 2R unterwegs erzählt; wir haben sie geprüft. Suche nach Ort, Region, Land oder einfach einem Wort.', 'zoek': 'Ort, Region, Land oder Wort suchen…', 'alles': 'Alle', 'leeg': 'Nichts gefunden — versuch ein anderes Wort.', 'nog': 'Noch keine Geschichten freigegeben.', 'resultaat': 'Geschichten', 'kaart': 'Auf der Karte'},
    'fr': {'kop': 'Fraîchement récoltées', 'lede': 'Ces récits ont été racontés par 2R en chemin, puis vérifiés par nos soins. Cherchez par lieu, région, pays ou simplement un mot.', 'zoek': 'Chercher un lieu, une région, un pays ou un mot…', 'alles': 'Tout', 'leeg': 'Rien trouvé — essayez un autre mot.', 'nog': "Aucun récit publié pour l'instant.", 'resultaat': 'récits', 'kaart': 'Sur la carte'},
    'es': {'kop': 'Recién llegadas del camino', 'lede': '2R contó estas historias por el camino y nosotros las revisamos. Busca por lugar, comarca, país o simplemente una palabra.', 'zoek': 'Busca lugar, comarca, país o palabra…', 'alles': 'Todo', 'leeg': 'No se encontró nada — prueba otra palabra.', 'nog': 'Todavía no hay historias publicadas.', 'resultaat': 'historias', 'kaart': 'En el mapa'},
    'pt': {'kop': 'Fresquinhas da estrada', 'lede': 'Estas histórias foram contadas pelo 2R durante a viagem e revistas por nós. Procure por lugar, região, país ou apenas uma palavra.', 'zoek': 'Procurar lugar, região, país ou palavra…', 'alles': 'Tudo', 'leeg': 'Nada encontrado — tente outra palavra.', 'nog': 'Ainda não há histórias publicadas.', 'resultaat': 'histórias', 'kaart': 'No mapa'},
}

LIVE_STORIES_API = 'https://mapsinfo.roelnentjes.workers.dev/api/published'

LIVE_TEMPLATE = """  <section class="block" id="live-verhalen"><div class="wrap">
    <div class="eyebrow">__KOP__</div>
    <p class="lede" style="max-width:62ch;margin-bottom:22px;">__LEDE__</p>

    <div class="verhaal-zoek">
      <input type="search" id="vz-zoek" placeholder="__ZOEK__" autocomplete="off">
      <div id="vz-chips" class="vz-chips"></div>
      <div id="vz-telling" class="vz-telling"></div>
    </div>

    <div id="vz-kaart" class="vz-kaart" aria-label="__KAART__"></div>
    <div id="live-lijst" class="story-grid-simple"></div>
  </div></section>

  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
  (function () {
    var API = "__API__";
    var T = { leeg: "__LEEG__", nog: "__NOG__", resultaat: "__RESULTAAT__", alles: "__ALLES__" };
    var lijst = document.getElementById('live-lijst');
    var chips = document.getElementById('vz-chips');
    var telling = document.getElementById('vz-telling');
    var zoekveld = document.getElementById('vz-zoek');
    var kaartEl = document.getElementById('vz-kaart');
    var kaart = null, laag = null, timer = null;
    var filter = { q: '', land: '', onderwerp: '' };

    function esc(s) {
      return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
      });
    }

    function toonKaart(verhalen) {
      var metPunt = verhalen.filter(function (v) { return v.lat && v.lng; });
      if (!metPunt.length) { kaartEl.style.display = 'none'; return; }
      kaartEl.style.display = 'block';
      if (!kaart) {
        kaart = L.map(kaartEl, { scrollWheelZoom: false });
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>', maxZoom: 19
        }).addTo(kaart);
      }
      if (laag) kaart.removeLayer(laag);
      laag = L.layerGroup(metPunt.map(function (v) {
        var mf = v.foto ? '<img src="' + esc(v.foto) + '" alt="" referrerpolicy="no-referrer" ' +
          'style="width:100%;height:96px;object-fit:cover;border-radius:6px;margin-bottom:6px" ' +
          '>' : '';
        return L.marker([v.lat, v.lng]).bindPopup(
          mf + '<b>' + esc(v.plek) + '</b><br>' + esc(v.gebied) +
          '<br><a href="#verhaal-' + v.id + '">lees het verhaal</a>',
          { maxWidth: 240, minWidth: 200 }
        );
      })).addTo(kaart);
      var bounds = L.latLngBounds(metPunt.map(function (v) { return [v.lat, v.lng]; }));
      kaart.fitBounds(bounds, { padding: [40, 40], maxZoom: 11 });
    }

    function toonChips(f) {
      var html = '';
      function groep(items, sleutel) {
        return items.map(function (it) {
          var actief = filter[sleutel] === it.waarde ? ' actief' : '';
          return '<button class="vz-chip' + actief + '" data-sleutel="' + sleutel +
                 '" data-waarde="' + esc(it.waarde) + '">' + esc(it.waarde) +
                 ' <span>' + it.n + '</span></button>';
        }).join('');
      }
      var leeg = !filter.land && !filter.onderwerp;
      html += '<button class="vz-chip' + (leeg ? ' actief' : '') + '" data-sleutel="wis">' + esc(T.alles) + '</button>';
      html += groep(f.landen || [], 'land');
      html += groep(f.onderwerpen || [], 'onderwerp');
      chips.innerHTML = html;
    }

    async function laden() {
      var p = new URLSearchParams();
      if (filter.q) p.set('q', filter.q);
      if (filter.land) p.set('land', filter.land);
      if (filter.onderwerp) p.set('onderwerp', filter.onderwerp);
      try {
        var r = await fetch(API + (p.toString() ? '?' + p.toString() : ''));
        if (!r.ok) throw new Error('offline');
        var d = await r.json();
        if (!d.totaal) { lijst.innerHTML = '<p class="vz-leeg">' + esc(T.nog) + '</p>'; kaartEl.style.display = 'none'; telling.textContent = ''; return; }
        toonChips(d.facetten || {});
        telling.textContent = d.gevonden + ' / ' + d.totaal + ' ' + T.resultaat;
        if (!d.verhalen.length) { lijst.innerHTML = '<p class="vz-leeg">' + esc(T.leeg) + '</p>'; kaartEl.style.display = 'none'; return; }
        lijst.innerHTML = d.verhalen.map(function (v) {
          var foto = v.foto ? '<img class="verhaal-foto" src="' + esc(v.foto) +
            '" alt="" referrerpolicy="no-referrer">' : '';
          return '<article class="story-card' + (v.foto ? ' met-foto' : '') + '" id="verhaal-' + v.id + '">' +
            foto +
            '<div class="story-card-body">' +
            '<div class="story-card-meta">' + esc(v.gebied) + (v.land ? ' · ' + esc(v.land) : '') +
            (v.onderwerp ? ' · ' + esc(v.onderwerp) : '') + '</div>' +
            '<h3>' + esc(v.plek) + '</h3><p>' + esc(v.tekst) + '</p></div></article>';
        }).join('');
        toonKaart(d.verhalen);
      } catch (e) {
        lijst.innerHTML = '<p class="vz-leeg">' + esc(T.nog) + '</p>';
        kaartEl.style.display = 'none';
      }
    }

    // Kapotte afbeeldingen netjes verbergen. Eén afvanger voor de hele
    // sectie in plaats van een onerror per afbeelding: dat scheelt geneste
    // aanhalingstekens, die eerder de hele pagina sloopten.
    document.getElementById('live-verhalen').addEventListener('error', function (e) {
      if (e.target && e.target.tagName === 'IMG') e.target.style.display = 'none';
    }, true);

    zoekveld.addEventListener('input', function (e) {
      clearTimeout(timer);
      timer = setTimeout(function () { filter.q = e.target.value.trim(); laden(); }, 300);
    });
    chips.addEventListener('click', function (e) {
      var knop = e.target.closest('.vz-chip');
      if (!knop) return;
      if (knop.dataset.sleutel === 'wis') { filter.land = ''; filter.onderwerp = ''; }
      else {
        var s = knop.dataset.sleutel;
        filter[s] = filter[s] === knop.dataset.waarde ? '' : knop.dataset.waarde;
      }
      laden();
    });
    laden();
  })();
  </script>
"""


def live_stories_section(lang):
    L = LIVE_STORIES_LABELS[lang]
    return (LIVE_TEMPLATE
            .replace('__KOP__', L['kop']).replace('__LEDE__', L['lede'])
            .replace('__ZOEK__', L['zoek']).replace('__ALLES__', L['alles'])
            .replace('__LEEG__', L['leeg']).replace('__NOG__', L['nog'])
            .replace('__RESULTAAT__', L['resultaat']).replace('__KAART__', L['kaart'])
            .replace('__API__', LIVE_STORIES_API))


# Verhalen-archief als levend reisboek (herbouw 29 aug). Nieuwe redactionele
# omlijsting; de verhalen zelf blijven de bron. Foto's per verhaal volgen later —
# nu papieren composities (geen verzonnen documentairefoto's van echte plekken).
FEATURED_SLUG = 'kasteel-nijenrode-breukelen'
STORIES_EXTRA = {
'nl': dict(hero_eyebrow='Het levende reisboek', hero_h1='Verhalen die onderweg begonnen.',
    hero_lede='Iedere plek draagt een verhaal. Soms hoef je er alleen maar langs te rijden. Deze verhalen werden tijdens echte ritten door 2R verteld, door ons nagelezen en voorzien van hun bron.',
    hero_cta='Lees het eerste verhaal', hero_alt='Een reiziger kijkt vanuit de auto naar een voorbijtrekkend Europees dorp, met een reisboek op schoot.',
    featured_label='Uitgelicht', read_story='Lees het verhaal', detail_source_h='Waar dit verhaal vandaan komt',
    related='Verder lezen', invite_h='Neem Route mee op je volgende reis'),
'en': dict(hero_eyebrow='The living travel book', hero_h1='Stories that began on the road.',
    hero_lede='Every place carries a story. Sometimes you only have to drive past it. These stories were told by 2R during real trips, checked by us and given their source.',
    hero_cta='Read the first story', hero_alt='A traveler looks from the car at a passing European village, with a travel book on their lap.',
    featured_label='Featured', read_story='Read the story', detail_source_h='Where this story comes from',
    related='Read on', invite_h='Take Route along on your next trip'),
'de': dict(hero_eyebrow='Das lebendige Reisebuch', hero_h1='Geschichten, die unterwegs begannen.',
    hero_lede='Jeder Ort trägt eine Geschichte. Manchmal musst du nur daran vorbeifahren. Diese Geschichten wurden von 2R während echter Fahrten erzählt, von uns geprüft und mit ihrer Quelle versehen.',
    hero_cta='Lies die erste Geschichte', hero_alt='Ein Reisender blickt aus dem Auto auf ein vorbeiziehendes europäisches Dorf, ein Reisebuch auf dem Schoß.',
    featured_label='Ausgewählt', read_story='Geschichte lesen', detail_source_h='Woher diese Geschichte stammt',
    related='Weiterlesen', invite_h='Nimm Route mit auf deine nächste Reise'),
'fr': dict(hero_eyebrow='Le carnet de voyage vivant', hero_h1='Des histoires nées en chemin.',
    hero_lede="Chaque lieu porte une histoire. Parfois, il suffit de passer devant. Ces récits ont été racontés par 2R lors de vrais trajets, vérifiés par nous et accompagnés de leur source.",
    hero_cta='Lire le premier récit', hero_alt="Un voyageur regarde depuis la voiture un village européen qui défile, un carnet de voyage sur les genoux.",
    featured_label='À la une', read_story='Lire le récit', detail_source_h="D'où vient cette histoire",
    related='À lire aussi', invite_h='Emportez Route lors de votre prochain voyage'),
'es': dict(hero_eyebrow='El libro de viaje vivo', hero_h1='Historias que empezaron en el camino.',
    hero_lede='Cada lugar guarda una historia. A veces solo tienes que pasar por delante. Estas historias fueron contadas por 2R durante viajes reales, revisadas por nosotros y con su fuente.',
    hero_cta='Lee la primera historia', hero_alt='Un viajero mira desde el coche un pueblo europeo que pasa, con un libro de viaje en el regazo.',
    featured_label='Destacado', read_story='Leer la historia', detail_source_h='De dónde viene esta historia',
    related='Sigue leyendo', invite_h='Lleva Route en tu próximo viaje'),
'pt': dict(hero_eyebrow='O livro de viagem vivo', hero_h1='Histórias que começaram no caminho.',
    hero_lede='Cada lugar guarda uma história. Às vezes basta passar por ela. Estas histórias foram contadas pelo 2R durante viagens reais, revistas por nós e com a sua fonte.',
    hero_cta='Leia a primeira história', hero_alt='Um viajante olha do carro para uma vila europeia que passa, com um livro de viagem no colo.',
    featured_label='Em destaque', read_story='Ler a história', detail_source_h='De onde vem esta história',
    related='Continue a ler', invite_h='Leve o Route na sua próxima viagem'),
}

def _story_excerpt(st, lang, n=150):
    return st['text'][lang][:n].rsplit(' ', 1)[0] + '…'

def magazine_card(lang, st, size='klein'):
    cat = CATEGORIES[st['category']][lang]
    return f'''<a class="mag-card mag-{size}" href="/{lang}/stories/{st['slug']}.html">
    <div class="mag-cover" aria-hidden="true"><span class="mag-cat-mark">{html.escape(cat)}</span></div>
    <div class="mag-body">
      <span class="mag-cat">{html.escape(cat)}</span>
      <h3>{html.escape(st['title'][lang])}</h3>
      <p>{html.escape(_story_excerpt(st, lang, 120 if size != 'groot' else 200))}</p>
      <span class="mag-meta">{html.escape(st['location'])} &middot; {st['date']}</span>
    </div>
  </a>'''

def build_stories_index(lang):
    s = SITE[lang]
    se = STORIES_EXTRA[lang]
    featured = next((st for st in STORIES if st['slug'] == FEATURED_SLUG), STORIES[0])
    rest = [st for st in STORIES if st is not featured]
    first_slug = STORIES[0]['slug']
    fcat = CATEGORIES[featured['category']][lang]
    featured_html = f'''<a class="mag-featured" href="/{lang}/stories/{featured['slug']}.html">
      <div class="mag-featured-cover" aria-hidden="true"><span class="mag-cat-mark">{html.escape(fcat)}</span></div>
      <div class="mag-featured-body">
        <span class="mag-featured-label">{se['featured_label']}</span>
        <span class="mag-cat">{html.escape(fcat)} &middot; {html.escape(featured['location'])}</span>
        <h2>{html.escape(featured['title'][lang])}</h2>
        <p>{html.escape(_story_excerpt(featured, lang, 240))}</p>
        <span class="mag-cta">{se['read_story']} <span aria-hidden="true">&#8594;</span></span>
      </div>
    </a>'''
    grid = ''.join(magazine_card(lang, st, 'middel' if i < 2 else 'klein') for i, st in enumerate(rest))
    body = f'''  <section class="stories-hero">
    <img class="stories-hero-img" src="/images/stories-hero-levend-reisboek.jpg" alt="{se['hero_alt']}" width="1536" height="1024" fetchpriority="high">
    <div class="stories-hero-shade" aria-hidden="true"></div>
    <div class="stories-hero-content">
      <p class="eyebrow on-photo">{se['hero_eyebrow']}</p>
      <h1>{se['hero_h1']}</h1>
      <p class="stories-hero-lede">{se['hero_lede']}</p>
      <a class="stories-hero-cta" href="/{lang}/stories/{first_slug}.html">{se['hero_cta']} <span aria-hidden="true">&#8594;</span></a>
    </div>
  </section>

  <section class="mag"><div class="wrap">
    {featured_html}
    <div class="mag-grid">{grid}</div>
  </div></section>
{live_stories_section(lang)}
'''
    return page_shell(lang, f"{s['nav_stories']} — 2R (Second Route)", se['hero_lede'][:150], 'stories', body)

def build_story_detail(lang, st):
    s = SITE[lang]
    se = STORIES_EXTRA[lang]
    cat = CATEGORIES[st['category']][lang]
    related = [x for x in STORIES if x is not st and x['category'] == st['category']]
    for x in STORIES:
        if len(related) >= 2:
            break
        if x is not st and x not in related:
            related.append(x)
    related_html = ''.join(magazine_card(lang, x, 'klein') for x in related[:2])
    body = f'''  <article class="story-detail">
    <div class="story-cover" aria-hidden="true"><span class="mag-cat-mark">{html.escape(cat)}</span></div>
    <div class="wrap story-detail-wrap">
      <p class="story-back-row"><a class="story-back" href="/{lang}/stories/">{s['story_back']}</a></p>
      <p class="story-place">{html.escape(st['location'])}</p>
      <p class="story-cat-line">{html.escape(cat)} <span class="story-date">&middot; {st['date']}</span></p>
      <h1>{html.escape(st['title'][lang])}</h1>
      <div class="story-read"><p>{html.escape(st['text'][lang])}</p></div>
      <div class="story-source">
        <p class="story-source-h">{se['detail_source_h']}</p>
        <p class="story-source-line">{s['story_told_by']} &middot; {s['story_source_lbl']}: <a href="{st['source_url']}" target="_blank" rel="noopener">{html.escape(st['source_label'])}</a></p>
      </div>
    </div>
  </article>

  <section class="story-related"><div class="wrap">
    <p class="story-related-h">{se['related']}</p>
    <div class="mag-grid">{related_html}</div>
  </div></section>

  <section class="story-invite"><div class="wrap">
    <h2>{se['invite_h']}</h2>
    <p>{s['invite_p']}</p>
    <a class="btn-primary" href="https://apps.apple.com/app/id6802613397">{s['invite_btn']} <span aria-hidden="true">&#8599;</span></a>
  </div></section>
'''
    return page_shell(lang, f"{st['title'][lang]} — 2R", st['text'][lang][:150], 'stories', body)

# ---------------------------------------------------------------------------
# Schrijf alles weg
# ---------------------------------------------------------------------------
def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)

for lang in LANGS:
    write(f'{lang}/index.html', build_home(lang))
    write(f'{lang}/roadmap.html', build_roadmap(lang))
    write(f'{lang}/zo-werkt-het.html', build_howto(lang))
    write(f'{lang}/privacy.html', build_privacy(lang))
    write(f'{lang}/stories/index.html', build_stories_index(lang))
    for st in STORIES:
        write(f'{lang}/stories/{st["slug"]}.html', build_story_detail(lang, st))
    for i in range(len(CITY_SLUGS)):
        write(f'{lang}/stad/{CITY_SLUGS[i]}.html', build_city_story(lang, i))

print(f"Klaar: {len(LANGS)} talen x ({5 + len(STORIES) + len(CITY_SLUGS)} pagina's) = {len(LANGS) * (5 + len(STORIES) + len(CITY_SLUGS))} bestanden")
