from wallee import Configuration
from wallee.api import TransactionServiceApi,RefundBankTransactionServiceApi,ChargeBankTransactionServiceApi,ShopifyTransactionServiceApi
from wallee.api_client import ApiClient
from wallee.models import EntityExportRequest,EntityQueryFilter,EntityQuery,EntityQueryFilterType,CriteriaOperator,EntityQueryOrderBy,EntityQueryOrderByType
from datetime import datetime
import threading
#setup the GUI
# import tkinter as tk
# label1=tk.Label(text='from')
import time
    
def setteld(year,mon,day,h,m,s,y2,mon2,d2,h2,m2,s2):
     
     # lastone=ordernames()
    
     
     year=year
     mon=mon    
     day=day
     hour=h
     min=m
     sec=s
     
     y2=y2
     mon2=mon2
     d2=d2
     h2=h2
     m2=m2
     s2=s2

     qyr=EntityQuery()
     qyr.language='en'
     #state=settled
     setteld=EntityQueryFilter(type='str')
     setteld.operator='EQUALS'
     setteld.field_name='bankTransaction.state'
     setteld.type='LEAF'
     setteld.value='SETTLED'
     #greater query
     greater=EntityQueryFilter(type='str')
     greater.operator='GREATER_THAN'
     greater.field_name='bankTransaction.valueDate'
     greater.type='LEAF'
     # greater.value='2023-09-21T18:46:06.446Z'
     greater.value=f'{year}-{mon}-{day}T{hour}:{min}:{sec}.567Z'
     #lessthan qurey
     lessthan=EntityQueryFilter(type='str')
     lessthan.operator='LESS_THAN'
     lessthan.field_name='bankTransaction.valueDate'
     lessthan.type='LEAF'
     # lessthan.value="2023-09-28T19:06:37.446Z"
     lessthan.value=f'{y2}-{mon2}-{d2}T{h2}:{m2}:{s2}.567Z'
     space_id=31423  
     config=Configuration(
     user_id=user_id,
     api_secret=api_secret,
     # default_headers={'x-meta-custom-header': 'value-1', 'x-meta-custom-header-2': 'value-2'},
     # set a custom request timeout if needed. (If not set, then the default value is: 25 seconds)
     request_timeout = 60
     )
     #main query

     qyr.filter=EntityQueryFilter(type='str')
     qyr.filter.type='AND'
     ap=ChargeBankTransactionServiceApi(config)
     # qyr.order_bys=EntityQueryOrderBy(field_name='bankTransaction.valueDate',sorting='DESC')
     qyr.filter.children=[lessthan,greater,setteld]
     thread=ap.search(async_req=True,space_id=space_id,query=qyr)
     result=thread.get()
     #formating data
     currency=[]
     id=[]
     pos_amount=[]
     state=[]
     created_on=[]
     val_amount=[]
     Tstate=[]
     merch=[]
     paymentconnectorname=[]
     paymentconnname=[]
     paymentmethodid=[]
     value_date=[]
     feecollect=[]
     type=[]
     T_id=[]
     linkedsapceid=[]
     order_names=[]
     for x in result:
          if x.bank_transaction.id in id:
               continue
          else:
               id.append(x.bank_transaction.id)
          pos_amount.append(x.bank_transaction.posting_amount)
          paymentconnectorname.append(x.transaction.payment_connector_configuration.name)
          state.append(x.bank_transaction.state)
          created_on.append(x.bank_transaction.created_on)
          val_amount.append(x.bank_transaction.value_amount)
          Tstate.append(x.transaction.state)
          merch.append(x.transaction.merchant_reference)
          currency.append(x.bank_transaction.currency_bank_account.currency)
          paymentmethodid.append(x.transaction.payment_connector_configuration.id)
          paymentconnname.append(x.transaction.payment_connector_configuration.payment_method_configuration.name) 
          feecollect.append(x.transaction.total_applied_fees)
          value_date.append(x.bank_transaction.value_date)
          linkedsapceid.append(x.transaction.linked_space_id)
          T_id.append(x.transaction.id)
          type.append('Charge')
          
          
     api=RefundBankTransactionServiceApi(configuration=config)
     refund1111=api.search(async_req=True,space_id=space_id,query=qyr)
     refu=refund1111.get()
     
     
     for x in refu:
          if x.bank_transaction.id in id:
               continue
          else:
               id.append(x.bank_transaction.id)
          pos_amount.append(x.bank_transaction.posting_amount)
          paymentconnectorname.append(x.refund.transaction.payment_connector_configuration.name)
          state.append(x.bank_transaction.state)
          created_on.append(x.bank_transaction.created_on)
          val_amount.append(x.bank_transaction.value_amount)
          Tstate.append(x.refund.transaction.state)
          merch.append(x.refund.transaction.merchant_reference)
          currency.append(x.bank_transaction.currency_bank_account.currency)
          paymentmethodid.append(x.refund.transaction.payment_connector_configuration.id)
          paymentconnname.append(x.refund.transaction.payment_connector_configuration.payment_method_configuration.name) 
          feecollect.append(x.refund.total_applied_fees)
          value_date.append(x.bank_transaction.value_date)
          linkedsapceid.append(x.refund.transaction.linked_space_id)
          T_id.append(x.refund.transaction.id)
          type.append('Refund')
          
          
          
     
     shoipy=ShopifyTransactionServiceApi(config)
     sho_qy=EntityQuery()
     sho_qy.filter=EntityQueryFilter(type='str')
     sho_qy.filter.type='LEAF'
     sho_qy.filter.operator='EQUALS'
     sho_qy.filter.field_name='transaction.id'
     
     for i in T_id:
          sho_qy.filter.value=i
          thread=shoipy.search(async_req=True,space_id=space_id,query=sho_qy)
          result=thread.get()
          order_names.append(result[0].order_name)
          
     
               
     
           
     # lastone.drop_duplicates(inplace=True)
     # len(lastone)
     import pandas as pd 

     df=pd.DataFrame({'Currency':currency,'id':id,'state':state,'type':type,'SpaceId':linkedsapceid,'createdOn':created_on,'ValueDate':value_date,'GrossAmount':pos_amount,'NetAmount':val_amount,'FeeCollected':feecollect,'PaymentConnectorConfigurationId':paymentconnname,"PaymentConnectorConfigurationName":paymentconnectorname,"PaymentConnectorConId":paymentmethodid,'T.state':Tstate,"T_id":T_id,'MerchantReference':merch,'orderName':order_names})
     # df=pd.merge(df,lastone,on='T_id',how='inner')
     # df.drop_duplicates(inplace=True)
     df.to_csv(rf'C:/Users/Public/setteldfunds{mon2,d2}.csv',index=False)


