# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_liquidityproviders.ipynb.

# %% auto 0
__all__ = ['liquidityproviders', 'CentralBank', 'Treasury']

# %% ../nbs/00_liquidityproviders.ipynb 5
class liquidityproviders():
    def __init__(self,name:str):
        self.name = name

#class cb_entry():
#    def __init__(self,name:str='Treasury',amount:float=0,side:str='asset'):
#        if name in central_bank.allowed_assets and side=='asset': # allowed CB assets are ['Treasury','CB Loan']
#            self.entry={name:amount}
#            self.side = side
#        elif name in central_bank.allowed_liabilities and side == 'liability': ## allowed liabilities are  ['Bank Reserves','Cash','TGA']
#            self.entry={name:amount}
#            self.side = side
#        else:
#            print('Wrong inputs! Will use the default values')
#            self.entry={'Treasury':0}
#            self.side='asset'
        

class CentralBank(liquidityproviders):
    allowed_assets=['Treasury','CB Loan']
    allowed_liabilities = ['Bank Reserves','Cash','TGA']  # TGA is treasury general account

    def __init__(self,asset_input:AccountEntry={},liability_input:AccountEntry={}):
        super().__init__('Central Bank')
        self.asset={k:0.0 for k in CentralBank.allowed_assets}
        self.liability={k:0.0 for k in CentralBank.allowed_liabilities}


        if (asset_input is not None) and (liability_input is not None) and \
                sum(asset_input.values()) == sum(liability_input.values()) and \
                set(asset_input.keys()).issubset(set(CentralBank.allowed_assets)) and \
                set(liability_input.keys()).issubset(set(CentralBank.allowed_liabilities)):
            for k, v in asset_input.items():
                self.asset[k] = v

            for k, v in liability_input.items():
                self.liability[k] = v
        else:
            raise NameError('Wrong inputs: Total asset has to equal to total liability!')

    @property
    def total_asset(self):
        return sum(self.asset.values())

    @property
    def total_liability(self):
        return sum(self.liability.values())
        
    
    def __str__(self):
        return f'{self.name}: total asset/liability is {self.total_asset}'
    
    __repr__=__str__

        
    def treasury_tranactions(self, counterparty:liquidityproviders, transaction:str='buy',amount:float=0.0)->None:
        "Central banks buys treasuries from Treasury or central banks buys/sells treasuries to commercial banks"
        if isinstance(counterparty,CentralBank):
            print('Central bank cannot trade with itself!')
        elif isinstance(counterparty,Treasury):
            if transaction =='sell':
                print('Central bank cannot sell treasuries to Treasuty!')

            elif transaction == 'buy':
                self.asset['Treasury'] += amount
                self.liability['TGA'] += amount
                counterparty.asset['TGA'] += amount
                counterparty.liability['Treasury'] +=amount
            else:
                print('Transaction has to be buy or sell!')
            
class Treasury(liquidityproviders):
    allowed_assets=['TGA']
    allowed_liabilities=['Treasury']
    
    def __init__(self,asset_input:AccountEntry={},liability_input:AccountEntry={}):
        super().__init__('Treasury')

        self.asset={k:0.0 for k in Treasury.allowed_assets}
        self.liability={k:0.0 for k in Treasury.allowed_liabilities}
        if (asset_input is not None) and (liability_input is not None) and \
                sum(asset_input.values()) == sum(liability_input.values()) and \
                set(asset_input.keys()).issubset(set(Treasury.allowed_assets)) and \
                set(liability_input.keys()).issubset(set(Treasury.allowed_liabilities)):
            for k, v in asset_input.items():
                self.asset[k] = v

            for k, v in liability_input.items():
                self.liability[k] = v
        else:
            raise NameError('Wrong inputs: Total asset has to equal to total liability!')

       
    @property
    def total_asset(self):
        return sum(self.asset.values())

    @property
    def total_liability(self):
        return sum(self.liability.values())
        
    
    def __str__(self):
        return f'{self.name}: total asset/liability is {self.total_asset}'
    
    __repr__=__str__

        
   
    def treasury_tranactions(self, counterparty:liquidityproviders, transaction:str='sell',amount:float=0.0)->None:
        "Treasury sells treasurie to central banks, commercial banks or private sector"
        if isinstance(counterparty,Treasury):
            print('Treasury cannot trade with itself!')
        elif isinstance(counterparty,CentralBank):
            if transaction =='buy':
                print('Treasury cannot buy treasuries from central bank!')

            elif transaction == 'sell':
                self.asset['TGA'] += amount
                self.liability['Treasury'] += amount
                counterparty.liability['TGA'] += amount
                counterparty.asset['Treasury'] +=amount
            else:
                print('Transaction has to be buy or sell!')

        
