data = frappe.db.sql("""
  SELECT Debido
    FROM CustomerPosition
   WHERE Cliente = %(customer)s
""", values = {'customer': doc.customer}, as_dict = 1)

debido = 0
try:
    debido = data[0].Debido
except IndexError:
  pass

doc.saldo_del_cliente = debido

# DROP TABLE IF EXISTS CustomerPayments;
# DROP VIEW IF EXISTS CustomerPayments;

# CREATE OR REPLACE VIEW CustomerPayments
# AS select
#         party
#       , count(PE.name) Payments 
#       , sum(PE.paid_amount) Paid
#  from `tabPayment Entry` PE
#  group by party
# ;

# DROP TABLE IF EXISTS CustomerInvoices;
# DROP VIEW IF EXISTS CustomerInvoices;

# CREATE OR REPLACE VIEW CustomerInvoices
# AS select
#         customer
#       , count(SI.name) Invoices
#       , sum(SI.grand_total) as Owed
#  from `tabSales Invoice` SI 
#  group by customer
# ;


# DROP TABLE IF EXISTS CustomerPosition;
# DROP VIEW IF EXISTS CustomerPosition;

# CREATE OR REPLACE VIEW CustomerPosition
# AS select
#     customer as Cliente
#   , Invoices as Facturas
#   , Owed as Comprado
#   , IFNULL(Payments, 0) as Pagos
#   , IFNULL(Paid, 0) as Pagado
#   , Owed - IFNULL(Paid, 0) as Debido
#  from CustomerInvoices 
#  left join CustomerPayments
#          on customer = party
# where Owed - IFNULL(Paid, 0) NOT BETWEEN -0.0001 AND 0.0001
# ;
