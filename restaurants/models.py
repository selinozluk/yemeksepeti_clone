from django.db import models

# Restoranlar için kategori modeli
class RestaurantCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
     db_table = 'restaurants_restaurantcategory' 

    def __str__(self):
        return self.name

# Menü öğeleri için kategori modeli
class MenuItemCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    category = models.ForeignKey(RestaurantCategory, on_delete=models.CASCADE, related_name='restaurants', null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
def upload_to(instance, filename):
    # Dosyaları "Proje Yemekleri" klasörüne kaydetmek için özel bir yol
    return f'Proje Yemekleri/{instance.restaurant.name}/{filename}'



class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    category = models.ForeignKey(MenuItemCategory, on_delete=models.CASCADE, related_name='menu_items', null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)  # Burada upload_to fonksiyonunu kullanıyoruz
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name



    # class Meta:
    #     db_table="menuitem"
