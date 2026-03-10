# Pattern Model for DSA

This repository includes various Data Structures and Algorithms (DSA) patterns with templates and related problems.

## Patterns

### 1. Two Pointers
   - **Template:**
     ```python
     def two_pointers_pattern(arr):
         left, right = 0, len(arr) - 1
         while left < right:
             # perform some action
             left += 1
             right -= 1
     ```
   - **Related Problems:**
     - Find a pair with a given sum.
     - Container with most water.

### 2. Sliding Window
   - **Template:**
     ```python
     def sliding_window_pattern(s):
         left, right = 0, 0
         while right < len(s):
             # expand the window
             right += 1
             # contract the window
     ```
   - **Related Problems:**
     - Longest substring without repeating characters.
     - Maximum sum of a subarray of size k.

### 3. Binary Search
   - **Template:**
     ```python
     def binary_search(arr, target):
         left, right = 0, len(arr) - 1
         while left <= right:
             mid = left + (right - left) // 2
             if arr[mid] == target:
                 return mid
             elif arr[mid] < target:
                 left = mid + 1
             else:
                 right = mid - 1
         return -1
     ```
   - **Related Problems:**
     - Search in a sorted array.
     - Find the peak element.

### 4. Dynamic Programming
   - **Template:**
     ```python
     def dynamic_programming_pattern(n):
         dp = [0] * (n + 1)
         dp[0], dp[1] = 1, 1
         for i in range(2, n + 1):
             dp[i] = dp[i - 1] + dp[i - 2] # example for Fibonacci
         return dp[n]
     ```
   - **Related Problems:**
     - 0/1 Knapsack Problem.
     - Longest Increasing Subsequence.

---

This document can be expanded with more patterns and problems as needed.