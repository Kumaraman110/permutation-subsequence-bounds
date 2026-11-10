#include <algorithm>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct Result {
    bool complete;
    std::vector<int> missing;
};

Result verify(const std::vector<int>& word, int n) {
    const int length = static_cast<int>(word.size());
    const int absent = length + 1;
    std::vector<std::vector<int>> next(length + 2, std::vector<int>(n, absent));
    for (int p = length - 1; p >= 0; --p) {
        if (word[p] < 0 || word[p] >= n) throw std::runtime_error("invalid symbol");
        next[p] = next[p + 1];
        next[p][word[p]] = p + 1;
    }
    const int states = 1 << n;
    std::vector<int> endpoint(states, 0), predecessor(states, -1);
    for (int mask = 1; mask < states; ++mask) {
        int worst = -1;
        for (unsigned int bits = mask; bits; bits &= bits - 1) {
            int c = __builtin_ctz(bits);
            int candidate = next[endpoint[mask ^ (1 << c)]][c];
            if (candidate > worst) {
                worst = candidate;
                predecessor[mask] = c;
            }
        }
        endpoint[mask] = worst;
    }
    if (endpoint.back() <= length) return {true, {}};
    std::vector<int> missing;
    for (int mask = states - 1; mask;) {
        int c = predecessor[mask];
        missing.push_back(c);
        mask ^= 1 << c;
    }
    std::reverse(missing.begin(), missing.end());
    return {false, missing};
}

bool directly_contains(const std::vector<int>& word, const std::vector<int>& target) {
    std::size_t j = 0;
    for (int c : word) if (j < target.size() && target[j] == c) ++j;
    return j == target.size();
}

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    std::string folder = argv[1];
    for (int n = 11; n <= 15; ++n) {
        std::string name = "n" + std::to_string(n) + ".txt";
        std::ifstream input(folder + "/inputs/" + name);
        if (!input) throw std::runtime_error("missing input");
        std::vector<int> word;
        for (int c; input >> c;) word.push_back(c);
        if (!verify(word, n).complete) throw std::runtime_error("original incomplete");
        std::ofstream certificates(folder + "/deletion_certificates_n" + std::to_string(n) + ".txt");
        certificates << "# Removed positions and missing permutations are one-based.\n";
        int failures = 0;
        for (std::size_t p = 0; p < word.size(); ++p) {
            auto shortened = word;
            shortened.erase(shortened.begin() + p);
            Result result = verify(shortened, n);
            if (result.complete) throw std::runtime_error("a deletion preserves completeness");
            if (result.missing.size() != static_cast<std::size_t>(n)
                || directly_contains(shortened, result.missing))
                throw std::runtime_error("invalid missing-permutation certificate");
            auto sorted = result.missing;
            std::sort(sorted.begin(), sorted.end());
            for (int i = 0; i < n; ++i)
                if (sorted[i] != i) throw std::runtime_error("certificate is not a permutation");
            certificates << p + 1 << ':';
            for (int c : result.missing) certificates << ' ' << c + 1;
            certificates << '\n';
            ++failures;
        }
        std::cout << "{\"n\":" << n << ",\"length\":" << word.size()
                  << ",\"complete\":true,\"single_deletions_tested\":" << failures
                  << ",\"all_deletions_fail\":true}" << std::endl;
    }
}
