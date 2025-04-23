#include <iostream>
#include <vector>
#include <numeric>
#include <ranges>
#include <algorithm>





int main(int argc, char const *argv[])
{
    int n = 10;
    std::vector<int> vec(n);
    for (int i = 0; i < n; i++) vec[i] = i;

    vec.push_back(n + 1);

    for(int i = 0; i < vec.size(); i++)
        if (vec[i] % 2 == 0) std::cout << vec[i] << " ";
    std::cout << std::endl;

    for (auto it = vec.begin(); it != vec.end(); it++)
        if (*it % 2 == 0) std::cout << *it << " ";
    std::cout << std::endl;


    std::cout << "vec before incrementation: ";
    for (const auto &el : vec) std::cout << el << " ";

    // range based loops
    for (auto &el : vec) el++;

    std::cout << std::endl;

    std::cout << "vec after incrementation: ";
    for (const auto &el : vec) std::cout << el << " ";

    std::cout << std::endl;

    // lambda expressions
    auto even = [](int i) {return i % 2 == 0;};
    for (const auto &e : vec | std::views::filter(even))
        std::cout << e << " ";
    std::cout << std::endl;

    auto doubler = [](auto x){return 2*x;};

    std::cout <<  doubler(10) << std::endl;

    std::vector<int> nums = {1, 2, 3, 4, 5};

    std::for_each(nums.begin(), nums.end(), [](int& x){return x *= 2;});
    std::for_each(nums.begin(), nums.end(), [](int& x){return x *= 2;});
    std::for_each(nums.begin(), nums.end(), [](int& x){return x *= 2;});
    std::for_each(nums.begin(), nums.end(), [](int& x){return x *= 2;});

    for (const auto& el : nums) std::cout << el << " ";
    std::cout << std::endl;




    return 0;
}
