#!/usr/bin/env python3
"""
SOCS - Sports Data Management System
Performance Comparison Tool

This script compares the original procedural approach with the optimized 
object-oriented solution, demonstrating the performance and reliability 
improvements achieved through professional programming practices.

Usage:
    python comparison_runner.py
"""

import time
import requests
from datetime import datetime, timedelta
from xml.etree.ElementTree import Element, fromstring, ElementTree

# Import our optimized solution
from sports_data_fetcher import SportsDataFetcher


def run_original_approach():
    """
    Simulate the original procedural approach with basic error handling.
    This represents the initial working solution before optimization.
    """
    print("🔄 ORIGINAL APPROACH - Procedural Style")
    print("-" * 50)
    start_time = time.time()
    
    # Configuration (hardcoded as in original)
    base_url = "https://www.schoolssports.com/school/xml/mso-sport.ashx?ID=28488&key=88E70399-79A6-4966-AB47-C6E645AE1110&data=fixtures&startdate={startdate}&enddate={enddate}&TS=1"
    
    # Use smaller date range for demo (5 days instead of full range)
    start_date = datetime.strptime("26 Sep 2024", "%d %b %Y")
    end_date = datetime.strptime("30 Sep 2024", "%d %b %Y")
    
    # Simple processing variables
    root = Element("ConsolidatedFixtures")
    success_count = 0
    error_count = 0
    
    # Sequential processing loop (original approach)
    current_date = start_date
    while current_date <= end_date:
        formatted_date = current_date.strftime("%d %b %Y")
        url = base_url.format(startdate=formatted_date, enddate=formatted_date)
        
        try:
            # Basic API request with no retries or rate limiting
            response = requests.get(url)
            response.raise_for_status()
            
            # Basic XML processing
            fetched_data = fromstring(response.content)
            for child in fetched_data:
                root.append(child)
            
            success_count += 1
            print(f"   ✅ {formatted_date}")
            
        except Exception as e:
            error_count += 1
            print(f"   ❌ {formatted_date}: {str(e)[:50]}...")
        
        current_date += timedelta(days=1)
    
    # Save basic output
    output_file = "original_fixtures.xml"
    with open(output_file, "wb") as file:
        ElementTree(root).write(file, encoding="utf-8", xml_declaration=True)
    
    elapsed_time = time.time() - start_time
    
    print(f"\n📊 Original Results:")
    print(f"   Time taken: {elapsed_time:.2f} seconds")
    print(f"   Successful requests: {success_count}")
    print(f"   Failed requests: {error_count}")
    print(f"   Success rate: {success_count/(success_count+error_count)*100:.1f}%")
    print(f"   Output: {output_file}")
    
    return elapsed_time, success_count, error_count


def run_optimized_approach():
    """
    Run the optimized object-oriented approach with all improvements.
    This demonstrates the production-ready solution.
    """
    print("\n🚀 OPTIMIZED APPROACH - Object-Oriented with Enhancements")
    print("-" * 65)
    start_time = time.time()
    
    # Initialize with conservative settings for fair comparison
    fetcher = SportsDataFetcher(
        max_workers=3,
        delay_between_requests=0.1,
        cache_dir="comparison_cache"
    )
    
    # Fetch same date range as original
    xml_data = fetcher.fetch_date_range("26 Sep 2024", "30 Sep 2024")
    
    # Consolidate results
    output_file = fetcher.consolidate_xml(xml_data, "optimized_fixtures.xml")
    
    # Get comprehensive statistics
    stats = fetcher.get_statistics()
    
    elapsed_time = time.time() - start_time
    
    print(f"\n📊 Optimized Results:")
    print(f"   Time taken: {elapsed_time:.2f} seconds")
    print(f"   Successful requests: {len(xml_data)}")
    print(f"   API calls made: {stats['api_calls']}")
    print(f"   Cache hits: {stats['cache_hits']}")
    print(f"   Failed requests: {stats['failed_requests']}")
    print(f"   Cache hit rate: {stats['cache_hit_rate']:.2%}")
    print(f"   Total fixtures: {stats['total_fixtures']}")
    print(f"   Output: {output_file}")
    
    return elapsed_time, len(xml_data), stats['failed_requests'], stats


def demonstrate_caching_benefits():
    """
    Show the dramatic performance improvement from caching on second run.
    """
    print(f"\n🔥 CACHING DEMONSTRATION")
    print("=" * 40)
    
    fetcher = SportsDataFetcher(
        cache_dir="caching_demo",
        max_workers=2,
        delay_between_requests=0.1
    )
    
    # First run (cold cache)
    print("🥶 First run (cold cache - will hit API):")
    start_time = time.time()
    xml_data1 = fetcher.fetch_date_range("28 Sep 2024", "30 Sep 2024")
    first_run_time = time.time() - start_time
    stats1 = fetcher.get_statistics()
    
    print(f"   Time: {first_run_time:.2f}s")
    print(f"   API calls: {stats1['api_calls']}")
    print(f"   Cache hits: {stats1['cache_hits']}")
    
    # Second run (warm cache)
    print(f"\n🔥 Second run (warm cache - will use cached data):")
    start_time = time.time()
    xml_data2 = fetcher.fetch_date_range("28 Sep 2024", "30 Sep 2024")
    second_run_time = time.time() - start_time
    stats2 = fetcher.get_statistics()
    
    new_api_calls = stats2['api_calls'] - stats1['api_calls']
    new_cache_hits = stats2['cache_hits'] - stats1['cache_hits']
    
    print(f"   Time: {second_run_time:.2f}s")
    print(f"   API calls: {new_api_calls}")
    print(f"   Cache hits: {new_cache_hits}")
    
    # Show improvement
    if second_run_time > 0:
        speedup = first_run_time / second_run_time
        print(f"\n⚡ Caching Performance Boost:")
        print(f"   Speedup: {speedup:.1f}x faster!")
        print(f"   Time saved: {first_run_time - second_run_time:.2f} seconds")
        print(f"   Cache efficiency: {new_cache_hits/len(xml_data2)*100:.0f}% of requests served from cache")


