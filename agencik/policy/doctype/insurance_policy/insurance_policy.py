import frappe
from frappe.model.document import Document
from frappe.utils import add_years

class InsurancePolicy(Document):
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
            component_name = component.insurance2
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


# class InsurancePolicy(Document):
#     def before_save(self):
#         if not self.agent:
#             self.set_agent_from_user()
    
#     def set_agent_from_user(self):
#         # Pobierz employee dla obecnego użytkownika
#         employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
        
#         if employee:
#             # Pobierz sales person z employee
#             sales_person = frappe.db.get_value("Employee", employee, "sales_person")
            
#             if sales_person:
#                 self.agent = sales_person