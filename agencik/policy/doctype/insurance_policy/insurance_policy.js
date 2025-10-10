frappe.ui.form.on('Insurance Policy', {
    calculate_your_commission: function (frm) {
        calculateCommission(frm);
    },

    // Automatyczne obliczanie przy zmianie komponentów
    insurancee_components_add: function (frm) {
        calculateCommission(frm);
    },

    insurancee_components_remove: function (frm) {
        calculateCommission(frm);
    }
});

function calculateCommission(frm) {
    if (!frm.doc.insurancee_components || frm.doc.insurancee_components.length === 0) {
        frappe.msgprint(__('Please select at least one insurance component first.'));
        frm.set_value('commission_vehicle', 0);
        frm.refresh_field('commission_vehicle');
        return;
    }

    // Użyj metody z dokumentu zamiast z modułu
    frm.call('calculate_commission_api').then(r => {
        if (r.message) {
            const commission_amount = r.message.commission;
            const components_count = r.message.components_count;

            // Odśwież pole (powinno być już ustawione przez backend)
            frm.refresh_field('commission_vehicle');

            frappe.show_alert({
                message: __('Commission calculated: {0} based on {1} components',
                    [format_currency(commission_amount), components_count]),
                indicator: 'green'
            });
        }
    }).catch(err => {
        console.error('Error calculating commission:', err);
        frappe.msgprint(__('Error calculating commission. Please try again.'));
    });
}