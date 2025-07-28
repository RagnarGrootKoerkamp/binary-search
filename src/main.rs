use std::{
    hint::black_box,
    time::{Duration, Instant},
};

use rand::random;
use rdst::RadixSort;

/// Generate a sorted list of n random integers.
fn random_sorted_vec(n: usize) -> Vec<u64> {
    let mut v: Vec<u64> = (0..n).map(|_| random()).collect();
    v.radix_sort_unstable();
    v
}

fn random_vec(n: usize) -> Vec<u64> {
    (0..n).map(|_| random()).collect()
}

fn binary_search(v: &[u64], x: u64) -> usize {
    let mut l = 0;
    // inclusive right end
    let mut h = v.len() - 1;
    while l < h {
        let m = (l + h + 1) / 2;
        if x < v[m] {
            h = m - 1;
        } else {
            l = m;
        }
    }
    l
}

fn sqrt_search(v: &[u64], x: u64, stride: usize, block: &[u64]) -> usize {
    let mut cnt = 0;
    for &v in block {
        cnt += (x >= v) as usize;
    }
    // eprintln!("cnt {cnt:?}");
    let offset = cnt * stride;
    let mut pos = 0;
    for &v in &v[offset.min(v.len())..(offset + stride).min(v.len())] {
        pos += (x >= v) as usize;
    }
    // eprintln!("pos {pos:?}");
    offset + pos
}

fn test(n: usize, q: usize) -> (Duration, Duration, Duration) {
    let lookup = {
        let data = random_sorted_vec(n);
        let queries = (0..q)
            .map(|_| random::<u64>() as usize % n)
            .collect::<Vec<_>>();

        let start = Instant::now();

        let mut seed = 0;
        for &q in &queries {
            seed = data[q ^ seed] as usize & 1;
        }

        start.elapsed()
    };

    let bs = {
        let data = random_sorted_vec(n);
        let queries = random_vec(q);

        let start = Instant::now();

        let mut seed = 0;
        for &q in &queries {
            seed = binary_search(&data, q ^ seed) as u64 & 1;
        }
        black_box(seed);

        start.elapsed()
    };

    let sqrt = {
        let data = random_sorted_vec(n);
        let queries = random_vec(q);
        let stride = n.isqrt();
        let block: Vec<u64> = (0..n).step_by(stride).map(|i| data[i]).collect();
        // eprintln!("{stride:?} {block:?}");

        let start = Instant::now();

        let mut seed = 0;
        for &q in &queries {
            seed = sqrt_search(&data, q ^ seed, stride, &block) as u64 & 1;
        }
        black_box(seed);

        start.elapsed()
    };

    (lookup, bs, sqrt)
}

fn main() {
    let mut ns = vec![];
    for i in 0.. {
        let n = ((1234. * 1.3f32.powi(i)) as usize).next_multiple_of(2);
        if n > 1000000000 {
            break;
        }
        ns.push(n);
    }

    let q = 1000000;

    for &n in &ns {
        let (mut lookup, mut bs, mut sqrt) = test(n, q);
        lookup /= q as u32;
        bs /= q as u32;
        sqrt /= q as u32;
        println!(
            "{n},{},{},{}",
            lookup.as_nanos(),
            bs.as_nanos(),
            sqrt.as_nanos()
        );
        eprintln!("n {n:>10} {lookup:>7?} {bs:>7?} {sqrt:>7?}");
    }
}
