import pytest
from discord.ext import commands  # noqa

from discord.ext.antispam import AntiSpamHandler, PluginCache  # noqa

from discord.ext.antispam.core import Core
from discord.ext.antispam.caches import Memory

from discord.ext.antispam.plugins import AntiMassMention, AntiSpamTracker


class MockClass:
    pass


@pytest.fixture
def create_bot():
    """Creates a commands.Bot instance"""
    return commands.Bot(command_prefix="!")


@pytest.fixture
def create_handler(create_bot):
    """Create a simple handler for usage"""
    return AntiSpamHandler(create_bot)


@pytest.fixture
def create_plugin_cache(create_handler):
    """Creates a PluginCache instance"""
    return PluginCache(create_handler, MockClass())


@pytest.fixture
def create_memory_cache(create_handler):
    return Memory(create_handler)


@pytest.fixture
def create_core(create_handler):
    return Core(create_handler)


@pytest.fixture
def create_anti_mass_mention(create_bot, create_handler):
    return AntiMassMention(create_bot, create_handler)


@pytest.fixture
def create_anti_spam_tracker(create_handler):
    return AntiSpamTracker(create_handler, 3)
