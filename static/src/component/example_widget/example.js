/** @odoo-module **/ // <-- Commento necessario
// Definisco e registro un widget personalizzato ExampleField.

// IMPORTAZIONI
const { xml, Component } = owl;
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
// standardFieldProps -> oggetto che contiene le proprietà standard per i campi di Odoo.
// Component ----------> è usato come base per creare componenti OWL.
// registry -----------> registro dei vari componenti, azioni, servizi, ecc.
// xml ----------------> è usato per definire i template dei componenti.

// DEFINISCO ExampleField ESTENDENDO Component.
export class ExampleField extends Component {
    // Sovrascrivo il metodo setup(). Metodo fondamentale per gestire la logica del ciclo di vita dei componenti OWL.
    setup() {
        this.props.value = "Default vaulue inserito da javascript."
        super.setup(); // Richiamo il metodo setup della classe padre per eseguire correttamente l'override.

        // PROPS EREDITATE DA standardFieldProps
        // this.props.name   = this.props.id = Il nome del campo su cui applico il widget
        // this.props.type   = Il tipo del campo su cui applico il widget
        // this.props.data   = ???
        // this.props.value  = Valore del campo su cui applico il widget
        // this.props.record = Oggetto definito in odoo/addons/web/static/src/views/basic_relational_model.js contiene molte info sul record corrente visualizzato nella vista.
        // this.props.record.data         = trovo i campi del modello e il relativo valore.
        // this.props.record.mode         = edit o read-only.
        // this.props.record.model        = L'attuale classe js con tutti i suoi meedtodi
        // this.props.record.fields       = Archivio key-value di tutti gli altri suoi campi.
        // this.props.record.context      = Oggetto che continere il contesto di Odoo
        // this.props.record.resModel     = Il modello della vista.
        // this.props.record.activeFields = I campi usati nella vista.
        // this.props.decorations = Oggetto particolare per evidenziare i campi di testo.
        // this.props.setDirty e this.props.update = Sono funzioni per aggiornare il db col nuovo valore del field.
    }

    async updateValue() {
        // Metodo per aggiornare il valore del campo, con controllo per evitare aggiornamenti non necessari.
        const value = this.currentValue;
        const lastValue = (this.props.value || "").toString();
        if (value !== null && !(!lastValue && value === "") && value !== lastValue) {
            await this.props.update(value); // Esegue l'aggiornamento del valore mediante la prop update.
        }
    }
}

// DEFINIRE TEMPLATE
// OPZIONE-1: TEMPLATE ESTERNO
ExampleField.template = "example_template";
// OPZIONE-2: TEMPLATE LITERAL
// ExampleField.template = xml`<pre t-esc="props.value" class="bg-primary text-white p-3 rounded"/>`;

// CREO LE PROPS CUSTOM DI DEFAULT
ExampleField.defaultProps = { bgColor: "primary", };

// DEFINISCO LE PROPS
// OPZIONE-1: Eredito props base + Aggiungo props custom.
ExampleField.props = {
    ...standardFieldProps, // spreddo standardFieldProps ereditanto le sue props
    bgColor: { type: String, optional: true },  // definisco la mia props custom
};
// OPZIONE-2: Eredito props base
// ExampleField.props = standardFieldProps;

// Estraggo le opzioni dal widget e le passo alle relative props
ExampleField.extractProps = ({ attrs, field }) => {
    return { bgColor: attrs.options.bg_color, };
};

// Registra il componente ExampleField nel registro di Odoo sotto la categoria "fields" con il nome "code".
// Questo consente al componente di essere riconosciuto e utilizzato all'interno dell'ecosistema Odoo come un tipo di campo personalizzato.
registry.category("fields").add("example", ExampleField);
