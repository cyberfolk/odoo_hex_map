/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { getAxes } from '../utility/utils.js';
const actionRegistry = registry.category("actions");

class ViewMacro extends Component {
    static template = "ViewMacro"
    static components = {};

    setup() {
        super.setup();
        this.action = useService("action");
        this.orm = useService("orm");
        this.macro = null
        this.zoom = '100%'
        this.currentColor = ""
        this.currentTile_id = ""
        this.tilesKit = null

        onWillStart(async () => {
            this.macro = await this.orm.call("hex.macro", "get_json_macro", [], {})
            .then((result) => { return JSON.parse(result) })
            this.tilesKit = await this.orm.call("asset.tile", "get_json_tiles_kit", [], {})
            .then((result) => { return JSON.parse(result) })
            console.log(this.macro)
        })
    }
    setZoom(percentage){
        this.zoom = percentage
        this.render();
    }

    setCurrentColor(color){
        this.currentColor = color
        this.currentTile = ''
        this.render();
    }

    setCurrentTile(tile_id){
        this.currentTile = tile_id
        this.currentColor = ''
        this.render();
    }

    /**
     * Gestisce l'azione di click su un oggetto "hex":
     *  apre il form del "hex" se non è presente un colore corrente,
     *  altrimenti cambia il colore del "hex".
     */
    async onClick(hex){
        const hex_id = hex.id;

        if (this.currentColor)
            this.changeColorHex(hex_id)
        else if (this.currentTile)
            this.setAssetTiles(hex_id)
        else {
            this.goToViewForm(hex_id)
        }
    }

     /**
     * Apre la view-form del hex_id passato.
     */
    goToViewForm(hex_id){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Form View',
            res_model: 'hex.hex',
            res_id: hex_id,
            views: [[false, 'form']],
            target: 'current'
        });
    }

    /**
     * Cambia il colore di hex_id settandolo con il currentColor, poi aggiorna la macroarea la renderizza.
     */
    async changeColorHex(hex_id){
        await this.orm.call("hex.hex", "change_hex_color", [hex_id, this.currentColor], {});
        console.log("Color changed successfully");
        this.macro = await this.orm.call("hex.macro", "get_json_macro", [], {})
            .then((result) => { return JSON.parse(result) })
        this.render(true);
    }

    /**
     * Cambia il colore di hex_id settandolo con il currentColor, poi aggiorna la macroarea la renderizza.
     */
    async setAssetTiles(hex_id){
        await this.orm.call("hex.hex", "set_asset_tiles", [hex_id, this.currentTile], {});
        console.log("Asset Set successfully");
        this.macro = await this.orm.call("hex.macro", "get_json_macro", [], {})
            .then((result) => { return JSON.parse(result) })
        this.render(true);
    }

    getHexStyle(hex) {
        return `${getAxes(hex.index, 0.95)}; background-color: ${hex.color}; filter: brightness(${120 - 3 * hex.index}%);`
    }

    getQuadStyle(quad) {
        return `${getAxes(quad.index, 0.97)}; z-index: ${20 - quad.index}; clip-path: ${quad.polygon};`
    }
}

actionRegistry.add('view_macro', ViewMacro);
