// Copyright (c) 2025, Jan and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Polisa", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Polisa', {
    typ_polisy: function (frm) {
        // Poczekaj aż formularz się odświeży
        setTimeout(function () {
            // Sprawdź czy pola istnieją przed ich ukrywaniem
            if (frm.fields_dict['szczegoly_komunikacyjna']) {
                frm.fields_dict['szczegoly_komunikacyjna'].df.hidden = 1;
            }
            if (frm.fields_dict['szczegoly_mieszkaniowa']) {
                frm.fields_dict['szczegoly_mieszkaniowa'].df.hidden = 1;
            }

            // Pokaż odpowiednią sekcję
            if (frm.doc.typ_polisy === 'Komunikacyjna') {
                if (frm.fields_dict['szczegoly_komunikacyjna']) {
                    frm.fields_dict['szczegoly_komunikacyjna'].df.hidden = 0;
                }
            } else if (frm.doc.typ_polisy === 'Mieszkaniowa') {
                if (frm.fields_dict['szczegoly_mieszkaniowa']) {
                    frm.fields_dict['szczegoly_mieszkaniowa'].df.hidden = 0;
                }
            }

            frm.refresh_fields();
        }, 100);
    },

    refresh: function (frm) {
        // Ukryj wszystkie na starcie
        if (frm.fields_dict['szczegoly_komunikacyjna']) {
            frm.fields_dict['szczegoly_komunikacyjna'].df.hidden = 1;
        }
        if (frm.fields_dict['szczegoly_mieszkaniowa']) {
            frm.fields_dict['szczegoly_mieszkaniowa'].df.hidden = 1;
        }

        // Jeśli typ jest już wybrany, pokaż odpowiednie pola
        if (frm.doc.typ_polisy) {
            frm.trigger('typ_polisy');
        }
    }
});

frappe.ui.form.on('Polisa', {
    refresh: function (frm) {
        // Sprawdzamy czy dokument jest zapisany na kilka sposobów
        var is_saved = frm.doc.name || frm.doc.__islocal === 0 || frm.doc.docstatus === 1;

        if (is_saved) {
            // Ustaw pole jako read-only
            frm.set_df_property('typ_polisy', 'read_only', 1);
            frm.refresh_field('typ_polisy');

            // Opcjonalnie: ukryj pole
            // frm.set_df_property('typ_polisy', 'hidden', 1);
        }
    }
});