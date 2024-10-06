/** @odoo-module **/
import { DirTiles } from '@cf_hex_base/ViewMacro/DirTiles/DirTiles';
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { store, useStore } from "../../store";

export class CurrentTiles extends Component {
    static template = "CurrentTiles"
    static props = ["*"]
    static components = { DirTiles };

    setup() {
        super.setup();
        this.store = useStore()
        this.store.add({
            tilesKit: null,
            currentTile: {tile_id: "", rotation: 0},
        })
        this.orm = useService("orm");

        onWillStart(async () => {
            store.tilesKit = await this.orm.call("asset.tile", "get_json_tiles_kit", [], {})
                .then((result) => { return JSON.parse(result) })
        })
    }
}
