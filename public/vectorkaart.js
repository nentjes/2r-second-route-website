/* 2R vectorkaart-renderer v1.0 (30 aug 2026)
 *
 * Tekent de door maak-vectorkaart.py voorbereide OSM-vectordata
 * (window.KAARTDATA) als merk-eigen 2R-kaart in Leaflet, op Canvas-basis.
 * Drie detailniveaus met zoomafhankelijke zichtbaarheid:
 *   niveau 1 (omgeving)    — altijd zichtbaar
 *   niveau 2 (gebied)      — vanaf zoom 12
 *   niveau 3 (routedetail) — vanaf zoom 14
 * Route, haltes en audio van de pagina blijven erbuiten; deze module levert
 * alleen de ondergrond en geeft het kaartobject terug.
 *
 * Gebruik:  var kaart = bouwVectorKaart(L, kaartEl);
 */
function bouwVectorKaart(L, kaartEl) {
  var D = window.KAARTDATA;
  var Q = D.meta.quant;

  // Delta-integers terug naar [lat, lng]-paren.
  function decodeer(enc) {
    var uit = [], lat = 0, lng = 0;
    for (var i = 0; i < enc.length; i += 2) {
      lat += enc[i]; lng += enc[i + 1];
      uit.push([lat * Q, lng * Q]);
    }
    return uit;
  }

  function naarLngLat(enc) {
    return decodeer(enc).map(function (p) { return [p[1], p[0]]; }); // GeoJSON = [lng,lat]
  }

  function alsGeoJSON(items, vlak) {
    return { type: 'FeatureCollection', features: items.map(function (it) {
      var geometrie;
      if (Array.isArray(it[1][0])) {
        // Multipolygoon-ringen (buitenring + eventuele gaten)
        geometrie = { type: 'Polygon', coordinates: it[1].map(naarLngLat) };
      } else {
        var co = naarLngLat(it[1]);
        var dicht = co.length > 3 &&
          co[0][0] === co[co.length - 1][0] && co[0][1] === co[co.length - 1][1];
        var alsVlak = vlak || (it[0] === 'gebouw' && dicht);
        geometrie = alsVlak ? { type: 'Polygon', coordinates: [co] }
                            : { type: 'LineString', coordinates: co };
      }
      return { type: 'Feature',
        properties: { k: it[0], brug: it[2] === 1 },
        geometry: geometrie };
    }) };
  }

  // 2R-kaartstijl: uitsluitend tinten van bestaande stijlgids-tokens.
  var INK = '#17242B', PETROL = '#173B3A', COGNAC = '#A96642',
      MOSS = '#66715C', GOUD = '#D8A85F';
  var VLAK = {
    bos:   { stroke: false, fillColor: MOSS,   fillOpacity: 0.22 },
    bebouwd: { stroke: false, fillColor: INK,  fillOpacity: 0.07 },
    heide: { stroke: false, fillColor: GOUD,   fillOpacity: 0.16 },
    zand:  { stroke: false, fillColor: GOUD,   fillOpacity: 0.30 },
    gras:  { stroke: false, fillColor: MOSS,   fillOpacity: 0.09 },
    water: { color: PETROL, weight: 0.6, opacity: 0.30, fillColor: PETROL, fillOpacity: 0.22 }
  };
  var LIJN = {
    snelweg:   { color: INK, weight: 2.6, opacity: 0.70 },
    hoofdweg:  { color: INK, weight: 1.9, opacity: 0.55 },
    secundair: { color: INK, weight: 1.4, opacity: 0.42 },
    lokaal:    { color: INK, weight: 1.0, opacity: 0.30 },
    erf:       { color: INK, weight: 0.7, opacity: 0.20 },
    spoor:     { color: INK, weight: 1.3, opacity: 0.45, dashArray: '6 5' },
    rivier:    { color: PETROL, weight: 2.0, opacity: 0.45 },
    kanaal:    { color: PETROL, weight: 1.5, opacity: 0.45 },
    beek:      { color: PETROL, weight: 1.0, opacity: 0.40 },
    fietspad:  { color: COGNAC, weight: 1.1, opacity: 0.50, dashArray: '5 3' },
    track:     { color: COGNAC, weight: 1.0, opacity: 0.45, dashArray: '7 3' },
    pad:       { color: COGNAC, weight: 1.2, opacity: 0.75, dashArray: '2.5 2.5' },
    gebouw:    { color: COGNAC, weight: 1.0, opacity: 0.55, fillColor: COGNAC, fillOpacity: 0.22 }
  };
  // Ver uitgezoomd horen wegen dunner en rustiger; dichtbij op volle sterkte.
  var verModus = false;
  function stijl(f) {
    var s, p = f.properties;
    if (f.geometry.type === 'Polygon' && p.k !== 'gebouw') s = VLAK[p.k];
    else s = LIJN[p.k];
    s = s ? Object.assign({}, s) : { color: INK, weight: 1, opacity: 0.3 };
    if (p.brug) { s.weight = (s.weight || 1) + 0.7; s.opacity = Math.min(1, (s.opacity || 0.5) + 0.2); }
    if (verModus && f.geometry.type === 'LineString') {
      s.weight = (s.weight || 1) * 0.55;
      s.opacity = (s.opacity || 0.5) * 0.8;
    }
    return s;
  }

  var kaart = L.map(kaartEl, {
    preferCanvas: true,
    scrollWheelZoom: false,
    minZoom: 11, maxZoom: 18,
    zoomSnap: 0.5,
    maxBounds: [[D.meta.maxBbox[0] - 0.01, D.meta.maxBbox[1] - 0.015],
                [D.meta.maxBbox[2] + 0.01, D.meta.maxBbox[3] + 0.015]],
    maxBoundsViscosity: 0.8,
    attributionControl: true
  });
  kaart.attributionControl.setPrefix(false);
  kaart.attributionControl.addAttribution('© OpenStreetMap contributors');

  // Vaste tekenvolgorde via panes: ondergrond per niveau, route en haltes
  // van de pagina komen in de standaard-panes (400/600) daar altijd bovenop.
  // Vlakken (bos, heide, water, bebouwing) zijn op elk zoomniveau zichtbaar —
  // anders "verdwijnt" het bos bij uitzoomen; alleen lijnen zijn zoomafhankelijk.
  var vlakGroepen = {}, lijnGroepen = {};
  [1, 2, 3].forEach(function (n) {
    var paneNaam = 'basis' + n;
    kaart.createPane(paneNaam).style.zIndex = String(190 + n * 10);
    var renderer = L.canvas({ pane: paneNaam });
    var laag = D.lagen[String(n)];
    vlakGroepen[n] = L.layerGroup([L.geoJSON(alsGeoJSON(laag.vlakken, true),
      { style: stijl, renderer: renderer, pane: paneNaam, interactive: false })]);
    lijnGroepen[n] = L.layerGroup([L.geoJSON(alsGeoJSON(laag.lijnen, false),
      { style: stijl, renderer: renderer, pane: paneNaam, interactive: false })]);
  });

  // Labels: plaatsnamen (niveau 1+2) en orientatiepunten (vanaf zoom 13).
  function labelLaag(labels, soortFilter, klasse, richting) {
    var g = L.layerGroup();
    labels.forEach(function (lb) {
      if (lb[1] !== soortFilter) return;
      var m = L.marker([lb[2], lb[3]], {
        icon: L.divIcon({ className: '', html: '', iconSize: [0, 0] }),
        interactive: false, keyboard: false
      });
      m.bindTooltip(lb[0], { permanent: true, direction: richting,
        className: klasse, opacity: 1, offset: [0, 0] });
      m.addTo(g);
    });
    return g;
  }
  var labelsPlaats1 = labelLaag(D.lagen['1'].labels, 'plaats', 'kl-plaats', 'center');
  var labelsPlaats2 = labelLaag(D.lagen['2'].labels, 'plaats', 'kl-gehucht', 'center');
  var labelsPunt = L.layerGroup();
  D.lagen['2'].labels.forEach(function (lb) {
    if (lb[1] !== 'punt') return;
    var stip = L.circleMarker([lb[2], lb[3]], {
      radius: 2.5, color: PETROL, weight: 1, opacity: 0.7,
      fillColor: GOUD, fillOpacity: 0.9, interactive: false
    });
    stip.bindTooltip(lb[0], { permanent: true, direction: 'right',
      className: 'kl-punt', opacity: 1, offset: [5, 0] });
    stip.addTo(labelsPunt);
  });

  vlakGroepen[1].addTo(kaart);
  vlakGroepen[2].addTo(kaart);
  vlakGroepen[3].addTo(kaart);
  lijnGroepen[1].addTo(kaart);
  labelsPlaats1.addTo(kaart);

  function herstijlLijnen() {
    [1, 2, 3].forEach(function (n) {
      lijnGroepen[n].eachLayer(function (l) { if (l.setStyle) l.setStyle(stijl); });
    });
  }

  function werkZichtbaarheidBij() {
    var z = kaart.getZoom();
    function zet(laag, aan) {
      if (aan && !kaart.hasLayer(laag)) kaart.addLayer(laag);
      if (!aan && kaart.hasLayer(laag)) kaart.removeLayer(laag);
    }
    zet(lijnGroepen[2], z >= 12);
    zet(lijnGroepen[3], z >= 14);
    zet(labelsPlaats2, z >= 12);
    zet(labelsPunt, z >= 13);
    var nieuwVer = z < 13;
    if (nieuwVer !== verModus) { verModus = nieuwVer; herstijlLijnen(); }
  }
  kaart.on('zoomend', werkZichtbaarheidBij);

  // Openen: de route met 30-40% context eromheen.
  var rb = D.meta.routeBbox;
  kaart.fitBounds([[rb[0], rb[1]], [rb[2], rb[3]]], { padding: [40, 40] });
  werkZichtbaarheidBij();

  return kaart;
}
