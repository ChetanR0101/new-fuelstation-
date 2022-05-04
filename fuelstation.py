from odoo import models,fields,api
from odoo.exceptions import ValidationError


class FuelStation_in_stock(models.Model):
    _name= "fuelstation.instock"
    _description ="IN Fuel Record"
    name = fields.Char("Recived By")
    date = fields.Datetime("Date:")
    fuel_type = fields.Many2one(comodel_name ="fuelstation.fueldata",string="Fuel Type") 
    instock_qut= fields.Float("IN stock Quantity")
    
    # To Update the stock
    @api.model
    def create(self, vals_list):
        res=super(FuelStation_in_stock,self).create(vals_list)
        res.fuel_type.avl_qut += res.instock_qut # to add stock
        return res



class FuelStation_out_stock(models.Model):
    _name="fuelstation.outstock"
    _description ="OUT Fuel Record"
    name = fields.Char("Customer Name")
    date = fields.Datetime("Date:")
    fuel_type = fields.Many2one(comodel_name ="fuelstation.fueldata",string="Fuel Type")
    order_qut= fields.Float("Fuel Quantity in Ltrs")
    fuel_price= fields.Float(string="Current Fuel Price",related='fuel_type.price') 
    avl_qut = fields.Float(string="Available Fuel",related='fuel_type.avl_qut')

    # Store current price
    @api.depends('fuel_type')
    def _price_store(self):
        for rec in self:
            temp_price=rec.fuel_price
        self.price=temp_price
        
    price= fields.Float(string="Fuel Price On Order",compute=_price_store,store=True)



    #  for Total price
    @api.depends('fuel_type','order_qut')
    def _cal_total(self):
        for rec in self:
            rec.total_price= rec.order_qut* rec.fuel_price
        self.total_price= rec.total_price

    total_price = fields.Float(string="Total Cost",compute=_cal_total,store=True)

    # To Update stock
    @api.depends('order_qut')
    def _update_stock(self):
        for rec in self:
            if rec.order_qut < rec.fuel_type.avl_qut: # to check out off stock condition
                rec.fuel_type.avl_qut -= rec.order_qut 
            else:
                raise ValidationError("Fuel Out off Stock")
        self.updated_stock= rec.fuel_type.avl_qut

    updated_stock= fields.Float(string="Updated Stock",compute=_update_stock,  store=True)



class FuelStation_fuel_data(models.Model):
    _name="fuelstation.fueldata"
    name= fields.Char(string= "Fuel Type")
    price= fields.Float(string="Fuel Price")
    avl_qut= fields.Float(" Available Fuel")


class FuelStation_transection_rec(models.Model):
    _name="fuelstation.record"
    name=fields.Char(string="Name")
    date = fields.Datetime("Date:")
    fuel_type = fields.Many2one(comodel_name ="fuelstation.fueldata",string="Fuel Type")
    order_qut= fields.Float("Fuel Quantity in Ltrs")
    fuel_price= fields.Float(string="Fuel Price",related='fuel_type.price')



class FuelStation_fuel_price(models.Model):
    _name= "fuelstation.fuelprice"
    name= fields.Char(string= "Fuel Type")
    fuel_type = fields.Many2one(comodel_name ="fuelstation.fueldata",string="Fuel Type")
    fuel_price= fields.Float(string="Fuel Price",related='fuel_type.price',readonly=False) 


class FuelStation_avl_stock(models.Model):
    _name= "fuelstation.avlstock"
    name= fields.Char(string= "Fuel Type")
    fuel_type = fields.Many2one(comodel_name ="fuelstation.fueldata",string="Fuel Type")
    avl_qut = fields.Float(string="Fuel Quantity in Ltrs",related='fuel_type.avl_qut',readonly=False, store=True)
