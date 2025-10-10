import frappe
from frappe.model.document import Document

# class SalesPersonController(Document):  # Nazwa klasy zgodna z plikiem
#     def before_insert(self):
#         # Ustaw aktualnie zalogowanego użytkownika
#         if frappe.session.user != "Administrator":  # Opcjonalnie: pomiń dla admina
#             self.user = frappe.session.user
    
#     def validate(self):
#         # Zabezpieczenie przed zmianą użytkownika
#         if self.is_new() and not self.user:
#             self.user = frappe.session.user


def before_insert(doc, method=None):
    """Auto-set logged in user when creating new Sales Person"""
    try:
        if not doc.get('user') and frappe.session.user:
            doc.user = frappe.session.user
    except Exception as e:
        frappe.log_error(f"Error in before_insert: {str(e)}")

def before_save(doc, method=None):
    """Auto-set user if missing on save"""
    try:
        if not doc.get('user') and frappe.session.user:
            doc.user = frappe.session.user
    except Exception as e:
        frappe.log_error(f"Error in before_save: {str(e)}")


def set_current_user(doc, method=None):
    """Set current user for Sales Person"""
    frappe.log_info(f"🎯 HOOK STARTED for {doc.doctype} - method: {method}", "Hook Debug")
    
    if doc.doctype == "Sales Person":
        frappe.log_info(f"📝 Processing Sales Person: {doc.get('name')}", "Hook Debug")
        frappe.log_info(f"👤 Session user: {frappe.session.user}", "Hook Debug")
        
        if not doc.get('user'):
            doc.user = frappe.session.user
            frappe.log_info(f"✅ User set to: {doc.user}", "Hook Debug")
        else:
            frappe.log_info(f"ℹ️ User already set to: {doc.get('user')}", "Hook Debug")
    
    frappe.log_info("🎯 HOOK COMPLETED", "Hook Debug")