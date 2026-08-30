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
    hero_lede='Of je nu wandelt, fietst, met de trein of auto reist: je navigatie wijst je de weg — <b>2 Route</b> vertelt het verhaal van die weg, spontaan of als zorgvuldig opgebouwd luisterverhaal.',
    hero_btn_demo='Hoor een verhaal', hero_btn_roadmap='Reis een stukje mee',
    hero_caption_coord='52.1045° N', hero_caption_note='Een avond onderweg · Utrecht',
    listen_label='01 · Een stem naast je', listen_h2='De wereld buiten wordt<br>een verhaal binnen.',
    listen_p='Geen lijst met weetjes. Route kiest één betekenisvol verhaal, vertelt het rustig en laat daarna weer ruimte voor het landschap — en voor elkaar.',
    listen_now='Route vertelt', listen_title='De grafheuvels<br>op de Stulpse heide', listen_sub='Echt fragment · luisterwandeling bij Kasteel Drakensteyn',
    journey_label='02 · Europa reist met je mee', journey_route_label='Europa · Route 02', journey_route_meta='vier windstreken · één reis',
    invite_label='Voor de volgende keer dat je op pad gaat', invite_h2='Wat zal Route op jouw<br>volgende reis vertellen?',
    invite_p='Neem een warme stem, een levend reisboek en een beetje verwondering met je mee.', invite_btn='Neem Route mee',
    footer_tagline='Niet de bestemming, maar de reis maakt ons wijs.',
    footer_credit='Gebouwd door Roel Nentjes, samen met Claude (Anthropic).',
    stat1_num='9', stat1_lbl='interesse-rubrieken — elk apart getest',
    stat2_num='6', stat2_lbl='talen op deze site — de app vertelt eerst in het Nederlands',
    stat3_num='4', stat3_lbl='reismodi — te voet, fiets, trein, auto', stat4_num='∞', stat4_lbl='plekken — overal, live gegenereerd',
    steps_eyebrow='Hoe het werkt', steps_h2='Van onderweg zijn naar luisteren in drie stappen',
    step1_h='Zet Route aan', step1_p='Eén knop. Kies je interesses — geschiedenis, natuur, kunst, eten & drinken — of typ er zelf een in.',
    step2_h='Wandel, fiets, rijd of pak de trein', step2_p='2R volgt je route via GPS en zoekt live naar wat er om je heen te vertellen valt — bij lokale bronnen, niet alleen Wikipedia.',
    step3_h='Luister naar Route', step3_p='Een warme, expressieve stem vertelt — eerlijk over wat je écht kunt zien, nooit doen-alsof.',
    why_eyebrow='Waarom 2R anders is', why_h2='Geen encyclopedie. Een reisgezel.',
    why_p="Bestaande reisverteller-apps werken met vooraf ingesproken scripts — beperkt tot populaire routes, hetzelfde verhaal voor iedereen. 2R genereert live, overal, en past zich aan jouw interesses aan.",
    f1_h='Lokale bronnen eerst', f1_p="Gemeentesites, VVV's en erfgoedorganisaties — niet alleen Wikipedia. In het buitenland wordt de lokale taal gebruikt en in jouw taal naverteld.",
    f2_h='Gidsmodus', f2_p='Eén doorlopend verhaal met het gebied als rode draad — land, provincie, streek, plaats — in plaats van losse weetjes.',
    f3_h='Eerlijk, altijd', f3_p='Route doet nooit alsof hij weet wat je ziet. Dichtbij: "kijk eens". Verder weg: "een omweg waard" — nooit andersom.',
    f4_h='Privacy-eerst', f4_p='Geen locatie-opslag, geen account nodig. Elk verzoek staat op zichzelf.',
    f5_h='Individueel of familie', f5_p='Eigen interesses, of samen luisteren — met spelletjes en quizjes onderweg in de maak.',
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
    hero_lede="Whether you walk, cycle, travel by train or car: your navigation shows you the road — <b>2 Route</b> tells the story of that road, spontaneously or as a carefully crafted audio story.",
    hero_btn_demo='Hear a story', hero_btn_roadmap='Come along for a bit',
    hero_caption_coord='52.1045° N', hero_caption_note='An evening on the road · Utrecht',
    listen_label='01 · A voice beside you', listen_h2='The world outside becomes<br>a story within.',
    listen_p='No list of facts. Route picks one meaningful story, tells it calmly, then makes room again for the landscape — and for each other.',
    listen_now='Route is telling', listen_title='The burial mounds<br>on the Stulp heath', listen_sub='Real excerpt (Dutch) · the Drakensteyn listening walk',
    journey_label='02 · Europe travels along with you', journey_route_label='Europe · Route 02', journey_route_meta='four compass points · one journey',
    invite_label='For the next time you head out', invite_h2='What will Route tell you<br>on your next trip?',
    invite_p='Bring a warm voice, a living travel journal, and a little wonder.', invite_btn='Take Route with you',
    footer_tagline='Not the destination — the journey makes us wise.',
    footer_credit='Built by Roel Nentjes, together with Claude (Anthropic).',
    stat1_num='9', stat1_lbl='interest categories — each individually tested',
    stat2_num='6', stat2_lbl='languages on this site — the app narrates in Dutch first',
    stat3_num='4', stat3_lbl='travel modes — walk, bike, train, car', stat4_num='∞', stat4_lbl='places — anywhere, generated live',
    steps_eyebrow='How it works', steps_h2='From setting out to listening, in three steps',
    step1_h='Turn Route on', step1_p='One switch. Pick your interests — history, nature, art, food & drink — or type in your own.',
    step2_h='Walk, cycle, drive or take the train', step2_p="2R follows your route via GPS and searches live for what's worth telling — from local sources, not just Wikipedia.",
    step3_h='Listen to Route', step3_p='A warm, expressive voice narrates — honestly about what you can actually see, never pretending.',
    why_eyebrow='Why 2R is different', why_h2='Not an encyclopedia. A travel companion.',
    why_p='Existing travel-narrator apps rely on pre-recorded scripts — limited to popular routes, the same story for everyone. 2R generates live, everywhere, and adapts to your interests.',
    f1_h='Local sources first', f1_p='Municipal sites, tourism boards and heritage organisations — not just Wikipedia. Abroad, local-language sources are used and retold in your own language.',
    f2_h='Guide mode', f2_p='One continuous story with the region as its through-line — country, province, area, town — instead of disconnected facts.',
    f3_h='Always honest', f3_p='Route never pretends to know what you can see. Close by: "look now." Further away: "worth a detour" — never the other way around.',
    f4_h='Privacy-first', f4_p='No location storage, no account required. Every request stands on its own.',
    f5_h='Solo or family', f5_p='Your own interests, or listening together — with games and quizzes for the road in the works.',
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
    hero_lede='Ob du wanderst, radelst, mit Bahn oder Auto reist: Deine Navigation zeigt dir den Weg — <b>2 Route</b> erzählt die Geschichte dieses Weges, spontan oder als sorgfältig aufgebaute Hörgeschichte.',
    hero_btn_demo='Höre eine Geschichte', hero_btn_roadmap='Reis ein Stück mit',
    hero_caption_coord='52,1045° N', hero_caption_note='Ein Abend unterwegs · Utrecht',
    listen_label='01 · Eine Stimme neben dir', listen_h2='Die Welt draußen wird<br>zur Geschichte drinnen.',
    listen_p='Keine Liste von Fakten. Route wählt eine bedeutsame Geschichte, erzählt sie ruhig und lässt danach wieder Raum für die Landschaft — und füreinander.',
    listen_now='Route erzählt', listen_title='Die Hügelgräber<br>auf der Stulp-Heide', listen_sub='Echter Ausschnitt (Niederländisch) · Hörwanderung bei Schloss Drakensteyn',
    journey_label='02 · Europa reist mit dir mit', journey_route_label='Europa · Route 02', journey_route_meta='vier Himmelsrichtungen · eine Reise',
    invite_label='Für das nächste Mal, wenn du losziehst', invite_h2='Was wird Route dir auf<br>deiner nächsten Reise erzählen?',
    invite_p='Nimm eine warme Stimme, ein lebendiges Reisetagebuch und ein bisschen Staunen mit.', invite_btn='Nimm Route mit',
    footer_tagline='Nicht das Ziel — die Reise macht uns weise.',
    footer_credit='Gebaut von Roel Nentjes, gemeinsam mit Claude (Anthropic).',
    stat1_num='9', stat1_lbl='Interessen-Rubriken — jede einzeln getestet',
    stat2_num='6', stat2_lbl='Sprachen auf dieser Website — die App erzählt zunächst auf Niederländisch',
    stat3_num='4', stat3_lbl='Reisemodi — zu Fuß, Rad, Bahn, Auto', stat4_num='∞', stat4_lbl='Orte — überall, live generiert',
    steps_eyebrow='So funktioniert es', steps_h2='In drei Schritten vom Unterwegssein zum Zuhören',
    step1_h='Route einschalten', step1_p='Ein Schalter. Wähle deine Interessen — Geschichte, Natur, Kunst, Essen & Trinken — oder gib eigene ein.',
    step2_h='Wandern, radeln, fahren oder Bahn nehmen', step2_p='2R folgt deiner Route per GPS und sucht live nach Erzählenswertem — aus lokalen Quellen, nicht nur Wikipedia.',
    step3_h='Route zuhören', step3_p='Eine warme, ausdrucksstarke Stimme erzählt — ehrlich über das, was du wirklich sehen kannst, nie vorgetäuscht.',
    why_eyebrow='Warum 2R anders ist', why_h2='Kein Lexikon. Ein Reisebegleiter.',
    why_p='Bestehende Reiseerzähler-Apps arbeiten mit vorab aufgenommenen Skripten — begrenzt auf beliebte Routen, dieselbe Geschichte für alle. 2R generiert live, überall, und passt sich deinen Interessen an.',
    f1_h='Lokale Quellen zuerst', f1_p='Gemeindeseiten, Tourismusverbände und Denkmalorganisationen — nicht nur Wikipedia. Im Ausland werden lokalsprachige Quellen genutzt und in deiner Sprache nacherzählt.',
    f2_h='Guide-Modus', f2_p='Eine durchgehende Geschichte mit der Region als rotem Faden — Land, Provinz, Gegend, Ort — statt einzelner Fakten.',
    f3_h='Immer ehrlich', f3_p='Route tut nie so, als wüsste sie, was du siehst. Ganz nah: "schau mal". Weiter weg: "einen Umweg wert" — nie andersherum.',
    f4_h='Datenschutz zuerst', f4_p='Keine Standortspeicherung, kein Konto nötig. Jede Anfrage steht für sich.',
    f5_h='Einzeln oder Familie', f5_p='Eigene Interessen, oder gemeinsam zuhören — mit Spielen und Quiz für unterwegs in Arbeit.',
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
    hero_lede="Que vous marchiez, pédaliez, voyagiez en train ou en voiture : votre navigation vous montre la route — <b>2 Route</b> raconte l'histoire de cette route, spontanément ou en récit audio soigneusement composé.",
    hero_btn_demo='Écouter une histoire', hero_btn_roadmap='Faire un bout de chemin',
    hero_caption_coord='52,1045° N', hero_caption_note='Une soirée sur la route · Utrecht',
    listen_label='01 · Une voix à vos côtés', listen_h2='Le monde extérieur devient<br>une histoire intérieure.',
    listen_p='Pas une liste de faits. Route choisit une histoire qui a du sens, la raconte calmement, puis laisse de nouveau place au paysage — et à vous.',
    listen_now='Route raconte', listen_title='Les tumulus<br>de la lande de Stulp', listen_sub='Extrait réel (en néerlandais) · la promenade sonore de Drakensteyn',
    journey_label="02 · L'Europe vous accompagne", journey_route_label='Europe · Itinéraire 02', journey_route_meta='quatre points cardinaux · un seul voyage',
    invite_label='Pour la prochaine fois que vous partez', invite_h2='Que vous racontera Route<br>lors de votre prochain trajet ?',
    invite_p="Emportez une voix chaleureuse, un carnet de voyage vivant et un peu d'émerveillement.", invite_btn='Emportez Route avec vous',
    footer_tagline="Pas la destination — c'est le voyage qui nous rend sages.",
    footer_credit='Conçu par Roel Nentjes, avec Claude (Anthropic).',
    stat1_num='9', stat1_lbl="catégories d'intérêt — chacune testée individuellement",
    stat2_num='6', stat2_lbl="langues sur ce site — l'app raconte d'abord en néerlandais",
    stat3_num='4', stat3_lbl='modes — à pied, vélo, train, voiture', stat4_num='∞', stat4_lbl='lieux — partout, générés en direct',
    steps_eyebrow='Comment ça marche', steps_h2="Du départ à l'écoute, en trois étapes",
    step1_h='Activez Route', step1_p="Un interrupteur. Choisissez vos centres d'intérêt — histoire, nature, art, gastronomie — ou saisissez les vôtres.",
    step2_h='Marchez, pédalez, roulez ou prenez le train', step2_p="2R suit votre itinéraire par GPS et cherche en direct ce qui vaut la peine d'être raconté — à partir de sources locales, pas seulement Wikipédia.",
    step3_h='Écoutez Route', step3_p="Une voix chaleureuse et expressive raconte — honnêtement, sur ce que vous pouvez réellement voir, jamais en faisant semblant.",
    why_eyebrow='Pourquoi 2R est différent', why_h2='Pas une encyclopédie. Un compagnon de voyage.',
    why_p="Les applications de guide de voyage existantes reposent sur des scripts préenregistrés — limitées aux itinéraires populaires, la même histoire pour tout le monde. 2R génère en direct, partout, et s'adapte à vos centres d'intérêt.",
    f1_h="Les sources locales d'abord", f1_p="Sites municipaux, offices de tourisme et organisations patrimoniales — pas seulement Wikipédia. À l'étranger, les sources en langue locale sont utilisées puis racontées dans votre propre langue.",
    f2_h='Mode guide', f2_p='Un récit continu avec la région comme fil conducteur — pays, province, terroir, ville — plutôt que des faits isolés.',
    f3_h='Toujours honnête', f3_p='Route ne prétend jamais savoir ce que vous voyez. Tout près : "regardez". Plus loin : "vaut le détour" — jamais l\'inverse.',
    f4_h="La confidentialité d'abord", f4_p="Aucune conservation de localisation, aucun compte requis. Chaque requête est indépendante.",
    f5_h='Solo ou en famille', f5_p="Vos propres centres d'intérêt, ou une écoute partagée — avec des jeux et des quiz pour la route en préparation.",
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
    hero_lede='Camines, pedalees, viajes en tren o en coche: tu navegador te indica el camino — <b>2 Route</b> cuenta la historia de ese camino, de forma espontánea o como un relato sonoro cuidadosamente construido.',
    hero_btn_demo='Escucha una historia', hero_btn_roadmap='Recorre un tramo con nosotros',
    hero_caption_coord='52,1045° N', hero_caption_note='Una tarde en la carretera · Utrecht',
    listen_label='01 · Una voz a tu lado', listen_h2='El mundo de fuera se convierte<br>en una historia dentro.',
    listen_p='Sin listas de datos. Route elige una historia con sentido, la cuenta con calma y luego vuelve a dejar espacio para el paisaje —y para vosotros.',
    listen_now='Route está contando', listen_title='Los túmulos<br>del brezal de Stulp', listen_sub='Fragmento real (en neerlandés) · el paseo sonoro de Drakensteyn',
    journey_label='02 · Europa viaja contigo', journey_route_label='Europa · Ruta 02', journey_route_meta='cuatro puntos cardinales · un solo viaje',
    invite_label='Para la próxima vez que salgas de camino', invite_h2='¿Qué te contará Route<br>en tu próximo viaje?',
    invite_p='Llévate una voz cálida, un diario de viaje vivo y un poco de asombro.', invite_btn='Llévate a Route',
    footer_tagline='No el destino — el viaje es lo que nos hace sabios.',
    footer_credit='Creado por Roel Nentjes, junto con Claude (Anthropic).',
    stat1_num='9', stat1_lbl='categorías de interés — cada una probada individualmente',
    stat2_num='6', stat2_lbl='idiomas en este sitio — la app narra primero en neerlandés',
    stat3_num='4', stat3_lbl='modos — a pie, bici, tren, coche', stat4_num='∞', stat4_lbl='lugares — en cualquier sitio, en vivo',
    steps_eyebrow='Cómo funciona', steps_h2='De salir de camino a escuchar, en tres pasos',
    step1_h='Activa Route', step1_p='Un interruptor. Elige tus intereses —historia, naturaleza, arte, gastronomía— o escribe los tuyos.',
    step2_h='Camina, pedalea, conduce o toma el tren', step2_p='2R sigue tu ruta por GPS y busca en vivo qué vale la pena contar —a partir de fuentes locales, no solo Wikipedia.',
    step3_h='Escucha a Route', step3_p='Una voz cálida y expresiva narra —con honestidad sobre lo que realmente puedes ver, nunca fingiendo.',
    why_eyebrow='Por qué 2R es diferente', why_h2='No es una enciclopedia. Es un compañero de viaje.',
    why_p='Las apps de narración de viajes existentes usan guiones pregrabados —limitadas a rutas populares, la misma historia para todos. 2R genera en vivo, en cualquier lugar, y se adapta a tus intereses.',
    f1_h='Fuentes locales primero', f1_p='Webs municipales, oficinas de turismo y organizaciones patrimoniales —no solo Wikipedia. En el extranjero se usan fuentes en el idioma local y se cuentan en tu propio idioma.',
    f2_h='Modo guía', f2_p='Una historia continua con la región como hilo conductor —país, provincia, comarca, localidad— en lugar de datos aislados.',
    f3_h='Siempre honesto', f3_p='Route nunca finge saber lo que puedes ver. Cerca: "mira ahora". Más lejos: "vale la pena el desvío" —nunca al revés.',
    f4_h='La privacidad primero', f4_p='Sin almacenamiento de ubicación, sin necesidad de cuenta. Cada solicitud es independiente.',
    f5_h='Individual o en familia', f5_p='Tus propios intereses, o escuchar juntos —con juegos y quizzes para el camino en desarrollo.',
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
    hero_lede='Caminhando, pedalando, de comboio ou de carro: seu navegador mostra o caminho — <b>2 Route</b> conta a história desse caminho, de forma espontânea ou como uma história sonora cuidadosamente construída.',
    hero_btn_demo='Ouça uma história', hero_btn_roadmap='Ande um trecho com a gente',
    hero_caption_coord='52,1045° N', hero_caption_note='Uma noite na estrada · Utrecht',
    listen_label='01 · Uma voz ao seu lado', listen_h2='O mundo de fora se torna<br>uma história por dentro.',
    listen_p='Nenhuma lista de fatos. A Route escolhe uma história com significado, narra com calma e depois abre espaço de novo para a paisagem — e para vocês.',
    listen_now='A Route está narrando', listen_title='Os túmulos<br>da charneca de Stulp', listen_sub='Trecho real (em neerlandês) · o passeio sonoro de Drakensteyn',
    journey_label='02 · A Europa viaja com você', journey_route_label='Europa · Rota 02', journey_route_meta='quatro pontos cardeais · uma só viagem',
    invite_label='Para a próxima vez que você se puser a caminho', invite_h2='O que a Route vai contar<br>na sua próxima viagem?',
    invite_p='Leve uma voz calorosa, um diário de viagem vivo e um pouco de encantamento.', invite_btn='Leve a Route com você',
    footer_tagline='Não o destino — a viagem é o que nos torna sábios.',
    footer_credit='Criado por Roel Nentjes, com a Claude (Anthropic).',
    stat1_num='9', stat1_lbl='categorias de interesse — cada uma testada individualmente',
    stat2_num='6', stat2_lbl='idiomas neste site — o app narra primeiro em neerlandês',
    stat3_num='4', stat3_lbl='modos — a pé, bici, comboio, carro', stat4_num='∞', stat4_lbl='lugares — em qualquer lugar, ao vivo',
    steps_eyebrow='Como funciona', steps_h2='Do caminho ao ouvir, em três passos',
    step1_h='Ative a Route', step1_p='Um interruptor. Escolha seus interesses — história, natureza, arte, gastronomia — ou digite os seus.',
    step2_h='Caminhe, pedale, dirija ou pegue o comboio', step2_p='O 2R segue sua rota por GPS e busca ao vivo o que vale a pena contar — de fontes locais, não só a Wikipédia.',
    step3_h='Ouça a Route', step3_p='Uma voz calorosa e expressiva narra — com honestidade sobre o que você realmente pode ver, nunca fingindo.',
    why_eyebrow='Por que o 2R é diferente', why_h2='Não é uma enciclopédia. É um companheiro de viagem.',
    why_p='Os apps de narração de viagem existentes usam roteiros pré-gravados — limitados a rotas populares, a mesma história para todos. O 2R gera ao vivo, em qualquer lugar, e se adapta aos seus interesses.',
    f1_h='Fontes locais primeiro', f1_p='Sites municipais, órgãos de turismo e organizações de patrimônio — não só a Wikipédia. No exterior, fontes no idioma local são usadas e recontadas no seu próprio idioma.',
    f2_h='Modo guia', f2_p='Uma história contínua com a região como fio condutor — país, província, região, cidade — em vez de fatos isolados.',
    f3_h='Sempre honesto', f3_p='A Route nunca finge saber o que você pode ver. Perto: "olhe agora". Mais longe: "vale o desvio" — nunca o contrário.',
    f4_h='Privacidade em primeiro lugar', f4_p='Sem armazenamento de localização, sem conta necessária. Cada solicitação é independente.',
    f5_h='Individual ou em família', f5_p='Seus próprios interesses, ou ouvir juntos — com jogos e quizzes para a estrada a caminho.',
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
# Website 2.0 — multimodale positionering
# De hero blijft poëtisch; productuitleg volgt pas in de hoofdstukken eronder.
# ---------------------------------------------------------------------------
HOME_20 = {
'nl': dict(
    nav_home='Ontdek 2R', nav_partners='Voor routebeheerders', nav_cta='Neem 2R mee →',
    hero_alt='Twee reizigers wandelen langs een oude Europese stad; verderop staan een fiets, een regionale trein en een landweg voor vier manieren van reizen.',
    hero_eyebrow='De reisgenoot die de wereld een stem geeft',
    hero_lede='2R geeft de wereld onderweg een stem. Wandel, fiets, reis met de trein of rijd — en hoor de verhalen achter de plekken die je passeert.',
    hero_primary='Hoor hoe 2R klinkt', hero_secondary='Ontdek luisterroutes',
    hero_caption='Te voet, op de fiets, per trein of met de auto · Europa',
    ways_label='Twee manieren om te luisteren', ways_h2='Laat je verrassen.<br>Of volg het hele verhaal.',
    ways_p='Soms wil je zonder plan op pad. Soms wil je een route die van het eerste tot het laatste hoofdstuk klopt. 2R beweegt met beide reizen mee.',
    free_label='01 · Vrij op pad', free_h='De wereld vertelt waar je bent.',
    free_p='Zet 2R aan en luister naar wat zich om je heen aandient. De verteller kijkt vooruit, kiest uit lokale bronnen en stemt ieder verhaal af op jouw tempo en interesses.',
    free_cta='Zo werkt vrij luisteren',
    book_label='02 · Luisterroute', book_h='Een route met een begin en een einde.',
    book_p='Volg een wandel- of fietsroute als levend reisboek: hoofdstukken op precies de goede plek, één rode draad en een slot dat de cirkel rond maakt.',
    book_cta='Ontdek luisterroutes',
    modes_label='Vier reistempo’s', modes_h2='Ieder tempo ziet een andere wereld.',
    modes_p='2R vertelt niet simpelweg vaker of minder vaak. De blik, afstand en vertelvorm veranderen mee met de manier waarop je reist.',
    europe_label='Overal in Europa', europe_h2='De bron is lokaal.<br>Het verhaal reist met je mee.',
    europe_p='Van een Noors fjord tot de olijfgaarden van Puglia: 2R zoekt naar de verhalen die bij een plek horen — liefst in lokale bronnen — en vertelt ze opnieuw in jouw taal.',
    europe_route='Europa · levend reisboek', europe_meta='vier streken · vier soorten kennis',
    modes=[
        ('Te voet', 'Dicht op het landschap. Paden, gebouwen en kleine sporen krijgen alle ruimte.'),
        ('Op de fiets', 'Het landschap ontvouwt zich. Dorpen en verhalen verbinden zich onderweg.'),
        ('Met de trein', 'Kijk naar buiten terwijl streken, steden en tijdlagen aan het raam voorbijtrekken.'),
        ('Met de auto', 'De weg wordt meer dan de afstand ertussenin — zonder je navigatie in de weg te zitten.'),
    ],
    partner_label='Voor routebeheerders en uitgevers', partner_h2='Uw route wijst de weg.<br>2R geeft haar een stem.',
    partner_p='Van GPX, wandelgids of erfgoedarchief naar een zorgvuldig verteld, meertalig routeboek — te beleven in de app, op het web of via een QR-code.',
    partner_cta='Laat één route proefvertellen', partner_more='Ontdek 2R voor routebeheerders',
),
'en': dict(
    nav_home='Discover 2R', nav_partners='For route publishers', nav_cta='Take 2R with you →',
    hero_alt='Two travellers walk beside an old European town; a bicycle, regional train and country road suggest four ways of travelling.',
    hero_eyebrow='The travel companion that gives the world a voice',
    hero_lede='2R gives the world a voice as you travel. Walk, cycle, take the train or drive — and hear the stories behind the places you pass.',
    hero_primary='Hear what 2R sounds like', hero_secondary='Discover listening routes',
    hero_caption='On foot, by bicycle, train or car · Europe',
    ways_label='Two ways to listen', ways_h2='Let the world surprise you.<br>Or follow the whole story.',
    ways_p='Sometimes you set out without a plan. Sometimes you want a route that makes sense from its first chapter to its last. 2R travels with both.',
    free_label='01 · Roam freely', free_h='The world tells you where you are.',
    free_p='Turn on 2R and listen to what appears around you. The narrator looks ahead, draws from local sources and adapts each story to your pace and interests.',
    free_cta='How free listening works',
    book_label='02 · Listening route', book_h='A route with a beginning and an ending.',
    book_p='Follow a walk or cycle route as a living travel book: chapters in exactly the right place, one narrative thread and an ending that closes the circle.',
    book_cta='Discover listening routes',
    modes_label='Four travelling rhythms', modes_h2='Every pace reveals a different world.',
    modes_p='2R does more than speak more or less often. Its perspective, range and storytelling change with the way you travel.',
    europe_label='Across Europe', europe_h2='The source is local.<br>The story travels with you.',
    europe_p='From a Norwegian fjord to the olive groves of Puglia, 2R looks for the stories that belong to a place — preferably in local sources — and retells them in your language.',
    europe_route='Europe · living travel book', europe_meta='four regions · four kinds of knowledge',
    modes=[
        ('On foot', 'Close to the landscape. Paths, buildings and small traces are given room.'),
        ('By bicycle', 'The landscape unfolds. Villages and stories connect along the way.'),
        ('By train', 'Look outside as regions, cities and layers of time pass the window.'),
        ('By car', 'The road becomes more than the distance in between — without getting in the way of navigation.'),
    ],
    partner_label='For route stewards and publishers', partner_h2='Your route shows the way.<br>2R gives it a voice.',
    partner_p='From GPX file, walking guide or heritage archive to a carefully narrated, multilingual route book — in the app, on the web or through a QR code.',
    partner_cta='Let us narrate one pilot route', partner_more='Discover 2R for route publishers',
),
'de': dict(
    nav_home='2R entdecken', nav_partners='Für Routenanbieter', nav_cta='2R mitnehmen →',
    hero_alt='Zwei Reisende wandern an einer alten europäischen Stadt entlang; Fahrrad, Regionalzug und Landstraße stehen für vier Arten des Reisens.',
    hero_eyebrow='Der Reisebegleiter, der der Welt eine Stimme gibt',
    hero_lede='2R gibt der Welt unterwegs eine Stimme. Wandere, fahre Rad, nimm den Zug oder das Auto — und höre die Geschichten hinter den Orten, an denen du vorbeikommst.',
    hero_primary='Hör, wie 2R klingt', hero_secondary='Hörrouten entdecken',
    hero_caption='Zu Fuß, mit dem Rad, der Bahn oder dem Auto · Europa',
    ways_label='Zwei Arten zuzuhören', ways_h2='Lass dich überraschen.<br>Oder folge der ganzen Geschichte.',
    ways_p='Manchmal ziehst du ohne Plan los. Manchmal möchtest du eine Route, die vom ersten bis zum letzten Kapitel trägt. 2R begleitet beides.',
    free_label='01 · Frei unterwegs', free_h='Die Welt erzählt, wo du bist.',
    free_p='Schalte 2R ein und höre, was dir unterwegs begegnet. Der Erzähler blickt voraus, nutzt lokale Quellen und stimmt jede Geschichte auf dein Tempo und deine Interessen ab.',
    free_cta='So funktioniert freies Hören',
    book_label='02 · Hörroute', book_h='Eine Route mit Anfang und Ende.',
    book_p='Erlebe eine Wander- oder Radroute als lebendiges Reisebuch: Kapitel am richtigen Ort, ein roter Faden und ein Ende, das den Kreis schließt.',
    book_cta='Hörrouten entdecken',
    modes_label='Vier Reiserhythmen', modes_h2='Jedes Tempo zeigt eine andere Welt.',
    modes_p='2R erzählt nicht einfach nur häufiger oder seltener. Blick, Entfernung und Erzählform verändern sich mit deiner Reiseart.',
    europe_label='Überall in Europa', europe_h2='Die Quelle ist lokal.<br>Die Geschichte reist mit dir.',
    europe_p='Vom norwegischen Fjord bis zu den Olivenhainen Apuliens sucht 2R die Geschichten, die zu einem Ort gehören — vorzugsweise in lokalen Quellen — und erzählt sie in deiner Sprache neu.',
    europe_route='Europa · lebendiges Reisebuch', europe_meta='vier Regionen · vier Arten von Wissen',
    modes=[
        ('Zu Fuß', 'Ganz nah an der Landschaft. Wege, Gebäude und kleine Spuren bekommen Raum.'),
        ('Mit dem Rad', 'Die Landschaft entfaltet sich. Dörfer und Geschichten verbinden sich unterwegs.'),
        ('Mit der Bahn', 'Schau hinaus, während Regionen, Städte und Zeitschichten am Fenster vorbeiziehen.'),
        ('Mit dem Auto', 'Die Straße wird mehr als die Entfernung dazwischen — ohne die Navigation zu stören.'),
    ],
    partner_label='Für Routenanbieter und Verlage', partner_h2='Ihre Route zeigt den Weg.<br>2R gibt ihr eine Stimme.',
    partner_p='Von GPX-Datei, Wanderführer oder Kulturerbe-Archiv zum sorgfältig erzählten, mehrsprachigen Routenbuch — in der App, im Web oder per QR-Code.',
    partner_cta='Eine Pilotroute erzählen lassen', partner_more='2R für Routenanbieter entdecken',
),
'fr': dict(
    nav_home='Découvrir 2R', nav_partners='Pour les éditeurs', nav_cta='Emporter 2R →',
    hero_alt="Deux voyageurs marchent près d'une ancienne ville européenne ; un vélo, un train régional et une route de campagne évoquent quatre façons de voyager.",
    hero_eyebrow='Le compagnon de voyage qui donne une voix au monde',
    hero_lede='2R donne une voix au monde en chemin. Marchez, pédalez, prenez le train ou la voiture — et écoutez les histoires qui se cachent derrière les lieux traversés.',
    hero_primary='Écouter la voix de 2R', hero_secondary="Découvrir les routes d'écoute",
    hero_caption='À pied, à vélo, en train ou en voiture · Europe',
    ways_label="Deux façons d'écouter", ways_h2="Laissez-vous surprendre.<br>Ou suivez toute l'histoire.",
    ways_p="Parfois, on part sans programme. Parfois, on veut un itinéraire qui se tient du premier au dernier chapitre. 2R accompagne les deux voyages.",
    free_label='01 · Partir librement', free_h='Le monde raconte où vous êtes.',
    free_p="Lancez 2R et écoutez ce qui se présente autour de vous. Le narrateur regarde devant, s'appuie sur des sources locales et adapte chaque récit à votre rythme et à vos intérêts.",
    free_cta="Comment fonctionne l'écoute libre",
    book_label="02 · Route d'écoute", book_h='Un itinéraire avec un début et une fin.',
    book_p="Suivez une randonnée ou une route cyclable comme un livre de voyage vivant : des chapitres au bon endroit, un fil rouge et une fin qui boucle la boucle.",
    book_cta="Découvrir les routes d'écoute",
    modes_label='Quatre rythmes de voyage', modes_h2='Chaque rythme révèle un autre monde.',
    modes_p='2R ne se contente pas de parler plus ou moins souvent. Le regard, la distance et la narration évoluent avec votre façon de voyager.',
    europe_label='Partout en Europe', europe_h2='La source est locale.<br>Le récit voyage avec vous.',
    europe_p="D'un fjord norvégien aux oliveraies des Pouilles, 2R cherche les histoires propres à chaque lieu — de préférence dans des sources locales — et les raconte dans votre langue.",
    europe_route='Europe · carnet de voyage vivant', europe_meta='quatre régions · quatre formes de savoir',
    modes=[
        ('À pied', "Au plus près du paysage. Sentiers, bâtiments et petites traces ont tout l'espace nécessaire."),
        ('À vélo', 'Le paysage se déploie. Villages et histoires se relient en chemin.'),
        ('En train', 'Regardez dehors : régions, villes et strates du temps défilent à la fenêtre.'),
        ('En voiture', "La route devient plus que la distance entre deux lieux — sans gêner la navigation."),
    ],
    partner_label='Pour les gestionnaires et éditeurs de routes', partner_h2='Votre route montre le chemin.<br>2R lui donne une voix.',
    partner_p="D'un fichier GPX, guide de randonnée ou fonds patrimonial à un livre de route multilingue soigneusement raconté — dans l'app, sur le web ou par QR code.",
    partner_cta='Faire raconter une route pilote', partner_more='Découvrir 2R pour les éditeurs',
),
'es': dict(
    nav_home='Descubre 2R', nav_partners='Para editores de rutas', nav_cta='Lleva 2R contigo →',
    hero_alt='Dos viajeros caminan junto a una antigua ciudad europea; una bicicleta, un tren regional y una carretera rural representan cuatro formas de viajar.',
    hero_eyebrow='El compañero de viaje que da voz al mundo',
    hero_lede='2R da voz al mundo mientras viajas. Camina, pedalea, toma el tren o conduce — y escucha las historias que hay detrás de los lugares por los que pasas.',
    hero_primary='Escucha cómo suena 2R', hero_secondary='Descubre rutas sonoras',
    hero_caption='A pie, en bicicleta, tren o coche · Europa',
    ways_label='Dos maneras de escuchar', ways_h2='Déjate sorprender.<br>O sigue la historia completa.',
    ways_p='A veces sales sin plan. Otras quieres una ruta que tenga sentido desde el primer capítulo hasta el último. 2R acompaña ambos viajes.',
    free_label='01 · Viajar libremente', free_h='El mundo te cuenta dónde estás.',
    free_p='Activa 2R y escucha lo que aparece a tu alrededor. El narrador mira hacia delante, consulta fuentes locales y adapta cada relato a tu ritmo e intereses.',
    free_cta='Cómo funciona la escucha libre',
    book_label='02 · Ruta sonora', book_h='Una ruta con principio y final.',
    book_p='Sigue una ruta a pie o en bicicleta como un libro de viaje vivo: capítulos en el lugar adecuado, un hilo conductor y un final que cierra el círculo.',
    book_cta='Descubre rutas sonoras',
    modes_label='Cuatro ritmos de viaje', modes_h2='Cada ritmo revela un mundo diferente.',
    modes_p='2R no se limita a hablar más o menos. La mirada, la distancia y la forma de narrar cambian según cómo viajes.',
    europe_label='Por toda Europa', europe_h2='La fuente es local.<br>La historia viaja contigo.',
    europe_p='Desde un fiordo noruego hasta los olivares de Apulia, 2R busca las historias que pertenecen a cada lugar — preferentemente en fuentes locales — y las vuelve a contar en tu idioma.',
    europe_route='Europa · libro de viaje vivo', europe_meta='cuatro regiones · cuatro formas de conocimiento',
    modes=[
        ('A pie', 'Muy cerca del paisaje. Senderos, edificios y pequeñas huellas tienen su espacio.'),
        ('En bicicleta', 'El paisaje se despliega. Pueblos e historias se conectan por el camino.'),
        ('En tren', 'Mira por la ventana mientras pasan regiones, ciudades y capas de tiempo.'),
        ('En coche', 'La carretera se convierte en algo más que la distancia entre dos puntos, sin estorbar a la navegación.'),
    ],
    partner_label='Para gestores y editores de rutas', partner_h2='Tu ruta muestra el camino.<br>2R le da voz.',
    partner_p='De un archivo GPX, una guía de senderismo o un archivo patrimonial a un libro de ruta multilingüe y cuidadosamente narrado — en la app, la web o mediante un código QR.',
    partner_cta='Deja que narremos una ruta piloto', partner_more='Descubre 2R para editores',
),
'pt': dict(
    nav_home='Descobrir 2R', nav_partners='Para editores de rotas', nav_cta='Levar 2R consigo →',
    hero_alt='Dois viajantes caminham junto a uma antiga cidade europeia; uma bicicleta, um comboio regional e uma estrada rural sugerem quatro formas de viajar.',
    hero_eyebrow='O companheiro de viagem que dá voz ao mundo',
    hero_lede='O 2R dá voz ao mundo durante a viagem. Caminhe, pedale, apanhe o comboio ou conduza — e ouça as histórias por detrás dos lugares por onde passa.',
    hero_primary='Ouça como soa o 2R', hero_secondary='Descubra rotas para ouvir',
    hero_caption='A pé, de bicicleta, comboio ou carro · Europa',
    ways_label='Duas formas de ouvir', ways_h2='Deixe-se surpreender.<br>Ou siga a história inteira.',
    ways_p='Às vezes parte sem plano. Outras vezes quer uma rota que faça sentido do primeiro ao último capítulo. O 2R acompanha ambas.',
    free_label='01 · Viajar livremente', free_h='O mundo conta onde está.',
    free_p='Ligue o 2R e ouça o que surge à sua volta. O narrador olha em frente, recorre a fontes locais e adapta cada história ao seu ritmo e interesses.',
    free_cta='Como funciona a escuta livre',
    book_label='02 · Rota para ouvir', book_h='Uma rota com princípio e fim.',
    book_p='Siga um percurso pedestre ou de bicicleta como um livro de viagem vivo: capítulos no lugar certo, um fio condutor e um final que fecha o círculo.',
    book_cta='Descubra rotas para ouvir',
    modes_label='Quatro ritmos de viagem', modes_h2='Cada ritmo revela um mundo diferente.',
    modes_p='O 2R não se limita a falar mais ou menos. O olhar, a distância e a narrativa mudam com a forma de viajar.',
    europe_label='Por toda a Europa', europe_h2='A fonte é local.<br>A história viaja consigo.',
    europe_p='De um fiorde norueguês aos olivais da Apúlia, o 2R procura as histórias que pertencem a cada lugar — de preferência em fontes locais — e volta a contá-las na sua língua.',
    europe_route='Europa · livro de viagem vivo', europe_meta='quatro regiões · quatro formas de conhecimento',
    modes=[
        ('A pé', 'Perto da paisagem. Caminhos, edifícios e pequenos vestígios ganham espaço.'),
        ('De bicicleta', 'A paisagem abre-se. Aldeias e histórias ligam-se pelo caminho.'),
        ('De comboio', 'Olhe pela janela enquanto regiões, cidades e camadas do tempo passam.'),
        ('De carro', 'A estrada torna-se mais do que a distância entre lugares — sem interferir com a navegação.'),
    ],
    partner_label='Para gestores e editores de rotas', partner_h2='A sua rota mostra o caminho.<br>O 2R dá-lhe voz.',
    partner_p='De um ficheiro GPX, guia pedestre ou arquivo patrimonial a um livro de rota multilingue e cuidadosamente narrado — na app, na web ou através de QR code.',
    partner_cta='Deixe-nos narrar uma rota-piloto', partner_more='Descubra o 2R para editores',
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
        '<strong>Standaard wordt je locatie niet opgeslagen en niet gelogd.</strong> Om te bepalen wat je passeert stuurt de app je actuele positie mee met een verhaal-verzoek; de server gebruikt die om de juiste plek te kiezen en bewaart hem niet. Er wordt geen locatiegeschiedenis of rittenregistratie opgebouwd.',
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
    h_data='Wat we wél bewaren',
    data_items=[
        "<strong>Technische gebeurtenissen.</strong> De app meldt aan onze server welk verhaal is verteld, over welke plek, hoelang het maken duurde en of er iets misging — met een willekeurig sessienummer per app-start. Zo zien we of 2R goed werkt. Deze logboeken bevatten standaard geen GPS-positie.",
        "<strong>Het verhalenarchief.</strong> Elk verteld verhaal bewaren we integraal: de tekst, de plek waar het verhaal over gaat en, bij testers, de opgegeven naam. Zo kunnen we teruglezen wat er verteld is en de mooiste verhalen cureren voor deze site. De positie van de reiziger bewaren we daarbij niet.",
        "<strong>Aankopen.</strong> Koop je een abonnement of tegoed, dan registreren we de transactie die Apple ons doorgeeft, samen met een anoniem apparaatnummer. Dat nummer staat los van je naam en is nodig om je aankoop te herkennen — ook na een herinstallatie. Betaalgegevens zien wij nooit; die blijven bij Apple.",
        "<strong>Bewaartermijn &amp; wissen.</strong> Deze gegevens bewaren we zolang 2R in ontwikkeling is. Wil je dat we iets van jou wissen — bijvoorbeeld je testernaam of je verhalen — mail ons, dan verwijderen we het.",
    ],
    h_accounts='Accounts',
    accounts_text='De app vereist geen account, inloggen of registratie. Testers kunnen vrijwillig een naam invullen; die naam reist mee met hun verhalen en aankopen zodat we de testfase kunnen volgen, en wordt op verzoek gewist.',
    h_contact='Contact',
    contact_text='Vragen over dit beleid? Mail naar <a href="mailto:nimco@nentjes.nl">nimco@nentjes.nl</a>.',
),
'en': dict(
    eyebrow='Privacy', title='Privacy Policy — 2R', updated='Last updated: August 2026',
    intro="2R (working title: MapsInfo) is a travel-guide app that narrates the world around you while you drive, cycle or walk. This policy explains exactly what data the app uses and why — no fine print.",
    h_location='Location',
    location_items=[
        'Your GPS location is used to determine which stories are relevant.',
        '<strong>By default your location is never stored and never logged.</strong> To work out what you are passing, the app sends your current position along with a story request; the server uses it to pick the right place and does not keep it. No location history or trip log is ever built up.',
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
    h_data='What we do keep',
    data_items=[
        "<strong>Technical events.</strong> The app tells our server which story was told, about which place, how long it took to generate and whether anything went wrong — with a random session number per app start. That is how we see whether 2R works well. These logs contain no GPS position by default.",
        "<strong>The story archive.</strong> Every story that is told is kept in full: the text, the place the story is about and, for testers, the name they entered. It lets us read back what was told and curate the best stories for this site. The traveller's position is not stored with it.",
        "<strong>Purchases.</strong> If you buy a subscription or credit, we record the transaction Apple passes on to us, together with an anonymous device number. That number is unrelated to your name and is needed to recognise your purchase — including after a reinstall. We never see payment details; those stay with Apple.",
        "<strong>Retention &amp; deletion.</strong> We keep this data while 2R is in development. Want something of yours removed — your tester name, your stories? Email us and we will delete it.",
    ],
    h_accounts='Accounts',
    accounts_text='The app requires no account, login or registration. Testers may voluntarily enter a name; it travels with their stories and purchases so we can follow the test phase, and is deleted on request.',
    h_contact='Contact',
    contact_text='Questions about this policy? Email <a href="mailto:nimco@nentjes.nl">nimco@nentjes.nl</a>.',
),
'de': dict(
    eyebrow='Datenschutz', title='Datenschutzerklärung — 2R', updated='Zuletzt aktualisiert: August 2026',
    intro='2R (Arbeitstitel: MapsInfo) ist eine Reiseführer-App, die während der Fahrt, beim Radfahren oder Wandern gesprochene Geschichten über die Umgebung erzählt. Diese Erklärung beschreibt genau, welche Daten die App verwendet und warum — ohne Kleingedrucktes.',
    h_location='Standort',
    location_items=[
        'Dein GPS-Standort wird verwendet, um zu bestimmen, welche Geschichten relevant sind.',
        '<strong>Standardmäßig wird dein Standort nicht gespeichert und nicht protokolliert.</strong> Um zu bestimmen, woran du gerade vorbeikommst, sendet die App deine aktuelle Position mit einer Geschichten-Anfrage mit; der Server nutzt sie, um den richtigen Ort zu wählen, und bewahrt sie nicht auf. Es entsteht kein Standortverlauf und keine Fahrtenaufzeichnung.',
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
    h_data='Was wir wohl aufbewahren',
    data_items=[
        "<strong>Technische Ereignisse.</strong> Die App meldet unserem Server, welche Geschichte erzählt wurde, über welchen Ort, wie lange die Erstellung dauerte und ob etwas schiefging — mit einer zufälligen Sitzungsnummer pro App-Start. So sehen wir, ob 2R gut funktioniert. Diese Protokolle enthalten standardmäßig keine GPS-Position.",
        "<strong>Das Geschichtenarchiv.</strong> Jede erzählte Geschichte bewahren wir vollständig auf: den Text, den Ort, um den es geht, und bei Testern den angegebenen Namen. So können wir nachlesen, was erzählt wurde, und die schönsten Geschichten für diese Website kuratieren. Die Position des Reisenden speichern wir dabei nicht.",
        "<strong>Käufe.</strong> Kaufst du ein Abonnement oder Guthaben, registrieren wir die Transaktion, die Apple uns übermittelt, zusammen mit einer anonymen Gerätenummer. Diese Nummer ist nicht mit deinem Namen verknüpft und wird gebraucht, um deinen Kauf wiederzuerkennen — auch nach einer Neuinstallation. Zahlungsdaten sehen wir nie; die bleiben bei Apple.",
        "<strong>Aufbewahrung &amp; Löschung.</strong> Diese Daten bewahren wir auf, solange sich 2R in Entwicklung befindet. Sollen wir etwas von dir löschen — deinen Testernamen, deine Geschichten? Schreib uns eine E-Mail, dann entfernen wir es.",
    ],
    h_accounts='Konten',
    accounts_text='Die App erfordert kein Konto, keine Anmeldung und keine Registrierung. Tester können freiwillig einen Namen angeben; er begleitet ihre Geschichten und Käufe, damit wir die Testphase nachvollziehen können, und wird auf Wunsch gelöscht.',
    h_contact='Kontakt',
    contact_text='Fragen zu dieser Erklärung? Schreib an <a href="mailto:nimco@nentjes.nl">nimco@nentjes.nl</a>.',
),
'fr': dict(
    eyebrow='Confidentialité', title='Politique de confidentialité — 2R', updated='Dernière mise à jour : août 2026',
    intro="2R (nom de travail : MapsInfo) est une application de guide de voyage qui raconte à voix haute ce qui vous entoure pendant que vous conduisez, roulez à vélo ou marchez. Cette politique explique précisément quelles données l'application utilise, et pourquoi — sans petits caractères.",
    h_location='Localisation',
    location_items=[
        'Votre position GPS est utilisée pour déterminer quelles histoires sont pertinentes.',
        "<strong>Par défaut, votre position n'est jamais stockée ni journalisée.</strong> Pour déterminer ce que vous croisez, l'application joint votre position actuelle à une requête d'histoire ; le serveur s'en sert pour choisir le bon lieu et ne la conserve pas. Aucun historique de localisation ni suivi de trajet n'est constitué.",
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
    h_data='Ce que nous conservons',
    data_items=[
        "<strong>Événements techniques.</strong> L'application signale à notre serveur quelle histoire a été racontée, sur quel lieu, combien de temps la génération a pris et si quelque chose a échoué — avec un numéro de session aléatoire à chaque démarrage. C'est ainsi que nous voyons si 2R fonctionne bien. Par défaut, ces journaux ne contiennent aucune position GPS.",
        "<strong>L'archive des histoires.</strong> Chaque histoire racontée est conservée intégralement : le texte, le lieu dont elle parle et, pour les testeurs, le nom saisi. Cela nous permet de relire ce qui a été raconté et de sélectionner les plus belles histoires pour ce site. La position du voyageur n'y est pas conservée.",
        "<strong>Achats.</strong> Si vous achetez un abonnement ou un crédit, nous enregistrons la transaction transmise par Apple, avec un numéro d'appareil anonyme. Ce numéro n'est pas lié à votre nom et sert à reconnaître votre achat — y compris après une réinstallation. Nous ne voyons jamais vos données de paiement ; elles restent chez Apple.",
        "<strong>Conservation &amp; suppression.</strong> Nous conservons ces données tant que 2R est en développement. Vous voulez que nous supprimions quelque chose — votre nom de testeur, vos histoires ? Écrivez-nous et nous l'effacerons.",
    ],
    h_accounts='Comptes',
    accounts_text="L'application ne nécessite aucun compte, connexion ni inscription. Les testeurs peuvent saisir un nom volontairement ; il accompagne leurs histoires et achats afin de suivre la phase de test, et il est supprimé sur simple demande.",
    h_contact='Contact',
    contact_text='Des questions sur cette politique ? Écrivez à <a href="mailto:nimco@nentjes.nl">nimco@nentjes.nl</a>.',
),
'es': dict(
    eyebrow='Privacidad', title='Política de privacidad — 2R', updated='Última actualización: agosto de 2026',
    intro='2R (nombre provisional: MapsInfo) es una app de guía de viaje que narra en voz alta lo que te rodea mientras conduces, pedaleas o caminas. Esta política explica con precisión qué datos usa la app y por qué — sin letra pequeña.',
    h_location='Ubicación',
    location_items=[
        'Tu ubicación GPS se usa para determinar qué historias son relevantes.',
        '<strong>Por defecto, tu ubicación nunca se almacena ni se registra.</strong> Para saber qué estás pasando, la app envía tu posición actual junto con la solicitud de una historia; el servidor la usa para elegir el lugar correcto y no la conserva. No se construye ningún historial de ubicación ni registro de trayectos.',
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
    h_data='Lo que sí guardamos',
    data_items=[
        "<strong>Eventos técnicos.</strong> La app comunica a nuestro servidor qué historia se contó, sobre qué lugar, cuánto tardó en generarse y si algo falló — con un número de sesión aleatorio por cada inicio. Así vemos si 2R funciona bien. Por defecto, estos registros no contienen ninguna posición GPS.",
        "<strong>El archivo de historias.</strong> Cada historia contada se guarda íntegra: el texto, el lugar del que trata y, en el caso de los testers, el nombre introducido. Nos permite releer lo contado y seleccionar las mejores historias para este sitio. La posición del viajero no se guarda con ello.",
        "<strong>Compras.</strong> Si compras una suscripción o un crédito, registramos la transacción que Apple nos comunica, junto con un número de dispositivo anónimo. Ese número no está vinculado a tu nombre y sirve para reconocer tu compra — también tras una reinstalación. Nunca vemos datos de pago; esos se quedan en Apple.",
        "<strong>Conservación y borrado.</strong> Guardamos estos datos mientras 2R esté en desarrollo. ¿Quieres que borremos algo tuyo — tu nombre de tester, tus historias? Escríbenos y lo eliminamos.",
    ],
    h_accounts='Cuentas',
    accounts_text='La app no requiere ninguna cuenta, inicio de sesión ni registro. Los testers pueden introducir un nombre de forma voluntaria; acompaña sus historias y compras para poder seguir la fase de pruebas, y se elimina si lo piden.',
    h_contact='Contacto',
    contact_text='¿Preguntas sobre esta política? Escribe a <a href="mailto:nimco@nentjes.nl">nimco@nentjes.nl</a>.',
),
'pt': dict(
    eyebrow='Privacidade', title='Política de Privacidade — 2R', updated='Última atualização: agosto de 2026',
    intro='O 2R (nome provisório: MapsInfo) é um app de guia de viagem que narra em voz alta o que está à sua volta enquanto você dirige, pedala ou caminha. Esta política explica exatamente quais dados o app usa e por quê — sem letras miúdas.',
    h_location='Localização',
    location_items=[
        'Sua localização GPS é usada para determinar quais histórias são relevantes.',
        '<strong>Por padrão, sua localização nunca é armazenada nem registrada.</strong> Para saber por onde você está passando, o app envia sua posição atual junto com o pedido de uma história; o servidor a usa para escolher o lugar certo e não a guarda. Nenhum histórico de localização ou registro de trajetos é criado.',
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
    h_data='O que guardamos',
    data_items=[
        "<strong>Eventos técnicos.</strong> O app informa ao nosso servidor qual história foi contada, sobre qual lugar, quanto tempo levou para gerar e se algo deu errado — com um número de sessão aleatório a cada início. Assim vemos se o 2R funciona bem. Por padrão, esses registros não contêm nenhuma posição GPS.",
        "<strong>O arquivo de histórias.</strong> Cada história contada é guardada na íntegra: o texto, o lugar de que trata e, no caso dos testadores, o nome informado. Isso nos permite reler o que foi contado e selecionar as melhores histórias para este site. A posição do viajante não é guardada.",
        "<strong>Compras.</strong> Se você compra uma assinatura ou um crédito, registramos a transação que a Apple nos repassa, junto com um número de aparelho anônimo. Esse número não está ligado ao seu nome e serve para reconhecer sua compra — inclusive após uma reinstalação. Nunca vemos dados de pagamento; esses ficam com a Apple.",
        "<strong>Retenção e exclusão.</strong> Guardamos esses dados enquanto o 2R estiver em desenvolvimento. Quer que apaguemos algo seu — seu nome de testador, suas histórias? Escreva para nós e removemos.",
    ],
    h_accounts='Contas',
    accounts_text='O app não exige conta, login ou registro. Testadores podem informar um nome voluntariamente; ele acompanha suas histórias e compras para acompanharmos a fase de testes, e é apagado mediante pedido.',
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
    ('Noord · Sognefjord, Noorwegen', 'Landschap · geologie', 'De ochtend begint waar de bergen het water raken.', 'Met Noorse bronnen laat 2R horen hoe het ijs dit landschap vormde — duizenden jaren voordat hier een weg of spoorlijn verscheen.'),
    ('West · Bourgogne, Frankrijk', 'Erfgoed · dorpsleven', 'Een abdij verschijnt tussen de platanen.', 'Lokale erfgoedbronnen verbinden de oude stenen met het dorp dat er nog altijd omheen leeft. Geen ansichtkaart, maar een plaats met een geheugen.'),
    ('Oost · Zuid-Bohemen, Tsjechië', 'Architectuur · geschiedenis', 'De toren maakt van de horizon een hoofdstuk.', 'Tsjechische bronnen laten zien hoe bouwstijlen en ideeën vanuit Wenen tot in deze kleine heuvelstad reisden.'),
    ('Zuid · Puglia, Italië', 'Mensen · landschap', 'Het avondlicht brengt iedereen even tot stilte.', 'Lokale verhalen over olijfbouw laten horen hoe mensen, steen en bomen hier al eeuwen samenleven met hitte en droogte.'),
],
'en': [
    ('North · Sognefjord, Norway', 'Landscape · geology', 'The morning begins where the mountains meet the water.', 'Drawing on Norwegian sources, 2R reveals how ice shaped this landscape thousands of years before a road or railway appeared.'),
    ('West · Burgundy, France', 'Heritage · village life', 'An abbey appears between the plane trees.', 'Local heritage sources connect the old stones to the village still living around them. Not a postcard, but a place with a memory.'),
    ('East · South Bohemia, Czechia', 'Architecture · history', 'The tower turns the horizon into a chapter.', 'Czech sources show how architectural styles and ideas travelled from Vienna to this small hilltop town.'),
    ('South · Puglia, Italy', 'People · landscape', 'The evening light brings everyone to a brief stillness.', 'Local stories of olive growing reveal how people, stone and trees have lived together here for centuries, with heat and drought.'),
],
'de': [
    ('Norden · Sognefjord, Norwegen', 'Landschaft · Geologie', 'Der Morgen beginnt dort, wo die Berge das Wasser berühren.', 'Mit norwegischen Quellen zeigt 2R, wie das Eis diese Landschaft formte — Jahrtausende bevor Straße oder Bahn erschienen.'),
    ('Westen · Burgund, Frankreich', 'Kulturerbe · Dorfleben', 'Eine Abtei erscheint zwischen den Platanen.', 'Lokale Kulturerbe-Quellen verbinden die alten Steine mit dem Dorf, das noch immer um sie herum lebt. Keine Postkarte, sondern ein Ort mit Gedächtnis.'),
    ('Osten · Südböhmen, Tschechien', 'Architektur · Geschichte', 'Der Turm macht den Horizont zu einem Kapitel.', 'Tschechische Quellen zeigen, wie Baustile und Ideen von Wien bis in dieses kleine Hügelstädtchen reisten.'),
    ('Süden · Apulien, Italien', 'Menschen · Landschaft', 'Das Abendlicht bringt alle für einen Moment zur Ruhe.', 'Lokale Geschichten vom Olivenanbau erzählen, wie Menschen, Stein und Bäume hier seit Jahrhunderten mit Hitze und Trockenheit leben.'),
],
'fr': [
    ('Nord · Sognefjord, Norvège', 'Paysage · géologie', "Le matin commence là où les montagnes rencontrent l'eau.", "À partir de sources norvégiennes, 2R raconte comment la glace a façonné ce paysage, bien avant l'arrivée des routes et du chemin de fer."),
    ('Ouest · Bourgogne, France', 'Patrimoine · vie du village', 'Une abbaye apparaît entre les platanes.', "Les sources patrimoniales locales relient les vieilles pierres au village qui vit encore autour d'elles. Pas une carte postale, mais un lieu qui a une mémoire."),
    ('Est · Bohême du Sud, Tchéquie', 'Architecture · histoire', "La tour transforme l'horizon en chapitre.", "Les sources tchèques montrent comment styles architecturaux et idées ont voyagé de Vienne jusqu'à cette petite ville sur la colline."),
    ('Sud · Pouilles, Italie', 'Habitants · paysage', "La lumière du soir apaise chacun, l'espace d'un instant.", "Les récits locaux sur l'oléiculture racontent comment habitants, pierre et arbres vivent ici depuis des siècles avec la chaleur et la sécheresse."),
],
'es': [
    ('Norte · Sognefjord, Noruega', 'Paisaje · geología', 'La mañana empieza donde las montañas tocan el agua.', 'A partir de fuentes noruegas, 2R cuenta cómo el hielo modeló este paisaje miles de años antes de que aparecieran la carretera o el ferrocarril.'),
    ('Oeste · Borgoña, Francia', 'Patrimonio · vida del pueblo', 'Una abadía aparece entre los plátanos.', 'Las fuentes patrimoniales locales conectan las piedras antiguas con el pueblo que aún vive a su alrededor. No una postal, sino un lugar con memoria.'),
    ('Este · Bohemia del Sur, Chequia', 'Arquitectura · historia', 'La torre convierte el horizonte en un capítulo.', 'Las fuentes checas muestran cómo los estilos y las ideas viajaron desde Viena hasta esta pequeña ciudad en la colina.'),
    ('Sur · Apulia, Italia', 'Personas · paisaje', 'La luz del atardecer trae a todos, por un momento, la calma.', 'Los relatos locales sobre el cultivo del olivo cuentan cómo personas, piedra y árboles conviven aquí desde hace siglos con el calor y la sequía.'),
],
'pt': [
    ('Norte · Sognefjord, Noruega', 'Paisagem · geologia', 'A manhã começa onde as montanhas tocam a água.', 'Com fontes norueguesas, o 2R conta como o gelo moldou esta paisagem milhares de anos antes de surgirem a estrada ou a ferrovia.'),
    ('Oeste · Borgonha, França', 'Património · vida da aldeia', 'Uma abadia aparece entre os plátanos.', 'Fontes patrimoniais locais ligam as pedras antigas à aldeia que ainda vive ao seu redor. Não um cartão-postal, mas um lugar com memória.'),
    ('Leste · Boêmia do Sul, Tchéquia', 'Arquitetura · história', 'A torre transforma o horizonte num capítulo.', 'Fontes checas mostram como estilos e ideias viajaram de Viena até esta pequena cidade na colina.'),
    ('Sul · Apúlia, Itália', 'Pessoas · paisagem', 'A luz da tarde traz a todos, por um instante, quietude.', 'Histórias locais sobre o cultivo da oliveira contam como pessoas, pedra e árvores convivem aqui há séculos com o calor e a seca.'),
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
    ('live', dict(nl='Het eerste levende routeboek', en='The first living route book', de='Das erste lebendige Routenbuch', fr='Le premier carnet de route vivant', es='El primer libro de ruta vivo', pt='O primeiro livro de rota vivo'),
     dict(nl='Boswachterspad Stulp en Kasteeltuin is online met officiële GPX, eigen kaart, twaalf verbonden hoofdstukken, audio en zeventig geverifieerde feiten.',
          en='The Stulp and Castle Garden forester trail is online with its official GPX, our own map, twelve connected chapters, audio and seventy verified facts.',
          de='Der Boswachterspad Stulp en Kasteeltuin ist online: offizieller GPX-Track, eigene Karte, zwölf verbundene Kapitel, Audio und siebzig geprüfte Fakten.',
          fr='Le sentier forestier Stulp et Jardin du Château est en ligne avec GPX officiel, carte maison, douze chapitres reliés, audio et soixante-dix faits vérifiés.',
          es='El sendero forestal Stulp y Jardín del Castillo está en línea con GPX oficial, mapa propio, doce capítulos conectados, audio y setenta datos verificados.',
          pt='O trilho florestal Stulp e Jardim do Castelo está online com GPX oficial, mapa próprio, doze capítulos conectados, áudio e setenta fatos verificados.')),
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
        nl='2R begon met een vraag tijdens een autorit: wat leeft er eigenlijk achter al die plekken die je passeert? Die vraag bleek veel groter dan de auto. Nu leert 2R wandelen, fietsen, treinreizen en vrije routes verbinden met levende routeboeken.',
        en='2R began with a question during a road trip: what lives behind all the places you pass? The question proved much bigger than the car. Now 2R is bringing walking, cycling, train travel and free exploration together with living route books.',
        de='2R begann mit einer Frage während einer Autofahrt: Was lebt hinter all den Orten, an denen man vorbeikommt? Die Frage war größer als das Auto. Heute verbindet 2R Wandern, Radfahren, Bahnreisen und freies Entdecken mit lebendigen Routenbüchern.',
        fr="2R est né d'une question en voiture : que vit-il derrière tous ces lieux traversés ? La question s'est révélée bien plus vaste que l'automobile. Aujourd'hui, 2R relie marche, vélo, train et exploration libre à des carnets de route vivants.",
        es='2R nació de una pregunta durante un viaje en coche: ¿qué vive detrás de todos los lugares que pasamos? La pregunta resultó mucho mayor que el coche. Hoy 2R une caminar, pedalear, viajar en tren y explorar libremente con libros de ruta vivos.',
        pt='O 2R nasceu de uma pergunta durante uma viagem de carro: o que vive por trás de todos os lugares por onde passamos? A pergunta revelou-se maior do que o carro. Hoje o 2R une caminhada, bicicleta, comboio e exploração livre a livros de rota vivos.'),
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
    h=dict(nl='Reis mee naar het vervolg.', en="Travel with us into what's next.",
           de='Reise mit uns ins nächste Kapitel.', fr='Voyagez avec nous vers la suite.',
           es='Viaja con nosotros hacia lo que viene.', pt='Viaje connosco para o que vem a seguir.'),
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
    lede='2R is je reisgezel die vertelt. Je start hem, je gaat op pad — te voet, met de fiets, in de trein of in de auto — en onderweg hoor je verhalen over de plekken die je passeert. Hieronder alles wat je moet weten — in een paar minuten.',
    sections=[
        dict(h='Beginnen', p='Tik op <b>Start de reis</b>, sta je locatie toe en kies hoe je reist. 2R vertelt vanzelf over de plekken die je passeert — zonder account of voorbereiding.'),
        dict(h='Vrij luisteren of een luisterroute', p='Ga spontaan op pad voor verhalen die bij je actuele omgeving passen, of kies een zorgvuldig opgebouwd routeboek met vaste hoofdstukken en één rode draad.'),
        dict(h='Samen met je muziek', p='Speel gerust je eigen muziek. Die gaat automatisch <b>zachter</b> zodra een verhaal begint en komt daarna weer terug. 2R streamt zelf geen muziek.'),
        dict(h='Luisteren op de achtergrond', p='Gebruik je ondertussen Kaarten of je muziek-app, dan blijft 2R vertellen. Het blauwe locatiesymbool van iOS laat zien dat de app je positie gebruikt; tik erop om naar 2R terug te keren.'),
        dict(h='Je stem kiezen', p='Kies bij <b>Instellingen → Stem</b> een vertelstem en klank die bij je past. Met “Beluister deze stem” hoor je het verschil meteen.'),
        dict(h='Jouw reistempo', p='Wandelen, fietsen, trein en auto vragen elk om een andere blik. 2R past zoekafstand, vertelritme en onderwerpkeuze daarop aan.'),
        dict(h='Rust en samenzijn', p='Pauzeer een verhaal, kies even stilte of speel samen een reisquiz. Jij bepaalt hoeveel ruimte de verteller krijgt.'),
        dict(h='Thuis uitproberen', p='Wil je 2R eerst leren kennen? Gebruik de <b>Route Simulator</b> om een reis na te bootsen zonder echt op pad te gaan.'),
    ],
    cta_h='Klaar om op pad te gaan?', cta_p='2R is beschikbaar voor testers; de openbare release volgt.', cta_btn='Probeer 2R →',
),
'en': dict(
    eyebrow='How 2R works', title='How 2R works',
    lede='2R is your travelling companion that tells stories. You start it, you head out — on foot, by bike, by train or by car — and along the way you hear stories about the places you pass. Here is everything you need to know — in a few minutes.',
    sections=[
        dict(h='Getting started', p='Tap <b>Start the journey</b>, allow location access and choose how you travel. 2R automatically narrates the places you pass — without an account or advance planning.'),
        dict(h='Free listening or a listening route', p='Set out spontaneously for stories that fit your current surroundings, or choose a carefully composed route book with fixed chapters and one narrative thread.'),
        dict(h='Alongside your music', p='Play your own music. It automatically <b>fades down</b> when a story starts and returns afterwards. 2R never streams music itself.'),
        dict(h='Listening in the background', p='Switch to Maps or your music app and 2R keeps narrating. The blue iOS location indicator shows that the app is using your position; tap it to return to 2R.'),
        dict(h='Choosing your voice', p='Under <b>Settings → Voice</b>, choose the narrator and tone that suit you. “Preview this voice” lets you hear the difference immediately.'),
        dict(h='Your travel pace', p='Walking, cycling, train and car each reveal a different world. 2R adapts its search radius, narrative rhythm and subject choices accordingly.'),
        dict(h='Quiet and togetherness', p='Pause a story, choose a moment of silence or play a travel quiz together. You decide how much space the narrator gets.'),
        dict(h='Try it at home', p='Want to get to know 2R first? Use the <b>Route Simulator</b> to recreate a journey without actually setting out.'),
    ],
    cta_h='Ready to head out?', cta_p='2R is available to testers; the public release will follow.', cta_btn='Try 2R →',
),
'de': dict(
    eyebrow='So funktioniert 2R', title='So funktioniert 2R',
    lede='2R ist dein erzählender Reisebegleiter. Du gehst los — zu Fuß, mit dem Rad, per Bahn oder Auto — und hörst unterwegs die Geschichten der Orte, an denen du vorbeikommst.',
    sections=[
        dict(h='Loslegen', p='Tippe auf <b>Reise starten</b>, erlaube den Standortzugriff und wähle deine Reiseart. 2R erzählt automatisch — ohne Konto oder Vorbereitung.'),
        dict(h='Frei hören oder einer Hörroute folgen', p='Lass dich spontan von deiner Umgebung überraschen oder wähle ein sorgfältig komponiertes Routenbuch mit festen Kapiteln und einem roten Faden.'),
        dict(h='Mit deiner Musik', p='Deine eigene Musik wird automatisch <b>leiser</b>, sobald eine Geschichte beginnt, und kehrt danach zurück. 2R streamt selbst keine Musik.'),
        dict(h='Im Hintergrund zuhören', p='Auch wenn du Karten oder deine Musik-App öffnest, erzählt 2R weiter. Das blaue iOS-Standortsymbol zeigt die Standortnutzung; tippe darauf, um zu 2R zurückzukehren.'),
        dict(h='Stimme wählen', p='Wähle unter <b>Einstellungen → Stimme</b> Erzähler und Klang. Mit der Hörprobe erkennst du den Unterschied sofort.'),
        dict(h='Dein Reisetempo', p='Wandern, Radfahren, Bahn und Auto zeigen jeweils eine andere Welt. 2R passt Suchradius, Erzählrhythmus und Themen daran an.'),
        dict(h='Ruhe und Zusammensein', p='Pausiere, wähle einen stillen Moment oder spielt gemeinsam ein Reisequiz. Du bestimmst, wie viel Raum die Stimme bekommt.'),
    ],
    cta_h='Bereit aufzubrechen?', cta_p='2R ist für Tester verfügbar; die öffentliche Veröffentlichung folgt.', cta_btn='2R ausprobieren →',
),
'fr': dict(
    eyebrow='Comment fonctionne 2R', title='Comment fonctionne 2R',
    lede='2R est le compagnon qui raconte votre voyage. Vous partez — à pied, à vélo, en train ou en voiture — et entendez les histoires des lieux traversés.',
    sections=[
        dict(h='Commencer', p='Touchez <b>Démarrer le voyage</b>, autorisez la localisation et choisissez votre façon de voyager. 2R raconte automatiquement, sans compte ni préparation.'),
        dict(h='Écoute libre ou route audio', p='Laissez-vous surprendre par ce qui vous entoure, ou choisissez un carnet de route soigneusement composé, avec des chapitres fixes et un fil narratif.'),
        dict(h='Avec votre musique', p='Votre musique baisse automatiquement lorsqu’un récit commence, puis revient ensuite. 2R ne diffuse pas de musique lui-même.'),
        dict(h='Écouter en arrière-plan', p='Ouvrez Plans ou votre application musicale : 2R continue de raconter. L’indicateur bleu d’iOS signale l’usage de votre position ; touchez-le pour revenir à 2R.'),
        dict(h='Choisir la voix', p='Dans <b>Réglages → Voix</b>, choisissez le narrateur et la sonorité qui vous conviennent. L’aperçu permet d’entendre immédiatement la différence.'),
        dict(h='Votre rythme de voyage', p='Marche, vélo, train et voiture révèlent chacun un monde différent. 2R adapte son rayon de recherche, son rythme et ses sujets.'),
        dict(h='Silence et partage', p='Mettez un récit en pause, choisissez un instant de silence ou jouez ensemble à un quiz. Vous décidez de la place de la voix.'),
    ],
    cta_h='Prêt à partir ?', cta_p='2R est disponible pour les testeurs ; la sortie publique suivra.', cta_btn='Essayer 2R →',
),
'es': dict(
    eyebrow='Cómo funciona 2R', title='Cómo funciona 2R',
    lede='2R es el compañero que narra tu viaje. Sales — a pie, en bici, en tren o en coche — y escuchas las historias de los lugares por los que pasas.',
    sections=[
        dict(h='Empezar', p='Pulsa <b>Iniciar el viaje</b>, permite la ubicación y elige cómo viajas. 2R narra automáticamente, sin cuenta ni preparación.'),
        dict(h='Escucha libre o ruta sonora', p='Déjate sorprender por tu entorno o elige un libro de ruta cuidadosamente compuesto, con capítulos fijos y un hilo narrativo.'),
        dict(h='Con tu música', p='Tu música baja automáticamente al comenzar una historia y vuelve después. 2R no reproduce música por su cuenta.'),
        dict(h='Escuchar en segundo plano', p='Abre Mapas o tu app de música y 2R seguirá narrando. El indicador azul de iOS muestra que usa tu ubicación; púlsalo para volver a 2R.'),
        dict(h='Elegir la voz', p='En <b>Ajustes → Voz</b>, elige el narrador y el tono que prefieras. La muestra permite oír la diferencia al instante.'),
        dict(h='Tu ritmo de viaje', p='Caminar, pedalear, viajar en tren o en coche revelan mundos distintos. 2R adapta el radio, el ritmo y los temas.'),
        dict(h='Silencio y compañía', p='Pausa una historia, elige un momento de silencio o jugad juntos a un quiz. Tú decides cuánto espacio ocupa la voz.'),
    ],
    cta_h='¿Listo para salir?', cta_p='2R está disponible para testers; el lanzamiento público llegará después.', cta_btn='Probar 2R →',
),
'pt': dict(
    eyebrow='Como funciona o 2R', title='Como funciona o 2R',
    lede='O 2R é o companheiro que narra a sua viagem. Você parte — a pé, de bicicleta, de comboio ou de carro — e ouve as histórias dos lugares por onde passa.',
    sections=[
        dict(h='Começar', p='Toque em <b>Iniciar a viagem</b>, permita a localização e escolha como viaja. O 2R narra automaticamente, sem conta nem preparação.'),
        dict(h='Escuta livre ou rota sonora', p='Deixe-se surpreender pelo que está ao seu redor ou escolha um livro de rota cuidadosamente composto, com capítulos fixos e um fio narrativo.'),
        dict(h='Com a sua música', p='A sua música baixa automaticamente quando uma história começa e volta depois. O 2R não transmite música.'),
        dict(h='Ouvir em segundo plano', p='Abra Mapas ou a aplicação de música e o 2R continua a narrar. O indicador azul do iOS mostra o uso da localização; toque nele para voltar ao 2R.'),
        dict(h='Escolher a voz', p='Em <b>Definições → Voz</b>, escolha o narrador e o tom que combinam consigo. A amostra permite ouvir a diferença imediatamente.'),
        dict(h='O seu ritmo de viagem', p='Caminhar, pedalar, viajar de comboio ou de carro revelam mundos diferentes. O 2R adapta o raio, o ritmo e os temas.'),
        dict(h='Silêncio e companhia', p='Pause uma história, escolha um momento de silêncio ou joguem juntos um quiz. Você decide quanto espaço a voz ocupa.'),
    ],
    cta_h='Pronto para partir?', cta_p='O 2R está disponível para testadores; o lançamento público virá depois.', cta_btn='Experimentar o 2R →',
),
}

# "Zo werkt het" als vijf filmische scènes (beelden van Codex, 29 aug).
# Volgorde/beeld gedeeld over alle talen. Het brede reisbeeld opent; de auto is
# daarna nog maar één van de mogelijke reisruimtes.
HOWTO_IMAGES = ['hero-journey-v2.jpg', 'reisjournaal.jpg', 'howto-03-verhaal.jpg', 'howto-04-muziek.jpg', 'howto-05-ritme.jpg']

FAQ_LABEL = {'nl': 'Goed om te weten voor vertrek', 'en': 'Good to know before you go',
             'de': 'Gut zu wissen vor der Abfahrt', 'fr': 'Bon à savoir avant de partir',
             'es': 'Bueno saber antes de salir', 'pt': 'Bom saber antes de partir'}

HOWTO_SCENES = {
'nl': [
    ('Hoofdstuk 01 · Voor je vertrekt', 'Eén knop. Daarna krijgt de wereld buiten een stem.',
     'Kies je tempo — te voet, op de fiets, per trein of met de auto — en laat 2R weten waar je nieuwsgierig naar bent.'),
    ('Hoofdstuk 02 · Kies je reis', 'Laat je verrassen. Of volg het hele verhaal.',
     'Ga vrij op pad en hoor wat zich om je heen aandient. Of kies een luisterroute die van het eerste hoofdstuk tot de laatste stap zorgvuldig is opgebouwd.'),
    ('Hoofdstuk 03 · Het verhaal', 'Route kiest één betekenisvol verhaal.',
     'Geen lijst met weetjes. Per plek één verhaal, rustig verteld, met ruimte voor de weg en voor elkaar — en je hoort waar het vandaan komt.'),
    ('Hoofdstuk 04 · Jouw muziek', 'De muziek zakt. Een stem komt naast je zitten.',
     'Je eigen muziek — Spotify, radio, podcast — duikt vanzelf zachtjes weg zodra de verteller begint, en zwelt weer aan als het verhaal klaar is.'),
    ('Hoofdstuk 05 · Jouw ritme', 'Luisteren, even stil zijn, of samen spelen.',
     'Luister, tik op "stil" als je rust wilt, of speel samen een reisquiz. Jij bepaalt het ritme; Route past zich aan.'),
],
'en': [
    ('Chapter 01 · Before you leave', 'One tap. Then the world outside finds a voice.',
     'Choose your pace — on foot, by bike, by train or by car — and tell 2R what makes you curious.'),
    ('Chapter 02 · Choose your journey', 'Let yourself be surprised. Or follow the whole story.',
     'Set out freely and hear what appears around you. Or choose a listening route composed with care from its opening chapter to the final step.'),
    ('Chapter 03 · The story', 'Route picks one meaningful story.',
     'Not a list of facts. One story per place, calmly told, with room for the road and for each other — and you hear where it comes from.'),
    ('Chapter 04 · Your music', 'The music softens. A voice sits down beside you.',
     'Your own music — Spotify, radio, podcast — automatically ducks the moment the narrator starts, and swells back up when the story ends.'),
    ('Chapter 05 · Your pace', 'Listen, fall quiet, or play together.',
     'Listen, tap "quiet" when you want a pause, or play a travel quiz together. You set the pace; Route adapts.'),
],
'de': [
    ('Kapitel 01 · Vor dem Aufbruch', 'Ein Tippen. Dann bekommt die Welt draußen eine Stimme.', 'Wähle dein Tempo — zu Fuß, mit dem Rad, per Bahn oder Auto — und sag 2R, was dich neugierig macht.'),
    ('Kapitel 02 · Wähle deine Reise', 'Lass dich überraschen. Oder folge der ganzen Geschichte.', 'Zieh frei los und höre, was um dich herum auftaucht. Oder wähle eine Hörroute, sorgfältig komponiert vom ersten Kapitel bis zum letzten Schritt.'),
    ('Kapitel 03 · Die Geschichte', 'Route wählt eine bedeutsame Geschichte.', 'Keine Faktenliste. Pro Ort eine ruhig erzählte Geschichte, mit Raum für die Landschaft und füreinander — samt nachvollziehbarer Quelle.'),
    ('Kapitel 04 · Deine Musik', 'Die Musik wird leiser. Eine Stimme setzt sich dazu.', 'Deine Musik wird automatisch leiser, sobald die Erzählung beginnt, und kehrt danach zurück.'),
    ('Kapitel 05 · Dein Rhythmus', 'Zuhören, still werden oder gemeinsam spielen.', 'Höre zu, wähle Ruhe oder spielt gemeinsam ein Reisequiz. Du gibst den Rhythmus vor; 2R passt sich an.'),
],
'fr': [
    ('Chapitre 01 · Avant le départ', 'Un geste. Puis le monde extérieur trouve une voix.', 'Choisissez votre rythme — à pied, à vélo, en train ou en voiture — et dites à 2R ce qui éveille votre curiosité.'),
    ('Chapitre 02 · Choisissez le voyage', 'Laissez-vous surprendre. Ou suivez toute l’histoire.', 'Partez librement et écoutez ce qui se présente. Ou choisissez une route audio composée avec soin, du premier chapitre au dernier pas.'),
    ('Chapitre 03 · Le récit', 'Route choisit une histoire qui compte.', 'Pas une liste de faits. Un récit par lieu, raconté calmement, avec de la place pour le paysage, pour vous et pour les sources.'),
    ('Chapitre 04 · Votre musique', 'La musique s’apaise. Une voix prend place à vos côtés.', 'Votre musique baisse d’elle-même lorsque la narration commence, puis revient une fois le récit terminé.'),
    ('Chapitre 05 · Votre rythme', 'Écouter, faire silence ou jouer ensemble.', 'Écoutez, choisissez le calme ou partagez un quiz. Vous donnez le rythme ; 2R s’adapte.'),
],
'es': [
    ('Capítulo 01 · Antes de salir', 'Un toque. Entonces el mundo exterior encuentra su voz.', 'Elige tu ritmo — a pie, en bici, en tren o en coche — y cuenta a 2R qué despierta tu curiosidad.'),
    ('Capítulo 02 · Elige tu viaje', 'Déjate sorprender. O sigue toda la historia.', 'Sal sin plan y escucha lo que aparece a tu alrededor. O elige una ruta sonora compuesta con cuidado desde el primer capítulo hasta el último paso.'),
    ('Capítulo 03 · La historia', 'Route elige una historia con significado.', 'Nada de listas de datos. Una historia por lugar, narrada con calma y con espacio para el paisaje, para compartir y para sus fuentes.'),
    ('Capítulo 04 · Tu música', 'La música baja. Una voz se sienta a tu lado.', 'Tu música baja por sí sola cuando comienza la narración y vuelve al terminar la historia.'),
    ('Capítulo 05 · Tu ritmo', 'Escuchar, guardar silencio o jugar juntos.', 'Escucha, elige un momento de calma o compartid un quiz. Tú marcas el ritmo; 2R se adapta.'),
],
'pt': [
    ('Capítulo 01 · Antes de partir', 'Um toque. Depois o mundo lá fora ganha voz.', 'Escolha o seu ritmo — a pé, de bicicleta, de comboio ou de carro — e diga ao 2R o que desperta a sua curiosidade.'),
    ('Capítulo 02 · Escolha a viagem', 'Deixe-se surpreender. Ou acompanhe toda a história.', 'Parta livremente e ouça o que surge ao redor. Ou escolha uma rota sonora composta com cuidado, do primeiro capítulo ao último passo.'),
    ('Capítulo 03 · A história', 'A Route escolhe uma história com significado.', 'Nada de listas de fatos. Uma história por lugar, narrada com calma e com espaço para a paisagem, para a companhia e para as fontes.'),
    ('Capítulo 04 · A sua música', 'A música baixa. Uma voz senta-se ao seu lado.', 'A sua música baixa automaticamente quando a narração começa e volta quando a história termina.'),
    ('Capítulo 05 · O seu ritmo', 'Ouvir, fazer silêncio ou jogar juntos.', 'Ouça, escolha um momento de calma ou partilhem um quiz. Você define o ritmo; o 2R adapta-se.'),
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
    return page_shell(lang, h['title'] + ' — 2R (Second Route)', h['lede'][:150], 'howto', body, path='zo-werkt-het.html')

def nav(lang, active):
    s = SITE[lang]
    h = HOME_20[lang]
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
        {link(f'/{lang}/', h['nav_home'], 'product')}
        {link(f'/{lang}/routes/', ROUTES_TXT[lang]['nav'], 'routes')}
        {link(f'/{lang}/stories/', s['nav_stories'], 'stories')}
        {link(f'/{lang}/partners/', h['nav_partners'], 'partners')}
        {link(f'/{lang}/zo-werkt-het.html', NAV_HOWTO[lang], 'howto')}
      </span>
      <div class="lang-switch">{others}</div>
      <a class="nav-cta" href="https://apps.apple.com/app/id6802613397">{h['nav_cta']}</a>
    </nav>
  </div>
  <div class="mobile-panel" id="mobile-panel">
    <div class="mobile-panel-links">
      {link(f'/{lang}/', h['nav_home'], 'product')}
      {link(f'/{lang}/routes/', ROUTES_TXT[lang]['nav'], 'routes')}
      {link(f'/{lang}/stories/', s['nav_stories'], 'stories')}
      {link(f'/{lang}/partners/', h['nav_partners'], 'partners')}
      {link(f'/{lang}/zo-werkt-het.html', NAV_HOWTO[lang], 'howto')}
    </div>
    <div class="lang-switch">{others}</div>
    <a class="nav-cta" href="https://apps.apple.com/app/id6802613397">{h['nav_cta']}</a>
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
    h = HOME_20[lang]
    return f'''<footer class="site">
  <div class="footer-grid">
    <a class="footer-brand" href="/{lang}/">
      <img class="brand-mark" src="/icon-2r.png" alt="2R">
      <span>Second Route</span>
    </a>
    <div class="footer-links">
      <a href="/{lang}/routes/">{ROUTES_TXT[lang]['nav']}</a>
      <a href="/{lang}/partners/">{h['nav_partners']}</a>
      <a href="/{lang}/roadmap.html">{s['nav_roadmap']}</a>
      <a href="/{lang}/stories/">{s['nav_stories']}</a>
      <a href="/{lang}/privacy.html">{s['nav_privacy']}</a>
      <a href="mailto:nimco@nentjes.nl">{s['footer_contact']}</a>
    </div>
  </div>
  <p class="footer-family">{s['footer_tagline']}</p>
  <p class="footer-credit">{s['footer_credit']} <a href="https://github.com/nentjes/2r-second-route-website">GitHub</a></p>
</footer>'''

# ---------------------------------------------------------------------------
# Blijvende siteshell (alleen /nl/): één persistente luisterspeler + een lichte
# client-side router, zodat een bewust gestarte vertelling zonder onderbreking
# doorloopt tijdens interne navigatie. Progressive enhancement: zonder JS blijven
# alle links en pagina's gewoon werken. (Codex-briefing 29 aug.)
# ---------------------------------------------------------------------------
SITE_SHELL_NL = '''
<div id="site-player" class="site-player" data-state="invite" hidden>
  <audio id="sp-audio" src="/audio/2r-intro.mp3" preload="none"></audio>
  <button id="sp-toggle" class="sp-toggle" type="button" aria-label="Speel het verhaal af">
    <span class="sp-wave" aria-hidden="true"><i></i><i></i><i></i></span>
    <span class="sp-play" aria-hidden="true"></span>
  </button>
  <div class="sp-info">
    <span class="sp-title">Tussen hier en verder</span>
    <span class="sp-sub" id="sp-sub">Luister onderweg</span>
  </div>
  <input id="sp-vol" class="sp-vol" type="range" min="0" max="100" value="70" aria-label="Volume">
  <button id="sp-close" class="sp-close" type="button" aria-label="Sluit speler">&times;</button>
</div>
<script>
(function () {
  var box = document.getElementById('site-player');
  var au = document.getElementById('sp-audio');
  if (!box || !au) return;
  var toggle = document.getElementById('sp-toggle'), sub = document.getElementById('sp-sub');
  var vol = document.getElementById('sp-vol'), closeBtn = document.getElementById('sp-close');
  var LSVOL = 'siteAudioVol', SSCLOSED = 'sitePlayerClosed', SSPOS = 'sitePlayerPos';
  function lees(s, k) { try { return s.getItem(k); } catch (e) { return null; } }
  function schrijf(s, k, v) { try { s.setItem(k, v); } catch (e) {} }
  var v0 = parseInt(lees(localStorage, LSVOL), 10); if (isNaN(v0)) v0 = 70; vol.value = v0; au.volume = v0 / 100;
  var gesloten = lees(sessionStorage, SSCLOSED) === '1';
  function fmt(t) { t = Math.max(0, Math.floor(t || 0)); var m = Math.floor(t / 60), s = t % 60; return m + ':' + (s < 10 ? '0' : '') + s; }
  function toon() {
    if (gesloten) { box.hidden = true; return; }
    box.hidden = false;
    var st = box.dataset.state;
    if (st === 'playing' || st === 'paused') sub.textContent = fmt(au.currentTime) + ' / ' + fmt(au.duration);
    else if (st === 'ended') sub.textContent = 'Luister opnieuw';
    toggle.setAttribute('aria-label', st === 'playing' ? 'Pauzeer verhaal' : (st === 'paused' ? 'Hervat verhaal' : (st === 'ended' ? 'Luister opnieuw' : 'Speel het verhaal af')));
  }
  function setMedia() {
    if (!('mediaSession' in navigator)) return;
    try {
      navigator.mediaSession.metadata = new MediaMetadata({ title: 'Tussen hier en verder', artist: '2R \\u00b7 Second Route' });
      navigator.mediaSession.setActionHandler('play', function () { speel(); });
      navigator.mediaSession.setActionHandler('pause', function () { au.pause(); });
      navigator.mediaSession.setActionHandler('stop', function () { au.pause(); });
    } catch (e) {}
  }
  function speel() { au.play().then(function () { box.dataset.state = 'playing'; toon(); setMedia(); }).catch(function () { box.dataset.state = 'paused'; toon(); }); }
  au.addEventListener('play', function () { box.dataset.state = 'playing'; toon(); });
  au.addEventListener('pause', function () { if (box.dataset.state !== 'ended') { box.dataset.state = 'paused'; toon(); } });
  au.addEventListener('ended', function () { box.dataset.state = 'ended'; try { sessionStorage.removeItem(SSPOS); } catch (e) {} toon(); });
  au.addEventListener('timeupdate', function () {
    if (box.dataset.state === 'playing') sub.textContent = fmt(au.currentTime) + ' / ' + fmt(au.duration);
    schrijf(sessionStorage, SSPOS, JSON.stringify({ t: au.currentTime, p: !au.paused, ts: Date.now() }));
  });
  toggle.addEventListener('click', function () {
    var st = box.dataset.state;
    if (st === 'playing') au.pause();
    else if (st === 'ended') { au.currentTime = 0; speel(); }
    else speel();
  });
  vol.addEventListener('input', function () { au.volume = vol.value / 100; schrijf(localStorage, LSVOL, vol.value); });
  closeBtn.addEventListener('click', function () { au.pause(); gesloten = true; schrijf(sessionStorage, SSCLOSED, '1'); box.hidden = true; });
  // Herstel na een onvermijdelijke volledige reload: alleen als knop, nooit autoplay.
  (function () {
    if (gesloten) return;
    var raw = lees(sessionStorage, SSPOS); if (!raw) return;
    try { var d = JSON.parse(raw); if (d && d.ts && (Date.now() - d.ts) < 3600000 && d.t > 1) { au.currentTime = d.t; box.dataset.state = 'paused'; box.hidden = false; sub.textContent = 'Ga verder \\u00b7 ' + fmt(d.t); } } catch (e) {}
  })();
  toon();

  // ---------- Lichte client-side router voor interne /nl/-navigatie ----------
  var origin = location.origin, bezig = false;
  function interneNl(a) {
    if (!a || a.target || a.hasAttribute('download')) return false;
    var href = a.getAttribute('href'); if (!href) return false;
    if (href.charAt(0) === '#' || href.indexOf('mailto:') === 0 || href.indexOf('tel:') === 0) return false;
    if (a.origin !== origin) return false;
    if (a.pathname.indexOf('/nl/') !== 0) return false;
    return true;
  }
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest ? e.target.closest('a') : null;
    if (!a || !interneNl(a)) return;
    e.preventDefault(); ga(a.href, true);
  });
  window.addEventListener('popstate', function () { ga(location.href, false); });
  function updateNav(href) {
    document.querySelectorAll('.nav-links a, .mobile-panel-links a').forEach(function (a) {
      a.classList.toggle('active', !!href && a.getAttribute('href') === href);
    });
  }
  function runScripts(container) {
    var scripts = [].slice.call(container.querySelectorAll('script'));
    // Scripts die via innerHTML in <main> terechtkomen, worden niet door de
    // browser uitgevoerd. Verwijder die slapende kopieen eerst, anders ziet de
    // controle hieronder ze ten onrechte aan voor reeds geladen scripts.
    scripts.forEach(function (script) { script.remove(); });
    return scripts.reduce(function (chain, old) {
      return chain.then(function () {
        var src = old.getAttribute('src');
        if (src) {
          var volledig = new URL(src, location.href).href;
          var geladen = [].some.call(document.scripts, function (script) { return script.src === volledig; });
          if (geladen) return;
          return new Promise(function (res) { var s = document.createElement('script'); s.src = volledig; s.onload = res; s.onerror = res; document.head.appendChild(s); });
        }
        var s = document.createElement('script'); s.textContent = old.textContent; document.body.appendChild(s); s.remove();
      });
    }, Promise.resolve());
  }
  function syncStyles(doc) {
    var wachten = [];
    doc.querySelectorAll('link[rel="stylesheet"][href]').forEach(function (link) {
      var volledig = new URL(link.getAttribute('href'), location.href).href;
      var bestaat = [].some.call(document.querySelectorAll('link[rel="stylesheet"][href]'), function (huidig) {
        return huidig.href === volledig;
      });
      if (bestaat) return;
      wachten.push(new Promise(function (res) {
        var stijl = document.createElement('link');
        stijl.rel = 'stylesheet'; stijl.href = volledig;
        stijl.onload = res; stijl.onerror = res;
        document.head.appendChild(stijl);
      }));
    });
    return Promise.all(wachten);
  }
  function ga(url, push) {
    if (bezig) return; bezig = true;
    fetch(url, { credentials: 'same-origin' }).then(function (r) { if (!r.ok) throw 0; return r.text(); }).then(function (htmlStr) {
      var doc = new DOMParser().parseFromString(htmlStr, 'text/html');
      var nieuw = doc.querySelector('main'), oud = document.querySelector('main');
      if (!nieuw || !oud) throw 0;
      try { if (window.__2rCleanup) { window.__2rCleanup(); window.__2rCleanup = null; } } catch (e) {}
      oud.innerHTML = nieuw.innerHTML;
      document.title = doc.title;
      var lg = doc.documentElement.getAttribute('lang'); if (lg) document.documentElement.setAttribute('lang', lg);
      var act = doc.querySelector('.nav-links a.active');
      updateNav(act ? act.getAttribute('href') : null);
      var panel = document.querySelector('.mobile-panel.open, .mobile-panel[aria-hidden="false"]');
      if (panel) { panel.classList.remove('open'); }
      if (push) history.pushState({ r: 1 }, '', url);
      syncStyles(doc).then(function () { return runScripts(oud); }).then(function () {
        window.scrollTo(0, 0);
        var h1 = oud.querySelector('h1');
        if (h1) { h1.setAttribute('tabindex', '-1'); try { h1.focus({ preventScroll: true }); } catch (e) { try { h1.focus(); } catch (e2) {} } }
        bezig = false;
      });
    }).catch(function () { bezig = false; window.location.href = url; });
  }
})();
</script>
'''

BASE_URL = 'https://2route.nl'

def _seo_pad(path):
    # index.html toont de site als mapadres
    return path[:-len('index.html')] if path.endswith('index.html') else path

def page_shell(lang, title, description, active, body, extra_head='', path=None):
    seo = ''
    if path is not None:
        p = _seo_pad(path)
        canon = f'{BASE_URL}/{lang}/{p}'
        alts = ''.join(f'<link rel="alternate" hreflang="{l}" href="{BASE_URL}/{l}/{p}">\n' for l in LANGS)
        seo = (f'<link rel="canonical" href="{canon}">\n'
               f'{alts}'
               f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}/nl/{p}">\n'
               f'<meta property="og:url" content="{canon}">\n')
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
{seo}</head>
<body>
{nav(lang, active)}
<main>
{body}
</main>
{footer(lang)}
{extra_head}
{SITE_SHELL_NL if lang == 'nl' else ''}
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
    return page_shell(lang, f"{html.escape(title)} — 2R (Second Route)", teaser, 'product', body, path=f'stad/{CITY_SLUGS[index]}.html')


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
    h = HOME_20[lang]
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
    modes_html = ''.join(f'''<article class="travel-mode">
        <span class="travel-mode-num">{i:02d}</span>
        <h3>{title}</h3>
        <p>{copy}</p>
      </article>''' for i, (title, copy) in enumerate(h['modes'], 1))

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

    body = f'''  <section class="hero hero-v2" id="top">
    <video class="hero-photo" aria-hidden="true" autoplay muted loop playsinline preload="metadata" poster="/images/hero-dame-poster.jpg">
      <source src="/images/hero-drive-loop.mp4" type="video/mp4">
    </video>
    <div class="hero-shade" aria-hidden="true"></div>
    <div class="hero-content">
      <p class="eyebrow on-photo">{h['hero_eyebrow']}</p>
      <h1>{s['hero_h1']}</h1>
      <p class="hero-lede">{h['hero_lede']}</p>
      <div class="hero-actions">
        <a class="btn-primary" href="#luisteren">{h['hero_primary']} <span>↓</span></a>
        <a class="text-link" href="/{lang}/routes/">{h['hero_secondary']} <span>→</span></a>
      </div>
    </div>
    <div class="hero-caption"><span>2R · Second Route</span><span>{h['hero_caption']}</span></div>
  </section>

  <section class="listening" id="luisteren">
    <div class="section-label">{s['listen_label']}</div>
    <div class="listening-copy">
      <h2>{s['listen_h2']}</h2>
      <p>{s['listen_p']}</p>
    </div>
    <div class="audio-experience" id="listen-demo" role="button" tabindex="0" aria-label="{s['listen_now']}: {s['listen_sub']}">
      <audio id="listen-audio" preload="none" src="/audio/drakensteyn-grafheuvels.mp3"></audio>
      <div class="audio-halo">
        <span class="play-button" id="listen-play" aria-hidden="true">▶</span>
      </div>
      <div class="audio-meta">
        <span>{s['listen_now']}</span>
        <strong>{s['listen_title']}</strong>
        <small>{s['listen_sub']}</small>
      </div>
    </div>
    <script>
    (function(){{
      var vak = document.getElementById('listen-demo');
      var audio = document.getElementById('listen-audio');
      var knop = document.getElementById('listen-play');
      if (!vak || !audio) return;
      vak.style.cursor = 'pointer';
      function wissel() {{
        if (audio.paused) {{ audio.play(); knop.textContent = '❚❚'; }}
        else {{ audio.pause(); knop.textContent = '▶'; }}
      }}
      vak.addEventListener('click', wissel);
      vak.addEventListener('keydown', function(e) {{
        if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); wissel(); }}
      }});
      audio.addEventListener('ended', function() {{ knop.textContent = '▶'; }});
    }})();
    </script>
    <p class="listen-more"><a class="text-link" href="/{lang}/routes/drakensteyn/">{ROUTES_TXT[lang]['home_link']}</a></p>
  </section>

  <section class="listening-ways" id="manieren">
    <div class="wrap">
      <div class="ways-intro">
        <div>
          <p class="section-label">{h['ways_label']}</p>
          <h2>{h['ways_h2']}</h2>
        </div>
        <p>{h['ways_p']}</p>
      </div>
      <div class="ways-grid">
        <article class="way way-free">
          <span class="way-label">{h['free_label']}</span>
          <h3>{h['free_h']}</h3>
          <p>{h['free_p']}</p>
          <a class="text-link on-paper" href="/{lang}/zo-werkt-het.html">{h['free_cta']} →</a>
        </article>
        <article class="way way-book">
          <span class="way-label">{h['book_label']}</span>
          <h3>{h['book_h']}</h3>
          <p>{h['book_p']}</p>
          <div class="way-proof"><b>{PARTNER_TXT[lang]['facts'][0][0]}</b><b>12 {ROUTES_TXT[lang]['hoofdstukken']}</b><b>{PARTNER_TXT[lang]['facts'][2][0]} {PARTNER_TXT[lang]['facts'][2][1]}</b></div>
          <a class="btn-primary" href="/{lang}/routes/">{h['book_cta']} <span>→</span></a>
        </article>
      </div>
    </div>
  </section>

  <section class="travel-rhythms">
    <div class="wrap">
      <div class="rhythms-head">
        <div>
          <p class="section-label">{h['modes_label']}</p>
          <h2>{h['modes_h2']}</h2>
        </div>
        <p>{h['modes_p']}</p>
      </div>
      <div class="travel-modes">{modes_html}</div>
    </div>
  </section>

  <section class="journey" id="reis">
    <div class="journey-visual" aria-hidden="true">
      <div class="window-frame">
        {journey_scenes_html}
        <span class="window-reflection"></span>
      </div>
      <div class="map-card">
        <span class="lbl">{h['europe_route']}</span>
        <strong id="journey-region">{first_region_short}</strong>
        <div class="route-line"><i></i><i></i><i></i></div>
        <span class="lbl">{h['europe_meta']}</span>
      </div>
    </div>
    <div class="journey-narrative">
      <div class="journey-intro">
        <div class="section-label">{h['europe_label']}</div>
        <h2>{h['europe_h2']}</h2>
        <p>{h['europe_p']}</p>
      </div>
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
    window.__2rCleanup = function(){{ observer.disconnect(); }};
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
    <p style="margin-top:26px;"><a class="text-link on-paper" href="/{lang}/stories/">{s['stories_view_all']}</a></p>
  </div></section>

  <section class="partner-invite">
    <div class="partner-invite-image" aria-hidden="true"></div>
    <div class="partner-invite-copy">
      <p class="eyebrow on-photo">{h['partner_label']}</p>
      <h2>{h['partner_h2']}</h2>
      <p>{h['partner_p']}</p>
      <div class="partner-actions">
        <a class="btn-primary" href="mailto:nimco@nentjes.nl?subject=Pilotroute%20voor%202R">{h['partner_cta']} <span>↗</span></a>
        <a class="text-link" href="/{lang}/partners/">{h['partner_more']} →</a>
      </div>
    </div>
  </section>

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
    title = {'nl': '2R (Second Route) — Luisterroutes en verhalen voor wandelen, fietsen, trein en auto',
             'en': '2R (Second Route) — Listening routes and stories for walking, cycling, train and car',
             'de': '2R (Second Route) — Hörrouten und Geschichten zum Wandern, Radfahren, für Bahn und Auto',
             'fr': "2R (Second Route) — Itinéraires d'écoute et récits à pied, à vélo, en train et en voiture",
             'es': '2R (Second Route) — Rutas para escuchar e historias a pie, en bici, en tren y en coche',
             'pt': '2R (Second Route) — Rotas para ouvir e histórias a pé, de bicicleta, de comboio e de carro'}[lang]
    # Live tellers (testers/verhalen vandaag) zijn van de publieke pagina
    # gehaald: dat was interne telemetrie en liet ongewild de prille schaal
    # zien. De strip toont nu stabiele productfeiten (stat3/stat4 in SITE).
    return page_shell(lang, title, h['hero_lede'], 'product', body, path='index.html')

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
    return page_shell(lang, f"Roadmap — 2R (Second Route)", s['rm_lede'], 'roadmap', body, path='roadmap.html')

# Nieuwe redactionele omlijsting voor de privacypagina (herbouw 29 aug). De
# juridische kernteksten blijven in PRIVACY[lang]; hieronder alleen de rustige
# samenvattingen, tabel en het slot. Faithful vertaald, geen nieuwe claims.
PRIV_EXTRA = {
'nl': dict(
    h1='Jouw reis blijft van jou.', alt='Een telefoon ligt met het scherm naar beneden naast een reisboek en wegenkaart in een geparkeerde auto.',
    lede='2R gebruikt alleen wat nodig is om onderweg het juiste verhaal te vertellen. Geen account, geen rittenregistratie en standaard geen opgeslagen locatie. Hier leggen we precies uit wat er wél gebeurt.',
    promises=[('01', 'Geen account nodig', 'Je hoeft niet in te loggen. Alleen testers vullen vrijwillig een naam in.'),
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
    promises=[('01', 'No account needed', "No login needed. Only testers voluntarily enter a name."),
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
    promises=[('01', 'Kein Konto nötig', 'Keine Anmeldung nötig. Nur Tester geben freiwillig einen Namen an.'),
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
    promises=[('01', 'Aucun compte nécessaire', 'Aucune connexion requise. Seuls les testeurs saisissent un nom, volontairement.'),
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
    promises=[('01', 'Sin cuenta', 'No hace falta iniciar sesión. Solo los testers introducen un nombre, de forma voluntaria.'),
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
    promises=[('01', 'Sem conta necessária', 'Não é preciso fazer login. Só os testadores informam um nome, voluntariamente.'),
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
    data_lis = '\n'.join(f'<li>{item}</li>' for item in p['data_items'])
    promises = ''.join(
        f'<div class="priv-promise"><span class="priv-pnum">{n}</span><div class="priv-pbody"><h3>{t}</h3><p>{d}</p></div></div>'
        for n, t, d in pe['promises'])
    toc_items = [('loc', p['h_location']), ('verhalen', p['h_stories']), ('limieten', p['h_limits']),
                 ('bewaard', p['h_data']), ('accounts', p['h_accounts']), ('contact', p['h_contact'])]
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

      <section id="bewaard" class="priv-sec">
        <h2>{p['h_data']}</h2>
        <ul>{data_lis}</ul>
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
    return page_shell(lang, p['title'], pe['lede'][:150], 'privacy', body, path='privacy.html')

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

  <link rel="stylesheet" href="/leaflet.css">
  <script src="/leaflet.js"></script>
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
      if (typeof L === 'undefined') { kaartEl.style.display = 'none'; return; }
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
        try { toonKaart(d.verhalen); } catch (e) { kaartEl.style.display = 'none'; }
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
    window.__2rCleanup = function () { try { if (kaart) kaart.remove(); } catch (e) {} if (timer) clearTimeout(timer); };
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
    hero_lede='Iedere plek draagt een verhaal. Soms hoef je er alleen maar langs te komen. Deze verhalen ontstonden tijdens wandelingen, ritten en reizen met 2R, zijn door ons nagelezen en voorzien van hun bron.',
    hero_cta='Lees het eerste verhaal', hero_alt='Een reiziger kijkt vanuit de auto naar een voorbijtrekkend Europees dorp, met een reisboek op schoot.',
    featured_label='Uitgelicht', read_story='Lees het verhaal', detail_source_h='Waar dit verhaal vandaan komt',
    related='Verder lezen', invite_h='Neem Route mee op je volgende reis'),
'en': dict(hero_eyebrow='The living travel book', hero_h1='Stories that began on the road.',
    hero_lede='Every place carries a story. Sometimes you only have to pass by. These stories emerged on walks, rides and journeys with 2R, and were checked and sourced by us.',
    hero_cta='Read the first story', hero_alt='A traveler looks from the car at a passing European village, with a travel book on their lap.',
    featured_label='Featured', read_story='Read the story', detail_source_h='Where this story comes from',
    related='Read on', invite_h='Take Route along on your next trip'),
'de': dict(hero_eyebrow='Das lebendige Reisebuch', hero_h1='Geschichten, die unterwegs begannen.',
    hero_lede='Jeder Ort trägt eine Geschichte. Manchmal musst du nur daran vorbeikommen. Diese Geschichten entstanden auf Wanderungen, Fahrten und Reisen mit 2R und wurden von uns geprüft und mit Quellen versehen.',
    hero_cta='Lies die erste Geschichte', hero_alt='Ein Reisender blickt aus dem Auto auf ein vorbeiziehendes europäisches Dorf, ein Reisebuch auf dem Schoß.',
    featured_label='Ausgewählt', read_story='Geschichte lesen', detail_source_h='Woher diese Geschichte stammt',
    related='Weiterlesen', invite_h='Nimm Route mit auf deine nächste Reise'),
'fr': dict(hero_eyebrow='Le carnet de voyage vivant', hero_h1='Des histoires nées en chemin.',
    hero_lede="Chaque lieu porte une histoire. Parfois, il suffit de passer devant. Ces récits sont nés de promenades et de voyages avec 2R, puis ont été vérifiés et sourcés par nos soins.",
    hero_cta='Lire le premier récit', hero_alt="Un voyageur regarde depuis la voiture un village européen qui défile, un carnet de voyage sur les genoux.",
    featured_label='À la une', read_story='Lire le récit', detail_source_h="D'où vient cette histoire",
    related='À lire aussi', invite_h='Emportez Route lors de votre prochain voyage'),
'es': dict(hero_eyebrow='El libro de viaje vivo', hero_h1='Historias que empezaron en el camino.',
    hero_lede='Cada lugar guarda una historia. A veces solo tienes que pasar por delante. Estas historias nacieron en paseos y viajes con 2R, y fueron revisadas y documentadas por nosotros.',
    hero_cta='Lee la primera historia', hero_alt='Un viajero mira desde el coche un pueblo europeo que pasa, con un libro de viaje en el regazo.',
    featured_label='Destacado', read_story='Leer la historia', detail_source_h='De dónde viene esta historia',
    related='Sigue leyendo', invite_h='Lleva Route en tu próximo viaje'),
'pt': dict(hero_eyebrow='O livro de viagem vivo', hero_h1='Histórias que começaram no caminho.',
    hero_lede='Cada lugar guarda uma história. Às vezes basta passar por ela. Estas histórias nasceram em caminhadas e viagens com o 2R, e foram revistas e documentadas por nós.',
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
    return page_shell(lang, f"{s['nav_stories']} — 2R (Second Route)", se['hero_lede'][:150], 'stories', body, path='stories/index.html')

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
    return page_shell(lang, f"{st['title'][lang]} — 2R", st['text'][lang][:150], 'stories', body, path=f'stories/{st["slug"]}.html')


# ---------------------------------------------------------------------------
# Luisterroutes — provinciebibliotheek + routepagina's (website 2.0, ronde 2)
# Inhoud per route in routes-content/<slug>.json; audio als losse mp3's in
# public/audio/routes/<slug>/; kaartdata uit de 2R-vectorkaartpijplijn.
# ---------------------------------------------------------------------------
ROUTES_TXT = {
'nl': dict(nav='Luisterroutes', eyebrow='Het levende routeboek', h1='De eerste wandeling<br>heeft een stem.', hero_alt='Twee wandelaars volgen samen een bospad langs heide en een oude kasteeltuin in het zachte ochtendlicht.',
    lede='Boswachterspad Stulp en Kasteeltuin is onze eerste complete luisterroute: officiële GPX, eigen kaart en twaalf hoofdstukken op precies de goede plek. Van hieruit groeit een bibliotheek door heel Nederland.',
    live='Beluister de route', productie='In productie', hoofdstukken='hoofdstukken', km='km',
    kwaliteit_h='Zo ontstaat kwaliteit', kwaliteit_p='Elk routeboek doorloopt dezelfde vijf stappen vóór het online komt:',
    kwaliteit=['Betrouwbare lokale bronnen — elk feit met bron-URL, dubbel gecontroleerd', 'Eén dragende verhaallijn van begin tot slot', 'Hoofdstukken op wandeltempo: elke vierhonderd tot zevenhonderd meter', 'Menselijke eindredactie, elke ingreep gelogd', 'Een warme vertelstem'],
    detail_eyebrow='Luisterwandeling · Utrecht', taalnoot='', hoofdstuk='Hoofdstuk', bron_lbl='Bronnen',
    gpx='Download de originele GPX', bronpagina='Routepagina van de beheerder', kaart_h='De route op de kaart',
    kaart_p='Een eigen 2R-kaart, getekend uit OpenStreetMap-geodata — zoom in tot op het wandelpad. Tik op een halte om naar het hoofdstuk te springen.',
    home_link='Beluister de hele wandeling →', terug='← Alle luisterroutes'),
'en': dict(nav='Listening routes', eyebrow='The living route book', h1='The first walk<br>has found its voice.', hero_alt='Two walkers follow a woodland path beside heath and an old castle garden in soft morning light.',
    lede='The Stulp and Castle Garden forester trail is our first complete listening route: official GPX, our own map and twelve chapters in exactly the right places. From here, a library across the Netherlands begins to grow.',
    live='Listen to this route', productie='In production', hoofdstukken='chapters', km='km',
    kwaliteit_h='How quality is made', kwaliteit_p='Every route book passes the same five steps before going live:',
    kwaliteit=['Reliable local sources — every fact with its URL, double-checked', 'One carrying storyline from start to finish', 'Chapters at walking pace: every four to seven hundred metres', 'Human editing, every change logged', 'A warm narrating voice'],
    detail_eyebrow='Listening walk · Utrecht', taalnoot='The chapters below are narrated in Dutch — the language the landscape speaks. Multilingual route books are on the roadmap.',
    hoofdstuk='Chapter', bron_lbl='Sources', gpx='Download the original GPX', bronpagina="The steward's route page",
    kaart_h='The route on the map', kaart_p='Our own 2R map, drawn from OpenStreetMap geodata — zoom in to the footpath itself. Tap a stop to jump to its chapter.',
    home_link='Listen to the full walk →', terug='← All listening routes'),
'de': dict(nav='Hörrouten', eyebrow='Das lebendige Routenbuch', h1='Die erste Wanderung<br>hat eine Stimme.', hero_alt='Zwei Wanderer folgen im sanften Morgenlicht einem Waldweg an Heide und altem Schlossgarten entlang.',
    lede='Der Boswachterspad Stulp en Kasteeltuin ist unsere erste vollständige Hörroute: offizieller GPX-Track, eigene Karte und zwölf Kapitel an genau den richtigen Orten. Von hier aus wächst eine Bibliothek in den ganzen Niederlanden.',
    live='Route anhören', productie='In Produktion', hoofdstukken='Kapitel', km='km',
    kwaliteit_h='So entsteht Qualität', kwaliteit_p='Jedes Routenbuch durchläuft vor der Veröffentlichung dieselben fünf Schritte:',
    kwaliteit=['Verlässliche lokale Quellen — jeder Fakt mit URL, doppelt geprüft', 'Eine tragende Erzähllinie von Anfang bis Ende', 'Kapitel im Wandertempo: alle vier- bis siebenhundert Meter', 'Menschliche Redaktion, jeder Eingriff protokolliert', 'Eine warme Erzählstimme'],
    detail_eyebrow='Hörwanderung · Utrecht', taalnoot='Die Kapitel unten werden auf Niederländisch erzählt — mehrsprachige Routenbücher stehen auf der Roadmap.',
    hoofdstuk='Kapitel', bron_lbl='Quellen', gpx='Original-GPX herunterladen', bronpagina='Routenseite des Verwalters',
    kaart_h='Die Route auf der Karte', kaart_p='Eine eigene 2R-Karte aus OpenStreetMap-Geodaten — zoome bis auf den Wanderweg. Tippe auf einen Halt, um zum Kapitel zu springen.',
    home_link='Die ganze Wanderung anhören →', terug='← Alle Hörrouten'),
'fr': dict(nav='Routes audio', eyebrow='Le carnet de route vivant', h1='La première promenade<br>a trouvé sa voix.', hero_alt="Deux marcheurs suivent un sentier forestier entre lande et ancien jardin de château dans la douce lumière du matin.",
    lede="Le sentier forestier Stulp et Jardin du Château est notre première route audio complète : GPX officiel, carte maison et douze chapitres aux endroits justes. À partir d'ici se construit une bibliothèque dans tous les Pays-Bas.",
    live='Écouter cette route', productie='En production', hoofdstukken='chapitres', km='km',
    kwaliteit_h='Comment naît la qualité', kwaliteit_p='Chaque carnet de route passe par les cinq mêmes étapes avant sa mise en ligne :',
    kwaliteit=['Des sources locales fiables — chaque fait avec son URL, vérifié deux fois', 'Une seule ligne narrative du début à la fin', 'Des chapitres au rythme de la marche : tous les quatre à sept cents mètres', 'Une relecture humaine, chaque intervention consignée', 'Une voix chaleureuse'],
    detail_eyebrow='Promenade sonore · Utrecht', taalnoot='Les chapitres ci-dessous sont racontés en néerlandais — les carnets multilingues sont sur la feuille de route.',
    hoofdstuk='Chapitre', bron_lbl='Sources', gpx='Télécharger le GPX original', bronpagina='Page officielle de la route',
    kaart_h='La route sur la carte', kaart_p="Une carte 2R maison, dessinée à partir des géodonnées OpenStreetMap — zoomez jusqu'au sentier. Touchez une halte pour rejoindre son chapitre.",
    home_link='Écouter toute la promenade →', terug='← Toutes les routes audio'),
'es': dict(nav='Rutas de audio', eyebrow='El libro de ruta vivo', h1='El primer paseo<br>ya tiene voz.', hero_alt='Dos caminantes siguen un sendero del bosque junto al brezal y un antiguo jardín de castillo bajo la suave luz de la mañana.',
    lede='El sendero forestal Stulp y Jardín del Castillo es nuestra primera ruta sonora completa: GPX oficial, mapa propio y doce capítulos en los lugares precisos. Desde aquí crecerá una biblioteca por todos los Países Bajos.',
    live='Escuchar esta ruta', productie='En producción', hoofdstukken='capítulos', km='km',
    kwaliteit_h='Así nace la calidad', kwaliteit_p='Cada libro de ruta pasa por los mismos cinco pasos antes de publicarse:',
    kwaliteit=['Fuentes locales fiables — cada dato con su URL, verificado dos veces', 'Una sola línea narrativa de principio a fin', 'Capítulos a ritmo de paseo: cada cuatrocientos a setecientos metros', 'Edición humana, cada cambio registrado', 'Una voz cálida'],
    detail_eyebrow='Paseo sonoro · Utrecht', taalnoot='Los capítulos siguientes se narran en neerlandés — los libros multilingües están en la hoja de ruta.',
    hoofdstuk='Capítulo', bron_lbl='Fuentes', gpx='Descargar el GPX original', bronpagina='Página oficial de la ruta',
    kaart_h='La ruta en el mapa', kaart_p='Un mapa 2R propio, dibujado con geodatos de OpenStreetMap — acércate hasta el propio sendero. Toca una parada para ir a su capítulo.',
    home_link='Escucha el paseo completo →', terug='← Todas las rutas de audio'),
'pt': dict(nav='Rotas de áudio', eyebrow='O livro de rota vivo', h1='O primeiro passeio<br>já tem voz.', hero_alt='Dois caminhantes seguem um trilho florestal junto à charneca e a um antigo jardim de castelo na suave luz da manhã.',
    lede='O trilho florestal Stulp e Jardim do Castelo é a nossa primeira rota sonora completa: GPX oficial, mapa próprio e doze capítulos nos lugares certos. A partir daqui cresce uma biblioteca por todos os Países Baixos.',
    live='Ouvir esta rota', productie='Em produção', hoofdstukken='capítulos', km='km',
    kwaliteit_h='Assim nasce a qualidade', kwaliteit_p='Cada livro de rota passa pelos mesmos cinco passos antes de ir ao ar:',
    kwaliteit=['Fontes locais confiáveis — cada fato com sua URL, verificado duas vezes', 'Uma única linha narrativa do início ao fim', 'Capítulos no ritmo da caminhada: a cada quatrocentos a setecentos metros', 'Edição humana, cada mudança registrada', 'Uma voz calorosa'],
    detail_eyebrow='Passeio sonoro · Utrecht', taalnoot='Os capítulos abaixo são narrados em neerlandês — livros multilíngues estão no roteiro.',
    hoofdstuk='Capítulo', bron_lbl='Fontes', gpx='Baixar o GPX original', bronpagina='Página oficial da rota',
    kaart_h='A rota no mapa', kaart_p='Um mapa 2R próprio, desenhado com geodados do OpenStreetMap — aproxime até a própria trilha. Toque numa parada para ir ao capítulo.',
    home_link='Ouça o passeio completo →', terug='← Todas as rotas de áudio'),
}

PARTNER_TXT = {
'nl': dict(
    title='Voor routebeheerders — 2R (Second Route)',
    description='Maak van een bestaande wandel- of fietsroute een levend, meertalig luisterverhaal met kaart, hoofdstukken, bronnen en een warme vertelstem.',
    eyebrow='Voor routebeheerders, uitgevers en erfgoedmakers',
    h1='Uw route wijst de weg.<br>2R geeft haar een stem.',
    lede='Een GPX-bestand vertelt waar iemand moet lopen of fietsen. 2R voegt toe waarom die weg ertoe doet — als één zorgvuldig opgebouwd luisterverhaal.',
    primary='Bespreek een pilotroute', secondary='Beluister onze eerste route',
    proof_label='Van pad naar verhaal', proof_h='Eén wandeling bewijst de hele keten.',
    proof_p='Voor Boswachterspad Stulp en Kasteeltuin brachten we de officiële route, lokale bronnen en OpenStreetMap-geodata samen in een routeboek dat op wandeltempo vertelt.',
    facts=[('5,7 km', 'officiële wandelroute'), ('12', 'verbonden hoofdstukken'), ('70', 'geverifieerde feiten'), ('1', 'dragende verhaallijn')],
    process_label='De werkwijze', process_h='Van bronmateriaal naar een levende route.',
    process=[
        ('De route', 'U levert een GPX-bestand, routebeschrijving of bestaande gids. Wij leggen het echte spoor en de relevante omgeving vast.'),
        ('De kennis', 'Lokale bronnen, erfgoedarchieven en informatie van de beheerder vormen de grondstof. Elk feit blijft herleidbaar.'),
        ('Het reisboek', 'Hoofdstukken krijgen één rode draad, het juiste ritme voor wandelen of fietsen en een menselijke eindredactie.'),
        ('De beleving', 'Publicatie kan in 2R, op het web of via een QR-code — met kaart, audio, leestekst en bronvermelding.'),
    ],
    audience_label='Voor wie', audience_h='Bestaande routes, een nieuw publiek.',
    audiences=[
        ('Wandel- en fietsorganisaties', 'Maak van GPX, knooppunten en papieren gidsen een ervaring die onderweg vanzelf begint.'),
        ('Natuur en erfgoed', 'Laat landschap, monumenten en lokale stemmen samen één betrouwbaar verhaal vertellen.'),
        ('Steden en regio’s', 'Ontvang bezoekers in hun eigen taal, zonder opnieuw een complete app te hoeven bouwen.'),
        ('Uitgevers', 'Voeg een luistereditie toe aan een bestaande gids of ontwikkel een nieuw digitaal routeboek.'),
    ],
    principle='Een GPX-bestand wijst de weg. 2R vertelt het verhaal van die weg.',
    studio_label='De volgende horizon', studio_h='Van pilot naar 2R Studio.',
    studio_p='We beginnen bewust met enkele routes die we samen met hun beheerders maken. Uit die praktijk groeit een Studio waarmee organisaties later zelf routes, bronnen en hoofdstukken kunnen beheren — terwijl 2R kwaliteit, stem en distributie bewaakt.',
    final_h='Welke route verdient als eerste een stem?',
    final_p='Stuur ons een GPX-bestand, gids of routepagina. We kiezen samen één route waarmee we de inhoud, techniek en publieksreactie kunnen bewijzen.',
    final_cta='Laat één route proefvertellen',
),
'en': dict(
    title='For route publishers — 2R (Second Route)',
    description='Turn an existing walking or cycling route into a living, multilingual audio story with a map, chapters, sources and a warm narrative voice.',
    eyebrow='For route stewards, publishers and heritage makers',
    h1='Your route shows the way.<br>2R gives it a voice.',
    lede='A GPX file tells people where to walk or cycle. 2R adds why that road matters — as one carefully composed listening story.',
    primary='Discuss a pilot route', secondary='Listen to our first route',
    proof_label='From path to story', proof_h='One walk proves the entire chain.',
    proof_p='For the Stulp and Castle Garden forester trail, we brought together the official route, local sources and OpenStreetMap geodata in a route book paced for walking.',
    facts=[('5.7 km', 'official walking route'), ('12', 'connected chapters'), ('70', 'verified facts'), ('1', 'carrying storyline')],
    process_label='The method', process_h='From source material to a living route.',
    process=[
        ('The route', 'You supply a GPX file, route description or existing guide. We map the actual trail and its meaningful surroundings.'),
        ('The knowledge', 'Local sources, heritage archives and steward information become the raw material. Every fact remains traceable.'),
        ('The route book', 'Chapters gain one narrative thread, the right walking or cycling pace and a final human edit.'),
        ('The experience', 'Publish in 2R, on the web or through a QR code — with map, audio, reading text and source notes.'),
    ],
    audience_label='Who it is for', audience_h='Existing routes, a new audience.',
    audiences=[
        ('Walking and cycling organisations', 'Turn GPX tracks, route networks and printed guides into an experience that starts by itself.'),
        ('Nature and heritage', 'Let landscape, monuments and local voices form one reliable story.'),
        ('Cities and regions', 'Welcome visitors in their own language without building an entire app from scratch.'),
        ('Publishers', 'Add a listening edition to an existing guide or create a new digital route book.'),
    ],
    principle='A GPX file shows the way. 2R tells the story of that way.',
    studio_label='The next horizon', studio_h='From pilot to 2R Studio.',
    studio_p='We deliberately begin with a few routes made together with their stewards. That practice can grow into a Studio where organisations manage routes, sources and chapters themselves, while 2R safeguards quality, voice and distribution.',
    final_h='Which route deserves a voice first?',
    final_p='Send us a GPX file, guide or route page. Together we will choose one route to prove the content, technology and audience response.',
    final_cta='Let us narrate one pilot route',
),
'de': dict(
    title='Für Routenanbieter — 2R (Second Route)',
    description='Verwandeln Sie eine Wander- oder Radroute in eine lebendige, mehrsprachige Hörgeschichte mit Karte, Kapiteln, Quellen und warmer Erzählstimme.',
    eyebrow='Für Routenanbieter, Verlage und Kulturerbe-Initiativen',
    h1='Ihre Route zeigt den Weg.<br>2R gibt ihr eine Stimme.',
    lede='Eine GPX-Datei zeigt, wo man wandert oder Rad fährt. 2R ergänzt, warum dieser Weg bedeutsam ist — als sorgfältig komponierte Hörgeschichte.',
    primary='Pilotroute besprechen', secondary='Unsere erste Route anhören',
    proof_label='Vom Weg zur Geschichte', proof_h='Eine Wanderung beweist die ganze Kette.',
    proof_p='Für den Boswachterspad Stulp en Kasteeltuin verbanden wir die offizielle Route, lokale Quellen und OpenStreetMap-Geodaten zu einem Routenbuch im Wandertempo.',
    facts=[('5,7 km', 'offizielle Wanderroute'), ('12', 'verbundene Kapitel'), ('70', 'geprüfte Fakten'), ('1', 'tragende Erzähllinie')],
    process_label='Die Arbeitsweise', process_h='Vom Quellenmaterial zur lebendigen Route.',
    process=[
        ('Die Route', 'Sie liefern GPX-Datei, Routenbeschreibung oder Reiseführer. Wir erfassen den echten Weg und sein relevantes Umfeld.'),
        ('Das Wissen', 'Lokale Quellen, Archive und Informationen des Anbieters bilden das Material. Jeder Fakt bleibt nachvollziehbar.'),
        ('Das Routenbuch', 'Kapitel erhalten einen roten Faden, das passende Wander- oder Radtempo und eine menschliche Schlussredaktion.'),
        ('Das Erlebnis', 'Veröffentlichung in 2R, im Web oder per QR-Code — mit Karte, Audio, Lesetext und Quellen.'),
    ],
    audience_label='Für wen', audience_h='Bestehende Routen, ein neues Publikum.',
    audiences=[
        ('Wander- und Radorganisationen', 'Machen Sie aus GPX, Routennetzen und gedruckten Führern ein Erlebnis, das unterwegs von selbst beginnt.'),
        ('Natur und Kulturerbe', 'Lassen Sie Landschaft, Denkmäler und lokale Stimmen eine verlässliche Geschichte erzählen.'),
        ('Städte und Regionen', 'Begrüßen Sie Gäste in ihrer Sprache, ohne selbst eine vollständige App zu bauen.'),
        ('Verlage', 'Ergänzen Sie einen Führer um eine Hörausgabe oder entwickeln Sie ein digitales Routenbuch.'),
    ],
    principle='Eine GPX-Datei zeigt den Weg. 2R erzählt die Geschichte dieses Weges.',
    studio_label='Der nächste Horizont', studio_h='Von der Pilotroute zum 2R Studio.',
    studio_p='Wir beginnen bewusst mit wenigen Routen, die gemeinsam mit ihren Anbietern entstehen. Daraus kann ein Studio wachsen, in dem Organisationen Routen, Quellen und Kapitel selbst verwalten — während 2R Qualität, Stimme und Distribution sichert.',
    final_h='Welche Route verdient zuerst eine Stimme?',
    final_p='Senden Sie uns GPX-Datei, Führer oder Routenseite. Gemeinsam wählen wir eine Route, an der Inhalt, Technik und Publikumsreaktion sichtbar werden.',
    final_cta='Eine Pilotroute erzählen lassen',
),
'fr': dict(
    title='Pour les éditeurs de routes — 2R (Second Route)',
    description="Transformez une randonnée ou un itinéraire cyclable en récit audio vivant et multilingue, avec carte, chapitres, sources et voix chaleureuse.",
    eyebrow='Pour les gestionnaires, éditeurs et acteurs du patrimoine',
    h1='Votre route montre le chemin.<br>2R lui donne une voix.',
    lede="Un fichier GPX indique où marcher ou pédaler. 2R ajoute pourquoi ce chemin compte — sous la forme d'un récit audio soigneusement construit.",
    primary='Parler d’une route pilote', secondary='Écouter notre première route',
    proof_label='Du sentier au récit', proof_h='Une randonnée démontre toute la chaîne.',
    proof_p="Pour le sentier forestier Stulp et Jardin du Château, nous avons réuni la route officielle, les sources locales et les géodonnées OpenStreetMap dans un carnet rythmé pour la marche.",
    facts=[('5,7 km', 'randonnée officielle'), ('12', 'chapitres reliés'), ('70', 'faits vérifiés'), ('1', 'fil narratif')],
    process_label='La méthode', process_h="Des sources à l'itinéraire vivant.",
    process=[
        ("L'itinéraire", 'Vous fournissez un fichier GPX, une description ou un guide. Nous cartographions le tracé réel et son environnement pertinent.'),
        ('Les connaissances', 'Sources locales, archives patrimoniales et informations du gestionnaire forment la matière. Chaque fait reste traçable.'),
        ('Le carnet de route', 'Les chapitres reçoivent un fil rouge, le bon rythme de marche ou de vélo et une relecture humaine finale.'),
        ("L'expérience", 'Publication dans 2R, sur le web ou par QR code — avec carte, audio, texte et sources.'),
    ],
    audience_label='Pour qui', audience_h='Des routes existantes, un nouveau public.',
    audiences=[
        ('Organisations de marche et de vélo', "Transformez GPX, réseaux et guides papier en expérience qui commence d'elle-même."),
        ('Nature et patrimoine', 'Faites du paysage, des monuments et des voix locales une histoire fiable.'),
        ('Villes et régions', 'Accueillez les visiteurs dans leur langue sans devoir construire une application complète.'),
        ('Éditeurs', "Ajoutez une édition audio à un guide existant ou créez un nouveau carnet de route numérique."),
    ],
    principle='Un fichier GPX montre le chemin. 2R raconte l’histoire de ce chemin.',
    studio_label="L'horizon suivant", studio_h='De la route pilote au 2R Studio.',
    studio_p="Nous commençons volontairement par quelques routes créées avec leurs gestionnaires. Cette pratique pourra devenir un Studio où les organisations gèrent routes, sources et chapitres, tandis que 2R veille à la qualité, à la voix et à la diffusion.",
    final_h='Quelle route mérite une voix en premier ?',
    final_p='Envoyez-nous un fichier GPX, un guide ou une page de route. Ensemble, choisissons un itinéraire pour éprouver le contenu, la technologie et la réaction du public.',
    final_cta='Faire raconter une route pilote',
),
'es': dict(
    title='Para editores de rutas — 2R (Second Route)',
    description='Convierte una ruta a pie o en bicicleta en un relato sonoro vivo y multilingüe, con mapa, capítulos, fuentes y una voz cálida.',
    eyebrow='Para gestores de rutas, editores y creadores de patrimonio',
    h1='Tu ruta muestra el camino.<br>2R le da voz.',
    lede='Un archivo GPX indica por dónde caminar o pedalear. 2R añade por qué ese camino importa, como un relato sonoro cuidadosamente construido.',
    primary='Hablar de una ruta piloto', secondary='Escuchar nuestra primera ruta',
    proof_label='Del camino a la historia', proof_h='Una caminata demuestra toda la cadena.',
    proof_p='Para el Boswachterspad Stulp en Kasteeltuin reunimos la ruta oficial, fuentes locales y geodatos de OpenStreetMap en un libro de ruta al ritmo del caminante.',
    facts=[('5,7 km', 'ruta oficial a pie'), ('12', 'capítulos conectados'), ('70', 'datos verificados'), ('1', 'hilo narrativo')],
    process_label='El método', process_h='Del material de origen a una ruta viva.',
    process=[
        ('La ruta', 'Aportas un archivo GPX, una descripción o una guía. Trazamos el recorrido real y su entorno relevante.'),
        ('El conocimiento', 'Fuentes locales, archivos patrimoniales e información del gestor forman la materia prima. Cada dato sigue siendo rastreable.'),
        ('El libro de ruta', 'Los capítulos reciben un hilo conductor, el ritmo adecuado para caminar o pedalear y una revisión humana final.'),
        ('La experiencia', 'Publicación en 2R, en la web o mediante QR — con mapa, audio, texto y fuentes.'),
    ],
    audience_label='Para quién', audience_h='Rutas existentes, un público nuevo.',
    audiences=[
        ('Organizaciones de senderismo y ciclismo', 'Convierte GPX, redes y guías impresas en una experiencia que comienza sola.'),
        ('Naturaleza y patrimonio', 'Haz que paisaje, monumentos y voces locales formen una historia fiable.'),
        ('Ciudades y regiones', 'Recibe a los visitantes en su idioma sin tener que construir una aplicación completa.'),
        ('Editoriales', 'Añade una edición sonora a una guía existente o crea un nuevo libro de ruta digital.'),
    ],
    principle='Un archivo GPX muestra el camino. 2R cuenta la historia de ese camino.',
    studio_label='El siguiente horizonte', studio_h='De la ruta piloto a 2R Studio.',
    studio_p='Empezamos deliberadamente con unas pocas rutas creadas junto a sus gestores. De esa práctica puede crecer un Studio donde las organizaciones gestionen rutas, fuentes y capítulos, mientras 2R cuida la calidad, la voz y la distribución.',
    final_h='¿Qué ruta merece una voz primero?',
    final_p='Envíanos un archivo GPX, una guía o una página de ruta. Juntos elegiremos una ruta para demostrar el contenido, la tecnología y la respuesta del público.',
    final_cta='Deja que narremos una ruta piloto',
),
'pt': dict(
    title='Para editores de rotas — 2R (Second Route)',
    description='Transforme um percurso pedestre ou de bicicleta numa história sonora viva e multilingue, com mapa, capítulos, fontes e uma voz calorosa.',
    eyebrow='Para gestores de rotas, editores e criadores de património',
    h1='A sua rota mostra o caminho.<br>O 2R dá-lhe voz.',
    lede='Um ficheiro GPX indica onde caminhar ou pedalar. O 2R acrescenta porque esse caminho importa — como uma história sonora cuidadosamente construída.',
    primary='Conversar sobre uma rota-piloto', secondary='Ouvir a nossa primeira rota',
    proof_label='Do caminho à história', proof_h='Uma caminhada demonstra toda a cadeia.',
    proof_p='Para o Boswachterspad Stulp en Kasteeltuin reunimos a rota oficial, fontes locais e geodados OpenStreetMap num livro de rota ao ritmo da caminhada.',
    facts=[('5,7 km', 'percurso oficial'), ('12', 'capítulos ligados'), ('70', 'factos verificados'), ('1', 'fio narrativo')],
    process_label='O método', process_h='Das fontes a uma rota viva.',
    process=[
        ('A rota', 'Fornece um ficheiro GPX, descrição ou guia. Mapeamos o percurso real e o contexto relevante.'),
        ('O conhecimento', 'Fontes locais, arquivos patrimoniais e informação do gestor formam a matéria-prima. Cada facto permanece rastreável.'),
        ('O livro de rota', 'Os capítulos ganham um fio condutor, o ritmo certo para caminhar ou pedalar e uma revisão humana final.'),
        ('A experiência', 'Publicação no 2R, na web ou por QR code — com mapa, áudio, texto e fontes.'),
    ],
    audience_label='Para quem', audience_h='Rotas existentes, um novo público.',
    audiences=[
        ('Organizações pedestres e de ciclismo', 'Transforme GPX, redes e guias impressos numa experiência que começa sozinha.'),
        ('Natureza e património', 'Faça da paisagem, dos monumentos e das vozes locais uma história fiável.'),
        ('Cidades e regiões', 'Receba visitantes na sua língua sem construir uma aplicação inteira.'),
        ('Editoras', 'Acrescente uma edição sonora a um guia ou crie um novo livro de rota digital.'),
    ],
    principle='Um ficheiro GPX mostra o caminho. O 2R conta a história desse caminho.',
    studio_label='O horizonte seguinte', studio_h='Da rota-piloto ao 2R Studio.',
    studio_p='Começamos de propósito com algumas rotas feitas em conjunto com os gestores. Dessa prática poderá crescer um Studio onde as organizações gerem rotas, fontes e capítulos, enquanto o 2R protege a qualidade, a voz e a distribuição.',
    final_h='Que rota merece primeiro uma voz?',
    final_p='Envie-nos um ficheiro GPX, guia ou página de rota. Juntos escolhemos uma rota para provar o conteúdo, a tecnologia e a reação do público.',
    final_cta='Deixe-nos narrar uma rota-piloto',
),
}

PROVINCIES = [
    ('Groningen', None), ('Friesland', None), ('Drenthe', None), ('Overijssel', None),
    ('Flevoland', None), ('Gelderland', None), ('Utrecht', 'drakensteyn'),
    ('Noord-Holland', None), ('Zuid-Holland', None), ('Zeeland', None),
    ('Noord-Brabant', None), ('Limburg', None),
]

with open(os.path.join(ROOT, 'routes-content', 'drakensteyn.json'), encoding='utf-8') as _f:
    ROUTE_DRAKENSTEYN = json.load(_f)
ROUTES = {'drakensteyn': ROUTE_DRAKENSTEYN}

# Korte routelede per taal (de hoofdstukken zelf blijven Nederlands)
ROUTE_LEDE = {
 'nl': 'Twaalf hoofdstukken over nonnen, boeren, een freule, boswachters en een koningin — duizend jaar landschap, verteld op precies de goede plek. Zeventig geverifieerde feiten, elk met bron.',
 'en': 'Twelve chapters about nuns, farmers, a baroness, foresters and a queen — a thousand years of landscape, told in exactly the right place. Seventy verified facts, each with its source.',
 'de': 'Zwölf Kapitel über Nonnen, Bauern, eine Freifrau, Förster und eine Königin — tausend Jahre Landschaft, erzählt am genau richtigen Ort. Siebzig verifizierte Fakten, jeder mit Quelle.',
 'fr': "Douze chapitres sur des religieuses, des paysans, une baronne, des forestiers et une reine — mille ans de paysage, racontés exactement au bon endroit. Soixante-dix faits vérifiés, chacun avec sa source.",
 'es': 'Doce capítulos sobre monjas, campesinos, una baronesa, guardabosques y una reina — mil años de paisaje, contados justo en el lugar correcto. Setenta datos verificados, cada uno con su fuente.',
 'pt': 'Doze capítulos sobre freiras, camponeses, uma baronesa, guardas florestais e uma rainha — mil anos de paisagem, contados no lugar certo. Setenta fatos verificados, cada um com sua fonte.',
}

FOCUS_LBL = {
 'nl': {'geschiedenis': 'Geschiedenis', 'natuur': 'Natuur', 'mensen': 'Mensen'},
 'en': {'geschiedenis': 'History', 'natuur': 'Nature', 'mensen': 'People'},
 'de': {'geschiedenis': 'Geschichte', 'natuur': 'Natur', 'mensen': 'Menschen'},
 'fr': {'geschiedenis': 'Histoire', 'natuur': 'Nature', 'mensen': 'Gens'},
 'es': {'geschiedenis': 'Historia', 'natuur': 'Naturaleza', 'mensen': 'Gente'},
 'pt': {'geschiedenis': 'História', 'natuur': 'Natureza', 'mensen': 'Pessoas'},
}


def build_routes_index(lang):
    t = ROUTES_TXT[lang]
    kaarten = ''
    # De route die echt beluisterbaar is staat altijd vooraan. Toekomstige
    # provincies tonen daarna de horizon, niet een blokkade vóór het product.
    for prov, slug in sorted(PROVINCIES, key=lambda item: 0 if item[1] else 1):
        if slug:
            r = ROUTES[slug]
            kaarten += f"""      <a class="prov-kaart live" href="/{lang}/routes/{slug}/">
        <span class="prov-naam">{prov}</span>
        <span class="prov-route">{html.escape(r['naam'])}</span>
        <span class="prov-meta">{str(r['lengte_km']).replace('.', ',')} {t['km']} · {r['hoofdstukken_n']} {t['hoofdstukken']}</span>
        <span class="prov-cta">{t['live']} →</span>
      </a>\n"""
        else:
            kaarten += f"""      <div class="prov-kaart stil">
        <span class="prov-naam">{prov}</span>
        <span class="prov-status">{t['productie']}</span>
      </div>\n"""
    stappen = ''.join(f'<li>{s}</li>' for s in t['kwaliteit'])
    body = f"""  <section class="routes-hero routes-library-hero">
    <img class="routes-hero-photo" src="/images/routes-hero-listening.jpg" alt="{html.escape(t['hero_alt'])}" width="1672" height="941" fetchpriority="high" decoding="async">
    <div class="hero-shade" aria-hidden="true"></div>
    <div class="wrap routes-hero-copy">
      <p class="eyebrow on-dark">{t['eyebrow']}</p>
      <h1>{t['h1']}</h1>
      <p class="routes-lede">{t['lede']}</p>
    </div>
  </section>
  <section class="block"><div class="wrap">
    <div class="prov-grid">
{kaarten}    </div>
  </div></section>
  <section class="block routes-kwaliteit"><div class="wrap">
    <h2>{t['kwaliteit_h']}</h2>
    <p>{t['kwaliteit_p']}</p>
    <ol class="kwaliteit-lijst">{stappen}</ol>
  </div></section>
"""
    titel = {'nl': 'Luisterroutes — 2R (Second Route)', 'en': 'Listening routes — 2R (Second Route)',
             'de': 'Hörrouten — 2R (Second Route)', 'fr': 'Routes audio — 2R (Second Route)',
             'es': 'Rutas de audio — 2R (Second Route)', 'pt': 'Rotas de áudio — 2R (Second Route)'}[lang]
    return page_shell(lang, titel, t['lede'][:150], 'routes', body, path='routes/index.html')


def build_route_page(lang, r):
    t = ROUTES_TXT[lang]
    fl = FOCUS_LBL[lang]
    stops_html = ''
    for c in r['hoofdstukken']:
        paras = ''.join(f'<p>{html.escape(p)}</p>' for p in c['paras'])
        bronnen = ' · '.join(f'<a href="{u}" target="_blank" rel="noopener">{html.escape(n)}</a>' for u, n in c['bronnen'])
        km = str(c['km']).replace('.', ',')
        stops_html += f"""    <article class="rt-stop" id="stop-{c['nr']}">
      <div class="rt-as"><span class="rt-nr">{c['nr']:02d}</span><span class="rt-lijn"></span></div>
      <div class="rt-body">
        <div class="rt-meta">{fl.get(c['focus'], c['focus'])} · {km} {t['km']}</div>
        <h3>{html.escape(c['titel'])}</h3>
        {paras}
        <div class="rt-speler"><span class="rt-speler-kop">{t['hoofdstuk']} {c['nr']:02d}</span>
        <audio controls preload="none" src="{c['audio']}"></audio></div>
        <div class="rt-bron">{t['bron_lbl']}: {bronnen}</div>
      </div>
    </article>\n"""
    haltes_js = json.dumps([{'nr': c['nr'], 'naam': c['titel'], 'lat': c['lat'], 'lng': c['lng']}
                            for c in r['hoofdstukken']], ensure_ascii=False)
    lijnen_js = json.dumps(r['lijnen'])
    taalnoot = f'<p class="rt-taalnoot">{t["taalnoot"]}</p>' if t['taalnoot'] else ''
    lengte = str(r['lengte_km']).replace('.', ',')
    body = f"""  <section class="routes-hero">
    <div class="wrap">
      <p class="eyebrow on-dark">{t['detail_eyebrow']}</p>
      <h1>{html.escape(r['naam'])}</h1>
      <p class="routes-lede">{ROUTE_LEDE[lang]}</p>
      <div class="rt-feiten">
        <div class="hfeit"><b>{lengte} {t['km']}</b></div>
        <div class="hfeit"><b>{r['duur']}</b></div>
        <div class="hfeit"><b>{r['hoofdstukken_n']} {t['hoofdstukken']}</b></div>
        <div class="hfeit"><b>{r['beheerder']}</b></div>
      </div>
    </div>
  </section>
  <section class="block"><div class="wrap">
    <h2>{t['kaart_h']}</h2>
    <p class="rt-kaart-p">{t['kaart_p']}</p>
    <div id="kaart"></div>
    <p class="rt-knoppen">
      <a class="btn-primary" href="{r['gpx_url']}" target="_blank" rel="noopener">{t['gpx']} <span>↓</span></a>
      <a class="text-link" href="{r['bron_url']}" target="_blank" rel="noopener">{t['bronpagina']} →</a>
    </p>
  </div></section>
  <section class="block"><div class="wrap rt-stops">
{taalnoot}
{stops_html}    <p><a class="text-link" href="/{lang}/routes/">{t['terug']}</a></p>
  </div></section>
  <script src="/leaflet.js"></script>
  <script src="{r['kaart_js']}"></script>
  <script src="/vectorkaart.js"></script>
  <script>
  (function() {{
    var kaart = null, wachttimer = null, gestopt = false, pogingen = 0;
    function initKaart() {{
      if (gestopt) return;
      var L = window.L;
      var kaartEl = document.getElementById('kaart');
      if (!kaartEl) return;
      if (!L || !window.KAARTDATA || !window.bouwVectorKaart || kaartEl.clientWidth === 0) {{
        if (pogingen++ < 60) wachttimer = setTimeout(initKaart, 100);
        return;
      }}
      if (kaartEl.dataset.kaartKlaar === '1') return;
      kaartEl.dataset.kaartKlaar = '1';
      kaart = window.bouwVectorKaart(L, kaartEl);
      var haltes = {haltes_js};
      haltes.forEach(function(p) {{
        var icoon = L.divIcon({{ className: '',
          html: '<div style="background:#173B3A;color:#D8A85F;width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:Newsreader,serif;font-weight:500;font-size:13px;border:2px solid #FAF6ED;box-shadow:0 2px 6px rgba(0,0,0,.3)">' + p.nr + '</div>',
          iconSize: [26, 26], iconAnchor: [13, 13] }});
        L.marker([p.lat, p.lng], {{ icon: icoon }}).addTo(kaart)
          .bindPopup('<b>' + p.naam + '</b>')
          .on('click', function() {{
            var el = document.getElementById('stop-' + p.nr);
            if (el) el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
          }});
      }});
      var lijnen = {lijnen_js};
      lijnen.forEach(function(l) {{ L.polyline(l, {{ color: '#FAF6ED', weight: 7, opacity: 0.75 }}).addTo(kaart); }});
      lijnen.forEach(function(l) {{ L.polyline(l, {{ color: '#D96552', weight: 4, opacity: 0.95 }}).addTo(kaart); }});
      setTimeout(function() {{ if (kaart && !gestopt) kaart.invalidateSize(); }}, 300);
    }}
    window.__2rCleanup = function() {{
      gestopt = true;
      if (wachttimer) clearTimeout(wachttimer);
      if (kaart) {{ kaart.remove(); kaart = null; }}
    }};
    initKaart();
  }})();
  </script>
"""
    titel = f"{r['naam']} — 2R"
    extra = '<link rel="stylesheet" href="/leaflet.css">'
    return page_shell(lang, titel, ROUTE_LEDE[lang][:150], 'routes', body,
                      extra_head=extra, path=f"routes/{r['slug']}/index.html")


def build_partners(lang):
    t = PARTNER_TXT[lang]
    facts = ''.join(f'''<div class="partner-fact"><b>{value}</b><span>{label}</span></div>'''
                    for value, label in t['facts'])
    process = ''.join(f'''<article class="partner-step">
        <span>{i:02d}</span><div><h3>{title}</h3><p>{copy}</p></div>
      </article>''' for i, (title, copy) in enumerate(t['process'], 1))
    audiences = ''.join(f'''<article class="partner-audience">
        <span class="num-mark">{i:02d}</span><h3>{title}</h3><p>{copy}</p>
      </article>''' for i, (title, copy) in enumerate(t['audiences'], 1))
    mail = 'mailto:nimco@nentjes.nl?subject=Pilotroute%20voor%202R'
    body = f'''  <section class="partner-hero">
    <img src="/images/reisjournaal.jpg" alt="Een open reisjournaal en kaart als begin van een luisterroute." width="1536" height="1024" fetchpriority="high" decoding="async">
    <div class="hero-shade" aria-hidden="true"></div>
    <div class="partner-hero-copy">
      <p class="eyebrow on-photo">{t['eyebrow']}</p>
      <h1>{t['h1']}</h1>
      <p>{t['lede']}</p>
      <div class="partner-actions">
        <a class="btn-primary" href="{mail}">{t['primary']} <span>↗</span></a>
        <a class="text-link" href="/{lang}/routes/drakensteyn/">{t['secondary']} →</a>
      </div>
    </div>
  </section>

  <section class="partner-proof"><div class="wrap">
    <div class="partner-proof-copy">
      <p class="section-label">{t['proof_label']}</p>
      <h2>{t['proof_h']}</h2>
      <p>{t['proof_p']}</p>
      <a class="text-link on-paper" href="/{lang}/routes/drakensteyn/">{t['secondary']} →</a>
    </div>
    <div class="partner-facts">{facts}</div>
  </div></section>

  <section class="partner-process"><div class="wrap">
    <div class="partner-section-head">
      <p class="section-label">{t['process_label']}</p>
      <h2>{t['process_h']}</h2>
    </div>
    <div class="partner-steps">{process}</div>
  </div></section>

  <section class="partner-principle">
    <blockquote>{t['principle']}</blockquote>
  </section>

  <section class="partner-audiences"><div class="wrap">
    <div class="partner-section-head">
      <p class="section-label">{t['audience_label']}</p>
      <h2>{t['audience_h']}</h2>
    </div>
    <div class="partner-audience-grid">{audiences}</div>
  </div></section>

  <section class="partner-studio"><div class="wrap">
    <p class="eyebrow on-dark">{t['studio_label']}</p>
    <h2>{t['studio_h']}</h2>
    <p>{t['studio_p']}</p>
  </div></section>

  <section class="partner-final"><div class="wrap">
    <h2>{t['final_h']}</h2>
    <p>{t['final_p']}</p>
    <a class="btn-primary" href="{mail}">{t['final_cta']} <span>↗</span></a>
  </div></section>
'''
    return page_shell(lang, t['title'], t['description'], 'partners', body, path='partners/index.html')


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
    write(f'{lang}/routes/index.html', build_routes_index(lang))
    write(f'{lang}/partners/index.html', build_partners(lang))
    for _r in ROUTES.values():
        write(f'{lang}/routes/{_r["slug"]}/index.html', build_route_page(lang, _r))
    for st in STORIES:
        write(f'{lang}/stories/{st["slug"]}.html', build_story_detail(lang, st))
    for i in range(len(CITY_SLUGS)):
        write(f'{lang}/stad/{CITY_SLUGS[i]}.html', build_city_story(lang, i))

# Sitemap + robots: alle publieke pagina's in zes talen
_paden = ['', 'roadmap.html', 'zo-werkt-het.html', 'privacy.html', 'stories/', 'routes/', 'partners/']
_paden += [f'routes/{sl}/' for sl in ROUTES]
_paden += [f'stories/{st["slug"]}.html' for st in STORIES]
_paden += [f'stad/{sl}.html' for sl in CITY_SLUGS]
_urls = [f'{BASE_URL}/{l}/{p}' for p in _paden for l in LANGS]
write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n'
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in _urls)
      + '</urlset>\n')
write('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n')

print(f"Klaar: {len(LANGS)} talen x ({5 + len(STORIES) + len(CITY_SLUGS)} pagina's) = {len(LANGS) * (5 + len(STORIES) + len(CITY_SLUGS))} bestanden")
