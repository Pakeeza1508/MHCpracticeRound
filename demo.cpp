#include <bits/stdc++.h>
using namespace std;

struct IOFiles {
    unique_ptr<istream> in_holder;
    unique_ptr<ostream> out_holder;
    istream* in;
    ostream* out;
    IOFiles(int argc, char** argv) {
        ios::sync_with_stdio(false);
        cin.tie(nullptr);
        if (argc >= 3) {
            in_holder = make_unique<ifstream>(argv[1]);
            out_holder = make_unique<ofstream>(argv[2]);
            if (!*in_holder) { cerr << "Failed to open input file\n"; exit(1); }
            if (!*out_holder){ cerr << "Failed to open output file\n"; exit(1); }
            in = in_holder.get();
            out = out_holder.get();
        } else {
            in = &cin;
            out = &cout;
        }
    }
};

int main(int argc, char** argv) {
    IOFiles io(argc, argv);
    istream& in = *io.in;
    ostream& out = *io.out;

    int T; 
    if (!(in >> T)) return 0;
    for (int tc = 1; tc <= T; ++tc) {
        int N, Q; long long L;
        in >> N >> Q >> L;
        vector<long long> X(N+1);
        vector<pair<long long,int>> ord;
        ord.reserve(N);
        for (int i = 1; i <= N; ++i) { in >> X[i]; ord.push_back({X[i], i}); }
        sort(ord.begin(), ord.end());
        vector<long long> pos_sorted(N);
        vector<int> idx_sorted(N);
        for (int i = 0; i < N; ++i) { pos_sorted[i] = ord[i].first; idx_sorted[i] = ord[i].second; }

        set<long long> walls;
        walls.insert(1);
        walls.insert(L);

        long long answer_sum = 0;

        for (int qi = 0; qi < Q; ++qi) {
            int type; in >> type;
            if (type == 1) {
                long long x; in >> x;
                walls.insert(x);
            } else {
                int r; long long s; in >> r >> s;
                long long xr = X[r];
                auto itR = walls.upper_bound(xr);
                long long b = *itR;
                auto itL = itR; --itL;
                long long a = *itL;
                long long len = b - a;

                long long best_j = 0;
                long double best_t = -1;

                auto lo_it = lower_bound(pos_sorted.begin(), pos_sorted.end(), a);
                auto hi_it = upper_bound(pos_sorted.begin(), pos_sorted.end(), b);
                int lo = int(lo_it - pos_sorted.begin());
                int hi = int(hi_it - pos_sorted.begin());

                long double Ld = (long double)len;
                for (int k = lo; k < hi; ++k) {
                    int j = idx_sorted[k];
                    if (j == r || j < r) continue;
                    long double num = (long double)X[r] + (long double)X[j] - 2.0L*(long double)a;
                    long double t0 = fmod(num*0.5L, Ld);
                    if (t0 < 0) t0 += Ld;
                    if ((long double)s + 1e-12L < t0) continue;
                    long double kf = floor(((long double)s - t0) / Ld);
                    long double tlast = t0 + kf * Ld;
                    if (tlast > best_t + 1e-12L || (fabsl(tlast - best_t) <= 1e-12L && j > best_j)) {
                        best_t = tlast;
                        best_j = j;
                    }
                }
                answer_sum += best_j;
            }
        }

        out << "Case #" << tc << ": " << answer_sum << "\n";
    }
    return 0;
}
