# scraper/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Property, PropertyImage
from .scraper import extract_data, extract_image_urls, download_images

def scrape_housing_data(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        try:
            data = extract_data(url)
            property_object = Property(**data)
            property_object.save()

            image_urls = extract_image_urls(url)
            for img_url in image_urls:
                image = PropertyImage(property=property_object, image=img_url)
                image.save()

            return redirect('scrape_housing_data')  # Redirect to the same page after scraping
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")

    properties = Property.objects.all()
    return render(request, 'scraper/scraped_properties.html', {'properties': properties})

def property_detail(request, property_id):
    property = Property.objects.get(pk=property_id)
    images = PropertyImage.objects.filter(property=property)
    return render(request, 'scraper/property_detail.html', {'property': property, 'images': images})
