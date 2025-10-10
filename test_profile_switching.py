#!/usr/bin/env python3
"""
QA Test Script for Profile Switching
Tests all locations where user profile data should appear
"""

import sys
from demo_app import DEMO_USERS, get_relative_time, generate_live_alerts

def test_user_profiles():
    """Test that all user profiles are properly defined"""
    print("🧪 Testing User Profiles...")
    print("=" * 60)
    
    required_keys = [
        'name', 'style', 'portfolio_value', 'today_pl', 'emotion_state',
        'calm_level', 'stress_level', 'trades_prevented', 'money_saved',
        'win_rate_calm', 'win_rate_stressed'
    ]
    
    for user_key, user_data in DEMO_USERS.items():
        print(f"\n✓ Testing: {user_key}")
        print(f"  Name: {user_data['name']}")
        print(f"  Style: {user_data['style']}")
        
        # Check all required keys exist
        for key in required_keys:
            if key not in user_data:
                print(f"  ❌ Missing key: {key}")
                return False
            else:
                print(f"  ✓ {key}: {user_data[key]}")
        
        # Validate data types and ranges
        assert isinstance(user_data['portfolio_value'], (int, float)), "portfolio_value should be numeric"
        assert isinstance(user_data['calm_level'], (int, float)), "calm_level should be numeric"
        assert 0 <= user_data['calm_level'] <= 100, "calm_level should be 0-100"
        assert 0 <= user_data['stress_level'] <= 100, "stress_level should be 0-100"
        assert user_data['win_rate_calm'] > user_data['win_rate_stressed'], "calm win rate should be higher"
        
    print("\n" + "=" * 60)
    print("✅ All user profiles validated!")
    return True

def test_relative_time():
    """Test relative timestamp function"""
    print("\n🧪 Testing Relative Time Function...")
    print("=" * 60)
    
    test_cases = [
        (0, "just now"),
        (0.5, "just now"),
        (1, "1 min ago"),
        (5, "5 mins ago"),
        (60, "1 hour ago"),
        (120, "2 hours ago"),
        (1440, "1 day ago"),
        (2880, "2 days ago"),
    ]
    
    for minutes, expected_start in test_cases:
        result = get_relative_time(minutes)
        print(f"  {minutes} minutes → '{result}'")
        
        # Check format is correct
        if minutes < 1:
            assert result == "just now", f"Expected 'just now' for {minutes} min"
        elif minutes < 60:
            assert "min" in result or result == "just now", f"Should contain 'min' for {minutes}"
        elif minutes < 1440:
            assert "hour" in result, f"Should contain 'hour' for {minutes}"
        else:
            assert "day" in result, f"Should contain 'day' for {minutes}"
    
    print("=" * 60)
    print("✅ Relative time function working correctly!")
    return True

def test_live_alerts():
    """Test live alerts generation for each user"""
    print("\n🧪 Testing Live Alerts Generation...")
    print("=" * 60)
    
    for user_key, user_data in DEMO_USERS.items():
        print(f"\n✓ Testing alerts for: {user_data['name']}")
        alerts = generate_live_alerts(user_data)
        
        assert len(alerts) >= 3, f"Should have at least 3 alerts, got {len(alerts)}"
        
        for i, alert in enumerate(alerts, 1):
            print(f"  Alert {i}:")
            print(f"    Type: {alert['type']}")
            print(f"    Icon: {alert['icon']}")
            print(f"    Message: {alert['message']}")
            print(f"    Time: {alert['time']}")
            print(f"    Detail: {alert['detail']}")
            
            # Validate alert structure
            assert 'type' in alert, "Alert should have 'type'"
            assert 'icon' in alert, "Alert should have 'icon'"
            assert 'message' in alert, "Alert should have 'message'"
            assert 'time' in alert, "Alert should have 'time'"
            assert 'detail' in alert, "Alert should have 'detail'"
            
            # Validate alert types
            assert alert['type'] in ['success', 'warning', 'info', 'danger'], f"Invalid alert type: {alert['type']}"
    
    print("\n" + "=" * 60)
    print("✅ Live alerts generated correctly for all users!")
    return True

def test_profile_differences():
    """Test that profiles have meaningful differences"""
    print("\n🧪 Testing Profile Differences...")
    print("=" * 60)
    
    sarah = DEMO_USERS['Sarah_Conservative']
    mike = DEMO_USERS['Mike_Aggressive']
    emma = DEMO_USERS['Emma_Balanced']
    
    print("\n📊 Calm Levels:")
    print(f"  Sarah: {sarah['calm_level']}%")
    print(f"  Mike: {mike['calm_level']}%")
    print(f"  Emma: {emma['calm_level']}%")
    
    print("\n💰 Portfolio Values:")
    print(f"  Sarah: ${sarah['portfolio_value']:,}")
    print(f"  Mike: ${mike['portfolio_value']:,}")
    print(f"  Emma: ${emma['portfolio_value']:,}")
    
    print("\n💸 Money Saved:")
    print(f"  Sarah: ${sarah['money_saved']:,}")
    print(f"  Mike: ${mike['money_saved']:,}")
    print(f"  Emma: ${emma['money_saved']:,}")
    
    print("\n📈 Win Rates (Calm vs Stressed):")
    print(f"  Sarah: {sarah['win_rate_calm']}% vs {sarah['win_rate_stressed']}%")
    print(f"  Mike: {mike['win_rate_calm']}% vs {mike['win_rate_stressed']}%")
    print(f"  Emma: {emma['win_rate_calm']}% vs {emma['win_rate_stressed']}%")
    
    # Verify differences exist
    assert sarah['calm_level'] != mike['calm_level'], "Sarah and Mike should have different calm levels"
    assert sarah['portfolio_value'] != mike['portfolio_value'], "Portfolios should differ"
    assert sarah['emotion_state'] != mike['emotion_state'], "Emotional states should differ"
    
    # Verify Mike has highest stress
    assert mike['stress_level'] > sarah['stress_level'], "Mike should be more stressed than Sarah"
    assert mike['stress_level'] > emma['stress_level'], "Mike should be more stressed than Emma"
    
    # Verify Emma has best calm level
    assert emma['calm_level'] > sarah['calm_level'], "Emma should be calmer than Sarah"
    assert emma['calm_level'] > mike['calm_level'], "Emma should be calmer than Mike"
    
    print("\n" + "=" * 60)
    print("✅ Profiles have meaningful differences for demo!")
    return True

def run_all_tests():
    """Run all QA tests"""
    print("\n" + "🚀 " * 30)
    print("PROFILE SWITCHING QA TEST SUITE")
    print("🚀 " * 30 + "\n")
    
    tests = [
        ("User Profiles", test_user_profiles),
        ("Relative Time", test_relative_time),
        ("Live Alerts", test_live_alerts),
        ("Profile Differences", test_profile_differences),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ {test_name} FAILED: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {status}: {test_name}")
        if not success:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Profile switching is working correctly!")
        print("\n✅ VERIFIED LOCATIONS:")
        print("  • User profile data structure")
        print("  • Relative timestamp conversion")
        print("  • Live alerts generation per user")
        print("  • Meaningful differences between profiles")
        print("\n🎬 Ready for presentation demos!")
        return 0
    else:
        print("\n⚠️ SOME TESTS FAILED - Please review errors above")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())

