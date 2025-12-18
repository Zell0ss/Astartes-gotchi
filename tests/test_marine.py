# tests/test_marine.py - Unit tests for SpaceMarine class
# Run with: python tests/test_marine.py

import sys
import os

# Add src directory to path
test_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(test_dir), 'src')
sys.path.insert(0, src_dir)

from lib.space_marine import SpaceMarine
import config

def test_marine_creation():
    """Test creating a new marine"""
    print("TEST: Marine creation...")
    marine = SpaceMarine("Test Brother")
    assert marine.name == "Test Brother"
    assert marine.geneseed_purity == 100
    assert marine.corruption == 0
    assert marine.is_alive == True
    print("  ✅ PASS")

def test_feeding():
    """Test feeding mechanics"""
    print("TEST: Feeding...")
    marine = SpaceMarine()

    # Feed ration
    marine.sustenance = 50
    marine.feed("ration")
    assert marine.sustenance == 70

    # Feed stimm (increases corruption)
    initial_corruption = marine.corruption
    marine.feed("stimm")
    assert marine.corruption > initial_corruption
    assert marine.stimm_count == 1

    print("  ✅ PASS")

def test_prayer():
    """Test prayer mechanics"""
    print("TEST: Prayer...")
    marine = SpaceMarine()
    marine.corruption = 50

    result = marine.pray()
    assert result == True
    assert marine.corruption < 50

    # Test cooldown
    result = marine.pray()
    assert result == False

    print("  ✅ PASS")

def test_evolution_algorithm():
    """Test chapter determination"""
    print("TEST: Evolution algorithm...")

    # Test Ultramarine path
    marine = SpaceMarine()
    marine.discipline = 80
    marine.corruption = 15
    marine.care_mistakes = 1
    marine.current_stage = SpaceMarine.STAGE_BATTLE_BROTHER

    chapter = marine._determine_chapter()
    assert chapter == SpaceMarine.CHAPTER_ULTRAMARINE

    # Test Khorne path
    marine2 = SpaceMarine()
    marine2.corruption = 70
    marine2.combat_experience = 85
    marine2.discipline = 20
    marine2.current_stage = SpaceMarine.STAGE_BATTLE_BROTHER

    chapter2 = marine2._determine_chapter()
    assert chapter2 == SpaceMarine.CHAOS_KHORNE

    print("  ✅ PASS")

def test_save_load():
    """Test serialization"""
    print("TEST: Save/Load...")

    marine = SpaceMarine("Savedius")
    marine.corruption = 25
    marine.combat_experience = 42

    data = marine.to_dict()
    assert data["name"] == "Savedius"
    assert data["corruption"] == 25

    marine2 = SpaceMarine.from_dict(data)
    assert marine2.name == "Savedius"
    assert marine2.corruption == 25
    assert marine2.combat_experience == 42

    print("  ✅ PASS")

def test_death():
    """Test death mechanics"""
    print("TEST: Death...")

    marine = SpaceMarine()
    marine.die("geneseed_failure")

    assert marine.is_alive == False
    assert marine.death_cause == "geneseed_failure"

    # Can't act when dead
    result = marine.feed("ration")
    assert result == False

    print("  ✅ PASS")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("ASTARTES-GOTCHI UNIT TESTS")
    print("="*50 + "\n")

    try:
        test_marine_creation()
        test_feeding()
        test_prayer()
        test_evolution_algorithm()
        test_save_load()
        test_death()

        print("\n" + "="*50)
        print("ALL TESTS PASSED! For the Emperor! 🦅")
        print("="*50 + "\n")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
