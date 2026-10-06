from django.apps import AppConfig

class InvestmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'investment'
class RealEstateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'real_estate'