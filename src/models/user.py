class User:
    def __init__(self, id, username, password, date_born, country, city, phone):
        self._id = id
        self._username = username
        self._password = password
        self._date_born = date_born
        self._country = country
        self._city = city
        self._phone = phone

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def date_born(self):
        return self._date_born

    @date_born.setter
    def date_born(self, date_born):
        self._date_born = date_born

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, country):
        self._country = country

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, city):
        self._city = city

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, phone):
        self._phone = phone
