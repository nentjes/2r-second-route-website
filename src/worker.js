// 2route.nl — minimale worker vóór de statische assets.
// Enige taak: www.2route.nl permanent doorverwijzen naar het hoofddomein,
// zodat de site op precies één adres leeft (canonicals wijzen daar al heen).
// Alle overige verzoeken gaan ongewijzigd door naar de assets.
export default {
    async fetch(request, env) {
        const url = new URL(request.url);
        if (url.hostname === 'www.2route.nl') {
            url.hostname = '2route.nl';
            return Response.redirect(url.toString(), 301);
        }
        const antwoord = await env.ASSETS.fetch(request);
        // Routeboek-data en -audio zijn publieke bestanden die de 2R-app
        // (origin capacitor://localhost) met fetch ophaalt — dat vereist
        // CORS. Alleen deze paden; de rest van de site blijft zonder.
        if (url.pathname.startsWith('/routes-data/') || url.pathname.startsWith('/audio/routes/')) {
            const open = new Response(antwoord.body, antwoord);
            open.headers.set('Access-Control-Allow-Origin', '*');
            return open;
        }
        return antwoord;
    }
};
