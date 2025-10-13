import frappe
from frappe.model.document import Document
from frappe.utils import add_years
from frappe import _

class InsurancePolicy(Document):




    def length_company(doc, method):
        if doc.insurance_company == "Allianz":
            if len(doc.policy_number) != 10:
                frappe.throw(_("For Allianz the policy number must be exactly 10 characters long"))
        
        elif doc.insurance_company == "Warta":
            if len(doc.policy_number) != 15:
                frappe.throw(_("For Warta the policy number must be exactly 15 characters long"))
        
        elif doc.insurance_company == "Proama":
            if len(doc.policy_number) != 11:
                frappe.throw(_("for Proama the policy number must be exactly 11 characters long"))





    def validate(self):
        """Automatycznie ustaw coverage_end na podstawie coverage_start"""
        if self.coverage_start:
            if not self.coverage_end or self.has_value_changed('coverage_start'):
                self.coverage_end = add_years(self.coverage_start, 1)
        
        # Automatyczne obliczanie prowizji
        if self.insurancee_components:
            self.calculate_commission()

    def calculate_commission(self):
        """Oblicza prowizję na podstawie wybranych komponentów ubezpieczenia"""
        if not self.insurancee_components or len(self.insurancee_components) == 0:
            self.commission_vehicle = 0
            return

        premium_values = {
            'OC': 1000,
            'AC': 800, 
            'Mini AC': 400,
            'Assistance': 200,
            'Life': 500,
            'Tires': 200,
            'Windows': 200,
            'Legal protection': 600
        }

        total_premium = 0
        commission_rate = 0.10  # 10%

        for component in self.insurancee_components:
            component_name = component.company_list
            total_premium += premium_values.get(component_name, 500)

        self.commission_vehicle = total_premium * commission_rate

    # Prosta metoda whitelist dla obliczeń
    @frappe.whitelist()
    def calculate_commission_api(self):
        """Metoda API do obliczania prowizji"""
        self.calculate_commission()
        return {
            'commission': self.commission_vehicle,
            'components_count': len(self.insurancee_components) if self.insurancee_components else 0
        }
    




    # def length_company(doc, method):
    #     # Słownik z firmami i wymaganymi długościami
    #     company_lengths = {
    #         "Allianz": 10,
    #         "Warta": 15,
    #         "Proama": 11
    #     }
        
    #     if doc.insurance_company in company_lengths:
    #         required_length = company_lengths[doc.insurance_company]
    #         if len(doc.policy_number) != required_length:
    #             frappe.throw(_(f"Dla {doc.insurance_company} numer polisy musi mieć dokładnie {required_length} znaków"))

