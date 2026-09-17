from __future__ import annotations
from abc import ABC, abstractmethod
<<<<<<< HEAD
import json
from loading import import_json
import json
=======
>>>>>>> 7987eb0 (V0)

CATEGORIES = ["education", "energy", "water", "internet", "food", "maintenance"]
MONTHS = []

class FinancialElement:     #for depense and categorie to have a same structure
    #try    #try/expect can only be used inside a methode
    def __init__(self, _name: str, _amount: float):
        try:
            self.name = _name
            self._amount = _amount  #self._amount mean protected
        except ValueError as error:
            print(f"Erreur d'initialisation : {error}")
            raise

    def get_amount(self):
        return self._amount

    def set_amount(self, _amount: float):
        self._amount += _amount

class Expense(FinancialElement, ABC):    #abstract necessary for all type of expense, ExpenseVaraible, ExpenseFixe, ...
    def __init__(self, _name, _amount, _cat: Categorie):
       super().__init__(_name, _amount)   #or the same ElementFinancier.__init__(self, _name, _amount) 
       self.cat = _cat

class Categorie(FinancialElement):
    def __init__(self, _name, _expenses: list[Expense], _limite: float = None):
        self.limite = _limite
        self.expenses = _expenses
        _amount = sum(e.get_amount() for e in _expenses)
        super().__init__(_name, _amount)

class ExpenseVariable(Expense):
    def __init__(self, _name, _amount, _cat, _date: float = None):     
        super().__init__(_name, _amount, _cat)      
        self.cat = _cat
        self.date = _date
    #def __init__   #added to that, we can't polymorphism the __init__ function

class ControlFin:  
    def __init__(self, _expenses_archive):
        self.expenses_list = _expenses_archive[0].get("expenses", [])
        self.dicCat = {cat_name: Categorie(cat_name, []) for cat_name in CATEGORIES}

    def add_expenses(self):
        for item in self.expenses_list:
            cat_name = item.get("category")
            if cat_name in self.dicCat:
                category_obj = self.dicCat[item.get("category")]
                category_obj.expenses.append(ExpenseVariable(item["name"], float(item["amount"]), category_obj, item.get("date")))
                category_obj.set_amount(float(item["amount"]))
            else:
                print(f"Attention : La catégorie '{cat_name}' n'existe pas.")        
        return self.dicCat