#!/usr/bin/env python3
"""
Test script for Gemini MCP Server

Tests the query function with a sample prompt to verify the server works correctly.
"""

import asyncio
import sys
from server import query


async def test_gemini_query():
    """Test the gemini query function with a sample prompt."""
    test_prompt = "Tell me the biggest news in the last 24 hours"
    
    print(f"Testing Gemini MCP Server...")
    print(f"Prompt: {test_prompt}")
    print("-" * 50)
    
    try:
        # Test the query function
        result = await query(test_prompt)
        print("✅ Success!")
        print(f"Response: {result}")
        return True
        
    except RuntimeError as e:
        if "not found" in str(e):
            print("❌ Test failed: 'gemini' command not found in PATH")
            print("Please install the gemini command-line tool and ensure it's accessible")
        else:
            print(f"❌ Test failed with runtime error: {e}")
        return False
        
    except ValueError as e:
        print(f"❌ Test failed with value error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Test failed with unexpected error: {e}")
        return False


async def test_empty_prompt():
    """Test the query function with an empty prompt to verify error handling."""
    print("\nTesting empty prompt handling...")
    print("-" * 50)
    
    try:
        await query("")
        print("❌ Test failed: Empty prompt should raise ValueError")
        return False
        
    except ValueError:
        print("✅ Success! Empty prompt correctly rejected")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with unexpected error: {e}")
        return False


async def main():
    """Run all tests."""
    print("Gemini MCP Server Test Suite")
    print("=" * 50)
    
    # Test normal query
    success1 = await test_gemini_query()
    
    # Test empty prompt handling
    success2 = await test_empty_prompt()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())