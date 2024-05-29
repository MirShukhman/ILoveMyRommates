
from .all_tenant import AllTenants

class AdminTenant(AllTenants):
    def __init__(self):
        super().__init__()
        

    def _get_admin_prem(self, front_end_token):
        try:
            ok = self.authenticator.get_admin_premmisions(front_end_token)
            output = ok
            return ok 
        
        except Exception as e:
            output = str(e)
            return False
            
        finally:
            self.logger.log('AdminTenant','_get_admin_prem', front_end_token, output)