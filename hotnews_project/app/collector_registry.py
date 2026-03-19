from app.collectors.rss import ExampleRssCollector
from app.collectors.sample_static import SampleStaticCollector


def get_collectors():
    return [
        ExampleRssCollector(),
        SampleStaticCollector(),
    ]


def get_collectors_map():
    collectors = get_collectors()
    return {collector.name: collector for collector in collectors}
