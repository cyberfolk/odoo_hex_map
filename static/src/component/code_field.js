/** @odoo-module **/ // <-- Commento necessario
// Definisco e registro un widget personalizzato CodeField.

const { xml, Component } = owl;
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
// standardFieldProps -> oggetto che contiene le proprietà standard per i campi di Odoo.
// Component ----------> è usato come base per creare componenti OWL.
// registry -----------> registro dei vari componenti, azioni, servizi, ecc.
// xml ----------------> è usato per definire i template dei componenti.

export class CodeField extends Component {
    // Estendo Component di OWL per creare un nuovo componente denominato CodeField.
    setup() {
        // Sovrascrivo il metodo setup(). Al momento non fa nulla.
        // Metodo fondamentale per gestire la logica del ciclo di vita dei componenti OWL.
        this.props.value = "Default vaulue inserito da javascript."
        console.log(`PROPS EREDITATE DA STANDARD-FIELD-PROPS`)
        console.log(`->   this.props.name = this.props.id = ${this.props.id} = Il nome del campo.`)
        console.log(`->   this.props.type = ${this.props.type}`)
        console.log(`->   this.props.data = ${this.props.data} = ???`)
        console.log(`->  this.props.value = ${this.props.value}`)
        console.log(`-> this.props.record = Oggetto definito in odoo/addons/web/static/src/views/basic_relational_model.js contiene molte info sul record corrente visualizzato nella vista.`)
        console.log(`->         ...mode = 'edit' o 'read-only'.`)
        console.log(`->        ...model = L'attuale classe js con tutti i suoi meedtodi`)
        console.log(`->       ...fields = Archivio key-value di tutti gli altri suoi campi.`)
        console.log(`->      ...context = Oggetto che continere il contesto di Odoo`)
        console.log(`->     ...resModel = Il modello della vista.`)
        console.log(`-> ...activeFields = I campi usati nella vista.`)
        console.log(this.props.record)
        console.log(`-> this.props.decorations =  Oggetto particolare per evidenziare i campi di testo.`)
        console.log(this.props.decorations)
        console.log(`-> this.props.setDirty e this.props.update = Sono funzioni per aggiornare il db col nuovo valore del field.`)
        super.setup();
        // Richiamo il metodo setup della classe padre, da fare quando faccio l'override di setup().
    }

    async updateValue() {
        const value = this.currentValue;
        const lastValue = (this.props.value || "").toString();
        if (value !== null && !(!lastValue && value === "") && value !== lastValue) {
            // calling the update function with await
            await this.props.update(value);
        }
    }

}

// OPZIONE-1 PER DEFINIRE IL TEMPLATE
CodeField.template = "cf.CodeField";
// OPZIONE-2 PER DEFINIRE IL TEMPLATE
// CodeField.template = xml`<pre t-esc="props.value" class="bg-primary text-white p-3 rounded"/>`;
// Definisce un template XML per il componente utilizzando la sintassi backtick per una stringa template literal.


// CREO LE PROPS CUSTOM DI DEFAULT
CodeField.defaultProps = {
    bgColor: "primary",
};

// OPZIONE-2 PER EREDITARE LE PROPS
// Assegno standardFieldProps alle proprietà del componente CodeField.
// Ciò significa che CodeField accetterà tutte le proprietà standard definite in standardFieldProps,
// Più le nuove proprietà custom rendendo il componente compatibile con altri campi in Odoo.
CodeField.props = {
    ...standardFieldProps,                      // spreddo standardFieldProps
    bgColor: { type: String, optional: true },  // definisco la mia props custom
};

// OPZIONE-2 PER EREDITARE LE PROPS
// CodeField.props = standardFieldProps;

// Extract bgColor from the attributes
CodeField.extractProps = ({ attrs, field }) => {
    console.log(attrs)
    return {
        // We are looking for attr "bg_color", snake case
        bgColor: attrs.options.bg_color,
    };
};
registry.category("fields").add("code", CodeField);
// Registra il componente CodeField nel registro di Odoo sotto la categoria "fields" con il nome "code".
// Questo consente al componente di essere riconosciuto e utilizzato all'interno dell'ecosistema Odoo come un tipo di campo personalizzato.