import tkinter as tk 
from tkinter import ttk
from tkinter import messagebox

def validate_variables(year, mon, day, h, m, s, y2, mon2, d2, h2, m2, s2):
     
     
    errors = []

    # Numeric Validation
    if not (year.isdigit() and mon.isdigit() and day.isdigit() and h.isdigit() and m.isdigit() and s.isdigit() and
            y2.isdigit() and mon2.isdigit() and d2.isdigit() and h2.isdigit() and m2.isdigit() and s2.isdigit()):
        errors.append("All variables must be numeric.")

    # Non-Empty Validation
    if not (year and mon and day and h and m and s and y2 and mon2 and d2 and h2 and m2 and s2):
        errors.append("All variables must be non-empty.")

    # Logical Validation
    if not (1 <= int(mon) <= 12 and 1 <= int(day) <= 31 and 0 <= int(h) <= 23 and 0 <= int(m) <= 59 and 0 <= int(s) <= 59 and
            1 <= int(mon2) <= 12 and 1 <= int(d2) <= 31 and 0 <= int(h2) <= 23 and 0 <= int(m2) <= 59 and 0 <= int(s2) <= 59):
        errors.append("Invalid values for one or more variables.")

    # Display error messages in a message box
    if errors:
        messagebox.showerror("Validation Error", "\n".join(errors))
        return False


    return True
def export():
    import threading
    """
    Retrieves input values from different entry fields, formats them, and passes them as arguments to the setteld function.
    Then displays an information message box.
    """
    start=time.time()
    
    year = year_entry.get()
    mon = mon_entry.get().zfill(2)
    day = day_entry.get().zfill(2)
    h = h_entry.get().zfill(2)
    m = min_entry.get().zfill(2)
    s = s_entry.get().zfill(2)
    y2 = year2_entry.get()
    mon2 = mon2_entry.get().zfill(2)
    d2 = day2_entry.get().zfill(2)
    h2 = h2_entry.get().zfill(2)
    m2 = min2_entry.get().zfill(2)
    s2 = s2_entry.get().zfill(2)
    if validate_variables(year, mon, day, h, m, s, y2, mon2, d2, h2, m2, s2) ==True:
     thread=threading.Thread(target=setteld(year, mon, day, h, m, s, y2, mon2, d2, h2, m2, s2) )
     thread.start()
     thread.join()
     end=time.time()
     print(end-start)
     messagebox.showinfo("done")
     

