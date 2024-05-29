
from log.logger import Logger

logger = Logger()

class StoredQueries:
    def __init__(self):
        pass
    
    
    def GetTenantByUserID(self,user_id):
        query = f'SELECT t.* FROM tenants t INNER JOIN users u ON t.ID = u.TenantID WHERE u.ID = {user_id};'
                
        logger.log('StoredQueries','GetTenantByUserID',user_id,query)
        return query
    
    
    def GetTenantByUsername(self,username):
        query = f'SELECT t.* FROM tenants t INNER JOIN users u ON t.ID = u.TenantID WHERE u.Username = "{username}";'
        
        logger.log('StoredQueries','GetTenantByUsername',username,query)
        return query
    
    
    def GetUserByUsername(self,username):
        query = f'SELECT * FROM users WHERE Username = "{username}";'
        
        logger.log('StoredQueries','GetUserByUsername',username,query)
        return query
    
    
    def GetUserByTenantID(self,tennantID):
        query = f'SELECT u.* FROM users u INNER JOIN tenants t ON t.ID = u.tennantID WHERE t.ID = {tennantID};'
        
        logger.log('StoredQueries','GetHomeByUserID',tennantID,query)
        return query
    
        
    def GetHomeByUserID(self,userId):
        query = f'SELECT h.* FROM homes h INNER JOIN tenants t ON h.ID = t.HomeID INNER JOIN users u ON t.ID = u.TenantID WHERE u.ID = {userId};'
        
        logger.log('StoredQueries','GetHomeByUserID',userId,query)
        return query
    
    
    def GetTenantsByHomeID(self,homeID):
        query = f'SELECT t.* FROM tenants t INNER JOIN homes h ON h.ID = t.HomeID WHERE h.ID = {homeID};'
        
        logger.log('StoredQueries','GetTenantsByHomeID',homeID,query)
        return query
    
    
    def GetBillsByTennantID(self,tennantID):
        query = f'SELECT b.* FROM bills b INNER JOIN tenants t ON t.ID = b.PaiedBy WHERE t.ID = {tennantID};'
        
        logger.log('StoredQueries','GetBillsByTennantID',tennantID,query)
        return query
    
    
    def GetBillsNotPaidByTenant(self,tennantID):
        query = f'SELECT b.* FROM bills b INNER JOIN tenants t ON t.ID = b.PaiedBy WHERE t.ID != {tennantID};'
        
        logger.log('StoredQueries','GetBillsNotPaidByTenant',tennantID,query)
        return query
    
        
    def GetPaymentsByTennantID(self,tennantID):
        query = f'SELECT p.* FROM payments p INNER JOIN tenants t ON t.ID = p.PaiedBy WHERE t.ID = {tennantID};'
        
        logger.log('StoredQueries','GetPaymentsByTennantID',tennantID,query)
        return query
    
    
    def GetRecivedPaymentsByTennantID(self,tennantID):
        query = f'SELECT p.* FROM payments p INNER JOIN tenants t ON t.ID = p.PaiedTo WHERE t.ID = {tennantID};'
        
        logger.log('StoredQueries','GetRecivedPaymentsByTennantID',tennantID,query)
        return query
    
    
    def GetBillsByHomeID(self,homeID):
        query = f'SELECT b.* FROM bills b INNER JOIN homes h ON h.ID = b.HomeID WHERE h.ID = {homeID};'
        
        logger.log('StoredQueries','GetBillsByHomeID',homeID,query)
        return query
    
    
    def GetSetBillsByHomeID(self,homeID):
        query = f'SELECT b.* FROM setbills b INNER JOIN homes h ON h.ID = b.HomeID WHERE h.ID = {homeID};'
        
        logger.log('StoredQueries','GetSetBillsByHomeID',homeID,query)
        return query
    
    
    def GetPaymentsByHomeID(self,homeID):
        query = f'SELECT p.* FROM payments p INNER JOIN tenants t ON t.ID = p.PaiedBy INNER JOIN homes h ON h.ID = t.HomeID WHERE h.ID = {homeID};'
        
        logger.log('StoredQueries','GetPaymentsByHomeID',homeID,query)
        return query
    
    
    def GetPaymentsByBillID(self,billID):
        query = f'SELECT p.* FROM payments p INNER JOIN bills b ON b.ID = p.BillID WHERE b.ID = {billID};'
        
        logger.log('StoredQueries','GetPaymentsByBillID',billID,query)
        return query
    
    
    def GetBillsByTennantIDAndDates(self,tennantID,startDate,endDate):
        query = f'SELECT b.* FROM bills b INNER JOIN tenants t ON t.ID = b.PaiedBy WHERE t.ID = {tennantID} AND b.BillDate BETWEEN "{startDate}" AND "{endDate}";'
        
        logger.log('StoredQueries','GetBillsByTennantIDAndDates',(tennantID,startDate,endDate),query)
        return query
    
    
    def GetRecivedPaymentsByTennantIDAndDates(self,tennantID,startDate,endDate):
        query = f'SELECT b.* FROM bills b INNER JOIN tenants t ON t.ID = b.PaiedTo WHERE t.ID = {tennantID} AND b.BillDate BETWEEN "{startDate}" AND "{endDate}";'
        
        logger.log('StoredQueries','GetRecivedPaymentsByTennantIDAndDates',(tennantID,startDate,endDate),query)
        return query
    
    
    def GetBillsByHomeIDAndDates(self,homeID,startDate,endDate):
        query = f'SELECT b.* FROM bills b INNER JOIN homes h ON h.ID = b.HomeID WHERE h.ID = {homeID} AND b.BillDate BETWEEN "{startDate}" AND "{endDate}";'
        
        logger.log('StoredQueries','GetBillsByHomeIDAndDates',(homeID,startDate,endDate),query)
        return query
    
    
    def GetPaymentsByHomeIDAndDates(self,homeID,startDate,endDate):
        query = f'SELECT p.* FROM payments p INNER JOIN tenants t ON t.ID = p.PaiedBy INNER JOIN homes h ON h.ID = t.HomeID WHERE h.ID = {homeID} AND p.PaymentDate BETWEEN "{startDate}" AND "{endDate}";'
        
        logger.log('StoredQueries','GetPaymentsByHomeIDAndDates',(homeID,startDate,endDate),query)
        return query
    
    
    def GetTokenByUserID(self,userId):
        query = f'SELECT t.* FROM Tokens t INNER JOIN users u ON t.UserID = u.ID WHERE u.ID = {userId};'
        
        logger.log('StoredQueries','GetTokenByUserID',userId,query)
        return query
    
    
    def CheckIfUserExists(self,username,email):
        query = f'SELECT u.* FROM Users u WHERE u.Username = "{username}" OR u.Email = "{email}";'
        
        logger.log('StoredQueries','GetTokenByUserID',(username,email),query)
        return query
    
    
    def GetUserByEmail(self,email):
        query = f'SELECT u.* FROM Users u WHERE u.Email = "{email}";'
        
        logger.log('StoredQueries','GetTokenByUserID',email,query)
        return query
    

    
    