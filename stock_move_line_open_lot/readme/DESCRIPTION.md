The existing button to the right of the lot/serial number, which currently opens a reduced (quick) view, is removed. It is replaced by a new button that opens the full form view of the corresponding lot/serial number when clicked.

This change is controlled by two new boolean fields:

- show_lot_button: If enabled, this field makes the icon "Open Lot Form" button visible on the picking form. When this button is clicked, it opens the full form view of the corresponding lot/serial number.

- lot_form_as_popup: If enabled, this field ensures the lot form opens as a popup/modal instead of a full form view.
