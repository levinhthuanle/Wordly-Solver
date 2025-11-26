#!/usr/bin/env python3
"""
Test script for modernized backend.
Run this to verify the new architecture works correctly.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.agent import wordlist, AgentSolver


def test_wordlist():
    """Test wordlist loading."""
    print("🧪 Testing wordlist loading...")
    words = wordlist.words
    assert len(words) > 0, "Word list is empty!"
    assert all(len(w) == 5 for w in words[:100]), "Words not 5 letters!"
    print(f"✅ Loaded {len(words)} words")
    print(f"   Sample: {words[:5]}")
    return True


def test_validation():
    """Test word validation."""
    print("\n🧪 Testing word validation...")
    assert wordlist.is_valid("AROSE"), "Valid word rejected!"
    assert wordlist.is_valid("HELLO"), "Valid word rejected!"
    assert not wordlist.is_valid("ZZZZZ"), "Invalid word accepted!"
    assert not wordlist.is_valid("ABC"), "Short word accepted!"
    print("✅ Validation works correctly")
    return True


def test_solver():
    """Test solver with sample game."""
    print("\n🧪 Testing solver...")
    
    # Test each algorithm
    for algo in ['dfs', 'hill-climbing', 'simulated-annealing']:
        print(f"\n  Testing {algo.upper()}...")
        solver = AgentSolver(algorithm=algo)
        
        # First guess
        guess1, conf1, remaining1 = solver.solve_next([], [])
        print(f"    First guess: {guess1} ({remaining1} words, {conf1:.1%} confidence)")
        assert guess1 in wordlist.words, f"Invalid guess: {guess1}"
        
        # Second guess with feedback
        guesses = ["AROSE"]
        evals = [["absent", "absent", "absent", "present", "absent"]]
        guess2, conf2, remaining2 = solver.solve_next(guesses, evals)
        print(f"    Next guess: {guess2} ({remaining2} words, {conf2:.1%} confidence)")
        assert guess2 in wordlist.words, f"Invalid guess: {guess2}"
        assert remaining2 < remaining1, "Not filtering words!"
    
    print("\n✅ All solvers working correctly")
    return True


def test_reasoning():
    """Test reasoning generation."""
    print("\n🧪 Testing reasoning...")
    solver = AgentSolver()
    
    reasons = [
        solver.get_reasoning(1, 1.0),
        solver.get_reasoning(3, 0.33),
        solver.get_reasoning(15, 0.07),
        solver.get_reasoning(100, 0.01),
        solver.get_reasoning(5000, 0.0002),
    ]
    
    for i, reason in enumerate(reasons, 1):
        print(f"    {i}. {reason}")
    
    print("✅ Reasoning generation works")
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Modernized Backend Test Suite")
    print("=" * 60)
    
    tests = [
        test_wordlist,
        test_validation,
        test_solver,
        test_reasoning,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed: {e}")
            failed += 1
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("\n🎉 All tests passed! Backend is ready.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
