from django.contrib import admin
import reversion
from app.models import AsymmetricalGame, TeamGame, AsymmetricalPlayer, TeamPlayer


class AsymmetricalPlayerAdmin(reversion.VersionAdmin):
    pass

admin.site.register(AsymmetricalPlayer, AsymmetricalPlayerAdmin)


class TeamPlayerAdmin(reversion.VersionAdmin):
    pass

admin.site.register(TeamPlayer, TeamPlayerAdmin)


class AsymmetricalGameAdmin(reversion.VersionAdmin):
    pass

admin.site.register(AsymmetricalGame, AsymmetricalGameAdmin)


class TeamGameAdmin(reversion.VersionAdmin):
    pass

admin.site.register(TeamGame, TeamGameAdmin)
