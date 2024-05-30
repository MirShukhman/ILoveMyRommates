
from log.logger import Logger

logger = Logger()

class Bookkeeper:
    def __init__(self):
        pass
    
    def calculate_current_debt_for_tenant(self, home_id, tenant_id):
        # debt = {}
        # get tenats % 
        # GetBillsNotPaidByTenant(tenant_id)
        # GetPaymentsByTennantID(tenant_id)
        # for bill in not my bills:
        #       calculte sum owed by tenat 
        #       GetPaymentsByBillID(bill_id)
        #       if payments:
        #           if sum (of all payments by bill_id) == bill_sum*% (and approved) pass 
        #           else append bill:bill_sum*%-payment debt dict 
        #       else: append bill:bill_sum*% to debt dict 
        # return: total, debt 
        
        pass
    
    
    def calculate_current_owed_to_tenant(self, home_id, tenant_id):
        # owed = {}
        # get tenats % 
        # my bills = GetBillsPaidByTenant(tenant_id)
        # tenants = GetTenantsByHomeID(home_id)
        # for bill in my bills:
        #   calculte sum owed by tenat
        #   payments = GetPaymentsByBillID(bill_id)
        #   division = calculate_bill_divison()
        #   if payments:
        #       if sum (of all payments by bill_id) == bill_sum*% (and approved) pass
        #       else: 
        #           for tenant in tenats:
        #               get tenant part from division
        #               get payments.PaiedBy tenat     
        #               part - tenant = owed_sum
        #               if owed_sum > 0:
        #                   owed[(tenant.id, tenant.name, bill_id)] = owed_sum
        #                                      
        #   else (no payments on the bill):
        #       append all division to owed where key != tenant_id
        #   
        # return: total, owed 
        
        pass
    
    
    def calculate_bill_divison(self, home_id, bill_id):
        # divison = {}
        # get bill by id
        # GetTenantsByHomeID(home_id)
        # for tenant in tenants:
        #   tenant.PaymentPart * bill.sum = tenants_part
        #   division[(tenant_id,tenat_name)]= tenants_part
        # return divison
        
        pass
    
    
    def recalculate_payment_part_after_tenant_leaving(self, home_id, tenant_id):
        # GetTenantsByHomeID(home_id) = tenats 
        # num of tenants = len(tenats)
        # get tenat by id (tenant_id) - get PaymentPart
        # PaymentPart/num of tenants = add
        # for tenant in tenats:
        #   new_payment_part = tenant.PaymentPart + add
        #   tenant.update (tenant.ID, PaymentPart = new_payment_part)
        # return bool
        pass