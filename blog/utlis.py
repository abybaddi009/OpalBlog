import random
import string

def slugify(sender, title: str) -> str:
    slug = title.lower().replace(" ", "-")
    if sender.objects.filter(slug=slug).count() == 0:
        return slug
    else:
        # Truncate the slug to the first 55 characters
        # generate random alphanumeric string of 8 characters
        return (
            slug[:56]
            + "-"
            + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        )
