#!/usr/bin/env python3
"""
Integration test for DBreconnection cog
Tests the actual database reconnection functionality
"""

import asyncio
import os
import sys
from unittest.mock import Mock, AsyncMock
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the cog
from Cogs.DBreconnection import DBreconnection


async def test_dbreconnection():
    """Test the database reconnection command"""
    print("Starting DBreconnection integration test...")
    
    # Create a mock bot
    bot = Mock(spec=commands.Bot)
    bot.get_cog = Mock(return_value=None)
    
    # Test 1: Initialize the cog
    print("\n1. Testing cog initialization...")
    try:
        cog = DBreconnection(bot)
        print("✅ Cog initialized successfully")
        
        # Check if connections were established
        if cog.book and cog.event and cog.saving:
            print("✅ All database connections established")
        else:
            print("⚠️  Some database connections failed to initialize")
    except Exception as e:
        print(f"❌ Failed to initialize cog: {e}")
        return
    
    # Test 2: Test reconnection with valid credentials
    print("\n2. Testing database reconnection...")
    
    # Create mock interaction
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.user = Mock()
    interaction.user.display_name = "TestUser"
    interaction.user.avatar = None
    interaction.response = AsyncMock()
    interaction.followup = AsyncMock()
    
    # Store the embed that would be sent
    sent_embed = None
    
    async def mock_send(embed=None, **kwargs):
        nonlocal sent_embed
        sent_embed = embed
    
    interaction.followup.send = mock_send
    
    try:
        # Execute the command
        await cog.dbreconnect(interaction)
        
        # Check the result
        if sent_embed:
            # Check if it's a success or error embed
            # Success embeds should have the success message
            embed_dict = sent_embed.to_dict() if hasattr(sent_embed, 'to_dict') else {}
            description = embed_dict.get('description', '')
            
            if "재연결 성공" in description or "성공" in str(sent_embed):
                print("✅ Database reconnection successful!")
            elif "재연결 실패" in description or "실패" in str(sent_embed):
                print("❌ Database reconnection failed")
                if 'fields' in embed_dict:
                    for field in embed_dict['fields']:
                        print(f"   Error: {field.get('value', 'Unknown error')}")
            else:
                print("⚠️  Unknown response from reconnection attempt")
        else:
            print("❌ No response from command")
            
    except Exception as e:
        print(f"❌ Error during reconnection test: {e}")
    
    # Test 3: Test reconnection with simulated failure
    print("\n3. Testing error handling...")
    
    # Temporarily break the connection by clearing environment variables
    original_host = os.getenv("DB_HOST")
    os.environ["DB_HOST"] = "invalid_host_12345"
    
    try:
        await cog.dbreconnect(interaction)
        
        if sent_embed:
            embed_dict = sent_embed.to_dict() if hasattr(sent_embed, 'to_dict') else {}
            description = embed_dict.get('description', '')
            
            if "재연결 실패" in description or "실패" in str(sent_embed):
                print("✅ Error handling working correctly")
            else:
                print("❌ Error was not properly handled")
    except Exception as e:
        print(f"✅ Exception caught as expected: {type(e).__name__}")
    finally:
        # Restore original environment variable
        if original_host:
            os.environ["DB_HOST"] = original_host
    
    print("\n✨ Integration test completed!")


async def test_command_registration():
    """Test that the command is properly registered"""
    print("\n4. Testing command registration...")
    
    # Create a real bot instance (but don't run it)
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="$", intents=intents)
    
    try:
        # Load the cog
        await bot.load_extension("Cogs.DBreconnection")
        
        # Check if command is registered
        commands_list = [cmd.name for cmd in bot.tree.get_commands()]
        if "dbreconnect" in commands_list:
            print("✅ Command 'dbreconnect' is properly registered")
        else:
            print("❌ Command 'dbreconnect' not found in command tree")
            
        # Get command details
        for cmd in bot.tree.get_commands():
            if cmd.name == "dbreconnect":
                print(f"   Description: {cmd.description}")
                break
                
    except Exception as e:
        print(f"❌ Failed to load cog: {e}")
    finally:
        await bot.close()


async def main():
    """Run all integration tests"""
    print("=" * 60)
    print("DBreconnection Integration Tests")
    print("=" * 60)
    
    # Run tests
    await test_dbreconnection()
    await test_command_registration()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    # Check if database environment variables are set
    required_vars = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_PORT"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️  Warning: Missing environment variables: {', '.join(missing_vars)}")
        print("   The test will continue but database connections may fail.")
        print("   Create a .env file with the required database credentials.\n")
    
    # Run the tests
    asyncio.run(main())