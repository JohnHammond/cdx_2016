
def add_badge(badge, model):
    "Put a badge on a model"
    if badge not in model.badges.all():
        model.badges.add(badge)

def batchbadge(badge, queryset):
    "Put a badge on all models that do not already have the badge"
    for model in queryset:
        add_badge(badge, model)
