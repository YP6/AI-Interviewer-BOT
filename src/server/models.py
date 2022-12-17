from djongo import models


class User(models.Model):
    id = models.ObjectIdField()
    username = models.CharField(max_length=50)
    accountType = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    dateOfBirth = models.DateTimeField()
    password = models.TextField()

    @staticmethod
    def getUser(username, email):
        if username:
            obj = User.objects.filter(username=username)
            return obj
        elif email:
            obj = User.objects.filter(email=email)
            return obj

        return None


class Question(models.Model):
    id = models.ObjectIdField()
    question = models.TextField()
    topic = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    visibility = models.CharField(max_length=50)
    answer = models.TextField()
    userCreated = models.EmbeddedField(
        model_container=User
    )


class Interview(models.Model):
    id = models.ObjectIdField()
    name = models.TextField()
    userCreated = models.EmbeddedField(
        model_container=User
    )
    questions = models.ArrayField(
        model_container=Question
    )
    date = models.DateTimeField()
    password = models.TextField()
    permission = models.CharField(max_length=10)
    allowedUsers = models.ArrayField(
        model_container=User
    )
    attendances = models.ArrayField(
        model_container=User
    )

    @staticmethod
    def getInterview(name):
        obj = Interview.objects.filter(name=name)
        return obj


class Weakness(models.Model):
    id = models.ObjectIdField()
    weakness = models.CharField(max_length=50)


class Strength(models.Model):
    id = models.ObjectIdField()
    strength = models.CharField(max_length=50)


class Report(models.Model):
    id = models.ObjectIdField()
    score = models.FloatField()
    summary = models.TextField()
    weaknesses = models.ArrayField(
        model_container=Weakness
    )
    strengths = models.ArrayField(
        model_container=Strength
    )
    date = models.DateTimeField()


class Attendance(models.Model):
    interview = models.TextField()
    startDate = models.DateTimeField(auto_now_add=True)
    endDate = models.DateTimeField(auto_now=True)
    report = models.TextField()
