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
        return env.ASSETS.fetch(request);
    }
};
