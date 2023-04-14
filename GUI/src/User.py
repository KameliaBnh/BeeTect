class User():

    def __init__(self, name, surname, email = None):
        """
        User information window class constructor.
        Opens once when the application is started for the first time.
        """

        # Class attributes
        self.name = name
        self.surname = surname
        self.email = email
        self.date = None
        self.time = None

    def set_email(self, email):
        """
        Sets the user email.
        """

        self.email = email

    def get_email(self):
        """
        Gets the user email.
        """

        return self.email

    def set_date(self, date):
        """
        Sets the user date.
        """

        self.date = date

    def get_date(self):
        """
        Gets the user date.
        """

        return self.date

    def set_time(self, time):
        """
        Sets the user time.
        """

        self.time = time

    def get_time(self):
        """
        Gets the user time.
        """

        return self.time