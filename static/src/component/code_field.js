/** @odoo-module **/ // <-- Commento necessario
// Definisco e registro un widget personalizzato CodeField.

const { xml, Component } = owl;
// Component ----------> è usato come base per creare componenti OWL.
// xml ----------------> è usato per definire i template dei componenti.
import { standardFieldProps } from "@web/views/fields/standard_field_props";
// standardFieldProps -> oggetto che contiene le proprietà standard per i campi di Odoo.
import { registry } from "@web/core/registry";
// registry -----------> registro dei vari componenti, azioni, servizi, ecc.




export class CodeField extends Component {
    // Estendo Component di OWL per creare un nuovo componente denominato CodeField.
    setup() {
        // Sovrascrivo il metodo setup(). Al momento non fa nulla.
        // Metodo fondamentale per gestire la logica del ciclo di vita dei componenti OWL.
        this.props.value = "Forzo il campo con questa stringa di Default."

        super.setup();
        // Richiamo il metodo setup della classe padre, da fare quando faccio l'override di setup().
    }
}


CodeField.template = xml`<pre t-esc="props.value" class="bg-primary text-white p-3 rounded"/>`;
// Definisce un template XML per il componente utilizzando la sintassi backtick per una stringa template literal.
// Il template mostra il valore passato al componente (props.value) all'interno di un elemento <pre>,
// con alcune classi CSS per lo stile (sfondo primario, testo bianco, padding, bordi arrotondati).

CodeField.props = standardFieldProps;
// Assegno standardFieldProps alle proprietà del componente CodeField.
// Ciò significa che CodeField accetterà tutte le proprietà standard definite in standardFieldProps, rendendolo compatibile con altri campi in Odoo.


registry.category("fields").add("code", CodeField);
// Registra il componente CodeField nel registro di Odoo sotto la categoria "fields" con il nome "code".
// Questo consente al componente di essere riconosciuto e utilizzato all'interno dell'ecosistema Odoo come un tipo di campo personalizzato.