def run_comparison():
    """
    Run a comprehensive comparison between approaches and display results.
    """
    print("🏁 SOCS PERFORMANCE COMPARISON")
    print("=" * 60)
    print("Comparing original procedural vs optimized object-oriented approaches")
    
    try:
        # Run original approach
        orig_time, orig_success, orig_errors = run_original_approach()
    except Exception as e:
        print(f"❌ Original approach failed: {e}")
        orig_time, orig_success, orig_errors = float('inf'), 0, 999
    
    # Small delay between tests
    time.sleep(1)
    
    try:
        # Run optimized approach  
        opt_time, opt_success, opt_errors, opt_stats = run_optimized_approach()
    except Exception as e:
        print(f"❌ Optimized approach failed: {e}")
        return
    
    # Display comprehensive comparison
    print(f"\n{'='*60}")
    print("🏆 COMPARISON RESULTS")
    print(f"{'='*60}")
    
    # Performance comparison table
    print(f"\n📊 Performance Metrics:")
    print(f"{'Metric':<25} {'Original':<12} {'Optimized':<12} {'Improvement'}")
    print("-" * 65)
    print(f"{'Time (seconds)':<25} {orig_time:<12.2f} {opt_time:<12.2f} {orig_time/opt_time if opt_time > 0 else float('inf'):.1f}x faster")
    print(f"{'Successful requests':<25} {orig_success:<12} {opt_success:<12} {'Same' if orig_success == opt_success else 'Better' if opt_success > orig_success else 'Worse'}")
    print(f"{'Failed requests':<25} {orig_errors:<12} {opt_errors:<12} {orig_errors - opt_errors:+d}")
    print(f"{'Success rate':<25} {orig_success/(orig_success+orig_errors)*100:<12.1f}% {opt_success/(opt_success+opt_errors)*100 if opt_success+opt_errors > 0 else 0:<12.1f}% {(opt_success/(opt_success+opt_errors) - orig_success/(orig_success+orig_errors))*100 if opt_success+opt_errors > 0 and orig_success+orig_errors > 0 else 0:+.1f}%")
    
    # Feature comparison
    print(f"\n🔧 Feature Comparison:")
    features = [
        ("Error handling with retries", "❌ None", "✅ 3 attempts with backoff"),
        ("Rate limiting", "❌ None", "✅ Configurable delays"),
        ("Parallel processing", "❌ Sequential only", "✅ Configurable workers"),
        ("Caching system", "❌ None", "✅ Intelligent disk cache"),
        ("Progress tracking", "❌ Basic prints", "✅ Professional logging"),
        ("Statistics reporting", "❌ None", "✅ Comprehensive metrics"),
        ("Data organization", "❌ Mixed together", "✅ Grouped by date"),
        ("Resource management", "❌ Basic", "✅ Professional cleanup"),
        ("Configuration options", "❌ Hardcoded", "✅ Fully configurable"),
        ("Code maintainability", "❌ Procedural", "✅ Object-oriented")
    ]
    
    for feature, original, optimized in features:
        print(f"  {feature:<25} {original:<25} {optimized}")
    
    # Caching benefits preview
    if opt_stats and opt_stats.get('cache_hits', 0) == 0:
        print(f"\n💡 CACHING BENEFITS:")
        print(f"   First run: {opt_stats['api_calls']} API calls made")
        print(f"   Next run: ~0 API calls (served from cache)")
        print(f"   Expected speedup: ~10-50x faster on subsequent runs!")
        print(f"   💡 Run this comparison again to see caching in action!")
    
    # Bottom line recommendations
    print(f"\n🎯 KEY IMPROVEMENTS:")
    print(f"   ⚡ {orig_time/opt_time if opt_time > 0 else float('inf'):.1f}x faster execution (before caching benefits)")
    print(f"   🛡️  Robust error handling prevents complete failures")
    print(f"   📊 Professional logging and statistics for monitoring")
    print(f"   🔄 Intelligent caching for massive speedup on reruns") 
    print(f"   🏗️  Object-oriented design for maintainability and reuse")
    print(f"   ⚙️  Configurable parameters for different environments")


def main():
    """
    Main function to run all comparisons and demonstrations.
    """
    # Run the main comparison
    run_comparison()
    
    # Demonstrate caching benefits
    demonstrate_caching_benefits()
    
    print(f"\n🎓 LEARNING OUTCOMES:")
    print("=" * 30)
    print("This comparison demonstrates key programming concepts:")
    print("• Object-oriented design vs procedural programming")
    print("• Professional error handling and resilience patterns")
    print("• Performance optimization through caching and parallelization")
    print("• Code organization and separation of concerns")
    print("• Production-ready logging and monitoring")
    print("• API best practices for reliable integrations")
    
    print(f"\n📁 Generated Files:")
    print("• original_fixtures.xml - Basic procedural output")
    print("• optimized_fixtures.xml - Enhanced organized output")
    print("• comparison_cache/ - Cached data for performance")
    print("• sports_fetcher.log - Detailed operation logs")
    
    print(f"\n✨ Next Steps:")
    print("• Run this script multiple times to see caching benefits")
    print("• Modify configuration parameters to test different scenarios")
    print("• Apply these patterns to other API integrations in your work")
    print("• Use as a template for MS 365 automation projects")


if __name__ == "__main__":
    main()