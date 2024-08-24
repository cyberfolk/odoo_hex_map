/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { jsonrpc } from "@web/core/network/rpc_service";
const actionRegistry = registry.category("actions");


class ExpTool extends Component {
    static template = "ExpTool";
    static components = {};

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.exp_table = null;
        const rpc = useService("rpc");  // Use the RPC service for making HTTP requests to the server

        onWillStart(async () => {
            this.exp_table = await jsonrpc(
            '/your_controller_route', {}
            ).then((res)=>{
                console.log(res)
                return res
            }).catch((error) => {
                console.error("Error fetching data:");
                return null;
            });

        });
    }
}
actionRegistry.add('exp_tool', ExpTool);
