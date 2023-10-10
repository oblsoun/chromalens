from django.conf import settings
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError

from django.core.files.storage import FileSystemStorage
from .ColorsApi import colordetection, colordetection_org

class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name

def index(request):
    message = ""
    prediction = ""
    fss = CustomFileSystemStorage()

    try:
        image = request.FILES["image"]
        _image = fss.save(image.name, image)

        ext = image.name.split('.')[-1]
        newname = '{}_{}'.format("origin", image.name, ext)
        _image_org = fss.save(newname, image)

        path = str(settings.MEDIA_ROOT) + "/" + image.name
        org_path=str(settings.MEDIA_ORG_ROOT) + "/" + newname

        # image details
        image_url = fss.url(_image)
        org_image_url = fss.url(_image_org)
        # Read the image
        products, total_product_count = colordetection(path)

        org_img = colordetection_org(org_path)

        return TemplateResponse(
            request,
            "index.html",
            {
                "org_img": org_img,
                "org_image_url": org_image_url,
                "message": message,
                "total_product_count": total_product_count,
                "image_url": image_url,
                "prediction": products,
            },
        )
    except MultiValueDictKeyError:

        return TemplateResponse(
            request,
            "index.html",
            {"message": "No Image Selected"},
        )

