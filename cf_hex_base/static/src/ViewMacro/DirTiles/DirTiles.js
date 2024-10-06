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
        if (this.store.currentTile.tile_id == tile_id){
            if (this.store.currentTile.rotation >= 300)
                this.store.currentTile.rotation = 0
            else
                this.store.currentTile.rotation += 60
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