#______________________widgets
root=tk.Tk()
export_butt=ttk.Button(root,text='export',command=lambda:export())

root.configure(background='#176B87')

from_frame=ttk.Frame(root,style='frame.TFrame',width=150)
to_frame=ttk.Frame(root,style='frame.TFrame',width=150)

#-__________________widgets frame one
from_lower=ttk.Label(from_frame,text='FROM LOWER DATE  \n MAKE SURE THAT HOUR IS FOLLOW 24 HOURS')
year_entry=ttk.Entry(from_frame,width=4 );
ylabel=ttk.Label(from_frame,text='year')
mon_entry=ttk.Entry(from_frame ,width=4 );
monlabel=ttk.Label(from_frame,text='month')
day_entry=ttk.Entry(from_frame ,width=4 );
daylabel=ttk.Label(from_frame,text='day')
h_entry=ttk.Entry(from_frame   ,width=4 );
hlabel=ttk.Label(from_frame,text='hour')
min_entry=ttk.Entry(from_frame ,width=4 );
minlabel=ttk.Label(from_frame,text='minute')
s_entry=ttk.Entry(from_frame   ,width=4 );
slabel=ttk.Label(from_frame,text='second')

#_-----------------------frame2 widgets
to_greater=ttk.Label(to_frame,text='TO GREATER DATE \n MAKE SURE THAT HOUR IS FOLLOW 24 HOURS')
year2_entry=ttk.Entry(to_frame,width=4 )
mon2_entry=ttk.Entry(to_frame, width=4  )
day2_entry=ttk.Entry(to_frame, width=4  )
h2_entry=ttk.Entry(to_frame  , width=4  )
min2_entry=ttk.Entry(to_frame, width=4  )
s2_entry=ttk.Entry(to_frame  , width=4  )
ylabel2=ttk.Label(to_frame,text='year')
monlabel2=ttk.Label(to_frame,text='month')
daylabel2=ttk.Label(to_frame,text='day')
hlabel2=ttk.Label(to_frame,text='hour')
minlabel2=ttk.Label(to_frame,text='minute')
slabel2=ttk.Label(to_frame,text='second')

#--------------------------grid    
export_butt.grid(column=1,row=2)
from_frame.grid(padx=15,pady=10,column=0,row=0,sticky='w')
to_frame.grid(padx=15,pady=10,column=0,row=1,sticky='w')
#____________________frame one grid
from_lower.grid(padx=5,pady=10,column=0,row=0)
year_entry.grid(pady=5,padx=5,column=0,row=1,sticky='e');ylabel.grid(pady=5,column=0,row=2,  sticky='e')
mon_entry.grid(pady=5,column=1,row=1, sticky="W");monlabel      .grid(pady=5,column=1,row=2,sticky="")
day_entry.grid(pady=5,column=2,row=1, sticky='');daylabel      .grid(pady=5,column=2,row=2,sticky='')
h_entry.grid(pady=5,column=3,row=1,   sticky='');hlabel        .grid(pady=5,column=3,row=2,sticky='')
min_entry.grid(pady=5,column=4,row=1, sticky='');minlabel      .grid(pady=5,column=4,row=2,sticky='')
s_entry.grid(pady=5,column=5,row=1,   sticky='');slabel        .grid(pady=5,column=5,row=2,sticky='')

#______________frame two grid
to_greater.grid(padx=5,pady=10)
year2_entry.grid(padx=5,pady=10,column=0,row=1,sticky='e')
mon2_entry.grid(padx=5,pady=10,column=1,row=1 ,sticky='')
day2_entry.grid(padx=5,pady=10,column=2,row=1 ,sticky='')
h2_entry.grid(padx=5,pady=10,column=3,row=1   ,sticky='')
min2_entry.grid(padx=5,pady=10,column=4,row=1 ,sticky='')
s2_entry.grid(padx=5,pady=10,column=5,row=1   ,sticky='')
ylabel2.grid(pady=5,column=0,row=2,  sticky='e')
monlabel2.grid(pady=5,column=1,row=2,sticky="")
daylabel2.grid(pady=5,column=2,row=2,sticky='')
hlabel2.grid(pady=5,column=3,row=2,sticky='')
minlabel2.grid(pady=5,column=4,row=2,sticky='')
slabel2.grid(pady=5,column=5,row=2,sticky='')

root.mainloop()




