/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { store, useStore } from "../../store";

export class DirTiles extends Component {
    static template = "DirTiles"
    static props = ["tiles"]

    setup() {
        super.setup();
        this.store = useStore()
        this.state = useState({
            collapse: true,
        })
        this.tiles = this.props.tiles
    }

    setCurrentTile(tile_id){
    store.currentColor = ''
        if (this.store.currentTile.tile_id == tile_id){
            this.store.currentTile.rotation += 60
            this.store.currentTile.rotation %= 360
        }
        else{
            this.store.currentTile.tile_id = tile_id
            this.store.currentTile.rotation = 0
        }
    }
    toggleCollapse(){
        this.state.collapse = !this.state.collapse
    }
}
