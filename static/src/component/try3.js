/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
const rpc = require('web.rpc');
export class MonteoreListController extends ListController {
   setup() {
       super.setup();
   }
   RecuperoOre() {
       this.actionService.doAction({
          type: 'ir.actions.act_window',
          res_model: 'wizard.monte.ore',
          name:'Open Wizard',
          view_mode: 'form',
          view_type: 'form',
          views: [[false, 'form']],
          target: 'new',
          res_id: false,
      });
   }

   UpdateHourCalculation() {
        var self = this; // Serve perchè nel then non funziona il this
        rpc.query({
            model: 'timesheet.analytic.week',
            method: 'update_record',
            args: [[]],
        }).then((result) => {
            self.actionService.doAction(result);
        });
   }
}
registry.category("views").add("button_monte_ore", {
   ...listView,
   Controller: MonteoreListController,
   buttonTemplate: "recupero_monte.ListView.Buttons",
});






