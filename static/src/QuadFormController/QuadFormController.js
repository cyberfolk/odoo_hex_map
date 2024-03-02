/** @odoo-module */
import {HelloWorld} from '@cf_owl/HelloWorld/HelloWorld';
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { Component } from '@odoo/owl';


class QuadFormController extends FormController {
    // static components = { QuadFormController, HelloWorld }; // TODO-: Da errore qui.

    // Your logic here, override or insert new methods...
    // if you override setup(), don't forget to call super.setup()
}

QuadFormController.template = "QuadFormView";

export const quadFormView = {
    ...formView, // contains the default Renderer/Controller/Model
    Controller: QuadFormController,
};

registry.category("views").add("quad_form", quadFormView);
