odoo.define('cf_hex_map.mio_modulo', function (require) {
    "use strict";

    var core = require('web.core');
    var QWeb = core.qweb;

    // Assumiamo che 'dati' sia l'oggetto che vuoi passare al template
    var dati = {name: "Mario", color: "Rosso"};

    // Renderizza il template e passa l'oggetto 'dati'
    var contenutoHTML = QWeb.render('template_dinamico', {
        dato: dati
    });

    // Il risultato 'contenutoHTML' può ora essere inserito nel DOM
    $("#elementoTarget").html(contenutoHTML);
});
