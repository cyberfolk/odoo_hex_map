/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { store, useStore } from "../../store";
import { getAxes } from '../../utility/utils.js';
import { useService } from "@web/core/utils/hooks";

export class HexHex extends Component {
    static template = "HexHex"
    static props = ["*"]

    setup() {
        super.setup();
        this.orm = useService("orm")
        this.action = useService("action");
        this.store = useStore()
        this.state = useState({
            id: this.props.id,
            index: this.props.index,
            color: this.props.color,
            hex_asset_id: this.props.hex_asset_id
        })
    }

    getHexStyle() {
        return `${getAxes(this.state.index, 0.95)}; background-color: ${this.state.color}; filter: brightness(${120 - 3 * this.state.index}%);`
    }

    /**
     * Gestisce l'azione di click su un oggetto "hex":
     *  apre il form del "hex" se non è presente un colore corrente,
     *  altrimenti cambia il colore del "hex".
     */
    async onClick(){
        if (this.store.currentColor)
            this.changeColorHex(this.state.id)
        else if (this.store.currentTile.tile_id){
            this.setAssetTiles(this.state.id)}
        else {
            this.goToViewForm(this.state.id)
        }
    }
    async changeColorHex(){
        await this.orm.call("hex.hex", "change_hex_color", [this.state.id, this.store.currentColor], {});
        this.state.color = this.store.currentColor
    }

    /**
     * Cambia il tales selezionato settandolo con il currentTile, poi aggiorna la macroarea.
     */
    async setAssetTiles(){
        await this.orm.call("hex.hex", "set_asset_tiles", [this.state.id , this.store.currentTile], {});
        const { rotation, tile_id } = this.store.currentTile;
        this.state.hex_asset_id = { rotation, tile_id };
    }


        /**
    * Apre la view-form del hex_id passato.
    */
    goToViewForm(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Form View',
            res_model: 'hex.hex',
            res_id: this.state.id,
            views: [[false, 'form']],
            target: 'current'
        });
    }

}
