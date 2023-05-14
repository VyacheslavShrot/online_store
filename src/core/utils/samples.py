from store.models import Archive, Category, Product


def sample_product(title: str, **params) -> Product:
    default = {"characteristic": "Default", "category": Category.objects.create()}
    default.update(params)

    return Product.objects.create(title=title, **default)


def sample_archive(title: str, **params) -> Archive:
    default = {"characteristic": "Default"}
    default.update(params)

    return Archive.objects.create(title=title, **default)
