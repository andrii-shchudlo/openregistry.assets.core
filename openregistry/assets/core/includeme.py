from pkg_resources import iter_entry_points
from pyramid.interfaces import IRequest
from openregistry.assets.core.utils import (
    extract_asset, isAsset, register_assetType,
    asset_from_data, SubscribersPicker
)
from openregistry.api.interfaces import IContentConfigurator
from openregistry.assets.core.models import IAsset
from openregistry.assets.core.adapters import AssetConfigurator


def includeme(config):
    from openregistry.assets.core.design import add_design
    add_design()
    config.add_request_method(extract_asset, 'asset', reify=True)

    # assetType plugins support
    config.registry.assetTypes = {}
    config.add_route_predicate('assetType', isAsset)
    config.add_subscriber_predicate('assetType', SubscribersPicker)
    config.add_request_method(asset_from_data)
    config.add_directive('add_assetType',
                         register_assetType)
    config.scan("openregistry.assets.core.views")
    config.scan("openregistry.assets.core.subscribers")
    config.registry.registerAdapter(AssetConfigurator, (IAsset, IRequest),
                                    IContentConfigurator)

    # search for plugins
    settings = config.get_settings()
    plugins = settings.get('plugins') and settings['plugins'].split(',')
    for entry_point in iter_entry_points('openregistry.assets.core.plugins'):
        if not plugins or entry_point.name in plugins:
            plugin = entry_point.load()
            plugin(config)
