import unittest
from project import db, app, customers
from project.customers.models import Customer

class TestCustomerModel(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Testy poprawnych danych
    def test_valid_customer_creation(self):
        """Tests correct creation of customers."""
        valid_customers = [
            {"name": "Jan Kowalski", "city": "Warszawa", "age": 35, "pesel": "85010212345", "street": "Aleje Jerozolimskie 10", "appNo": "PL001"},
            {"name": "Anna Nowak", "city": "Kraków", "age": 28, "pesel": "92120456789", "street": "Wawelska 22", "appNo": "PL002"},
            {"name": "Marek Wiśniewski", "city": "Gdańsk", "age": 45, "pesel": "78051123456", "street": "Długa 30", "appNo": "PL003"},
            {"name": "Karolina Kwiatkowska", "city": "Poznań", "age": 22, "pesel": "01020309876", "street": "Św. Marcin 5", "appNo": "PL004"},
            {"name": "Piotr Zieliński", "city": "Wrocław", "age": 50, "pesel": "70101056789", "street": "Rynek 12", "appNo": "PL005"}
        ]
        for data in valid_customers:
            customer = Customer(**data)
            db.session.add(customer)
        db.session.commit()

        for data in valid_customers:
            retrieved = Customer.query.filter_by(name=data["name"]).first()
            self.assertIsNotNone(retrieved)
            self.assertEqual(retrieved.city, data["city"])
            self.assertEqual(retrieved.age, data["age"])

    def test_get_customer_by_id(self):
        """Tests get method of the customer object."""
        customer_data = {
            "name": "Jan Kowalski", 
            "city": "Warszawa", 
            "age": 35, 
            "pesel": "85010212345", 
            "street": "Aleje Jerozolimskie 10", 
            "appNo": "PL001"
        }
        customer = Customer(**customer_data)
        db.session.add(customer)
        db.session.commit()

        retrieved = Customer.query.get(customer.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Jan Kowalski")
        self.assertEqual(retrieved.city, "Warszawa")
        self.assertEqual(retrieved.pesel, "85010212345")
        self.assertEqual(retrieved.street, "Aleje Jerozolimskie 10")

    def test_duplicate_customer(self):
        """Tests duplicated customer."""
        customer_data = {
            "name": "Anna Nowak", 
            "city": "Kraków", 
            "age": 28, 
            "pesel": "92120456789", 
            "street": "Wawelska 22", 
            "appNo": "PL002"
        }

        customer1 = Customer(**customer_data)
        db.session.add(customer1)
        db.session.commit()

        duplicate_customer = Customer(**customer_data)
        with self.assertRaises(Exception):
            db.session.add(duplicate_customer)
            db.session.commit()


    # Testy niepoprawnych danych
    def test_invalid_customer_missing_field(self):
        """Tests None value in all fields of created object."""
        invalid_customers = [
            {"name": None, "city": "Łódź", "age": 35, "pesel": "85010212345", "street": "Piotrkowska 100", "appNo": "PL001"},
            {"name": "Ewa Malinowska", "city": None, "age": 28, "pesel": "92120456789", "street": "Lipowa 3", "appNo": "PL002"},
            {"name": "Tomasz Nowicki", "city": "Gdynia", "age": None, "pesel": "78051123456", "street": "Morska 15", "appNo": "PL003"},
            {"name": "Agata Kowalczyk", "city": "Lublin", "age": 40, "pesel": None, "street": "Zamojska 25", "appNo": "PL004"},
            {"name": "Dariusz Więckowski", "city": "Białystok", "age": 29, "pesel": "90010123456", "street": None, "appNo": "PL005"},
            {"name": "Dariusz Więckowski", "city": "Białystok", "age": 29, "pesel": "90010123456", "street": "Groove Street", "appNo": None}

        ]
        for data in invalid_customers:
            with self.assertRaises(Exception):
                customer = Customer(**data)
                db.session.add(customer)
                db.session.commit()
                
    def test_invalid_customer_input(self):
        """Tests invalid input from user."""
        invalid_customers = [
            {"name": 1, "city": "Katowice", "age": 25, "pesel": "12345678901", "street": "Uliczna 2", "appNo": "PL006"},
            {"name": "Zofia Nowak", "city": 1, "age": 25, "pesel": "12345678901", "street": "Uliczna 2", "appNo": "PL006"},
            {"name": "Zofia Nowak", "city": "Katowice", "age": -1, "pesel": "12345678901", "street": "Uliczna 2", "appNo": "PL006"},
            {"name": "Zofia Nowak", "city": "Katowice", "age": 25, "pesel": 1, "street": "Uliczna 2", "appNo": "PL006"},
            {"name": "Zofia Nowak", "city": "Katowice", "age": 25, "pesel": "12345678901", "street": 1, "appNo": "PL006"},
            {"name": "Zofia Nowak", "city": "Katowice", "age": 25, "pesel": "12345678901", "street": "Uliczna 2", "appNo": 1}

        ]
        for data in invalid_customers:
            with self.assertRaises(Exception):
                customer = Customer(**data)
                db.session.add(customer)
                db.session.commit()            
                
    # Testy SQL injection
    def test_sql_injection_in_name(self):
        """Tests SQL injection in input name field."""
        injection_payloads = [
            "'; DROP TABLE customers; --",
            "' OR '1'='1",
            "admin'--",
            "'); DELETE FROM customers; --",
            "' AND 'a'='a"
        ]
        for payload in injection_payloads:
            customer = Customer(name=payload, city="Warszawa", age=25, pesel="12345678901", street="Injection Street", appNo="PL009")
            db.session.add(customer)
        db.session.commit()

        for payload in injection_payloads:
            retrieved = Customer.query.filter_by(name=payload).first()
            self.assertIsNotNone(retrieved)
            self.assertEqual(retrieved.name, payload)

    def test_javascript_injection_in_street(self):
        """Tests XSS in street name field."""
        injection_payloads = [
            "<script>alert('Hacked');</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('Injected')></svg>",
            "<body onload=alert('Hack')>",
            "<iframe src='javascript:alert(\"XSS\")'></iframe>"
        ]
        for payload in injection_payloads:
            customer = Customer(name="Rafal", city="Groove Street", age=25, pesel="12345678901", street=payload, appNo="PL010")
            db.session.add(customer)
        db.session.commit()

        for payload in injection_payloads:
            retrieved = Customer.query.filter_by(street=payload).first()
            self.assertIsNotNone(retrieved)
            self.assertEqual(retrieved.street, payload)

    # Testy ekstremalne
    def test_extreme_data_length(self):
        """Tests extreme values for given fields of an object."""
        extreme_customers = [
            {"name": "Rafal", "city": "Warszawa", "age": 30, "pesel": "1" * 1000000, "street": "S", "appNo": "PL1"},
            {"name": "R"*1000000, "city": "Warszawa", "age": 30, "pesel": "12345678901", "street": "S", "appNo": "PL1"},
            {"name": "Rafal", "city": "W"*1000000, "age": 30, "pesel": "12345678901", "street": "S", "appNo": "PL1"},
            {"name": "Rafal", "city": "Warszawa", "age": 30, "pesel": "1" * 1000000, "street": "S", "appNo": "PL1"},
            {"name": "Rafal", "city": "Warszawa", "age": 30, "pesel": "12345678901", "street": "S"*1000000, "appNo": "PL1"},
            {"name": "Rafal", "city": "Warszawa", "age": 30, "pesel": "12345678901", "street": "S", "appNo": "P"*1000000}
        ]
        for data in extreme_customers:
            with self.assertRaises(Exception):
                customer = Customer(**data)
                db.session.add(customer)
        db.session.commit()

if __name__ == "__main__":
    unittest.main()
