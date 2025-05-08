class MessagingRouter:
    """
    A router to control all database operations on models in the messaging app.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == "Messenger":
            return "messaging"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "Messenger":
            return "messaging"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == "Messenger" or obj2._meta.app_label == "Messenger":
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == "Messenger":
            return db == "messaging"
        return None
